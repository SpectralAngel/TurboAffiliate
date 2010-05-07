#!/usr/bin/env python
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

from turbogears import controllers, flash, redirect, identity
from turbogears import expose, validate, validators
from turboaffiliate import model

class Account(controllers.Controller):
	
	"""Controller for Accounts in Affiliate Program"""
	
	@identity.require(identity.not_anonymous())
	#@expose(template="turboaffiliate.templates.account.index")
	def index(self):
		return dict()
	
	@identity.require(identity.not_anonymous())
	#@expose(template="turboaffiliate.templates.account.account")
	@expose("json")
	@validate(validators=dict(code=validators.Int()))
	def default(self, code):
	
		account = model.Account.byCode(code)
		return dict(account=account)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.account.add")
	def add(self):
		return dict()
	
	@expose()
	@validate(validators=dict(amount=validators.Number(),code=validators.Int(),
							  name=validators.String()))
	def save(self, **kw):
		try:
			account = model.Account.byCode(kw['code'])
			account.name = kw['name']
			account.amount = kw['amount']
			
			log = dict()
			log['user'] = identity.current.user
			log['action'] = "Agregada cuenta de %s" % account.id
			model.Logger(**log)
			
		except model.SQLObjectNotFound:
			account = model.Account(**kw)
		except ValueError:
			raise redirect('/account/add')
		
		flash("La cuenta ha sido grabada")
		raise redirect('/account/%s' % account.code)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.account.retrasada")
	def retrasada(self):
		
		return dict(accounts=model.Account.select())
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(mes=validators.Int(), anio=validators.Int(),
							  account=validators.Int()))
	def agregarRetrasada(self, account, **kw):
		
		account = model.Account.get(account)
		kw['account'] = account
		retrasada = model.CuentaRetrasada(**kw)
		retrasada.account = account
		
		raise redirect('/account/retrasada')
