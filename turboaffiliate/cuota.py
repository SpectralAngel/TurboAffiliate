#!/usr/bin/python
# -*- coding: utf8 -*-
#
# affiliate.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2008 Carlos Flores <cafg10@gmail.com>
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
from decimal import *
from datetime import datetime, date

class Cuota(controllers.Controller):

	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.cuota.add')
	def pay(self, cardID):
		try:
			affiliate = model.Affiliate.get(int(cardID))
			return dict(affiliate=affiliate)
		except model.SQLObjectNotFound:
				flash('No existe el Afiliado con Identidad %s' % cardID)
				redirect('/affiliate')

	@identity.require(identity.not_anonymous())
	@expose()
	def save(self, **kw):
		kw['how'] = int(kw['how'])
		
		if kw['amount'] == '':
			flash('Cantidad incorrecta')
			raise redirect('/affiliate/cuota/pay/%s' % kw['affiliate'])
		
		kw['amount'] = Decimal(str(kw['amount']))
		kw['day'] = datetime.strptime(kw['day'], "%Y-%m-%d").date()
		kw['year'] = kw['day'].year
		kw['month'] = kw['day'].month
		try:
			
			kw['affiliate'] = model.Affiliate.get(int(kw['affiliate']))
			if kw['how'] == 1:
				kw['affiliate'].pay_cuotas(kw['amount'])
				raise redirect('/affiliate')
			
			if kw['how'] == 2:
				kw['affiliate'].pay_cuota(kw['year'], kw['month'])
				raise redirect("/receipt/add")
			
		except model.SQLObjectNotFound:
			flash('No existe el Afiliado %s' % kw['affiliate'])

		except ValueError:
			flash(u'Numero de Afiliado invalido')
			raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def remove(self, id):
		
		try:
			table = model.CuotaTable.get(int(id))
			affiliate = table.affiliate
			table.destroySelf()
			raise redirect('/affiliate/status/%s' % affiliate.id)
		except:
			raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.cuota.edit')
	def edit(self, code):
		try:
			table = model.CuotaTable.get(int(code))
			return dict(table=table)
		
		except model.SQLObjectNotFound:
			flash('No existe el Afiliado %s' % kw['affiliate'])
			
		except ValueError:
			flash(u'Numero de Afiliado invalido')
			raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def change(self, **kw):

		try:
			table = model.CuotaTable.get(int(kw['id']))
			del kw['id']
			for n in range(1, 13):
				try:
					setattr(table, "month%s" % n, kw['month%s' % n])
				except KeyError:
					setattr(table, "month%s" % n, False)
			
		except model.SQLObjectNotFound:
			flash('No existe el Afiliado %s' % kw['affiliate'])
		
		except ValueError:
			flash(u'Numero de Afiliado invalido')
			raise redirect('/affiliate')
		
		raise redirect('/affiliate/status/%s' % table.affiliate.id)
