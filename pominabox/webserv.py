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
import pominabox

class webservHandler(http.server.BaseHTTPRequestHandler):

    def do_POST(self):
        data_len = int(self.headers['content-length'])
        data = self.rfile.read(data_len)

        try:
            params = json.loads(data.decode())
        except ValueError:
            self.send_response(400)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes('Invalid JSON input\n', 'utf-8'))
            return



        return self.do_req(self.path, params)

    def do_GET(self):
        return self.do_req(self.path, None)

    def do_req(self, path, data):
        req = self.path.split('/')
        if req[1] == 'api':
            # methods starting with _ are private
            if len(req) < 4 or req[2].startswith('_'):
                self.send_response(400)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(bytes('No method specified\n', 'utf-8'))
                return
            self.do_api(req[2], req[3], data)
            return
 
        self.send_response(404)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes('404 not found\n', "utf-8"))

        return

    def do_api(self, endpoint, method, params):
        try:
            api_func = getattr(self.webapi, endpoint)
        except AttributeError:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            rsp = {
                'status': 'error',
                'msg': 'API endpoint ' + endpoint + ' does not exists'
            }
            self.wfile.write(json.dumps(rsp).encode())
            return

        retval = api_func(method, params)


        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(retval).encode())
        return

#    def log_request(self, code='-', size='-'):
#        return

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


class webserv():

    def __init__(self, config):
        self.port = config.httpd_port_get()
        self.handler = webservHandler
        self.handler.webapi = pominabox.webapi(config)
        self.httpd = ThreadedTCPServer(("", self.port), self.handler)

    def run(self):
        print("Listening on port", self.port)
        server_thread = threading.Thread(target=self.httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    def kill(self):
        self.httpd.shutdown()
        self.httpd.server_close()
