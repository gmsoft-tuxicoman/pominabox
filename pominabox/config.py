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
import os

class config():

    def __init__(self, args):
        self.nodes = {}
        self.nodes_inst = {}
        self.httpd_port = args.httpd_port
        self.ui_dir = os.path.normpath(args.ui_dir)
        self.db = None

    def pomng_node_add(self, name, url):
        if name in self.nodes:
            return [ False, 'Node already exists' ]
        if name == '*':
            return [ False, 'Invalid node name' ]
        inst = pominabox.pomng(self, name)
        ret = inst.set_url(url)
        if not ret[0]:
            return ret
        ret = inst.enable()
        if not ret[0]:
            return ret
        self.nodes[name] = { 'url' : url, 'enabled' : True }
        self.nodes[name].update(ret[2])
        self.nodes_inst[name] = inst
        return ret

    def pomng_node_remove(self, name):
        if not name in self.nodes:
            return [ False, 'Node does not exists' ]

        del self.nodes_inst[name]
        del self.nodes[name]
        return [ True, 'Node removed' ]

    def pomng_node_set_url(self, name, url):
        if not name in self.nodes:
            return [ False, 'Node does not exists' ]
        ret = self.nodes_inst[name].set_url(url)
        if not ret[0]:
            return ret
        self.nodes[name]['url'] = url
        return ret

    def pomng_nodes_get(self):
        return [ True, 'Node list', { "nodes": self.nodes } ]

    def pomng_node_enable(self, name, enabled):
        if not name in self.nodes:
            return [ False, 'Node does not exists' ]

        ret = {}
        if enabled:
            ret = self.nodes_inst[name].enable()
            if ret[0]:
                # Update node informations
                self.nodes[name].update(ret[2])
        else:
            ret = eelf.nodes_inst[name].disable()
        return ret

    def pomng_node_event_enable(self, node_name, event_name):
        node_inst = self.nodes_inst[node_name]
        return node_inst.event_enable(event_name)

    def pomng_node_event_disable(self, node_name, event_name):
        node_inst = self.nodes_inst[node_name]
        return node_inst.event_disable(event_name)

    def pomng_node_events_get(self, node_name, event_name):
        node_inst = self.nodes_inst[node_name]
        return node_inst.events_get()

    def httpd_port_get(self):
        return self.httpd_port

    def db_nodes_set(self, db_nodes):
        self.db = pominabox.db(db_nodes)
        return self.es_nodes

    def db_get(self):
        if not self.db:
            self.db = pominabox.db(['localhost'])
        return self.db

    def web_ui_dir(self):
        return self.ui_dir

    def save():
        return
