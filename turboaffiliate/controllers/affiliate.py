#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# affiliate.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2007 Carlos Flores <cafg10@gmail.com>
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
from turboaffiliate.controllers import cuota, extra, billing, deduced
from decimal import *
from datetime import date, datetime

class Affiliate(controllers.Controller):
	
	"""Manage Affiliate data"""
	
	cuota = cuota.Cuota()
	extra = extra.Extra()
	billing = billing.Billing()
	deduced = deduced.Deduced()
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.index')
	def index(self):
		import time
		return dict(now=time.ctime())
	
	@error_handler(index)
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.affiliate')
	@validate(validators=dict(affiliate=validators.Int()))
	def default(self, affiliate):
		
		return dict(affiliate=model.Affiliate.get(affiliate))
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.search')
	@validate(validators=dict(cardID=validators.String()))
	def byCardID(self, cardID):
		
		return dict(affiliates=model.Affiliate.select(model.Affiliate.q.cardID==cardID))
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.affiliate')
	@validate(validators=dict(copemh=validators.Int()))
	def byCopemh(self, copemh):
		
		return self.default(copemh)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.search')
	@validate(validators=dict(escalafon=validators.String()))
	def byEscalafon(self, escalafon):
		
		return dict(affiliates=model.Affiliate.select(model.Affiliate.q.escalafon==escalafon))
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.affiliate.add")
	def add(self):
		return dict()
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(
			cardID=validators.String(),
			birthday=validators.DateTimeConverter(format='%Y-%m-%d'),
			escalafon=validators.String(),
			phone=validators.String(),
			birthPlace=validators.String(),
			gender=validators.String(),
			payment=validators.String(),
			escalafon=validators.String(),
			school=validators.String(),
			school2=validators.String(),
			inprema=validators.String(),
			town=validators.String(),
			state=validators.String(),
	))
	def save(self, **kw):
		
		if kw['cardID'] == '':
			flash(u'No se escribio un número de identidad')
			raise redirect('affiliate/add')
		try:
			affiliate = model.Affiliate.get(int(kw['affiliate']))
			del kw['affiliate']
			
			for key in kw.keys():
				setattr(affiliate, key, kw[key])
			
			flash('El afiliado ha sido actualizado!')
		
		except KeyError:
			affiliate = model.Affiliate(**kw)
			affiliate.complete(date.today().year)
			flash('El afiliado ha sido guardado!')
		
		raise redirect('/affiliate/%s' % affiliate.id)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.edit')
	def edit(self, cardID):
		
		affiliate = model.Affiliate.get(int(cardID))
		return dict(affiliate=affiliate)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.status')
	@validate(validators=dict(affiliate=validators.Int()))
	def status(self, affiliate):
		
		affiliate = model.Affiliate.get(affiliate)
		return dict(affiliate=affiliate, day=date.today())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.search')
	@validate(validators=dict(name=validators.string()))
	def search(self, name):
		
		if name == '':
			raise redirect('/affiliate')
		name.replace('\0', '')
		name = name.replace('*', '%')
		query = "affiliate.first_name LIKE '%%%s%%' or affiliate.last_name LIKE '%%%s%%'" % (name, name)
		affiliates = model.Affiliate.select(query)
		return dict(result=affiliates)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(cardID=validators.String()))
	def card(self, cardID):
		
		affiliate = model.Affiliate.select(model.Affiliate.q.cardID==cardID)
		
		if affiliate.count() == 0:
			flash(u'Número de identidad no encontrado')
			raise redirect('/affiliate')
		
		raise redirect('/affiliate/%s' % affiliate[0].id)
		
		redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(affiliate=validators.Int()))
	def off(self, affiliate):
		
		affiliate = model.Affiliate.get(affiliate)
		affiliate.active = False
		
		raise redirect('/affiliate/%s' % affiliate.id)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(affiliate=validators.Int()))
	def on(self, affiliate):
		
		affiliate = model.Affiliate.get(affiliate)
		affiliate.active = True
		
		raise redirect('/affiliate/%s' % affiliate.id)

	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(affiliate=validators.Int(),year=validators.Int()))
	def populate(self, affiliate, year):
		
		affiliate = model.Affiliate.get(affiliate)
		affiliate.complete(year)
		
		raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(affiliate=validators.Int()))
	def remove(self, affiliate):
		
		affiliate = model.Affiliate.get(affiliate)
		
		for loan in affiliate.loans:
			loan.remove()
		
		for cuota in affiliate.cuotaTables:
			cuota.destroySelf()
		
		affiliate.destroySelf()
		flash('El afiliado ha sido removido')
		
		raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.report')
	@validate(validators=dict(state=validators.String()))
	def department(self, state):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.state==state)
		count = affiliates.count()
		return dict(affiliates=affiliates, state=state, count=count)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.card')
	@validate(validators=dict(affiliate=validators.String()))
	def byRange(self, cardID):
		
		affiliates = model.Affiliate.select("affiliate.card_id like '%%%s%%'" % cardID)
		return dict(affiliates=affiliates, code=code, count=affiliates.count())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.list')
	@validate(validators=dict(year=validators.Int(),month=validators.Int(), how=validators.String()))
	def cotization(self, how, year, month):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.payment==how, orderBy="lastName")
		total = sum(a.total(year), month) for a in affiliates)
		return dict(affiliates=affiliates, count=affiliates.count(), year=year, month=month, how=how, total=total)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(affiliate=validators.Int(),how=validators.String(),
							  year=validators.Int(),month=validators.Int()))
	def posteo(self, code, how, year, month):
		
		affiliate = model.Affiliate.get(affiliate)
		affiliate.pay_cuota(year, month)
		
		for loan in affiliate.loans:
			loan.pay(loan.get_payment(), date.today(), "Planilla")
		
		raise redirect('/affiliate/cotization/?how=%s&year=%s&month=%s' % (how, year, month))

	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.report')
	@validate(begin=dict(affiliate=validators.Int(),end=validators.Int()))
	def aList(self, begin, end):
		
		query = "affiliate.id <= %s and affiliate.id >= %s" % (begin, end)
		affiliates = model.Affiliate.select(query)
		return dict(affiliates=affiliates, count=affiliates.count())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.affiliate')
	def last(self):
		
		return dict(affiliate=model.Affiliate.select(orderBy="-id")[0])
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.deactivate')
	@validate(validators=dict(affiliate=validators.Int()))
	def deactivate(self, affiliate):
		
		return dict(affiliate=model.Affiliate.get(affiliate))
	
	@identity.require(identity.not_anonymous())
	@validate(validators=dict(affiliate=validators.Int(), reason=validators.String()))
	def deactivateTrue(self, affiliate, reason):
		
		affiliate = model.Affiliate.get(code)
		affiliate.active = False
		affiliate.reason = reason
		raise redirect('/affiliate/%s' % affiliate.id)
	
	@identity.require(identity.not_anonymous())
	@validate(validators=dict(affiliate=validators.Int()))
	def activate(self, affiliate):
		
		affiliate = model.Affiliate.get(int(code))
		affiliate.active = True
		raise redirect('/affiliate/%s' % affiliate.id)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.payment')
	@validate(validators=dict(how=validators.String()))
	def payment(self, how):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.payment==how, orderBy="lastName")
		return dict(affiliates=affiliates, count=affiliates.count(), how=how)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.age')
	@validate(validators=dict(joined=validators.Int(),age=validators.Int()))
	def age(self, joined, age):
		
		day = date.today().year - age
		affiliates = model.Affiliate.select(model.Affiliate.birthday>=day)
		affiliates = [affiliate for affiliate in affiliates if affiliate.joined.year <= joined]
		
		return dict(affiliates=affiliate)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.posting')
	@validate(validators=dict(payment=validators.String(), year=validators.Int(),
							  month=validators.Int()))
	def posting(self, payment, year, month):
		
		query = "obligation.year = %s and obligation.month = %s" % (year, month)
		obligation = model.Obligation.select(query)[0]
		if payment == "INPREMA":
			obligation = obligation.inprema
		
		affiliates = model.Affiliate.select(model.Affiliate.q.payment==payment, orderBy="lastName")
		return dict(affiliates=affiliates, count=affiliates.count(), how=payment, obligation=obligation)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.show')
	def byDate(self, start, end):
		
		start = datetime.strptime(start, "%Y-%m-%d").date()
		end = datetime.strptime(end, "%Y-%m-%d").date
		query = "affiliate.joined >= '%s' and affiliate.joined <= '%s'" % (start, end)
		affiliates = model.Affiliate.select(query)
		return dict(affiliates=affiliates, start=start, end=end, show="Fecha de Afiliaci&oacute;n", count=affiliates.count())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.show')
	def byTown(self, town):
		
		town = str(town)
		affiliates = model.Affiliate.select(model.Affiliate.q.town==town)
		return dict(affiliates=affiliates, show="Municipio", count=affiliates.count())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.show')
	@validate(validators=dict(school=validators.String()))
	def bySchool(self, school):
		
		query = "affiliate.school = '%s' or affiliate.school2 = '%s'" % (school, school)
		affiliates = model.Affiliate.select(query)
		return dict(affiliates=affiliates, show="Instituto", count=affiliates.count())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.show')
	def disabled(self):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.active==False)
		return dict(affiliates=affiliates, show="Inhabilitados", count=affiliates.count())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.show')
	def all(self):
		
		affiliates = model.Affiliate.select()
		return dict(affiliates=affiliates, show="Todos", count=affiliates.count())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.manual')
	@validate(validators=dict(affiliate=validators.Int(),year=validators.Int(),month=validators.Int()))
	def manual(self, affiliate, year, month):
		
		affiliate = model.Affiliate.get(int(affiliate))
		query = "obligation.year = %s and obligation.month = %s" % (int(year), int(month))
		obligations = model.Obligation.select(query)
		obligation = 0
		
		if affiliate.payment == "INPREMA":
			obligation = sum(obligation.inprema for obligation in obligations)
			
		else:
			obligation = sum(obligation.amount for obligation in obligations)
		
		return dict(affiliate=affiliate, obligation=obligation, year=year, month=month)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(affiliate=validators.Int(), year=validators.Int(), month=validators.Int()))
	def complete(self, affiliate, year, month):
		
		affiliate = model.Affiliate.get(affiliate)
		[e.manual() for e in affiliate.extras]
		
		for loan in affiliate.loans:
			payment = loan.get_payment()
			
			kw = {}
			kw['amount'] = payment
			kw['affiliate'] = affiliate
			kw['account'] = model.Account.get(373)
			model.Deduced(**kw)
			model.OtherDeduced(**kw)
			loan.pay(payment, "Planilla", date.today())
		
		affiliate.pay_cuota(year, month)
		kw = {}
		
		query = "obligation.year = %s and obligation.month = %s" % (year, month)
		obligations = model.Obligation.select(query)
		if affiliate.payment == "INPREMA":
			kw['amount'] = sum(obligation.inprema for obligation in obligations)
		else:
			kw['amount'] = sum(obligation.amount for obligation in obligations)
		
		kw['affiliate'] = affiliate
		kw['account'] = model.Account.get(1)
		model.Deduced(**kw)
		model.OtherDeduced(**kw)
		
		return self.listmanual(affiliate.payment, year, month)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(extra=validators.Int(), year=validators.Int(), month=validators.Int()))
	def postextra(self, extra, year, month):
		
		extra = model.Extra.get(int(extra))
		affiliate = extra.affiliate
		extra.manual()
		
		flash('Se ha posteado la deduccion')
		
		return self.manual(affiliate.id, year, month)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(loan=validators.Int(),amount=validators.Money(),
							   year=validators.Int(),month=validators.Int()))
	def postloan(self, loan, amount, year, month):
		
		loan = model.Loan.get(loan)
		payment = loan.get_payment()
		kw = {}
		kw['amount'] = payment
		affiliate = loan.affiliate
		kw['affiliate'] = loan.affiliate
		kw['account'] = model.Account.get(373)
		model.Deduced(**kw)
		model.OtherDeduced(**kw)
		loan.pay(payment, "Planilla", date.today())
		
		flash('Se ha posteado el prestamo')
		
		return self.manual(loan.affiliate.id, year, month)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(loan=validators.Int(),amount=validators.Money()))
	def prestamo(self, loan, amount):
		
		loan = model.Loan.get(int(loan))
		kw = {}
		kw['amount'] = payment
		kw['affiliate'] = affiliate
		kw['account'] = model.Account.get(373)
		model.Deduced(**kw)
		model.OtherDeduced(**kw)
		loan.pay(payment, "Planilla", date.today())
		
		flash('Se ha posteado el prestamo')
		
		return self.manual(loan.affiliate.id, year, month)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(affiliate=validators.Int(),year=validators.Int(),month=validators.Int()))
	def postobligation(self, affiliate, month, year):
		
		affiliate = model.Affiliate.get(affiliate)
		affiliate.pay_cuota(year, month)
		
		kw = {}
		query = "obligation.year = %s and obligation.month = %s" % (year, month)
		obligations = model.Obligation.select(query)
		
		if affiliate.payment == "INPREMA":
			kw['amount'] = sum(obligation.inprema for obligation in obligations)
		else:
			kw['amount'] = sum(obligation.amount for obligation in obligations)
		
		kw['affiliate'] = affiliate
		kw['account'] = model.Account.get(1)
		model.Deduced(**kw)
		model.OtherDeduced(**kw)
		
		flash('Se ha posteado la obligacion')
		
		return self.manual(affiliate.id, year, month)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.payment2')
	def listmanual(self, payment, month, year):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.payment==str(payment), orderBy="lastName")
		return dict(affiliates=affiliates, count=affiliates.count(), how=payment, year=year, month=month)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.debt')
	def debt(self, payment):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.payment==str(payment))
		return dict(affiliates=affiliates, show=payment, count=affiliates.count())
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(payment=validators.String(),year=validators.String()))
	def massChange(self, payment, change):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.payment==payment)
		
		for affiliate in affiliates:
			
			affiliate.payment = change
		
		flash("Se han cambiado %s afiliados" % affiliates.count())
		raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.show')
	@validate(validators=dict(year=validators.Int()))
	def solvent(self, year):
		
		affiliates = model.Affiliate.select()
		affiliates = [affiliate for affiliate in affiliates if affiliate.multisolvent(year)]
		show = "Solventes al %s" % year
		return dict(affiliates=affiliates, show=show, count=len(affiliates))
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.year')
	def solventYear(self):
		
		years = {}
		tables = model.CuotaTable.select()
		
		for table in tables:
			
			if table.all():
				try:
					years[table.year] += 1
				except:
					years[table.year] = 1
		
		return dict(years=years)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.show')
	def none(self):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.joined==None)
		show = "Sin Año de Afiliación"
		return dict(affiliates=affiliates, show=show, count=affiliates.count())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.show')
	def noCard(self):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.cardID==None)
		show = "Sin N&uacute;mero de identidad"
		return dict(affiliates=affiliates, show=show, count=affiliates.count())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.jubilate')
	@validate(validators=dict(affiliate=validators.Int()))
	def jubilate(self, affiliate):
		
		affiliate = model.Affiliate.get(affiliate)
		return dict(affiliate=affiliate)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(affiliate=validators.Int(),
							  jubilated=validators.DateTimeConverter(format='%Y-%m-%d')))
	def inprema(self, affiliate, jubilated):
		
		affiliate = model.Affiliate.get(affiliate)
		affiliate.jubilated = jubilated
		affiliate.payment = "INPREMA"
		flash(affiliate.jubilated)
		return self.default(affiliate.id)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(affiliate=validators.Int(),start=validators.Int(),end=validators.Int()))
	def fill(self, affiliate, start, end):
		
		affiliate = model.Affiliate.get(affiliate)
		
		for n in range(start, end + 1):
			[affiliate.pay_cuota(n, month) for month in range(1, 13)]
		
		return self.status(affiliate.id)

