#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# controllers.py
# This file is part of TurboAffiliate
#
# Copyright © 2009 Carlos Flores <cafg10@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from turbogears import controllers, flash, redirect, identity, url
from turbogears import expose, validate, validators, error_handler
from cherrypy import request, response, NotFound, HTTPRedirect
from turboaffiliate import model, json, num2stres
from datetime import date, datetime
from decimal import *

class Logger(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.log.index")
	def index(self):
		
		return dict()
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.log.day")
	@validate(validators=dict(start=validators.DateTimeConverter(format='%Y-%m-%d'),
							  end=validators.DateTimeConverter(format='%Y-%m-%d')))
	def day(self, start, end):
		
		query = "logger.day >= '%s' and logger.day <= '%s'" % (start, end)
		
		logs = model.Logger.select(query)
		
		return dict(logs=logs,start=start,end=end)

