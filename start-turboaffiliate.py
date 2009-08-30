#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# start-turboaffiliate.py
# This file is part of Turboaffiliate
#
# Copyright (C) 2009 - Carlos Flores <cafg10@gmail.com>
#
# Turboaffiliate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Turboaffiliate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Turboaffiliate; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, 
# Boston, MA  02110-1301  USA

import pkg_resources
pkg_resources.require("TurboGears")

import locale
locale.setlocale(locale.LC_ALL, "")
print locale.getlocale()

from turbogears import update_config, start_server
import cherrypy
cherrypy.lowercase_api = True
from os.path import *
import sys

# first look on the command line for a desired config file,
# if it's not on the command line, then
# look for setup.py in this directory. If it's not there, this script is
# probably installed
if len(sys.argv) > 1:
    update_config(configfile=sys.argv[1], 
        modulename="turboaffiliate.config")
elif exists(join(dirname(__file__), "setup.py")):
    update_config(configfile="dev.cfg",modulename="turboaffiliate.config")
else:
    update_config(configfile="prod.cfg",modulename="turboaffiliate.config")

from turboaffiliate.controllers import root

start_server(root.Root())

