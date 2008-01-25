#!/usr/bin/python
# -*- coding: utf8 -*-
#
# account.py
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
from decimal import *
from mx.DateTime import *

class Account(controllers.Controller):
	
	"""Controller for Accounts in Affiliate Program"""
	
	@identity.require(identity.not_anonymous())
	#@expose(template="turboaffiliate.templates.account.index")
	def index(self):
		return dict()
	
	@identity.require(identity.not_anonymous())
	#@expose(template="turboaffiliate.templates.account.account")
	@expose("json")
	def default(self, code):
		try:
			account = model.Account.byCode(int(code))
			return dict(account=account)
		except model.SQLObjectNotFound:
			flash('No se encontro la cuenta')
			return dict(account=None)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.account.add")
	def add(self):
		return dict()
	
	@expose()
	def save(self, **kw):
		try:
			kw['amount'] = Decimal(kw['amount'])
			kw['code'] = int(kw['code'])
			account = model.Account.byCode(int(kw['code']))
			account.name = kw['name']
			account.code = kw['code']
			account.amount = kw['amount']
		except model.SQLObjectNotFound:
			account = model.Account(**kw)
		except ValueError:
			raise redirect('/account/add')
		flash("La cuenta ha sido grabada")
		raise redirect('/account/%s' % account.code)
	
	@identity.require(identity.not_anonymous())
	#@expose(template="turboaffiliate.templates.account.resume")
	def resume(self):
		accounts = model.Account.select()
		companies = model.Account.select()
