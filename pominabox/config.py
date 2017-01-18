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

class config():

    def __init__(self):
        self.nodes = {};
        self.database = {};
        self.httpd_port = 8081

    def nodes_add(self, name, url):
        if name in self.nodes:
            return [ False, 'Node already exists' ]
        self.nodes[name] = { 'url' : url, 'enabled' : False }
        return [ True, 'Node added' ]

    def nodes_get(self):
        return [ True, 'Node list', self.nodes ]

    def nodes_enable(self, name):
        if not name in self.nodes:
            return [ False, 'Node does not exists' ]
        node = self.nodes[name]
        if node.enable:
            return [ True, 'Node already enabled' ]




    def httpd_port_get(self):
        return self.httpd_port

    def save():
        return
