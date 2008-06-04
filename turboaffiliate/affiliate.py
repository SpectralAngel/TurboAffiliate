#!/usr/bin/python
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

from turbogears import controllers, expose, flash, identity, redirect
from cherrypy import request, response, NotFound, HTTPRedirect
from turboaffiliate import model, json, cuota, extra
from decimal import *
from datetime import date, datetime

class Affiliate(controllers.Controller):
	
	"""Manage Affiliate data"""
	
	cuota = cuota.Cuota()
	extra = extra.Extra()
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.index')
	def index(self):
		import time
		return dict(now=time.ctime())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.affiliate')
	def default(self, affiliate):
		
		try:
			affiliate = model.Affiliate.get(int(affiliate))
		except model.SQLObjectNotFound:
			flash('No existe el Afiliado con Identidad %s' % cardID)
			redirect('/affiliate')
		else:
			return dict(affiliate=affiliate)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.search')
	def byCardID(self, cardID):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.cardID==cardID)
		return dict(affiliates=affiliates)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.deduced')
	def deduced(self, code):
		
		try:
			affiliate = model.Affiliate.get(int(code))
			return dict(deduced=affiliate.deduced)
		except model.SQLObjectNotFound:
			flash('No existe el Afiliado con Identidad %s' % code)
			redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.affiliate')
	def byCopemh(self, copemh):
		
		try:
			affiliate = model.Affiliate.get(int(copemh))
			return dict(affiliate=affiliate)
		except model.SQLObjectNotFound:
			flash('El numero de COPEMH no se encontro')
			raise redirect('/affiliate')

		except ValueError:
			flash(u'Número de Afiliado invalido')
			raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.search')
	def byEscalafon(self, escalafon):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.escalafon==escalafon)
		return dict(affiliates=affiliates)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.affiliate.add")
	def add(self):
		return dict()
	
	@identity.require(identity.not_anonymous())
	@expose()
	def save(self, **kw):
		
		if kw['cardID'] == '':
			flash(u'No se escribio un número de identidad')
			raise redirect('affiliate/add')
			
		kw['birthday'] = datetime.strptime(kw['birthday'], "%Y-%m-%d").date()
		kw['escalafon'] = kw['escalafon'].upper()
		
		try:
			affiliate = model.Affiliate.get(int(kw['affiliate']))
			del kw['affiliate']
			kw['joined'] = datetime.strptime(kw['joined'], "%Y-%m-%d").date()
			
			for key in kw.keys():
				setattr(affiliate, key, kw[key])
			
			flash('El afiliado ha sido actualizado!')
		
		except model.SQLObjectNotFound:
			affiliate = model.Affiliate(**kw)
			affiliate.complete(date.today().year)
			flash('El afiliado ha sido guardado!')
		
		except KeyError:
			affiliate = model.Affiliate(**kw)
			affiliate.complete(date.today().year)
			flash('El afiliado ha sido guardado!')
		
		except ValueError:
			flash(u'Número de Afiliado invalido')
			raise redirect('/affiliate')
		
		raise redirect('/affiliate/%s' % affiliate.id)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.edit')
	def edit(self, cardID):
		
		affiliate = model.Affiliate.get(int(cardID))
		return dict(affiliate=affiliate)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.status')
	def status(self, cardID):
		
		try:
			affiliate = model.Affiliate.get(int(cardID))
			return dict(affiliate=affiliate, day=date.today())
		
		except model.SQLObjectNotFound:
			flash('No existe el Afiliado %s' % cardID)
		
		except ValueError:
			flash(u'Número de Afiliado invalido')
			raise redirect('/affiliate')
		
		redirect('/afiliate')
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.search')
	def search(self, name):
		
		if name == '':
			raise redirect('/affiliate')
		name = str(name)
		name.replace('\0', '')
		name = name.replace('*', '%')
		query = "affiliate.first_name LIKE '%%%s%%' or affiliate.last_name LIKE '%%%s%%'" % (name, name)
		affiliates = model.Affiliate.select(query)
		return dict(result=affiliates)
	
	@identity.require(identity.not_anonymous())
	@expose()
	def card(self, cardID):
		
		try:
			cardID = str(cardID)
			affiliate = model.Affiliate.select(model.Affiliate.q.cardID==cardID)
			
			if affiliate.count() == 0:
				flash(u'Número de identidad no encontrado')
				raise redirect('/affiliate')
			
			raise redirect('/affiliate/%s' % affiliate[0].id)
		
		except ValueError:
			flash(u'Número de Afiliado invalido')
			raise redirect('/affiliate')
		
		redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def off(self, cardID):
		
		try:
			affiliate = model.Affiliate.get(int(cardID))
			affiliate.active = False
		
		except model.SQLObjectNotFound:
			flash('El numero de affiliado %s no se encontro.' % cardID)
		
		except ValueError:
			flash(u'Numero de Afiliado invalido')
			raise redirect('/affiliate')
		
		raise redirect('/affiliate/%s' % cardID)
	
	@identity.require(identity.not_anonymous())
	@expose()
	def on(self, cardID):
		
		try:
			affiliate = model.Affiliate.get(int(cardID))
			affiliate.active = True
		
		except model.SQLObjectNotFound:
			flash('El número de afiliado %s no se encontró³.' % cardID)
		
		except ValueError:
			flash('Número de Afiliado invalido')
			raise redirect('/affiliate')
		
		raise redirect('/affiliate/%s' % cardID)

	@identity.require(identity.not_anonymous())
	@expose()
	def populate(self, **kw):
		
		try:
			affiliate = model.Affiliate.get(int(kw['affiliate']))
			affiliate.complete(int(kw['year']))
		
		except model.SQLObjectNotFound:
			flash(u'No se encontró el afiliado')
		
		except ValueError:
			flash(u'Número de Afiliado invalido')
			raise redirect('/affiliate')
		
		raise redirect('/affiliate')

	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.print')
	def printer(self, code):
		try:
			affiliate = model.Affiliate.get(int(code))
			return dict(affiliate=affiliate, day=date.today())
		
		except model.SQLObjectNotFound:
			flash(u'No se encontró el afiliado')
			raise redirect('/affiliate')
		
		except ValueError:
			flash(u'Número de Afiliado invalido')
			raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def remove(self, code):
		
		try:
			affiliate = model.Affiliate.get(int(code))
		
		except model.SQLObjectNotFound:
			flash('El número de identidad %s no se encontró' % code)

		except ValueError:
			flash('Número de Afiliado invalido')
			raise redirect('/affiliate')
		
		else:
			for loan in affiliate.loans:
				loan.remove()
			
			for cuota in affiliate.cuotaTables:
				cuota.destroySelf()
			
			affiliate.destroySelf()
			flash('El afiliado ha sido removido')
		
		raise redirect('/affiliate')

	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.resume')
	def resume(self, code):
		
		try:
			affiliate = model.Affiliate.get(int(code))
			return dict(affiliate=affiliate)
		
		except model.SQLObjectNotFound:
			raise redirect('/affiliate')
		
		except ValueError:
			flash(u'NÃºmero de Afiliado invalido')
			raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.report')
	def department(self, state):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.state==str(state))
		count = affiliates.count()
		return dict(affiliates=affiliates, state=state, count=count)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.card')
	def byRange(self, code):
		
		query = "affiliate.card_id like '%%%s%%'" % (str(code))
		affiliates = model.Affiliate.select(query)
		return dict(affiliates=affiliates, code=code, count=affiliates.count())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.list')
	def cotization(self, how, year, month):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.payment==str(how), orderBy="lastName")
		total = sum(a.total(int(year), int(month)) for a in affiliates)
		return dict(affiliates=affiliates, count=affiliates.count(), year=str(year), month=str(month), how=how, total=total)
	
	@identity.require(identity.not_anonymous())
	@expose()
	def posteo(self, code, how, year, month):
		
		try:
			affiliate = model.Affiliate.get(int(code))
			affiliate.pay_cuota(int(year), int(month))
			
			for loan in affiliate.loans:
				loan.pay2(loan.get_payment(), date.today(), "Planilla")
		
		except model.SQLObjectNotFound:
			flash(u'El numero de identidad %s no se encontro' % code)
		
		raise redirect('/affiliate/cotization/?how=%s&year=%s&month=%s' % (how, year, month))

	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.report')
	def aList(self, begin, end):
		
		query = "affiliate.id <= %s and affiliate.id >= %s"
		affiliates = model.Affiliate.select(query)
		return dict(affiliates=affiliates, count=affiliates.count())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.affiliate')
	def last(self):
		
		return dict(affiliate=model.Affiliate.select(orderBy="-id")[0])
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.deactivate')
	def deactivate(self, code):
		
		return dict(affiliate=model.Affiliate.get(code))
	
	@identity.require(identity.not_anonymous())
	def deactivateTrue(self, code, reason):
		
		try:
			affiliate = model.Affiliate.get(int(code))
			affiliate.active = False
			affiliate.reason = reason
			raise redirect('/affiliate/%s' % affiliate.id)
		
		except:
			raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	def activate(self, code):
		
		try:
			affiliate = model.Affiliate.get(int(code))
			affiliate.active = True
			raise redirect('/affiliate/%s' % affiliate.id)
		
		except:
			raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.payment')
	def payment(self, how):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.payment==str(how), orderBy="lastName")
		return dict(affiliates=affiliates, count=affiliates.count(), how=how)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.age')
	def age(self, joined, age):
		
		day = date.today().year - int(age)
		affiliates = model.Affiliate.select(model.Affiliate.birthday>=day)
		affiliates = [affiliate for affiliate in affiliates if affiliate.joined.year <= joined]
		
		return dict(affiliates=affiliate)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.posting')
	def posting(self, payment, year, month):
		
		query = query = query = "obligation.year = %s and obligation.month = %s" % (int(year), int(month))
		obligation = model.Obligation.select(query)[0]
		if payment == "INPREMA":
			obligation = obligation.inprema
		
		affiliates = model.Affiliate.select(model.Affiliate.q.payment==str(payment), orderBy="lastName")
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
	def bySchool(self, school):
		
		school = str(school)
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
	def complete(self, affiliate, year, month):
		
		affiliate = model.Affiliate.get(int(affiliate))
		(year, month) = (int(year), int(month))
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
		
		query = "obligation.year = %s and obligation.month = %s" % (int(year), int(month))
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
	def postextra(self, extra, year, month):
		
		extra = model.Extra.get(int(extra))
		affiliate = extra.affiliate
		extra.manual()
		
		flash('Se ha posteado la deduccion')
		
		return self.manual(affiliate.id, year, month)
	
	@identity.require(identity.not_anonymous())
	@expose()
	def postloan(self, loan, amount, year, month):
		
		loan = model.Loan.get(int(loan))
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
	def postobligation(self, affiliate, month, year):
		
		affiliate = model.Affiliate.get(int(affiliate))
		(year, month) = (int(year), int(month))
		affiliate.pay_cuota(year, month)
		
		kw = {}
		query = "obligation.year = %s and obligation.month = %s" % (int(year), int(month))
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
	def massChange(self, payment, change):
		
		(payment, change) = (str(payment), str(change))
		affiliates = model.Affiliate.select(model.Affiliate.q.payment==payment)
		
		for affiliate in affiliates:
			
			affiliate.payment = change
		
		flash("Se han cambiado %s afiliados" % affiliates.count())
		raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.show')
	def solvent(self, year):
		
		year = int(year)
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
	def jubilate(self, affiliate):
		
		try:
			affiliate = model.Affiliate.get(int(affiliate))
			return dict(affiliate=affiliate)
		except:
			raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def inprema(self, **kw):
		
		try:
			affiliate = model.Affiliate.get(kw['affiliate'])
			affiliate.jubilated = datetime.strptime(kw['jubilated'], "%Y-%m-%d").date()
			affiliate.payment = "INPREMA"
			flash(affiliate.jubilated)
			return self.default(affiliate.id)
		except:
			return self.index()
	
	@identity.require(identity.not_anonymous())
	@expose()
	def fill(self, affiliate, start, end):
		
		(affiliate, start, end) = (int(affiliate), int(start), int(end))
		
		affiliate = model.Affiliate.get(affiliate)
		
		for n in range(start, end + 1):
			[affiliate.pay_cuota(n, month) for month in range(1, 13)]
		
		return self.status(affiliate.id)
