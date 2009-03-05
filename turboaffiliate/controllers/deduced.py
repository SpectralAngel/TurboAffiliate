#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# deduced.py
# This file is part of TurboAffiliate
#
# Copyright (C) 2009 - Carlos Flores
#
# TurboAffiliate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# TurboAffiliate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TurboAffiliate; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, 
# Boston, MA  02110-1301  USA

from turbogears import controllers, flash, redirect, identity
from turbogears import expose, validate, validators, error_handler
from turboaffiliate import model, json
from decimal import *
from datetime import date, datetime

class Deduced(controllers.Controller):
	
	def index(self):
		 
		 pass
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.deduced.deduced')
	@validate(validators=dict(code=validators.Int()))
	def default(self, code):
		
		affiliate = model.Affiliate.get(code)
		return dict(deduced=affiliate.deduced)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.deduced.add')
	@validate(validators=dict(affiliate=validators.Int()))
	def add(self, affiliate):
		
		return dict(affiliate=model.Affiliate.get(affiliate), accounts=model.Accounts.select())
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(affiliate=validators.Int(), account=validators.Int(),
							amount=validators.Money(), year=validators.Int(),
							month=validators.Int()))
	def save(self, affiliate, account, **kw):
	
		kw['affiliate'] = model.Affiliate.get(affiliate)
		kw['account'] = model.Account.get(account)
		model.Deduced(**kw)
		
		raise redirect("/affiliate/deduced/%s" % affiliate)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(deduced=validators.Int())
	def delete(self, deduced):
		
		deduced = model.Deduced.get(deduced)
		affiliate = deduced.affiliate
		deduced.DestroySelf()
		
		raise redirect("/affiliate/deduced/%s" % affiliate.id)

