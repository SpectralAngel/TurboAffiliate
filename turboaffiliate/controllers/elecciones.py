#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# status.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2009 Carlos Flores <cafg10@gmail.com>
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

from turbogears import controllers, flash, redirect, identity
from turbogears import expose, validate, validators, error_handler
from cherrypy import request, response, NotFound, HTTPRedirect
from turboaffiliate import model, json
from decimal import *
from datetime import date, datetime

class Elecciones(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.elecciones.index")
	def index(self):
		return dict(accounts=model.Account.select())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.elecciones.listado')
	def all(self):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.active==True)
		return dict(affiliates=affiliates, count=affiliates.count())
