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

class webapi():

    def __init__(self, config):
        self.config = config

    def PUT_config(self, req, params):
        if len(req) < 1:
            return [ 400, { 'msg' : 'No config name specified' } ]

        return self.config.save(req[0])

    def GET_config(self, req, params):
        if len(req) < 1:
            return [ 400, { 'msg' : 'No config name specified' } ]

        return self.config.load(req[0])


    def PUT_nodes(self, req, params):
        if len(req) < 1:
            return [ 400, { 'msg' : 'No node name specified' } ]

        node_name = req[0]

        # Check if it's a PUT for a node resource
        if len(req) >= 2:
            if req[1] == 'events':
                return self.PUT_nodes_event(node_name, req[2:], params)
            return [ 404, { 'msg' : 'No such method' } ]

        # We are adding a node
        if not params:
            return [ 400, { 'msg' : 'No parameter provided' } ]

        if not 'url' in params:
            return [ 400, { 'msg' : 'No URL provided' } ]

        return self.config.pomng_node_add(name = node_name, url = params['url'])


    def POST_nodes(self, req, params):
        if not params:
            return [ 400, { 'msg' : 'No parameter provided' } ]
        if len(req) < 1:
            return [ 400, { 'msg' : 'No node name specified' } ]

        node_name = req[0]

        if 'enabled' in params:
            ret = self.config.pomng_node_enable(node_name, params['enabled'])
            return ret

        return [ 200, { 'msg' : ret[1], 'node' : self.config.pomng_nodes_get()[1]['nodes'][node_name] } ]

    def DELETE_nodes(self, req, params):
        if len(req) < 1:
            return [ 400, { 'msg' : 'No node name specified' } ]

        node_name = req[0]
        return self.config.pomng_node_remove(node_name)


    def GET_nodes(self, req, params):
        if len(req) >= 1:
            node_name = req[0]
            nodes = self.config.pomng_nodes_get()[1]['nodes']
            if not node_name in nodes:
                return [ 404, { 'msg' : 'Node does not exists' } ]
            return [ 200, { 'msg' : 'Node details', 'node' : nodes[node_name] } ]

        return self.config.pomng_nodes_get()

    def PUT_nodes_event(self, node_name, req, params):
        if len(req) < 1:
            return [ 400, { 'msg' : 'No node event name specified' } ]
        event_name = req[0]
        return self.config.pomng_node_event_enable(node_name, event_name)

    def POST_db(self, req, params):
        if len(req) < 1:
            return [ 400, { 'msg' :'No action specified' } ]

        if req[0] == 'search_template':
            return self.POST_db_search_template(req[1:], params)

        return self._return_error("Invalid DB action")

    def POST_db_search_template(self, req, params):
        db = self.config.db_get()
        return db.search_template(params)


