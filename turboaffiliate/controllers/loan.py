#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# loan.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2007, 2008, 2009 Carlos Flores <cafg10@gmail.com>
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

from turbogears import controllers, flash, redirect, identity, url
from turbogears import expose, validate, validators, error_handler
from cherrypy import request, response, NotFound, HTTPRedirect
from turboaffiliate import model, json, num2stres
from datetime import date, datetime
from decimal import *
import copy

class Deduction(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.deduction.add")	
	@validate(validators=dict(loan=validators.Int()))
	def add(self, loan):
		try:
			loan = model.Loan.get(loan)
			accounts = [a for a in model.Account.select() if a.code > 1000 and a.code < 2000]
			return dict(loan=loan, accounts=accounts)
		
		except model.SQLObjectNotFound:
			flash('El prestamo no se ha encontrado')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'No se encontro el prestamo')
			raise redirect('/loan')
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(loan=validators.Int(),account=validators.Int(),
							  amount=validators.String(),
							  description=validators.String()))
	def save(self, **kw):
		try:
			kw['loan'] = model.Loan.get(kw['loan'])
			kw['account'] = model.Account.get(kw['account'])
			kw['amount'] = Decimal(kw['amount'])
			kw['name'] = kw['account'].name
			
			log = dict()
			log['user'] = identity.current.user
			log['action'] = "Deduccion de %s al prestamo %s" % (kw['amount'], kw['loan'].id)
			model.Logger(**log)
			
			deduction = model.Deduction(**kw)
		
		except model.SQLObjectNotFound:
			flash('El préstamo no se ha encontrado')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'No se encontro el prestamo')
			raise redirect('/loan')
		raise redirect('/loan/%s' % kw['loan'].id)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(deduction=validators.Int()))
	def remove(self, deduction):
		
		try:
			deduction = model.Deduction.get(deduction)
			loan = deduction.loan
			deduction.destroySelf()
			
			log = dict()
			log['user'] = identity.current.user
			log['action'] = "Eliminada deduccion prestamo %s" % kw['loan'].id
			model.Logger(**log)
			
			raise redirect('/loan/%s' % loan.id)
		
		except model.SQLObjectNotFound:
			flash(u'No se encontro el prestamo')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'No se encontro el prestamo')
			raise redirect('/loan')

class Pay(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.pay.add")
	@validate(validators=dict(code=validators.Int()))
	def add(self, code):
		try:
			loan = model.Loan.get(code)
		
		except model.SQLObjectNotFound:
			flash('El prestamo no se ha encontrado')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'No se encontro el prestamo')
			raise redirect('/loan')
		
		return dict(loan=loan)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.pay.addfree")
	@validate(validators=dict(code=validators.Int()))
	def addfree(self, code):
		try:
			loan = model.Loan.get(code)
		
		except model.SQLObjectNotFound:
			flash('El prestamo no se ha encontrado')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'No se encontro el prestamo')
			raise redirect('/loan')
		
		return dict(loan=loan)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(code=validators.Int()))
	def remove(self, code):
		
		pay = model.Pay.get(code)
		loan = pay.loan
		pay.revert()
		raise redirect('/loan/%s' % loan.id)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(amount=validators.String(),code=validators.Int(),
							  receipt=validators.String(),
							  day=validators.DateTimeConverter(format='%Y-%m-%d')))
	def newfree(self, amount, day, code, receipt):
		
		loan = model.Loan.get(code)
		amount = Decimal(amount)
		id = loan.id
		if day == None: day = date.today()
		if loan.payfree(amount, receipt, day): raise redirect('/payed/%s' % id)
		log = dict()
		log['user'] = identity.current.user
		log['action'] = "Pago de %s al prestamo %s" % (amount, loan.id)
		model.Logger(**log)
		flash('El pago se ha efecutado')
		raise redirect('/loan/%s' % loan.id)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(amount=validators.String(),code=validators.Int(),
						  receipt=validators.String(),
						  day=validators.DateTimeConverter(format='%Y-%m-%d')))
	def new(self, amount, day, code, receipt):
		amount = Decimal(amount)
		loan = model.Loan.get(code)
		id = loan.id
		if day == None: day = date.today()
		log = dict()
		log['user'] = identity.current.user
		log['action'] = "Pago de %s al prestamo %s" % (amount, loan.id)
		model.Logger(**log)
		if loan.pay(amount, receipt, day): raise redirect('/payed/%s' % id)
		flash('El pago se ha efecutado')
		raise redirect('/loan/%s' % loan.id)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.pay.resume')
	@validate(validators=dict(start=validators.DateTimeConverter(format='%Y-%m-%d'),
							  end=validators.DateTimeConverter(format='%Y-%m-%d')))
	def resume(self, start, end):
		
		query = "pay.day >= '%s' and pay.day <= '%s'" % (start, end)
		
		pays = model.Pay.select(query)
		count = pays.count()
		capital = sum(pay.capital for pay in pays)
		interest = sum(pay.interest for pay in pays)
		
		return dict(pays=pays, count=count, capital=capital, interest=interest)

