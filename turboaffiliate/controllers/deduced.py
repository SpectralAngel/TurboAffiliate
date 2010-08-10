#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# deduced.py
# This file is part of TurboAffiliate
#
# Copyright (C) 2009 - 2010 Carlos Flores
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

from turbogears import controllers, flash, redirect, identity, url
from turbogears import expose, validate, validators
from turboaffiliate import model
from decimal import Decimal

class Deduced(controllers.Controller):
	
	"""Permite administrar las deducciones realizadas a un afiliado"""
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.deduced.deduced')
	@validate(validators=dict(code=validators.Int()))
	def default(self, code):
		
		return dict(affiliate=model.Affiliate.get(code), accounts=model.Account.select())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.deduced.mostrar')
	@validate(validators=dict(afiliado=validators.Int(), mes=validators.Int(),
							  anio=validators.Int()))
	def mostrar(self, afiliado, mes, anio):
		
		afiliado = model.Affiliate.get(afiliado)
		deducciones = model.Deduced.selectBy(affiliate=afiliado, month=mes, year=anio)
		return dict(affiliate=afiliado, deducciones=deducciones)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.deduced.mostrar')
	@validate(validators=dict(afiliado=validators.Int(), anio=validators.Int()))
	def anual(self, afiliado, anio):
		
		afiliado = model.Affiliate.get(afiliado)
		deducciones = model.Deduced.selectBy(affiliate=afiliado, year=anio)
		return dict(affiliate=afiliado, deducciones=deducciones, anio=anio)
	
	@identity.require(identity.has_permission("Deductor"))
	@expose()
	@validate(validators=dict(affiliate=validators.Int(), account=validators.Int(),
							amount=validators.String(), year=validators.Int(),
							month=validators.Int()))
	def save(self, affiliate, account, **kw):
	
		kw['affiliate'] = model.Affiliate.get(affiliate)
		kw['amount'] = Decimal(kw['amount'])
		kw['account'] = model.Account.get(account)
		model.Deduced(**kw)
		
		flash("Agregado Detalle de Deducción")
		
		raise redirect(url("/affiliate/deduced/%s" % affiliate))
	
	@identity.require(identity.has_permission("Deductor"))
	@expose()
	@validate(validators=dict(deduced=validators.Int()))
	def delete(self, deduced):
		
		deduced = model.Deduced.get(deduced)
		affiliate = deduced.affiliate
		deduced.destroySelf()
		
		raise redirect(url("/affiliate/deduced/%s" % affiliate.id))
