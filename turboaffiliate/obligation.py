#!/usr/bin/python
# -*- coding: utf8 -*-
#
# obligation.py
# This file is part of TurboAffiliate
#
# Copyright © 2007 Carlos Flores <cafg10@gmail.com>
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

from turbogears import controllers, expose, flash, identity, redirect
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
	def default(self, code):
		
		try:
			obligation =  model.Obligation.get(int(code))
			return dict(obligation=obligation)
		except model.SQLObjectNotFound:
			flash('La obligación no se encontró')
			raise redirect('/obligation')
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.obligation.add")
	def add(self):
		
		return dict(companies=model.Company.select(), accounts=model.Account.select(orderBy="code"))
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.obligation.edit")
	def edit(self, code):
		try:
			obligation = model.Obligation.get(int(code))
			return dict(obligation=obligation)
		except model.SQLObjectNotFound:
			flash(u'La obligación no se encontró')
			raise redirect('/obligation')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def save(self, **kw):
		try:			
			kw['company'] = model.Company.get(int(kw['company']))
			kw['year'] = int(kw['year'])
			kw['month'] = int(kw['month'])
			kw['account'] = model.Account.get(int(kw['account']))
		
		except model.SQLObjectNotFound:
			flash(u'La Compañía no se encontró')
			raise redirect('/obligation')
		
		except ValueError:
			flash(u'Número invalido')
			raise redirect('/obligation/add')
		
		obligation = model.Obligation(**kw)
		flash('La obligación se ha añadido')
		raise redirect('/obligation/%s' % obligation.id)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.obligation.obligations")
	def view(self, company, year):
		try:
			company = model.Company.get(int(company))
		except model.SQLObjectNotFound:
			raise redirect('/obligation')
		obligations = model.Obligation.select(model.Obligation.q.year==int(year))
		return dict(obligations=obligations)
	
	@identity.require(identity.not_anonymous())
	@expose()
	def remove(self, code):
		try:
			obligation =  model.Obligation.get(int(code))
			obligation.destroySelf()
		except model.SQLObjectNotFound:
			flash('La obligación no se encontró')
		raise redirect('/obligation')
