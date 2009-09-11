#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# payed.py
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

class Pay(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.payed.pay")
	@validate(validators=dict(code=validators.Int()))
	def add(self, code):
		
		return dict(loan=model.PayedLoan.get(code))
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(code=validators.Int()))
	def remove(self, code):
		
		pay = model.OldPay.get(code)
		loan = pay.payedLoan
		capital = pay.capital
		pay.destroySelf()
		loan = loan.to_loan(identity.current.user)
		loan.debt += capital
		
		log = dict()
		log['user'] = identity.current.user
		log['action'] = "Eliminar pago del prestamo %s" % loan.id
		model.Logger(**log)
		
		raise redirect(url('/payed/%s' % loan.id))
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(amount=validators.Number(),
							day=validators.DateTimeConverter(format='%Y-%m-%d'),
							payedLoan=validators.Int()
							))
	def new(self, payedLoan, **kw):
		
		payedLoan = model.PayedLoan.get(payedLoan)
		
		model.OldPay(payedLoan=payedLoan, **kw)
		#loan.pay2(amount, day, receipt)
		
		log = dict()
		log['user'] = identity.current.user
		log['action'] = "Agregar pago al prestamo %s" % loan.id
		model.Logger(**log)
		
		flash('El pago se ha efecutado')
		raise redirect(url('/payed/%s' % payedLoan.id))

class PayedLoan(controllers.Controller):
	
	pay = Pay()
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.payed.payed")
	@validate(validators=dict(loan=validators.Int()))
	def default(self, loan):
		
		return dict(loan=model.PayedLoan.get(loan), day=date.today())
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.payed.list")
	@validate(validators=dict(payment=validators.String(),
							  start=validators.DateTimeConverter(format='%Y-%m-%d'),
							  end=validators.DateTimeConverter(format='%Y-%m-%d')))
	def payment(self, start, end, payment):
		
		query = "payed_loan.last >= '%s' and payed_loan.last <= '%s'" % (start, end)
		
		loans = model.PayedLoan.select(query)
		
		loans = [l for l in loans if l.affiliate.payment==payment]
		
		return dict(loans=loans, count=len(loans),
					payment="de %s Periodo del %s al %s" % (payment,
							start.strftime('%d de %B de %Y'),
							end.strftime('%d de %B de %Y')),
					capital=sum(l.capital for l in loans))
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.payed.list")
	@validate(validators=dict(start=validators.DateTimeConverter(format='%Y-%m-%d'),
							  end=validators.DateTimeConverter(format='%Y-%m-%d')))
	def period(self, start, end):
		
		query = "payed_loan.last >= '%s' and payed_loan.last <= '%s'" % (start, end)
		
		loans = model.PayedLoan.select(query)
		
		return dict(loans=loans, count=loans.count(),
					payment="Periodo del %s al %s" % (start.strftime('%d de %B de %Y'),
														end.strftime('%d de %B de %Y')),
					capital=sum(l.capital for l in loans))
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.payed.view')
	@validate(validators=dict(loan=validators.Int()))
	def view(self, loan):
		
		return dict(loan=model.PayedLoan.get(loan))
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(loan=validators.Int(),payment=validators.String()))
	def modify(self, loan, payment):
		
		loan = model.PayedLoan.get(loan)
		loan.payment = Decimal(payment)
		raise redirect(url('/payed/%s' % loan.id))
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(loan=validators.Int(),debt=validators.Number()))
	def debt(self, loan, debt):
		
		loan = model.PayedLoan.get(loan)
		loan.debt = debt
		raise redirect(url('/payed/%s' % loan.id))
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(loan=validators.Int()))
	def toLoan(self, loan):
		
		loan = model.PayedLoan.get(loan)
		loan = loan.to_loan(identity.current.user)
		raise redirect(url('/loan/%s' % loan.id))
	
	@identity.require(identity.All(identity.not_anonymous(), identity.has_permission("delete")))
	@expose()
	@validate(validators=dict(loan=validators.Int()))
	def remove(self, loan):
		
		loan = model.PayedLoan.get(loan)
		affiliate = loan.affiliate
		loan.remove()
		raise redirect(url('/affiliate/%s' % affiliate.id))
