#!/usr/bin/python
#
# payed.py
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

class Pay(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.payed.pay")
	def add(self, code):
		try:
			loan = model.PayedLoan.get(code)
		
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
			pay = model.OldPay.get(int(code))
			loan = pay.payedLoan
			capital = pay.capital
			pay.destroySelf()
			loan = loan.to_loan()
			loan.debt += capital
			raise redirect('/payed/%s' % loan.id)
		
		except model.SQLObjectNotFound:
			flash(u'No se encontro el pago')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'No se encontro el pago')
			raise redirect('/loan')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def new(self, **kw):
		try:
			day = datetime.strptime(kw['day'], "%Y-%m-%d").date()
			kw['payedLoan'] = model.PayedLoan.get(kw['payedLoan'])
			
			if kw['amount'] == '':
				flash(u'Cantidad incorrecta')
				raise redirect('/loan')
			
			model.OldPay(**kw)
			#loan.pay2(amount, day, receipt)
			flash('El pago se ha efecutado')
			raise redirect('/payed/%s' % kw['payedLoan'].id)
		
		except model.SQLObjectNotFound:
			flash('El prestamo no se ha encontrado')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'No se encontro el prestamo')
			raise redirect('/loan')

class PayedLoan(controllers.Controller):
	
	pay = Pay()
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.payed.payed")
	def default(self, id):
		
		try:
			loan = model.PayedLoan.get(int(id))
			return dict(loan=loan, day=date.today())
		
		except model.SQLObjectNotFound:
			flash(u'No se encontró el préstamo')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'No se encontró el préstamo')
			raise redirect('/loan')
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.loan.payed.view')
	def view(self, code):
		
		try:
			loan = model.PayedLoan.get(int(code))
			return dict(loan=loan)
		
		except model.SQLObjectNotFound:
			flash(u'No se encontro el prestamo')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'No se encontro el prestamo')
			raise redirect('/loan')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def modify(self, loan, payment):
		
		try:
			loan = model.PayedLoan.get(int(loan))
			loan.payment = Decimal(payment)
			raise redirect('/payed/%s' % loan.id)
		except:
			pass
		raise redirect('/payed/%s' % loan.id)
	
	@identity.require(identity.not_anonymous())
	@expose()
	def debt(self, loan, debt):
		
		try:
			loan = model.PayedLoan.get(int(loan))
			loan.debt = Decimal(debt)
			raise redirect('/payed/%s' % loan.id)
		except:
			pass
		raise redirect('/payed/%s' % loan.id)
	
	@identity.require(identity.not_anonymous())
	@expose()	
	def toLoan(self, loan):
		
		try:
			loan = model.PayedLoan.get(int(loan))
			loan = loan.to_loan()
			raise redirect('/loan/%s' % loan.id)
		
		except model.SQLObjectNotFound:
			flash(u'No se encontró el préstamo')
			raise redirect('/loan')
		
		except ValueError:
			flash(u'No se encontró el préstamo')
			raise redirect('/loan')