class Loan(controllers.Controller):
	
	pay = Pay()
	deduction = Deduction()
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.index')
	def index(self):
		return dict()
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.loan')
	@expose("json")
	@validate(validators=dict(code=validators.Int()))
	def default(self, code):
		
		loan = model.Loan.get(code)
		return dict(loan=loan, day=date.today())
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.pay")
	def payment(self, code):
	
		return dict(loan=model.Loan.get(code))
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.list")
	@validate(validators=dict(start=validators.DateTimeConverter(format='%Y-%m-%d'),
							  end=validators.DateTimeConverter(format='%Y-%m-%d'),
							  payment=validators.String()))
	def cotizacion(self, start, end, payment):
		
		query = "loan.start_date >= '%s' and loan.start_date <= '%s'" % (start, end)
		
		loans = model.Loan.select(query)
		
		loans = [l for l in loans if l.affiliate.payment==payment]
		
		return dict(loans=loans, count=len(loans),
					payment="de %s Periodo del %s al %s" % (payment,
							start.strftime('%d de %B de %Y'),
							end.strftime('%d de %B de %Y')),
					capital=sum(l.capital for l in loans),
					debt=sum(l.debt for l in loans))
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.list")
	@validate(validators=dict(depto=validators.String(),cotizacion=validators.String()))
	def cotizacionDepto(self, depto, cotizacion):
		
		loans = model.Loan.select()
		l = list()
		
		for loan in loans:
			
			if loan.affiliate.state == depto and loan.affiliate.payment == cotizacion:
			
				l.append(loan)
		
		return dict(loans=l, count=len(l), payment=cotizacion,
				debt=sum(loan.debt for loan in l), capital=sum(loan.capital for loan in l))
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.list")
	def dobles(self):
		
		loans = model.Loan.select()
		
		l = []
		
		for loan in loans:
			
			if len(loan.affiliate.loans) > 1:
				
				l.append(loan)
		
		return dict(loans=l, count=len(l), payment='',
				debt=sum(loan.debt for loan in l), capital=sum(loan.capital for loan in l))
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.add')
	@validate(validators=dict(affiliate=validators.Int()))
	def add(self, affiliate):

		affiliate = model.Affiliate.get(affiliate)
		#if (date.today() - affiliate.joined).days < 365:
		#	flash(u"El afiliado aún no tiene un año de afiliación")
		#	raise redirect('/affiliate/%s' % affiliate.id)
		#if len(affiliate.loans) > 0:
		#	
		#	for loan in affiliate.loans:
		#		
		#		if loan.percent() < 59:
		#			
		#			flash("El Afiliado no ha pagado el 60% del préstamo anterior")
		#			raise redirect('/affiliate/%s' % affiliate.id)
			
		return dict(affiliate=affiliate)
	
	@identity.require(identity.All(identity.not_anonymous(),
								   identity.has_permission("refinance")))
	@expose(template='turboaffiliate.templates.loan.add')
	@validate(validators=dict(affiliate=validators.Int()))
	def authorize(self, affiliate):
		
		return dict(affiliate=affiliate)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.edit')
	@validate(validators=dict(loan=validators.Int()))
	def edit(self, loan):
		
		return dict(loan=model.Loan.get(loan))
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(loan=validators.Int(),
							  months=validators.Int(),
							  capital=validators.Number(),
							  payment=validators.String()))
	def save(self, loan, capital, months, payment):
		
		
		log = dict()
		log['user'] = identity.current.user
		log['action'] = "Modificacion al prestamo %s" % loan.id
		model.Logger(**log)
		
		loan = model.Loan.get(loan)
		loan.capital = capital
		loan.months = months
		loan.payment = Decimal(payment).quantize(Decimal("0.01"))
		return self.default(loan.id)
		
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(affiliate=validators.Int(),
							  months=validators.Int(),
							  capital=validators.Number(),
							  payment=validators.String(),
							  startDate=validators.DateTimeConverter(format='%Y-%m-%d'),
							  id=validators.String()))
	def new(self, affiliate, **kw):
		
		affiliate = model.Affiliate.get(affiliate)
		kw['payment'] = Decimal(kw['payment']).quantize(Decimal("0.01"))
		kw['debt'] = kw['capital']
		kw['letters'] = num2stres.parse(kw['capital']).capitalize()
		if kw['id'] == '': del kw['id']
		if kw['capital'] < 0: raise redirect('/loan/add/%s' % affiliate.id)
		kw["aproval"] = identity.current.user
		loan = model.Loan(affiliate=affiliate, **kw)
		
		log = dict()
		log['user'] = identity.current.user
		log['action'] = "Otorgar prestamo al afiliado %s" % affiliate.id
		model.Logger(**log)
		
		raise redirect(url("/loan/%s" % loan.id))
	
	@identity.require(identity.All(identity.not_anonymous(), identity.has_permission("delete")))
	@expose()
	@validate(validators=dict(code=validators.Int()))
	def remove(self, code):
		
		loan = model.Loan.get(code)
		loan.remove()
		flash('El prestamo ha sido removido')
		raise redirect('/payed/%s' % code)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(loan=validators.Int(),months=validators.Int(),
			 payment=validators.String()))
	def month(self, loan, months, payment):
		
		loan = model.Loan.get(loan)
		loan.months = months
		loan.payment = Decimal(payment).quantize(Decimal("0.01"))
		raise redirect('/loan/%s' % loan.id)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(loan=validators.Int()))
	def refinance(self, loan):
		
		loan = model.Loan.get(loan)
		affiliate = loan.affiliate
		
		log = dict()
		log['user'] = identity.current.user
		log['action'] = "Prestamo %s refinanciado" % loan.id
		model.Logger(**log)
		
		loan.refinance()
		
		flash('El prestamo anterior ha sido movido a refinanciamiento')
		raise redirect('/loan/add/%s' % affiliate.id)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.pagare')
	@validate(validators=dict(loan=validators.Int()))
	def pagare(self, loan):
	
		return dict(loan=model.Loan.get(loan))
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.receipt')
	@validate(validators=dict(loan=validators.Int()))
	def receipt(self, loan):
		
		return dict(loan=model.Loan.get(loan))
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(loan=validators.Int()))
	def search(self, loan):
		raise redirect('/loan/%s' % loan)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.day')
	@validate(validators=dict(day=validators.DateTimeConverter(format='%Y-%m-%d')))
	def day(self, day):
		
		loans = model.Loan.select(model.Loan.q.startDate==day)
		amount = sum(l.capital for l in loans)
		return dict(amount=amount, loans=loans,day=day)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.list')
	@validate(validators=dict(first=validators.DateTimeConverter(format='%Y-%m-%d'),
							  last=validators.DateTimeConverter(format='%Y-%m-%d')))
	def period(self, first, last):
		
		query = "loan.start_date >= '%s' and loan.start_date <= '%s'" % (first, last)
		
		loans = model.Loan.select(query)
		count = loans.count()
		amount = sum(l.capital for l in loans)
		return dict(loans=loans, count=loans.count(),
					payment="Periodo del %s al %s" % (first.strftime('%d de %B de %Y'),
														last.strftime('%d de %B de %Y')),
					capital=sum(l.capital for l in loans),
					debt=sum(l.debt for l in loans))
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.cartera')
	@validate(validators=dict(first=validators.DateTimeConverter(format='%Y-%m-%d'),
							  last=validators.DateTimeConverter(format='%Y-%m-%d')))
	def cartera(self, first, last):
		
		loans = list()
		query = "loan.start_date >= '%s' and loan.start_date <= '%s' order by start_date" % (first, last)
		adeudados = [loan for loan in model.Loan.select(query)]
		
		query = "payed_loan.start_date >= '%s' and payed_loan.start_date <= '%s'" % (first, last)
		pagados = [loan for loan in model.PayedLoan.select(query)]
		
		for n in range(first.day, last.day + 1):
			loans.extend(loan for loan in adeudados if loan.startDate.day == n)
			loans.extend(loan for loan in pagados if loan.startDate.day == n)
		
		amount = sum(l.capital for l in loans)
		return dict(amount=amount, loans=loans, first=first, last=last, count=len(loans))
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.view')
	@validate(validators=dict(loan=validators.Int()))
	def view(self, loan):
		
		return dict(loan=model.Loan.get(loan))
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(loan=validators.Int(),payment=validators.String()))
	def modify(self, loan, payment):
		
		loan = model.Loan.get(loan)
		loan.payment = Decimal(payment)
		
		log = dict()
		log['user'] = identity.current.user
		log['action'] = "Cambio de cuota a %s de prestamo %s" % (payment, kw['loan'].id)
		model.Logger(**log)
		
		raise redirect('/loan/%s' % loan.id)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(loan=validators.Int(),debt=validators.String()))
	def debt(self, loan, debt):
		
		loan = model.Loan.get(loan)
		loan.debt = Decimal(debt)
		raise redirect('/loan/%s' % loan.id)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.monthly')
	@validate(validators=dict(start=validators.DateTimeConverter(format='%Y-%m-%d'),
							  end=validators.DateTimeConverter(format='%Y-%m-%d')))
	def monthly(self, start, end):
		
		query = "loan.start_date >= '%s' and loan.start_date <= '%s'" % (start, end)
		
		loans = model.Loan.select(query)
		
		li = list()
		
		for n in range(start.month, end.month + 1):
			
			month = dict()
			month['month'] = n
			month['amount'] = sum(l.capital for l in loans if l.startDate.month == n)
			month['number'] = len(l for l in loans if l.startDate.month == n)
			li.append(month)
		
		total = sum(m['amount'] for m in li)
		
		return dict(months=li, total=total)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.list')
	@validate(validators=dict(payment=validators.String()))
	def bypayment(self, payment):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.payment==payment)
		
		loans = list()
		for a in affiliates:
			loans.extend(l for l in a.loans)
		
		debt = sum(l.debt for l in loans)
		capital = sum(l.capital for l in loans)
		
		count = len(loans)
		
		return dict(loans=loans, count=count, debt=debt, capital=capital, payment=payment)
		
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.list')
	@validate(validators=dict(start=validators.DateTimeConverter(format='%Y-%m-%d'),
							  end=validators.DateTimeConverter(format='%Y-%m-%d'),
							  payment=validators.String()))
	def paymentDate(self, payment, start, end):
		
		query = "loan.start_date >= '%s' and loan.start_date <= '%s'" % (start, end)
		
		loans = model.Loan.select(query)
		
		loans = [l for l in loans if l.affiliate.payment==payment]
		
		debt = sum(l.debt for l in loans)
		capital = sum(l.capital for l in loans)
		
		count = len(loans)
		
		return dict(loans=loans, count=count, debt=debt, capital=capital, payment=payment)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.liquid')
	@validate(validators=dict(start=validators.DateTimeConverter(format='%Y-%m-%d'),
							  end=validators.DateTimeConverter(format='%Y-%m-%d')))
	def liquid(self, start, end):
		
		query = "loan.start_date >= '%s' and loan.start_date <= '%s'" % (start, end)
		
		loans = model.Loan.select(query)
		debt = sum(l.net() for l in loans)
		capital = sum(l.capital for l in loans)
		count = loans.count()
		
		return dict(loans=loans, count=count, debt=debt, capital=capital, payment="")
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(loan=validators.Int()))
	def increase(self, loan):
		
		loan = model.Loan.get(loan)
		loan.number += 1
		
		return self.default(loan.id)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(loan=validators.Int()))
	def decrease(self, loan):
		
		loan = model.Loan.get(loan)
		loan.number -= 1
		return self.default(loan.id)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.bypay')
	@validate(validators=dict(day=validators.DateTimeConverter(format='%Y-%m-%d')))
	def byCapital(self, day):
		
		pays = model.Pay.select(model.Pay.q.day==day)
		
		capital = sum(pay.capital for pay in pays)
		interest = sum(pay.interest for pay in pays)
		
		return dict(pays=pays, capital=capital, interest=interest)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.resume')
	@validate(validators=dict(start=validators.DateTimeConverter(format='%Y-%m-%d'),
							  end=validators.DateTimeConverter(format='%Y-%m-%d')))
	def resume(self, start, end):
		
		query = "pay.day >= '%s' and pay.day <= '%s'" % (start, end)
		
		pays = model.Pay.select(query)
		count = pays.count()
		capital = sum(pay.capital for pay in pays)
		interest = sum(pay.interest for pay in pays)
		
		query = "old_pay.day >= '%s' and old_pay.day <= '%s'" % (start, end)
		pays = model.OldPay.select(query)
		capital += sum(pay.capital for pay in pays)
		interest += sum(pay.interest for pay in pays)
		
		return dict(capital=capital, interest=interest, start=start, end=end)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.diverge')
	@validate(validators=dict(payment=validators.String(),
							  start=validators.DateTimeConverter(format='%d/%m/%Y'),
							  end=validators.DateTimeConverter(format='%d/%m/%Y')))
	def diverge(self, payment, start, end):
		
		query = "payed_loan.last >= '%s' and payed_loan.last <= '%s'" % (start, end)
		payed = model.PayedLoan.select(query)
		
		payed = [p for p in payed if len(p.affiliate.loans) > 0]
		
		payed = [p for p in payed if p.affiliate.loans[0].get_payment() != p.payment]
		
		payed = [p for p in payed if p.affiliate.payment == payment]
		
		return dict(payed=payed)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.payment')
	@validate(validators=dict(payment=validators.String()))
	def listPayment(self, payment):
		
		loans = model.Loan.select()
		
		return dict(loans=[l for l in loans if l.affiliate.payment == payment])

