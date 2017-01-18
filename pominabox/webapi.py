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
            v['value'] = ret[2]
        return v

    def db(self, method, params):
        if method == "status":
            return { 'status' : 'ok' }

        return self._return_error("No such method")

    def nodes(self, method, params):
        if method == "add":
            if not params:
                return self._return_error("No parameter provided")
            if not 'url' in params:
                return self._return_error("No url specified")
            if not 'name' in params:
                return self._return_error("No name specified")
            return self._return_result(self.config.nodes_add(name = params['name'], url = params['url']))
        elif method == "get":
            return self._return_result(self.config.nodes_get())
        return self._return_error('No such method')
