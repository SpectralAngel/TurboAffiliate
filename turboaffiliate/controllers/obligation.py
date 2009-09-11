#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# obligation.py
# This file is part of TurboAffiliate
#
# Copyright © 2007, 2008, 2009 Carlos Flores <cafg10@gmail.com>
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
from turboaffiliate import model, json
from datetime import date

class Obligation(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.obligation.index")
	def index(self):
		
		return dict(companies=model.Company.select(), accounts=model.Account.select(orderBy="code"))
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.obligation.obligation")
	@expose("json")
	@validate(validators=dict(code=validators.Int()))
	def default(self, code):
		
		obligation =  model.Obligation.get(int(code))
		return dict(obligation=model.Obligation.get(code))
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.obligation.add")
	def add(self):
		
		return dict(companies=model.Company.select(), accounts=model.Account.select(orderBy="code"))
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.obligation.edit")
	@validate(validators=dict(code=validators.Int()))
	def edit(self, code):
		try:
			obligation = model.Obligation.get(int(code))
			return dict(obligation=obligation)
		except model.SQLObjectNotFound:
			flash(u'La obligación no se encontró')
			raise redirect('/obligation')
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(account=validators.Int(),company=validators.Int(),
							  year=validators.Int(),month=validators.Int(),
							  filiales=validators.Int(), inprema=validators.Number(),
							  amount=validators.Number()))
	def save(self, account, company, **kw):
		
		company = model.Company.get(company)
		account = model.Account.get(account)
		
		obligation = model.Obligation(company=company, account=account, **kw)
		flash('La obligación se ha añadido')
		raise redirect('/obligation/%s' % obligation.id)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.obligation.obligations")
	@validate(validators=dict(company=validators.Int(), year=validators.Int()))
	def view(self, company, year):
		
		company = model.Company.get(company)
		obligations = model.Obligation.select(model.Obligation.q.year==year)
		return dict(obligations=obligations)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(code=validators.Int()))
	def remove(self, code):
		
		obligation =  model.Obligation.get(code)
		obligation.destroySelf()
		raise redirect('/obligation')
