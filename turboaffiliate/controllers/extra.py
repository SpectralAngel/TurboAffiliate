#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# affiliate.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2008, 2009 Carlos Flores <cafg10@gmail.com>
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
from turboaffiliate import model
from decimal import *

class Extra(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.extra.index')
	def index(self):
		return dict(accounts=model.Account.select())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.extra.add')
	@validate(validators=dict(affiliate=validators.Int()))
	def add(self, affiliate):
		
		affiliate = model.Affiliate.get(affiliate)
		accounts = model.Account.select()
		return dict(affiliate=affiliate, accounts=accounts)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(affiliate=validators.Int(),
							  account=validators.Int(),
							  months=validators.Int(),
							  retrasada=validators.Bool(),
							  amount=validators.String()))
	def save(self, affiliate, account, **kw):
		
		kw['affiliate'] = model.Affiliate.get(affiliate)
		kw['account'] = model.Account.get(account)
		kw['amount'] = Decimal(kw['amount'])
		extra = model.Extra(**kw)
		raise redirect('/affiliate/%s' % kw['affiliate'].id)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(account=validators.Int(), months=validators.Int(),
							  first=validators.Int(), last=validators.Int(),
							  amount=validators.Number()))
	def many(self, first, last, account, **kw):
		
		kw['account'] = model.Account.get(account)
		for n in range(first, last +1):
			kw['affiliate'] = model.Affiliate.get(n)
			extra = model.Extra(**kw)
		raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(code=validators.Int()))
	def delete(self, code):
		
		extra = model.Extra.get(code)
		affiliate = extra.affiliate
		extra.destroySelf()
		
		raise redirect('/affiliate/%s' % affiliate.id)

