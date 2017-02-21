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
import configparser
import time
import sys
import os
import pominabox

argparser = argparse.ArgumentParser(description='Archive server for pom-ng')
argparser.add_argument('--cfgfile', '-c', dest='cfgfile',  help='Configuration file', default='pominabox.ini')

if __name__ == "__main__":
    args = argparser.parse_args()
    cfgfile = configparser.ConfigParser()
    try:
        cfgfile.read(args.cfgfile)
    except Exception as e:
        print("Error while reading the config file : " + str(e))
        sys.exit(1)

    config = pominabox.config(cfgfile)

    httpsrv = pominabox.webserv(config)
    httpsrv.run()
    print("Pominabox started !")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    httpsrv.kill()
