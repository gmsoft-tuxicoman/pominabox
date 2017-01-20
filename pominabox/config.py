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

import pominabox

class config():

    def __init__(self):
        self.nodes = {}
        self.nodes_inst = {}
        self.database = {}
        self.httpd_port = 8081

    def nodes_add(self, name, url):
        if name in self.nodes:
            return [ False, 'Node already exists' ]
        if name == '*':
            return [ False, 'Invalid node name' ]
        self.nodes[name] = { 'url' : url, 'enabled' : False }
        return [ True, 'Node added' ]

    def nodes_get(self):
        return [ True, 'Node list', self.nodes ]

    def nodes_enable(self, name, enabled):
        if not name in self.nodes:
            return [ False, 'Node does not exists' ]
        node = self.nodes[name]
        if node['enabled'] == enabled:
            if enabled:
                return [ True, 'Node already enabled' ]
            else:
                return [ True, 'Node already disabled' ]

        self.nodes_inst[name] = pominabox.pomng(node['url'])
        ret = {}
        if enabled:
            ret = self.nodes_inst[name].enable()
        else:
            ret = eelf.nodes_inst[name].disable()
        if ret[0]:
            self.nodes[name]['enabled'] = enabled
        return ret

    def nodes_event_add(self, node_name, event_name):
        node_inst = self.nodes_inst[node_name]
        return node_inst.event_add(event_name)

    def nodes_event_remove(self, node_name, event_name):
        node_inst = self.nodes_inst[node_name]
        return node_inst.event_remove(event_name)

    def nodes_events_get(self, node_name, event_name):
        node_inst = self.nodes_inst[node_name]
        return node_inst.events_get()

    def httpd_port_get(self):
        return self.httpd_port

    def save():
        return
