#!/usr/bin/python
# -*- coding: utf8 -*-
#
# loan.py
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
from turboaffiliate import model, json, num2stres
from datetime import date, datetime
from decimal import *
import copy

class Deduction(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.deduction.add")	
	def add(self, code):
		try:
			loan = model.Loan.get(int(code))
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
	def save(self, **kw):
		try:
			kw['loan'] = model.Loan.get(int(kw['loan']))
			kw['account'] = model.Account.get(int(kw['account']))
			if kw['amount'] == '':
				flash(u'Cantidad incorrecta')
				raise redirect('/loan')
			
			kw['name'] = kw['account'].name
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
	def remove(self, deduction):
		
		try:
			deduction = model.Deduction.get(int(deduction))
			loan = deduction.loan
			deduction.destroySelf()
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
	def remove(self, code):
		
		try:
			pay = model.Pay.get(int(code))
			pay.loan.debt += pay.capital
			loan = pay.loan
			loan.number -= 1
			pay.destroySelf()
			raise redirect('/loan/%s' % loan.id)
		
		except model.SQLObjectNotFound:
			flash(u'No se encontró el pago')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'No se encontró el pago')
			raise redirect('/loan')
		
	
	@identity.require(identity.not_anonymous())
	@expose()
	def newfree(self, amount, day, code, receipt):
		try:
			day = datetime.strptime(day, "%Y-%m-%d").date()
			loan = model.Loan.get(code)
			
			if amount == '':
				flash(u'Cantidad incorrecta')
				raise redirect('/loan')
			
			id = loan.id
			if loan.payfree(amount, receipt, day):
				raise redirect('/payed/%s' % id)
			flash('El pago se ha efecutado')
			raise redirect('/loan/%s' % loan.id)
		
		except model.SQLObjectNotFound:
			flash('El prestamo no se ha encontrado')
			raise redirect('/payed/%s' % loan.id)
		
		except ValueError:
			flash(u'No se encontro el prestamo')
			raise redirect('/loan')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def new(self, amount, day, code, receipt):
		try:
			day = datetime.strptime(day, "%Y-%m-%d").date()
			loan = model.Loan.get(code)
			
			if amount == '':
				flash(u'Cantidad incorrecta')
				raise redirect('/loan')
			
			id = loan.id
			if loan.pay(amount, receipt, day):
				raise redirect('/payed/%s' % id)
			flash('El pago se ha efecutado')
			raise redirect('/loan/%s' % loan.id)
		
		except model.SQLObjectNotFound:
			flash('El prestamo no se ha encontrado')
			raise redirect('/payed/%s' % loan.id)
		
		except ValueError:
			flash(u'No se encontro el prestamo')
			raise redirect('/loan')
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.pay.resume')
	def resume(self, start, end):
		
		start = datetime.strptime(start, "%Y-%m-%d").date()
		end = datetime.strptime(end, "%Y-%m-%d").date()
		
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
	def default(self, code):
		
		try:
			loan = model.Loan.get(int(code))
			return dict(loan=loan, day=date.today())
		
		except model.SQLObjectNotFound:
			flash(u'No se encontró el préstamo')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'No se encontró el préstamo')
			raise redirect('/loan')
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.pay")
	def payment(self, code):
	
		try:
			loan = model.Loan.get(int(code))
			return dict(loan=loan)
		
		except model.SQLObjectNotFound:
			flash(u'No se encontrÃ³ el prÃ©stamo')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'No se encontró el prÃ©stamo')
			raise redirect('/loan')
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.add')
	def add(self, cardID):
		try:
			affiliate = model.Affiliate.get(int(cardID))
			#if (date.today() - affiliate.joined).days < 365:
			#	flash(u"El afiliado aún no tiene un año de afiliación")
			#	raise redirect('/affiliate/%s' % affiliate.id)
			return dict(affiliate=affiliate)
		
		except model.SQLObjectNotFound:
			flash('No se encontro el Afiliado')
			raise redirect('/loan')
		
		except ValueError:
			flash('Número de Afiliado invalido')
			raise redirect('/loan')
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.edit')
	def edit(self, code):
		try:
			loan = model.Loan.get(int(code))
			return dict(loan=loan)
		
		except model.SQLObjectNotFound:
			flash('No se encontro el Afiliado')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'NÃºmero de Afiliado invalido')
			raise redirect('/loan')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def save(self, **kw):
		
		try:
			loan = model.Loan.get(int(kw['id']))
			loan.capital = kw['capital'].replace(',', '')
			loan.months = int(kw['months'])
			loan.payment = Decimal(kw['payment']).quantize(Decimal("0.01"))
			return self.default(loan.id)
		
		except model.SQLObjectNotFound:
			flash('No se encontro el Afiliado')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'Número de Afiliado invalido')
			raise redirect('/loan')
		
	@identity.require(identity.not_anonymous())
	@expose()
	def new(self, **kw):
		
		try:
			kw['affiliate'] = model.Affiliate.get(kw['cardID'])
		
		except model.SQLObjectNotFound:
			flash('No se encontro el Afiliado')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'Número de Afiliado invalido')
			raise redirect('/loan')
		
		if kw['capital'] == '' or kw['capital'] < 0:
			flash(u'Cantidad incorrecta')
			raise redirect('/loan/add')
		try:
			loank = copy.copy(kw)
			del loank['cardID']
			del loank['avalCard']
			del loank['avalFirst']
			del loank['avalLast']
			
			# Cleaning amount from commas
			loank['capital'] = loank['capital'].replace(',', '')
			loank['capital'] = Decimal(loank['capital'])
			loank['debt'] = loank['capital']
			loank['letters'] = num2stres.parse(loank['capital']).capitalize()
			loank['months'] = int(loank['months'])
			loank['payment'] = Decimal(loank['payment']).quantize(Decimal("0.01"))
			loank['startDate'] = datetime.strptime(loank['startDate'], "%Y-%m-%d").date()
			
			if loank['id'] == '':
				del loank['id']

		except ValueError:
			flash(u'Campo Invalido')
			raise redirect('/loan/add/%s' % kw['affiliate'].id)
		
		aval = {}
		aval['cardID'] = kw['avalCard']
		aval['firstName'] = kw['avalFirst']
		aval['lastName'] = kw['avalLast']
		# loank['aval'] = model.Aval(**aval)
		
		loan = model.Loan(**loank)
		flash(u'Se ha otorgado el préstamo')
		return self.default(loan.id)
	
	@identity.require(identity.not_anonymous())
	@expose()
	def remove(self, code):
		
		try:
			loan = model.Loan.get(int(code))
			loan.remove()
			flash('El prestamo ha sido removido')
			raise redirect('/payed/%s' % code)
		
		except model.SQLObjectNotFound:
			flash(u'No se encontró el prestamo')
			raise redirect('/loan')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def month(self, **kw):
		
		try:
			loan = model.Loan.get(int(kw['loan']))
			loan.months = int(kw['months'])
			loan.payment = Decimal(kw['payment'])
			raise redirect('/loan/%s' % loan.id)
		except KeyError:
			flash('Ha ocurrido un error')
			raise redirect('/loan')
		except model.SQLObjectNotFound:
			flash('No se encontro el prestamo')
			raise redirect('/loan')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def refinance(self, loan):
		
		loan = model.Loan.get(int(loan))
		affiliate = loan.affiliate
		loan.refinance()
		flash('El prestamo anterior ha sido movido a refinanciamiento')
		raise redirect('/loan/add/%s' % affiliate.id)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.pagare')
	def pagare(self, code):
		code = int(code)
		try:
			loan = model.Loan.get(code)
			return dict(loan=loan)
		
		except model.SQLObjectNotFound:
			flash('No se encontró el préstamo')
			raise redirect('/loan')
		
		except ValueError:
			flash('No se encontró el préstamo')
			raise redirect('/loan')
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.receipt')
	def receipt(self, code):
		try:
			loan = model.Loan.get(int(code))
			return dict(loan=loan)
		
		except model.SQLObjectNotFound:
			flash('No se encontró el préstamo')
			raise redirect('/loan')
		
		except ValueError:
			flash('No se encontró el préstamo')
			raise redirect('/loan')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def search(self, code):
		raise redirect('/loan/%s' % code)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.day')
	def day(self, day):
		
		day = datetime.strptime(day, "%Y-%m-%d").date()
		
		loans = model.Loan.select(model.Loan.q.startDate==day)
		amount = sum(l.capital for l in loans)
		return dict(amount=amount, loans=loans,day=day)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.period')
	def period(self, first, last):
		
		first = datetime.strptime(first, "%Y-%m-%d").date()
		last = datetime.strptime(last, "%Y-%m-%d").date()
		
		query = "loan.start_date >= '%s' and loan.start_date <= '%s'" % (first, last)
		
		loans = model.Loan.select(query)
		count = loans.count()
		amount = sum(l.capital for l in loans)
		return dict(amount=amount, loans=loans, first=first, last=last, count=count)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.cartera')
	def cartera(self, first, last):
		
		first = datetime.strptime(first, "%Y-%m-%d").date()
		last = datetime.strptime(last, "%Y-%m-%d").date()
		
		query = "loan.start_date >= '%s' and loan.start_date <= '%s'" % (first, last)
		
		loans = model.Loan.select(query)
		count = loans.count()
		amount = sum(l.capital for l in loans)
		return dict(amount=amount, loans=loans, first=first, last=last, count=count)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.view')
	def view(self, code):
		
		try:
			loan = model.Loan.get(int(code))
			return dict(loan=loan)
		
		except model.SQLObjectNotFound:
			flash(u'No se encontró el préstamo')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'No se encontró el préstamo')
			raise redirect('/loan')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def modify(self, loan, payment):
		
		try:
			loan = model.Loan.get(int(loan))
			loan.payment = Decimal(payment)
			raise redirect('/loan/%s' % loan.id)
		except:
			pass
		raise redirect('/loan/%s' % loan.id)
	
	@identity.require(identity.not_anonymous())
	@expose()
	def debt(self, loan, debt):
		
		try:
			loan = model.Loan.get(int(loan))
			loan.debt = Decimal(debt)
			raise redirect('/loan/%s' % loan.id)
		except:
			pass
		raise redirect('/loan/%s' % loan.id)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.monthly')
	def monthly(self, start, end):
		
		start = datetime.strptime(start, "%Y-%m-%d").date()
		end = datetime.strptime(end, "%Y-%m-%d").date()
		
		query = "loan.start_date >= '%s' and loan.start_date <= '%s'" % (start, end)
		
		loans = model.Loan.select(query)
		
		li = []
		
		for n in range(start.month, end.month + 1):
			
			month = {}
			month['month'] = n
			month['amount'] = sum(l.capital for l in loans if l.startDate.month == n)
			month['number'] = len(l for l in loans if l.startDate.month == n)
			li.append(month)
		
		total = sum(m['amount'] for m in li)
		
		return dict(months=li, total=total)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.list')
	def bypayment(self, payment):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.payment==str(payment))
		
		loans = []
		for a in affiliates:
			loans.extend(l for l in a.loans)
		
		debt = sum(l.debt for l in loans)
		capital = sum(l.capital for l in loans)
		
		count = len(loans)
		
		return dict(loans=loans, count=count, debt=debt, capital=capital, payment=payment)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.liquid')
	def liquid(self, start, end):
		
		start = datetime.strptime(start, "%Y-%m-%d").date()
		end = datetime.strptime(end, "%Y-%m-%d").date()
		
		query = "loan.start_date >= '%s' and loan.start_date <= '%s'" % (start, end)
		
		loans = model.Loan.select(query)
		debt = sum(l.net() for l in loans)
		capital = sum(l.capital for l in loans)
		count = loans.count()
		
		return dict(loans=loans, count=count, debt=debt, capital=capital, payment="")
	
	@identity.require(identity.not_anonymous())
	@expose()
	def increase(self, loan):
		
		try:
			loan = model.Loan.get(int(loan))
			loan.number += 1
		except:
			pass
		return self.default(loan.id)
	
	@identity.require(identity.not_anonymous())
	@expose()
	def decrease(self, loan):
		
		try:
			loan = model.Loan.get(int(loan))
			loan.number -= 1
		except:
			pass
		return self.default(loan.id)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.bypay')
	def byCapital(self, day):
		
		day = datetime.strptime(day, "%Y-%m-%d").date()
		
		pays = model.Pay.select(model.Pay.q.day==day)
		
		capital = sum(pay.capital for pay in pays)
		interest = sum(pay.interest for pay in pays)
		
		return dict(pays=pays, capital=capital, interest=interest)
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.resume')
	def resume(self, start, end):
		
		start = datetime.strptime(start, "%Y-%m-%d").date()
		end = datetime.strptime(end, "%Y-%m-%d").date()
		
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
