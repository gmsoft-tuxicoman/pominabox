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

    def _return_error(self, msg):
        return { 'status' : 'error', 'msg' : msg }

    def _return_result(self, ret):
        v = { 'status' : 'ok', 'msg' : ret[1] }
        if not ret[0]:
            v['status'] = 'error'
        if len(ret) > 2:
            v.update(ret[2])
        return v


    def PUT_nodes(self, req, params):
        if len(req) < 1:
            return self._return_error("No node name specified")

        retval = [ True, 'Node parameters updated' ]
        node_name = req[0]

        # Check if it's a PUT for a node resource
        if len(req) >= 2:
            if req[1] == 'events':
                return self.PUT_nodes_event(node_name, req[2:], params)
            return self._return_error("No such method")

        # We are adding a node
        if not params:
            return self._return_error("No parameter provided")

        if not 'url' in params:
            return self._return_error("No URL provided")

        return self._return_result(self.config.pomng_node_add(name = node_name, url = params['url']))


    def POST_nodes(self, req, params):
        if not params:
            return self._return_error("No parameter provided")
        if len(req) < 1:
            return self._return_error("No node name specified")

        node_name = req[0]

        if 'enabled' in params:
            ret = self.config.pomng_node_enable(node_name, params['enabled'])
            if not ret[0]:
                return self._return_result(ret)

        return { 'status' : 'ok', 'node' : self.config.pomng_nodes_get()[2]['nodes'][node_name] }

    def DELETE_nodes(self, req, params):
        if len(req) < 1:
            return self._return_error("No node name specified")

        node_name = req[0]
        return self.config.pomng_node_remove(node_name)


    def GET_nodes(self, req, params):
        return self._return_result(self.config.pomng_nodes_get())

    def PUT_nodes_event(self, node_name, req, params):
        if len(req) < 1:
            return self._return_error("No node event name specified")
        event_name = req[0]
        return self._return_result(self.config.pomng_node_event_enable(node_name, event_name))

