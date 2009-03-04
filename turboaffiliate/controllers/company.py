#!/usr/bin/python
# -*- coding: utf8 -*-
#
# company.py
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
from turboaffiliate.controllers import obligation

class Company(controllers.Controller):
	
	obligation = obligation.Obligation()
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.company.index")
	def index(self):
		
		return dict()
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.company.company")
	@expose("json")
	def default(self, rtn):
		try:
			company = model.Company.byRtn(rtn)
			return dict(company=company)
		except model.SQLObjectNotFound:
			flash('La Compañía con RTN %s no se encontró.' % code)
			raise redirect('/company')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def search(self, rtn):
		
		raise redirect('/company/%s' % rtn)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.company.add")
	def add(self):
		
		return dict()
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.company.edit")
	def edit(self, code):
		
		try:
			company = model.Company.get(int(code))
			return dict(company=company)
		
		except model.SQLObjectNotFound:
			flash('La Compañía no se encontró.' % code)
			raise redirect('/company')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def save(self, **kw):
		
		try:
			company = model.Company.byRtn(str(kw['rtn']))
			company.name = kw['name']
			company.rtn = kw['rtn']
			raise redirect('/company/%s' % company.rtn)
		
		except model.SQLObjectNotFound:
			company = model.Company(**kw)
			raise redirect('/company/%s' % company.rtn)

	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.company.view")
	def view(self):
		companies = model.Company.select()
		return dict(companies=companies)
	
	@identity.require(identity.not_anonymous())
	@expose()
	def delete(self, code):
		try:
			model.Company.get(int(code)).destroySelf()
		
		except model.SQLObjectNotFound:
			pass
		
		except ValueError:
			pass
		
		raise redirect('/company')
