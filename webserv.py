#  This file is part of pom-ng-console.
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


class webservHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        self.send_response(404)
        self.send_header('Server', 'pominabox')
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes("404 not found", "utf-8"))

        return

    def log_request(self, code='-', size='-'):
        return

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


class webserv():

    def __init__(self, port):
        self.port = port
        self.handler = webservHandler
        self.httpd = ThreadedTCPServer(("", self.port), self.handler)

    def run(self):
        print("Listening on port", self.port)
        server_thread = threading.Thread(target=self.httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    def kill(self):
        self.httpd.shutdown()
        self.httpd.server_close()
