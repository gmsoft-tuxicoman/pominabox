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
import configparser
import os

class config():

    def __init__(self, cfgfile):
        self.nodes = {}
        self.nodes_inst = {}

        self.httpd_port = 8081
        try:
            self.httpd_port = cfgfile.getint('main', 'port')
        except (configparser.NoSectionError, configparser.NoOptionError):
            pass

        self.ui_dir = '/web-ui'
        try:
            self.ui_dir = os.path.normpath(cfgfile.get('main', 'web-ui-path'))
        except (configparser.NoSectionError, configparser.NoOptionError):
            pass

        es_opts = {'nodes': 'localhost'}
        if 'elasticsearch' in cfgfile.sections():
            es_opt_list = cfgfile.options('elasticsearch')
            if 'nodes' in es_opt_list:
                es_opts['nodes'] = cfgfile.get('elasticsearch', 'nodes').split(',')
            if 'sniff_on_start' in es_opt_list:
                es_opts['sniff_on_start'] = cfgfile.getboolean('elasticsearch', 'sniff_on_start')
            if 'sniff_on_connection_failure' in es_opt_list:
                es_opts['sniff_on_connection_failure'] = cfgfile.getboolean('elasticsearch', 'sniff_on_connection_failure')
            if 'sniffer_timeout' in es_opt_list:
                es_opts['sniffer_timeout'] = cfgfile.getint('elasticsearch', 'sniffer_timeout')

        self.db = pominabox.db(**es_opts)
        self.config_index = '.pominabox_config'

    def pomng_node_add(self, name, url):
        if name in self.nodes:
            return [ 409, { 'msg' : 'Node already exists' } ]
        if name == '*':
            return [ 400, { 'msg' : 'Invalid node name' } ]
        inst = pominabox.pomng(self, name)
        ret = inst.set_url(url)
        if ret[0] != 200:
            return ret
        ret = inst.enable()
        if ret[0] != 200:
            return ret
        self.nodes[name] = { 'url' : url, 'enabled' : True }
        del ret[1]['msg']
        self.nodes[name].update(ret[1])
        self.nodes_inst[name] = inst
        ret[0] = 201
        ret[1]['msg'] = 'Node added'
        return ret

    def pomng_node_remove(self, name):
        if not name in self.nodes:
            return [ 409, { 'msg' : 'Node does not exists' } ]

        del self.nodes_inst[name]
        del self.nodes[name]
        return [ 200, { 'msg' : 'Node removed' } ]

    def pomng_node_set_url(self, name, url):
        if not name in self.nodes:
            return [ 400, { 'msg' : 'Node does not exists' } ]
        ret = self.nodes_inst[name].set_url(url)
        if ret[0] != 200:
            return ret
        self.nodes[name]['url'] = url
        return ret

    def pomng_nodes_get(self):
        return [ 200, { 'msg' : 'Node list', "nodes": self.nodes } ]

    def pomng_node_enable(self, name, enabled):
        if not name in self.nodes:
            return [ 400, { 'msg' : 'Node does not exists' } ]

        ret = {}
        if enabled:
            ret = self.nodes_inst[name].enable()
            if ret[0] == 200:
                # Update node informations
                self.nodes[name].update(ret[2])
        else:
            ret = eelf.nodes_inst[name].disable()
        return ret

    def pomng_node_event_enable(self, node_name, event_name):
        if not node_name in self.nodes_inst:
            return [ 400, { 'msg' : 'Node does not exists' } ]
        node_inst = self.nodes_inst[node_name]
        return node_inst.event_enable(event_name)

    def pomng_node_event_disable(self, node_name, event_name):
        if not node_name in self.nodes_inst:
            return [ 400, { 'msg' : 'Node does not exists' } ]
        node_inst = self.nodes_inst[node_name]
        return node_inst.event_disable(event_name)

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
        return self.db

    def web_ui_dir(self):
        return self.ui_dir

    def save(self, conf_name):
        conf = {}
        conf['nodes'] = {}
        for node_name in self.nodes:
            node = self.nodes[node_name]
            conf['nodes'][node_name] = {
                'url' : node['url'],
                'enabled' : node['enabled'],
                'events' : {}
            }
            for evt in node['events']:
                conf['nodes'][node_name]['events'][evt] = {
                    'description' : node['events'][evt]['description'],
                    'enabled' : node['events'][evt]['enabled']
                }

        self.db.put(self.config_index, 'main_config', conf_name, conf)
        return [ 200, { 'msg' : 'Configuration saved' } ]

    def load(self, conf_name):
        self.reset()
        ret = self.db.get(self.config_index, 'main_config', conf_name)
        for node_name in ret['nodes']:

            node = ret['nodes'][node_name]
            node_info = {}
            inst = pominabox.pomng(self, node_name)
            ret = inst.set_url(node['url'])
            if ret[0] != 200:
                continue
            if (node['enabled']):
                ret = inst.enable()
                if ret[0] != 200:
                    continue
                del ret[1]['msg']
                node_info = ret[1]

            self.nodes[node_name] = node
            self.nodes_inst[node_name] = inst

            for evt in node['events']:
                if evt in node_info:
                    node_info['evt']['enabled'] = node['events']['enable']

                if node['enabled'] and node['events'][evt]['enabled']:
                    inst.event_enable(evt)

            self.nodes[node_name].update(node_info)

        return [ 200, { 'msg' : 'Configuration ' + conf_name + ' loaded' } ]

    def reset(self):
        for node_name in self.nodes:
            self.nodes_inst[node_name].disable()

        self.nodes = {}
        self.nodes_inst = {}
