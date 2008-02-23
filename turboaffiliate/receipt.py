#!/usr/bin/python
# -*- coding: utf8 -*-
#
# receipt.py
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
from turboaffiliate import model, json
from datetime import date,datetime
from decimal import *

class Line(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose()
	def save(self, **kw):
		
		try:
			receipt = model.Receipt.get(int(kw['receipt']))
		except model.SQLObjectNotFound:
			flash('No se ha encontrado el recibo %s' % kw['receipt'])
			raise redirect('/receipt')
		except ValueError:
			flash(u'Número de recibo incorrecto')
			raise redirect('/receipt')
		
		try:
			kw['account'] = model.Account.byCode(int(kw['account']))
		except model.SQLObjectNotFound:
			flash('No se ha encontrado la cuenta %s' % kw['account'])
			raise redirect('/receipt')
		except ValueError:
			flash(u'Número de recibo incorrecto')
			raise redirect('/receipt')
		
		kw['receipt'] = receipt
		kw['qty'] = int(kw['qty'])
		line = model.Line(**kw)
		line.act()
		raise redirect('/receipt/%s' % receipt.id)
	
	@identity.require(identity.not_anonymous())
	@expose()
	def remove(self, code):
		try:
			line = model.Line.get(int(code))
			c = line.receipt.id
			line.undo()
			line.destroySelf()
		except model.SQLObjectNotFound:
			raise redirect('/receipt/')
		raise redirect('/receipt/%s' % c)

class Cuotas(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.receipt.cuotas.cuotas")
	def default(self, **kw):
		
		day = datetime.strptime(kw['day'], "%Y-%m-%d").date()
		house = int(kw['house'])
		
		query = "receipt.day = '%s' and receipt.house_id = %s" % (day, house)
		receipts = model.Receipt.select(query)
		
		accounts = [456, 463, 472, 479, 488, 496, 504, 530, 541, 571, 581, 616, 619, 630, 643]
		accounts.sort()
		accounts = [model.Account.get(account) for account in accounts]
		
		cuotas = {}
		
		for receipt in receipts:
			for line in receipt.lines:
				if line.account in accounts:
					try:
						cuotas[line.account] += 1
					except:
						cuotas[line.account] = 1
		
		return dict(cuotas=cuotas, day=day)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.receipt.cuotas.company")
	def company(self, **kw):
		
		day = datetime.strptime(kw['day'], "%Y-%m-%d").date()
		house = int(kw['house'])
		
		query = "receipt.day = '%s' and receipt.house_id = %s" % (day, house)
		receipts = model.Receipt.select(query)
		
		accounts = [456, 463, 472, 479, 488, 496, 504, 530, 541, 571, 581, 616, 619, 630, 643]
		accounts.sort()
		accounts = [model.Account.get(account) for account in accounts]
		
		cuotas = {}
		
		for receipt in receipts:
			for line in receipt.lines:
				if line.account in accounts:
					try:
						cuotas[line.account] += 1
					except:
						cuotas[line.account] = 1
		
		return dict(cuotas=cuotas, day=day, company=str(kw['company']))

class Cut(controllers.Controller):
		
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.receipt.cut.cut")
	def default(self, **kw):
		
		try:
			house = model.House.get(int(kw['house']))
		
		except model.SQLObjectNotFound:
			raise redirect('/')
		
		except ValueError:
			flash(u'Valor No Válido')
			raise redirect('/')
		
		day = datetime.strptime(kw['day'], "%Y-%m-%d").date()
		
		a = model.Account.select()
		accounts = {}
		for account in a:
			accounts[account] = 0
		
		query = "receipt.day = '%s' and receipt.house_id = %s" % (day, house.id)
		receipts = model.Receipt.select(query)
		for receipt in receipts:
			for line in receipt.lines:
				accounts[line.account] += line.amount
		
		for key in accounts.keys():
			if accounts[key] == 0:
				del accounts[key]
		
		total = sum(item for key, item in accounts.items())
		
		return dict(accounts=accounts, house=house, day=day, total=total)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.receipt.cut.company")
	def company(self, **kw):
		
		try:
			house = model.House.get(int(kw['house']))
		
		except model.SQLObjectNotFound:
			raise redirect('/')
		
		except ValueError:
			flash(u'Valor No Válido')
			raise redirect('/')
		
		day = Pdatetime.strptime(kw['day'], "%Y-%m-%d").date()
		
		a = model.Account.select()
		accounts = {}
		for account in a:
			accounts[account] = 0
		
		query = "receipt.day = '%s' and receipt.house_id = %s" % (day, house.id)
		receipts = model.Receipt.select(query)
		
		for receipt in receipts:
			for line in receipt.lines:
				if line.account.company == kw['company']:
					accounts[line.account] += line.amount
		
		for key in accounts.keys():
			if accounts[key] == 0:
				del accounts[key]
		
		total = sum(value for value in accounts.values())
		
		receipts = model.Receipt.select(query)
		
		account = [456, 463, 472, 479, 488, 496, 504, 530, 541, 571, 581, 616,
					619, 630, 643]
		account.sort()
		account = [model.Account.get(account) for account in account]
		
		cuotas = {}
		
		for receipt in receipts:
			for line in receipt.lines:
				if line.account in account:
					try:
						cuotas[line.account] += 1
					except:
						cuotas[line.account] = 1
		
		cuotaTotal = {}
		for key in cuotas.keys():
			
			cuotaTotal[key] = sum(detail.amount * cuotas[key] for detail in key.details if detail.company == kw['company'])
		
		company = str()
		if kw['company'] == 'fas':
			company = 'Fondo AutoSeguro'
		
		else:
			company = 'Junta Directiva Central'
		
		grandTotal = sum(cuotaTotal[key] for key in cuotaTotal.keys()) + total
		
		return dict(accounts=accounts, house=house, day=day, total=total, grandTotal=grandTotal,
					cuotas=cuotas, company=kw['company'], cuotaTotal=cuotaTotal, title=company)

class Receipt(controllers.Controller):
	
	"""Controller for receipt management
	
	It is in charge of managing receipt creation, automatic account posting and
	receipt printing
	"""
	
	line = Line()
	cut = Cut()
	cuotas = Cuotas()
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.receipt.index")
	def index(self):
		
		return dict(houses=model.House.select())
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.receipt.receipt")
	@expose("json")
	def default(self, code):
		
		try:
			receipt = model.Receipt.get(int(code))
			return dict(receipt=receipt, accounts=model.Account.select())
		except model.SQLObjectNotFound:
			flash("El recibo %s no ha sido encontrado" % code)
			return dict(receipt=None)

	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.receipt.receipt")
	def search(self, code):
		
		raise redirect('/receipt/%s' % code)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.receipt.add")
	def add(self):
		
		houses = model.House.select()
		return dict(houses=houses)
	
	@identity.require(identity.not_anonymous())
	@expose()
	def new(self, **kw):
		
		try:
			if kw['affiliate'] != '':
				affiliate = model.Affiliate.get(int(kw['affiliate']))
				kw['affiliate'] = affiliate.id
				kw['name'] = affiliate.firstName + ' ' + affiliate.lastName
			
			else:
				kw['affiliate'] = 0
			
			if kw['day'] == '':
				del kw['day']
			
			else:
				kw['day'] = datetime.strptime(kw['day'], "%Y-%m-%d").date()
			
			kw['id'] = int(kw['id'])
			kw['house'] = model.House.get(int(kw['house']))
		
		except ValueError:
			flash(u'Valor No Válido')
			raise redirect('/receipt/add')
		
		receipt = model.Receipt(**kw)
		raise redirect('/receipt/%s' % receipt.id)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.receipt.edit")
	def edit(self, receipt):
		
		try:
			receipt = model.Receipt.get(int(receipt))
			receipt.closed = False
			return dict(receipt=receipt, accounts=model.Account.select())
			
		except:
			raise redirect('/receipt')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def save(self, **kw):
		
		try:
			receipt = model.Receipt.get(kw['receipt'])
			del kw['receipt']
			for key in kw.keys():
				if kw[key] == '':
					continue
				if key == 'affiliate':
					kw[key] = int(kw[key])
				setattr(receipt, key, kw[key])
			receipt.closed = True
		
		except model.SQLObjectNotFound:
			flash('Recibo no encontrado')
		except ValueError:
			flash('Datos incorrectos')
			raise redirect('/receipt/edit/%s' % kw['receipt'])
		
		raise redirect('/receipt')
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.receipt.print")
	def printer(self, code):
		
		try:
			receipt = model.Receipt.get(int(code))
			receipt.closed = True
			return dict(receipt=receipt)
		
		except model.SQLObjectNotFound:
			flash("El recibo %s no ha sido encontrado" % code)
			raise redirect('/')
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.receipt.daily")
	def daily(self, house, day):
		
		try:
			house = model.House.get(int(house))
			day = datetime.strptime(day, "%Y-%m-%d").date()
			query = "receipt.day = '%s' and receipt.house_id = %s and receipt.amount > 0" % (day, house.id)
			receipts = model.Receipt.select(query)
			return dict(house=house, receipts=receipts, day=day)
		except:
			raise redirect('/receipt')