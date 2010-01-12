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

class Billing(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.billing.index')
	def index(self):
		
		return dict()
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.billing.status')
	@validate(validators=dict(state=validators.String()))
	def state(self, state):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.state==state)
		
		return dict(affiliates=affiliates, day=date.today())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.billing.status')
	@validate(validators=dict(payment=validators.String()))
	def payment(self, payment):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.payment==payment)
		
		affiliates = (a for a in affiliates if a.joined != None)
		
		return dict(affiliates=affiliates, day=date.today())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.billing.status')
	@validate(validators=dict(school=validators.String()))
	def school(self, school):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.school==school)
		
		affiliates = (a for a in affiliates if a.joined != None)
		
		return dict(affiliates=affiliates, day=date.today())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.billing.status')
	@validate(validators=dict(start=validators.Int(), end=validators.Int))
	def rango(self, start, end):
		
		query = "affiliate.id >= %s and affiliate.id <= %s" % (start, end)
		
		affiliates = model.Affiliate.select(query)
		
		affiliates = (a for a in affiliates if a.joined != None)
		
		return dict(affiliates=affiliates, day=date.today())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.billing.loans')
	@validate(validators=dict(state=validators.String()))
	def loanState(self, state):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.state==state)
		loans = list()
		for affiliate in affiliates:
			loans.extend(affiliate.loans)
		
		return dict(loans=loans, day=date.today())
