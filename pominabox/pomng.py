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


import xmlrpc.client
import _thread
import time

class pomng():

    def __init__(self, url, config):
        self.url = url
        self.config = config
        self.proxy = None
        self.timeout = 60
        self.events = {}
        self.listeners = {}
        self.monitor_session = -1
        return

    def enable(self):
        if self.proxy:
            return True
        self.proxy = xmlrpc.client.ServerProxy(self.url)
        try:
            version = self.proxy.core.getVersion()
        except Exception as e:
            return [ False, "Error while connecting to the node : " + str(e) ]
        print("Connected to " + self.url + " version " + version)
        self.monitor_session = self.proxy.monitor.start(self.timeout)
        _thread.start_new_thread(self._monitor, (self.monitor_session, xmlrpc.client.ServerProxy(self.url), ))

        # Listen to all the events
        for event_name in self.events:
            self.events[event_name] = self.proxy.monitor.eventAddListener(self.monitor_session, event_name, "", True, True)
            self.listeners[self.events[event_name]] = event_name

        return [ True, "Node version " + version ]

    def disable(self):
        print("TODO")
        return

    def _monitor(self, sessionID, pollProxy):
        while True:
            try:
                res = pollProxy.monitor.poll(sessionID)
            except Exception as e:
                print("Error while polling " + self.url + " : " + str(e))
                time.sleep(1)
                continue
            if 'events' in res:
                for evt in res['events']:
                    self._process_event(evt)

    def _process_event(self, event):
        listener_id = event['listeners'][0]
        db = self.config.db_get()
        db.put(self.listeners[listener_id], event['data'])
        return True

    def event_add(self, event_name):
        if event_name in self.events:
            return [ True, "Event already monitored" ]

        self.events[event_name] = True

        if self.monitor_session != -1:
            self.events[event_name] = self.proxy.monitor.eventAddListener(self.monitor_session, event_name, "", False, True)
            self.listeners[self.events[event_name]] = event_name

        return [ True, "Event monitoring started" ]

    def event_remove(self, event_name):
        if not event_name in self.events:
            return [ True, "Event isn't monitored" ]

        listener_id = self.events[event_name]
        del self.events[event_name]
        del self.listeners[listener_id]
        if self.monitor_session != -1:
            self.proxy.monitor.eventRemoveListener(self.monitor_session, listener_id)

    def events_get(self):
        return keys(self.events)

