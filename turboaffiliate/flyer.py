#!/usr/bin/python
# -*- coding: utf8 -*-
#
# flyer.py
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
from turbogears import validate, validators
from turboaffiliate import model, json, obligation
from decimal import *
from datetime import date

months = {
			1:'Enero', 2:'Febrero', 3:'Marzo',
			4:'Abril', 5:'Mayo', 6:'Junio',
			7:'Julio', 8:'Agosto', 9:'Septiembre',
			10:'Octubre', 11:'Noviembre', 12:'Diciembre'
				}

class Flyer(controllers.Controller):
	
	"""Imports the escalafon definition file for Affiliate cuota payment"""
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.escalafon.index")
	def index(self):
		return dict(accounts=model.Account.select())
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.escalafon.post")
	def postReport(self, year, month):
		
		query = "post_report.month = %s and post_report.year = %s" % (int(month), int(year))
		report = model.PostReport.select(query)[0]
		total = sum(r.amount for r in report.reportAccounts)
		
		return dict(total=total, month=month, year=year, report=report)
	
	@identity.require(identity.not_anonymous())
	@expose()
	def export(self, year, month):
	
		model.Flyer.clearTable()
		
		affiliates = model.Affiliate.select(model.Affiliate.q.payment=="Escalafon")
		query = "obligation.year = %s and obligation.month = %s" % (int(year), int(month))
		obligations = model.Obligation.select(query)
		oblig = sum([o.amount for o in obligations])
		
		for affiliate in affiliates:
			if not affiliate.active:
				continue
			kw = {}
			kw['amount'] = 0
			kw['affiliate'] = affiliate
			for e in affiliate.extras:
				kw['amount'] += e.amount
			# for loan in affiliate.refinancedLoans:
			#	kw['amount'] += loan.get_payment()
			for loan in affiliate.loans:
				kw['amount'] += loan.get_payment()
			kw['amount'] += oblig
			model.Flyer(**kw)
		
		raise redirect('/escalafon/download?year=%s;month=%s' % (year, month))
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.escalafon.download")
	def download(self, year, month):
		filename = "./turboaffiliate/static/%(year)s%(month)02dCOPEMH.txt" % {'year':int(year), 'month':int(month)}
		f = open(filename, 'w')
		flyers = model.Flyer.select()
		start = "%(year)s%(month)02d" % {'year':int(year), 'month':int(month)}
		for flyer in flyers:
			if str(flyer) == "":
				continue
			l = start + str(flyer) + "\n"
			f.write(l)
		return dict(filename="static/%(year)s%(month)02dCOPEMH.txt" % {'year':int(year), 'month':int(month)})
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.escalafon.report")
	def report(self, payment, year, month):
	
		affiliates = model.Affiliate.select(model.Affiliate.q.payment==str(payment))
		
		accounts = model.Account.select()
		query = query = "obligation.year = %s and obligation.month = %s" % (int(year), int(month))
		obligations = model.Obligation.select(query)
		obligation = sum(o.amount for o in obligations)
		
		loans = model.Loan.select()
		loans = [loan for loan in loans if loan.affiliate.payment==str(payment)]
		loand = {}
		loand['amount'] = sum(loan.get_payment() for loan in loans)
		loand['count'] = len(loans)
		
		kw = {}
		total = Decimal(0)
		for account in accounts:
			kw[account] = {}
			li = [extra for extra in account.extras if extra.affiliate.payment==str(payment)]
			kw[account]['amount'] = sum(e.amount for e in li)
			kw[account]['count'] = len(li)
			total += kw[account]['amount']
		
		for account in accounts:
			if kw[account]['amount'] == 0:
				del kw[account]
		
		return dict(deductions=kw, count=affiliates.count(), obligation=obligation, legend=payment, loans=loand, total=total)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.escalafon.extra")
	def extra(self, account):
		
		try:
			account = model.Account.get(int(account))
			return dict(account=account, extras=account.extras)
		except:
			flash(account)
			raise redirect('/escalafon')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def OtherReport(self, payment, month, year):
		
		(payment, month, year) = (str(payment), int(month), int(year))
		otherDeduced = model.OtherDeduced.select()
		otherDeduced = [o for o in otherDeduced if o.affiliate.payment == payment]
		
		kw = {}
		init = {}
		i = {"payment":payment, "month":month, "year":year}
		init["otherReport"] = model.OtherReport(**i)
		for other in otherDeduced:
			
			try:
				# The account is already in the report, just add the amount
				kw[other.account].add(other.amount)
			except KeyError:
				init['account'] = other.account
				kw[other.account] = model.OtherAccount(**init)
				kw[other.account].add(other.amount)
			
			other.destroySelf()
		
		flash('Reporte Generado')
		raise redirect('/escalafon')
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.escalafon.other")
	def showReport(self, year, month, payment):
		
		try:
			report = model.OtherReport.select(model.OtherReport.q.payment==str(payment))
			report = [r for r in report if r.year == int(year) and r.month == int(month)][0]
			return dict(month=month, year=year, report=report, payment=payment)
		except:
			flash('Ha ocurrido un error.')
			raise redirect('/escalafon')
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.escalafon.filiales")
	def filiales(self, year, month):
		
		(month, year) = (int(month), int(year))
		affiliates = model.Affiliate.select(model.Affiliate.q.payment=="Escalafon")
		query = "obligation.year = %s and obligation.month >= %s" % (year, month)
		obligation = model.Obligation.select(query)[0]
		
		filiales = {"Atlantida":{'total':0}, "Choluteca":{'total':0}, "Colon":{'total':0}, "Comayagua":{'total':0},
						"Copan":{'total':0}, "Cortes":{'total':0}, "El Paraiso":{'total':0}, "Francisco Morazan":{'total':0},
						"Gracias a Dios":{'total':0}, "Intibuca":{'total':0}, "Islas de la Bahia":{'total':0},
						"La Paz":{'total':0}, "Lempira":{'total':0}, "Olancho":{'total':0}, "Ocotepeque":{'total':0},
						"Santa Barbara":{'total':0}, "Valle":{'total':0}, "Yoro":{'total':0}}
		
		for affiliate in affiliates:
			if affiliate.get_month(year, month):
				try:
					filiales[affiliate.state][affiliate.school] += 1
					filiales[affiliate.state]['total'] += 1
				except KeyError:
					try:
						filiales[affiliate.state][affiliate.school] = 1
						filiales[affiliate.state]['total'] += 1
					except:
						pass
		
		return dict(filiales=filiales)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.escalafon.filiales")
	def filialesFive(self):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.payment=="Escalafon")
		
		filiales = {"Atlantida":{}, "Choluteca":{}, "Colon":{}, "Comayagua":{},
						"Copan":{}, "Cortes":{}, "El Paraiso":{}, "Francisco Morazan":{},
						"Gracias a Dios":{}, "Intibuca":{}, "Islas de la Bahia":{},
						"La Paz":{}, "Lempira":{}, "Olancho":{}, "Ocotepeque":{},
						"Santa Barbara":{}, "Valle":{}, "Yoro":{}}
		for affiliate in affiliates:
			try:
				filiales[affiliate.state][affiliate.school] += 1
				filiales[affiliate.state]['total'] += 1
			except KeyError:
				try:
					filiales[affiliate.state][affiliate.school] = 1
					filiales[affiliate.state]['total'] = 1
				except:
					pass
		
		for dept in filiales.keys():
			for school in filiales[dept].keys():
				if filiales[dept][school] < 5:
					del filiales[dept][school]
		
		return dict(filiales=filiales)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.escalafon.aportaciones")
	def aportaciones(self, year, month):
		
		query = "deduced.year = %s and deduced.month = %s and deduced.account_id = 1" % (int(year), int(month))
		
		deduced = model.Deduced.select(query)
		
		return dict(deduced=deduced, year=year, month=month)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.escalafon.filiales")
	def filialesAll(self):
		
		affiliates = model.Affiliate.select(model.Affiliate.q.payment=="Escalafon")
		
		filiales = {"Atlantida":{'total':0}, "Choluteca":{'total':0}, "Colon":{'total':0}, "Comayagua":{'total':0},
						"Copan":{'total':0}, "Cortes":{'total':0}, "El Paraiso":{'total':0}, "Francisco Morazan":{'total':0},
						"Gracias a Dios":{'total':0}, "Intibuca":{'total':0}, "Islas de la Bahia":{'total':0},
						"La Paz":{'total':0}, "Lempira":{'total':0}, "Olancho":{'total':0}, "Ocotepeque":{'total':0},
						"Santa Barbara":{'total':0}, "Valle":{'total':0}, "Yoro":{'total':0}}
		for affiliate in affiliates:
			try:
				filiales[affiliate.state][affiliate.school] += 1
				filiales[affiliate.state]['total'] += 1
			except KeyError:
				try:
					filiales[affiliate.state][affiliate.school] = 1
					filiales[affiliate.state]['total'] += 1
				except:
					pass
		
		return dict(filiales=filiales)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.escalafon.filialesdept")
	def filialesDept(self, state):
		
		query = "affiliate.payment = '%s' and affiliate.state = '%s'" % ('Escalafon', state)
		affiliates = model.Affiliate.select(query)
		
		filiales = {}
		
		for affiliate in affiliates:
			try:
				filiales[affiliate.school] += 1
			except KeyError:
				filiales[affiliate.school] = 1
		
		return dict(filiales=filiales, state=state)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.escalafon.cuotas")
	def cuotas(self, year, month):
		
		(month, year) = (int(month), int(year))
		
		if month == 6 and year == 2007:
			
			retrasada = {Decimal(10):10, Decimal("128.48"):512, Decimal("135.77"):725,
						Decimal("166.00"):812, Decimal("20.50"):153, Decimal("22"):120,
						Decimal("32"):211, Decimal("33"):178, Decimal("34"):138,
						Decimal(5):1, Decimal("50"):191, Decimal("55"):190, Decimal("62"):146,
						Decimal("65"):182, Decimal("78.90"):356, Decimal("92.53"):378,
						Decimal("39"):325, Decimal("250"):898}
			total = sum(k * v for k, v in retrasada.items())
			return dict(retrasada=retrasada, total=total)
		
		retrasada = {}
		query = "deduced.year = %s and deduced.month = %s and deduced.account_id = 673" % (year, month)
		deduced = model.Deduced.select(query)
		for d in deduced:
			
			try:
				retrasada[d.amount] += 1
			
			except KeyError:
				retrasada[d.amount] = 1
		total = sum(k * v for k, v in retrasada.items())
		
		return dict(retrasada=retrasada, total=total, year=year, month=month)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.escalafon.deduced")
	def deduced(self, account, month, year):
		
		year = int(year)
		account = model.Account.get(int(account))
		query = "deduced.month = %s and deduced.account_id = %s and deduced.year = %s" % (int(month), account.id, year)
		
		deduced = model.Deduced.select(query)
		
		total = sum(d.amount for d in deduced)
		
		return dict(deduced=deduced, account=account, month=months[int(month)], year=year, total=total)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.escalafon.payment")
	def deducedPayment(self, account, month, year, payment):
		
		(year, account, month) = (int(year), model.Account.get(int(account)), int(month))
		query = "deduced.month = %s and deduced.account_id = %s and deduced.year = %s" % (int(month), account.id, year)
		
		deduced = model.Deduced.select(query)
		deduced = [d for d in deduced if d.affiliate.payment == payment]
		total += sum(d.amount for d in deduced)
		return dict(deduced=deduced, account=account, month=months[month], year=year, total=total, payment=payment)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.affiliate.show")
	def empty(self, year, payment):
		
		year = int(year)
		tables = model.CuotaTable.select(model.CuotaTable.q.year==year)
		
		affiliates = []
		for table in tables:
			
			if not table.empty() and table.affiliate.payment == payment:
				
				affiliates.append(table.affiliate)
		
		return dict(affiliates=affiliates, show="Cotizan por %s y pagaron un mes en %s" % (payment, year), count=len(affiliates))
