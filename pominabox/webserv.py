#  This file is part of pominabox.
#  Copyright (C) 2017 Guy Martin <gmsoft@tuxicoman.be>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


import http.server
import threading
import socketserver
import json
import os
import pominabox

class webservHandler(http.server.BaseHTTPRequestHandler):

    server_version = 'Pominabox'

    content_types = {
        'css' : 'text/css',
        'js' : 'application/javascript',
        'html' : 'text/html',
        'htm' : 'text/html',
        'jpg' : 'image/jpeg',
        'jpeg' : 'image/jpeg',
        'png' : 'image/png',

    }

    def do_GET(self):

        if self.path == '/':
            self.send_response(302)
            self.send_header('Location', '/ui/index.html')
            self.end_headers()
            return

        if self.path.startswith('/ui/'):
            return self.do_ui(self.path[4:])

        return self.do_req("GET")

    def do_POST(self):
        return self.do_req("POST")

    def do_PUT(self):
        return self.do_req("PUT")

    def do_DELETE(self):
        return self.do_req("DELETE")

    def do_req(self, req_type):

        data_len = 0
        data = None

        if 'content-length' in self.headers:
            data_len = int(self.headers['content-length'])

        if data_len > 0:
            data = self.rfile.read(data_len)

        req = self.path.split('/')
        if req[1] == 'api':
            return self.do_api(req_type, req[2:], data)
 
        self.send_response(404)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes('404 not found\n', "utf-8"))

        return

    def do_api(self, req_type, req, data):

        params = {}
        if data:
            try:
                params = json.loads(data.decode())
            except ValueError:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({ 'status' : 'error', 'msg' : 'Malformed input JSON' }).encode())
                return
        try:
            api_func = getattr(self.webapi, req_type + '_' + req[0])
        except AttributeError:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            rsp = {
                'status': 'error',
                'msg': 'API endpoint ' + req[0] + ' does not exists'
            }
            self.wfile.write(json.dumps(rsp).encode())
            return

        retval = api_func(req[1:], params)

        self.send_response(retval[0])
        if type(retval[1]) is dict:
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write((json.dumps(retval[1]) + "\r\n").encode())
        else:
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(retval[1].encode())

        return

    def do_ui(self, path):
        path = path.split('?')[0]
        ui_dir = self.config.web_ui_dir()
        fpath = os.path.join(ui_dir, path)
        if not os.path.normpath(fpath).startswith(ui_dir):
            self.send_response(400)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes("Bad request", "utf-8"))
            return
        try:
            f = open(fpath, mode='rb')
        except Exception as e:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(str(e), "utf-8"))
            return

        self.send_response(200)
        ext = path.split('.')[-1]
        content_type = 'binary/octet-stream'
        if ext in self.content_types:
            content_type = self.content_types[ext]
        self.send_header('Content-Type', content_type)
        self.end_headers()
        self.wfile.write(f.read())
        f.close()

#    def log_request(self, code='-', size='-'):
#        return

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


class webserv():

    def __init__(self, config):
        self.port = config.httpd_port_get()
        self.handler = webservHandler
        self.handler.webapi = pominabox.webapi(config)
        self.handler.config = config
        self.httpd = ThreadedTCPServer(("", self.port), self.handler)

    def run(self):
        print("Listening on port", self.port)
        server_thread = threading.Thread(target=self.httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    def kill(self):
        self.httpd.shutdown()
        self.httpd.server_close()
