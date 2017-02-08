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

from elasticsearch import Elasticsearch
import time

class db():

    def __init__(self, es_nodes):
        self.es = Elasticsearch(es_nodes)
        self.index = 'pominabox'
        settings = {
            "settings" : {
                "number_of_replicas" : 0
            },
            "mappings" : {
                "http_request" : {
                    "properties" : {
                        "query_time" : {
                            "type" : "date",
                            "doc_values" : True,
                        },
                        "response_time" : {
                            "type" : "date",
                            "doc_values" : True
                        },
                        "client_addr" : {
                            "type" : "ip",
                            "doc_values" : True
                        },
                        "server_addr" : {
                            "type" : "ip",
                            "doc_values" : True
                        },
                        "query_headers" : {
                            "type" : "nested"
                        },
                        "response_headers" : {
                            "type" : "nested"
                        }
                    }
                }
            }
        }

        for m in settings['mappings']:
            settings['mappings'][m]['properties'] = {
                "pominabox" : {
                    "properties" : {
                        "event_ts" : {
                            "type" : "date",
                            "doc_values" : True
                        }
                    }
                }
            }
        print(settings)
        ret = self.es.indices.create(index=self.index, ignore = 400, body=settings)
        print(ret)
        return

    def _pomts_to_epochts(self, pomts):
        return int((pomts['sec'] * 1000) + (pomts['usec'] / 1000))

    def put(self, doc_type, data, pomng_node):

        if doc_type == "http_request":
            if 'query_time' in data:
                data['query_time'] = self._pomts_to_epochts(data['query_time'])
            if 'response_time' in data:
                data['response_time'] = self._pomts_to_epochts(data['response_time'])

        data['pominabox'] = {
            "event_ts" : int(time.time() * 1000),
            "pomng_node" : pomng_node
        }

        ret = self.es.index(index=self.index, doc_type=doc_type, body=data)
        print(ret)

