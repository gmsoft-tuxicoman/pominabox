#!/usr/bin/python3
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


import argparse
import time
import sys
import os
import pominabox

argparser = argparse.ArgumentParser(description='Archive server for pom-ng')
argparser.add_argument('--config', '-c', dest='config',  help='Configuration file')
argparser.add_argument('--port', '-p', dest='httpd_port', help='Port to bind to', default=8081, type=int)
argparser.add_argument('--elasticsearch', '-e', dest='es_nodes', help='Elastic search nodes', default='localhost')
argparser.add_argument('--web-ui-dir', '-w', dest='ui_dir', help='Path to the web-ui directory', default=os.path.dirname(sys.argv[0]) + '/web-ui' )


if __name__ == "__main__":
    args = argparser.parse_args()
    config = pominabox.config(args)

    httpsrv = pominabox.webserv(config)
    httpsrv.run()
    print("Pominabox started !")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    httpsrv.kill()
