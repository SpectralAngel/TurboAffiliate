﻿#!/usr/bin/python
#
# model.py
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

import copy
from datetime import datetime, date
from turbogears.database import PackageHub
from decimal import *
from sqlobject import *
from turbogears import identity
from turboaffiliate import release
from turboaffiliate import num2stres

dot01 = Decimal(".01")
Zero = Decimal(0)

hub = PackageHub("turboaffiliate")
__connection__ = hub

class Application(SQLObject):
	"""Application Specific Information

	It holds data important only to the aplication
	"""
	lastDrop = DateCol()
	version = StringCol(length=8, notNone=True)
	db_version = IntCol()

	@classmethod
	def createTable(cls, *args, **kw):
		super(Application, cls).createTable(*args, **kw)
		count = Application.select().count()
		if count == 0:
			Application(version=release.version, 
						db_version=release.db_version, 
						lastDrop=date.today())
		elif count > 1:
			raise AppConfigError
		elif count == 1:
			app = Application.get(1)
			app.version = release.version
			app.db_version = release.db_version

class Affiliate(SQLObject):

	"""A person that is affiliated to a Company"""

	firstName = UnicodeCol()
	lastName = UnicodeCol()
	cardID = StringCol(length=15, default="")
	gender = StringCol(length=1, varchar=False)
	birthday = DateCol(default=datetime.now)
	birthPlace = UnicodeCol()
	
	address = StringCol(default="")
	phone = UnicodeCol(default="")
	
	state = StringCol(length=50, default="")
	school = StringCol(length=50, default="")
	school2 = StringCol(length=50, default="")
	town = StringCol(length=50, default="")
	
	joined = DateCol(default=datetime.now)
	active = BoolCol(default=True, notNone=True)
	
	escalafon = StringCol(length=11, varchar=False)
	inprema = StringCol(length=11)
	jubilated = DateCol(default=datetime.now)
	
	payment = StringCol(default="Ventanilla", length=20)
	
	# History of cuota payment
	cuotaTables = MultipleJoin("CuotaTable", orderBy='year')
	# Active loans
	loans = MultipleJoin("Loan", orderBy='startDate')
	# Payed loans
	payedLoans = MultipleJoin("PayedLoan", orderBy='startDate')
	# Refinanced Loans
	refinancedLoans = MultipleJoin("RefinancedLoan", orderBy='startDate')
	extras = MultipleJoin("Extra")
	flyers = MultipleJoin("Flyer")
	deduced = MultipleJoin("Deduced")
	
	def get_monthly(self):
		
		extras = sum(e.amount for e in self.extras)
		loans = sum(l.get_payment() for l in self.loans)
		
		return extras + loans
	
	def populate(self, year):
		kw = {}
		for n in range(1, 13):
			kw["month%s" % n] = False
		return kw
	
	def complete(self, year):
		kw = {}
		kw['affiliate'] = self
		kw['year'] = year
		table = CuotaTable(**kw)
	
	def payment_check(self, string):
		
		return self.payment == string

	def retrasada(self):
		
		tables = (t for t in self.cuotaTables if not t.all())
		for table in tables:
			old = table.old()
			if old != Zero:
				return old
		return Zero
	
	def pay_retrasada(self):
		tables = (t for t in self.cuotaTables if not t.all())
		for table in tables:
			value = table.pay_old()
			if value == True:
				return
	
	def pay_cuota(self, year, month):
		tables = [t for t in self.cuotaTables if t.year == year]
		table = None
		if len(tables) == 0:
			kw = self.populate(year)
			kw['affiliate'] = self
			kw['year'] = year
			table = CuotaTable(**kw)
		else:
			table = tables[0]
		table.pay_month(month)
	
	def remove_cuota(self, year, month):
		tables = [t for t in self.cuotaTables if t.year == year]
		table = None
		if len(tables) == 0:
			kw = self.populate(year)
			kw['affiliate'] = self
			kw['year'] = year
			table = CuotaTable(**kw)
		else:
			table = tables[0]
			table.remove_month(month)
	
	def aport(self):
	
		return sum(table.payed() for table in self.cuotaTables)
	
	def loan(self):
		
		"""Returns the amount debt by payment"""
		
		return sum(loan.debt() for loan in self.loans)
	
	def debt(self):
		
		return sum(table.debt() for table in self.cuotaTables)
	
	def solvent(self, year):
		
		table = [table for table in self.cuotaTables if table.year == year][0]
		
		return table.all()
	
	def multisolvent(self, year):
		
		for table in self.cuotaTables:
			if table.year > year:
				break
			if not table.all():
				return False
		return True
	
	def remove(self):
		[table.remove() for table in self.cuotaTables]
		for loan in self.loans:
			loan.remove()
		self.destroySelf()
	
	def total(self, month, year):

		query = "obligation.year = %s and obligation.month = %s" % (year, month)
		os = Obligation.select(query)
		obligations = sum(o.amount for o in os)
		extras = sum(e.amount for e in self.extras)
		loan = sum(loan.get_payment() for loan in self.loans)
		return extras + loan + obligations
	
	def get_month(self, year, month):
		
		query = 'cuota_table.affiliate_id = %s and cuota_table.year = %s' % (self.id, year)
		tables = CuotaTable.select(query)
		if tables.count() == 0:
			return False
		else:
			table = tables[0]
			return getattr(table, "month%s" % month)
	
	def link(self, year, month):
		
		return "/affiliate/posteo/?how=%s&year=%s&month=%s&code=%s" % (self.payment, year, month, self.id)
	
	def get_age(self):
		
		return (date.today() - self.birthday).days / 365

class Aval(SQLObject):
	
	"""A Person that is used as warranty for a Loan"""
	
	firstName = UnicodeCol()
	lastName = UnicodeCol()
	cardID = StringCol(length=15, varchar=False)
	loan = ForeignKey("Loan")

class CuotaTable(SQLObject):
	
	"""Contains the payed months as Boolen values"""
	
	affiliate = ForeignKey("Affiliate")
	year = IntCol()
	affiliateYear = DatabaseIndex("affiliate", "year", unique=True)
	
	month1 = BoolCol(default=False)
	month2 = BoolCol(default=False)
	month3 = BoolCol(default=False)
	month4 = BoolCol(default=False)
	month5 = BoolCol(default=False)
	month6 = BoolCol(default=False)
	month7 = BoolCol(default=False)
	month8 = BoolCol(default=False)
	month9 = BoolCol(default=False)
	month10 = BoolCol(default=False)
	month11 = BoolCol(default=False)
	month12 = BoolCol(default=False)
	
	def total(self):
		total = Decimal(0)
		if self.all():
			query = "obligation.year = %s" % (self.year)
			os = Obligation.select(query)
			total += sum(o.amount for o in os)
			return total
		for n in range(1, 13):
			query = "obligation.year = %s and obligation.month = %s" % (self.year, n)
			os = Obligation.select(query)
			total += sum(o.amount for o in os)
		return total
	
	def debt(self):
		if self.affiliate.joined == None:
			return Zeros
		if self.year == self.affiliate.joined.year:
			total = Decimal(0)
			query = "obligation.year = %s and obligation.month >= %s" % (self.year, self.affiliate.joined.month)
			os = Obligation.select(query)
			if self.affiliate.payment == "INPREMA":
				if self.affiliate.jubilated.year == self.year:
					total += sum(o.amount for o in os if o.month < self.affiliate.jubilated.month)
					total += sum(o.inprema for o in os if o.month >= self.affiliate.jubilated.month)
				elif self.affiliate.jubilated.year < self.year:
					total += sum(o.inprema for o in os)
				elif self.affiliate.jubilated.year > self.year:
					total += sum(o.amount for o in os)
			else:
				total += sum(o.amount for o in os)
			return total - self.payed()
		else:
			return self.total() - self.payed()
	
	def edit_line(self, month):
		text = ' name="month%s"' % month
		if getattr(self, "month%s" % month):
			return text + ' checked'
		else:
			return text + ' '
	
	def old(self):
		today = date.today()
		if self.affiliate.joined == None:
			return Zeros
		
		if self.year == self.affiliate.joined.year:
			
			for n in range(self.affiliate.joined.month, 13):
				month = getattr(self, "month%s" % n)
				if month:
					continue
				query = "obligation.year = %s and obligation.month = %s" % (self.year, n)
				os = Obligation.select(query)
				total = sum(o.amount for o in os)
				return total
		else:
			for n in range(1, 13):
				if self.year == today.year and n == today.month:
					return Zero
				month = getattr(self, "month%s" % n)
				if month:
					continue
				query = "obligation.year = %s and obligation.month = %s" % (self.year, n)
				os = Obligation.select(query)
				total = sum(o.amount for o in os)
				return total
		return Zero
	
	def pay_old(self):
		
		if self.affiliate.joined == None:
			return Zeros
		
		if self.year == self.affiliate.joined.year:
			for n in range(self.affiliate.joined.month, 13):
				month = getattr(self, "month%s" % n)
				if month:
					continue
				getattr(self, "month%s" % n, True)
				return True
		else:
			for n in range(1, 13):
				month = getattr(self, "month%s" % n)
				if month:
					continue
				getattr(self, "month%s" % n, True)
				return True
		return False

	def amount(self, month):
		
		if self.affiliate.joined == None:
			return Zeros
		
		if self.affiliate.joined.year == self.year and month < self.affiliate.joined.month:
			return 0
		if not getattr(self, "month%s" % month):
			return 0
		
		query = "obligation.year = %s and obligation.month = %s" % (self.year, month)
		os = Obligation.select(query)
		
		if self.affiliate.payment == "INPREMA" and self.affiliate.jubilated.year >= self.year:
			total = sum(o.inprema for o in os)
		else:
			total = sum(o.amount for o in os)
		
		return total
	
	def pay(self, amount):
		if amount <= 0:
			return
		for n in range(1, 13):
			month = getattr(self, "month%s" % n)
			if month:
				continue
			query = "obligation.year = %s and obligation.month = %s" % (self.year, n)
			os = Obligation.select(query)
			total = sum(o.amount for o in os)
			if amount < total and total == 0:
				continue
			month = True
			amount -= total
	
	def pay_month(self, month):
		setattr(self, "month%s" % month, True)
	
	def remove_month(self, month):
		setattr(self, "month%s" % month, False)
	
	def all(self):
		today = date.today()
		if self.year == today.year:
			for n in range(1, today.month):
				if not getattr(self, "month%s" % n):
					return False
			return True
		if self.affiliate.joined == None:
			return self.month1 and self.month2 and self.month3 and self.month4 and self.month5 and self.month6 and self.month7 and self.month8 and self.month9 and self.month10 and self.month11 and self.month12
		if self.year == self.affiliate.joined.year:
			for n in range(self.affiliate.joined.month, 13):
				if not getattr(self, "month%s" % n):
					return False
			return True
		else:
			return self.month1 and self.month2 and self.month3 and self.month4 and self.month5 and self.month6 and self.month7 and self.month8 and self.month9 and self.month10 and self.month11 and self.month12
	
	def payed(self):
		total = Decimal(0)
		if self.all():
			if self.year == self.affiliate.joined.year:
				query = "obligation.year = %s and obligation.month >= %s" % (self.year, self.affiliate.joined.month)
			else:
				query = "obligation.year = %s" % (self.year)
			os = Obligation.select(query)
			if self.affiliate.payment == "INPREMA":
				if self.affiliate.jubilated.year == self.year:
					total += sum(o.amount for o in os if o.month < self.affiliate.jubilated.month)
					total += sum(o.inprema for o in os if o.month >= self.affiliate.jubilated.month)
				elif self.affiliate.jubilated.year < self.year:
					total += sum(o.inprema for o in os)
				elif self.affiliate.jubilated.year > self.year:
					total += sum(o.amount for o in os)
			else:
				total += sum(o.amount for o in os)
			return total
		for n in range(1, 13):
			if getattr(self, "month%s" % n):
				query = "obligation.year = %s and obligation.month = %s" % (self.year, n)
				os = Obligation.select(query)
				if self.affiliate.payment == "INPREMA":
					if self.affiliate.jubilated.year == self.year:
						total += sum(o.amount for o in os if o.month < self.affiliate.jubilated.month)
						total += sum(o.inprema for o in os if o.month >= self.affiliate.jubilated.month)
					elif self.affiliate.jubilated.year < self.year:
						total += sum(o.inprema for o in os)
					elif self.affiliate.jubilated.year > self.year:
						total += sum(o.amount for o in os)
				else:
					total += sum(o.amount for o in os)
		return total

class Loan(SQLObject):

	"""Data concerning to Loans"""
	
	affiliate = ForeignKey("Affiliate")
	aval = SingleJoin("Aval")
	
	capital = CurrencyCol(default=0, notNone=True)
	letters = StringCol()
	debt = CurrencyCol(default=0, notNone=True)
	payment = CurrencyCol(default=0, notNone=True)
	interest = DecimalCol(default=20, notNone=True, size=4, precision=2)
	months = IntCol()
	last = DateCol(default=datetime.now)
	number = IntCol(default=0)
	
	startDate = DateCol(notNone=True, default=datetime.now)
	aproved = BoolCol(default=False)
	
	pays = MultipleJoin("Pay", orderBy="day")
	deductions = MultipleJoin("Deduction")
	
	def percent(self):
	
		x = (Decimal(self.debt) * Decimal(100)).quantize(dot01)
		total = x / Decimal(self.capital).quantize(dot01)
		return total
	
	def get_payment(self):
	
		if self.debt < self.payment:
			return self.debt
		return self.payment
	
	def start(self):
	
		self.debt = self.capital
	
	def refinance(self):
		
		kw = {}
		kw['id'] = self.id
		kw['affiliate'] = self.affiliate
		kw['capital'] = self.capital
		kw['letters'] = self.letters
		kw['debt'] = self.debt
		kw['payment'] = self.payment
		kw['interest'] = self.interest
		kw['months'] = self.months
		kw['last'] = self.last
		kw['number'] = self.number
		kw['startDate'] = self.startDate
		
		refinancedLoan = RefinancedLoan(**kw)
		
		for pay in self.pays:
			pay.refinance(refinancedLoan)
		
		for deduction in self.deductions:
			deduction.refinace(refinancedLoan)
		
		refinancedLoan.debt = refinancedLoan.get_payment()
		
		self.destroySelf()
	
	def pay(self, amount, receipt, day=date.today()):
		
		"""Charges a normal payment for the loan
		
		Calculates the composite interest and acredits the made payment
		"""
		
		kw['amount'] = Decimal(amount).quantize(dot01)
		kw['day'] = day
		kw['receipt'] = receipt
		kw['loan'] = self
		
		# When the amount to pay is bigger or equal the debt, it is considered
		# the last payment, so interests are not calculated
		if(self.debt <= amount):
			
			self.last = kw['day']
			# Register the payment in the database
			Pay(**kw)
			# Remove the loan and convert it to PayedLoan
			self.remove()
			return True
		
		# Otherwise calculate interest for the loan's payment
		kw['interest'] = (self.debt * self.interest / 1200).quantize(dot01)
		# Increase the loans debt by the interest
		self.debt += ints
		# Decrease debt by the payment amount
		self.debt -= kw['amount']
		# Calculate how much money was used to pay the capital
		kw['capital'] = kw['amount'] - ints
		# Change the last payment date
		self.last = day
		# Register the payment in the database
		Pay(**kw)
		# Increase the number of payments by one
		self.number += 1
		
		if self.debt == 0:
			self.remove()
			return True
		
		return False
	
	def payfree(self, amount, receipt, day=date.today()):
		
		"""Creates a new payment for the loan without chargin interest"""
		
		kw['amount'] = Decimal(amount).quantize(dot01)
		kw['day'] = day
		kw['receipt'] = receipt
		kw['loan'] = self
		
		# When the amount to pay is bigger or equal the debt, it is considered
		# the last payment, so interests are not calculated
		if(self.debt <= amount):
			
			self.last = kw['day']
			# Register the payment in the database
			Pay(**kw)
			# Remove the loan and convert it to PayedLoan
			self.remove()
			return True
		
		# Otherwise calculate interest for the loan's payment
		kw['interests'] = 0
		# Increase the loans debt by the interest
		self.debt += interests
		# Decrease debt by the payment amount
		self.debt -= amount
		# Calculate how much money was used to pay the capital
		kw['capital'] = amount - interests
		# Change the last payment date
		self.last = day
		# Register the payment in the database
		Pay(**kw)
		# Increase the number of payments by one
		self.number += 1
		
		if self.debt == 0:
			self.remove()
			return True
		
		return False
	
	def net(self):
		
		"""Obtains the amount that was given to the affiliate in the check"""
		
		return self.capital - sum(d.amount for d in self.deductions)
	
	def remove(self):
		
		kw = {}
		kw['id'] = self.id
		kw['affiliate'] = self.affiliate
		kw['capital'] = self.capital
		kw['letters'] = self.letters
		kw['interest'] = self.interest
		kw['months'] = self.months
		kw['last'] = self.last
		kw['startDate'] = self.startDate
		kw['payment'] = self.payment
		payed = PayedLoan(**kw)
		
		for pay in self.pays:
			pay.remove(payed)
		
		for deduction in self.deductions:
			deduction.remove(payed)
		
		self.destroySelf()
	
	def future(self):
		
		debt = copy.copy(self.debt)
		li = []
		months = {
			1:'Enero', 2:'Febrero', 3:'Marzo', 
			4:'Abril', 5:'Mayo', 6:'Junio', 
			7:'Julio', 8:'Agosto', 9:'Septiembre', 
			10:'Octubre', 11:'Noviembre', 12:'Diciembre'
				}
		start = self.startDate.month
		if self.startDate.day == 24 and self.startDate.month == 8:
			start += 1
		year = self.startDate.year
		for n in range(1, self.months - self.number + 2):
			kw = {}
			kw['number'] = "%s/%s" % (n + self.number, self.months)
			kw['month'] = self.number + n + start
			kw['year'] = year
			while kw['month'] > 12:
				kw['month'] = kw['month'] - 12
				kw['year'] += 1
			kw['month'] = "%s %s" % (months[kw['month']], kw['year'])
			kw['interest'] = Decimal(debt * self.interest / 1200).quantize(dot01)
			if debt < self.payment:
				kw['amount'] = 0
				kw['capital'] = debt
				kw['payment'] = kw['interest'] + kw['capital']
				li.append(kw)
				break
			kw['capital'] = self.payment - kw['interest']
			debt = debt + kw['interest'] - self.payment
			kw['amount'] = debt
			kw['payment'] = kw['interest'] + kw['capital']
			li.append(kw)
		return li

class Pay(SQLObject):
	
	loan = ForeignKey("Loan")
	day = DateCol(default=datetime.now)
	capital = CurrencyCol(default=0, notNone=True)
	interest = CurrencyCol(default=0, notNone=True)
	amount = CurrencyCol(default=0, notNone=True)
	receipt = StringCol()
	month = StringCol(default="")
	
	def refinance(self, refinancedLoan):
		
		kw = {}
		kw['refinacedLoan'] = refinacedLoan
		kw['day'] = self.day
		kw['capital'] = self.capital
		kw['interest'] = self.interest
		kw['amount'] = self.amount
		kw['receipt'] = self.receipt
		kw['month'] = self.month
		
		refinancedPay = RefinancedPay(**kw)
		self.destroySelf()
	
	def remove(self, payedLoan):
		
		kw = {}
		kw['payedLoan'] = payedLoan
		kw['day'] = self.day
		kw['capital'] = self.capital
		kw['interest'] = self.interest
		kw['amount'] = self.amount
		kw['receipt'] = self.receipt
		kw['month'] = self.month
		self.destroySelf()
		OldPay(**kw)

class Account(SQLObject):
	
	"""Simple Account made for affiliate handling"""
	
	name = StringCol()
	code = IntCol(alternateID=True)
	
	company = StringCol()
	extras = MultipleJoin("Extra")
	
	details = MultipleJoin("AccountDetail")
	intermediates = MultipleJoin("Intermediate")

class House(SQLObject):
	
	name = StringCol()
	receipts = MultipleJoin("Receipt")
	
	@classmethod
	def createTable(cls, *args, **kw):
		super(House, cls).createTable(*args, **kw)
		count = House.select().count()
		if count == 0:
			House(name="Tegucigalpa")
			House(name="San Pedro Sula")
			House(name="La Ceiba")

class Receipt(SQLObject):
	
	"""Information about Receipts"""
	
	name = StringCol()
	affiliate = IntCol(default=0)
	amount = CurrencyCol(default=0)
	day = DateCol(default=datetime.now)
	house = ForeignKey("House")
	lines = MultipleJoin("Line")
	closed = BoolCol(default=False)
	
	def letters(self):
		
		return num2stres.parse(self.amount)

class Line(SQLObject):
	
	"""Represents the lines of the receipt"""
	
	account = ForeignKey("Account")
	receipt = ForeignKey("Receipt")
	amount = CurrencyCol(default=0)
	qty = IntCol()
	unit = CurrencyCol()
	detail = StringCol()
	acted = BoolCol(default=False)
	
	def value(self):
		return self.qty * self.unit
	
	def act(self):
		
		if self.acted:
			return
		self.amount = self.value()
		self.receipt.amount += self.amount
		self.acted = True
	
	def undo(self):
		
		if not self.acted:
			return
		self.amount = self.value()
		self.receipt.amount -= self.amount
		self.acted = False

class Extra(SQLObject):
	
	"""Represents a Deduction that will be made"""
	
	affiliate = ForeignKey("Affiliate")
	amount = CurrencyCol(default=0)
	months = IntCol(default=1)
	retrasada = BoolCol(default=False)
	account = ForeignKey("Account")
	
	def act(self):
		self.months -= 1
		if self.retrasada:
			self.affiliate.pay_retrasada()
		self.to_deduced()
		if self.months == 0:
			self.destroySelf()
	
	def to_deduced(self):
		
		kw = {}
		kw['amount'] = self.amount
		kw['affiliate'] = self.affiliate
		kw['account'] = self.account
		Deduced(**kw)
	
	def to_other(self):
		
		kw = {}
		kw['amount'] = self.amount
		kw['affiliate'] = self.affiliate
		kw['account'] = self.account
		OtherDeduced(**kw)
	
	def manual(self):
		
		self.to_other()
		self.act()

class Flyer(SQLObject):
	
	affiliate = ForeignKey("Affiliate")
	amount = CurrencyCol(default=0)
	
	def __str__(self):
		total = self.amount * Decimal(100)
		zeros = '%(#)018d' % {"#":total}
		if self.affiliate.cardID == None:
			return ""
		return self.affiliate.cardID.replace('-', '') + '0011' + zeros

class Reinteger(SQLObject):
	
	affiliate = ForeignKey("Affiliate")
	amount = CurrencyCol(default=0)
	concept = StringCol()

class Funebre(SQLObject):
	
	affiliate = ForeignKey("Affiliate")
	reason = StringCol()
	cheque = IntCol()
	day = DateCol(default=datetime.now)
	amount = CurrencyCol()

class Survival(SQLObject):
	
	affiliate = ForeignKey("Affiliate")
	amount = CurrencyCol()
	day = DateCol(default=datetime.now)
	reason = StringCol()
	cheque = IntCol()

class Devolution(SQLObject):
	
	affiliate = IntCol(default=0)
	name = StringCol()
	amount = CurrencyCol()

class Deduction(SQLObject):
	
	loan = ForeignKey("Loan")
	name = StringCol()
	amount = CurrencyCol()
	account = ForeignKey("Account")
	description = StringCol()
	
	def refinance(self, refinancedLoan):
		
		kw = {}
		kw['refinancedLoan'] = refinancedLoan
		kw['name'] = self.name
		kw['amount'] = self.amount
		kw['account'] = self.account
		kw['description'] = self.description
		
		refinanedDeduction = RefinancedDeduction(**kw)
		self.destroySelf()
	
	def remove(self, payedLoan):
		
		kw = {}
		kw['payedLoan']
		kw['name'] = self.name
		kw['amount'] = self.amount
		kw['account'] = self.account
		kw['description'] = self.description
		PayedDeduction(**kw)
		deduction.destroySelf()

class Company(SQLObject):
	name = UnicodeCol()
	description = UnicodeCol(default="")
	rtn = StringCol(length=20, alternateID=True)
	obligations = MultipleJoin("Obligation")
	
	@classmethod
	def createTable(cls, *args, **kw):
		super(Company, cls).createTable(*args, **kw)
		count = Company.select().count()
		if count == 0:
			Company(name="Junta Directiva", rtn="")
			Company(name="Fondo del AutoSeguro", rtn=" ")
	
	def loan(self, amount):
		self.loans += amount
	
	def reset(self):
		self.accumulated = Decimal(0)
	
	def accumulate(self, amount):
		self.accumulated += amount

class Obligation(SQLObject):
	
	"""The description of the Cuota payment"""
	
	name = UnicodeCol()
	amount = CurrencyCol(default=0, notNone=True)
	inprema = CurrencyCol(default=0, notNone=True)
	month = IntCol()
	year = IntCol()
	company = ForeignKey("Company")
	account = ForeignKey("Account")
	filiales = CurrencyCol(default=4, notNone=True)
	
	def accumulate(self):
		self.account.increase(self.amount)
	
class History(SQLObject):
	
	"""Registers every action made by any user"""
	
	user = ForeignKey("User")
	activity = StringCol()
	day = DateTimeCol(default=datetime.now)

class Lost(SQLObject):
	
	affiliate = ForeignKey("Affiliate")
	reason = StringCol()
	amount = CurrencyCol()

class AccountDetail(SQLObject):
	
	name = StringCol()
	amount = CurrencyCol(default=0)
	account = ForeignKey("Account")
	company = StringCol()

class ReportAccount(SQLObject):
	
	name = StringCol()
	code = IntCol(default=0)
	quantity = IntCol()
	amount = CurrencyCol(default=0)
	postReport = ForeignKey("PostReport")

	def add(self, amount):
		self.amount += amount
		self.quantity += 1

class Intermediate(SQLObject):
	
	account = ForeignKey("Account")
	amount = CurrencyCol(default=0)

class PostReport(SQLObject):

	year = IntCol()
	month = IntCol()
	reportAccounts = MultipleJoin("ReportAccount", orderBy="name")

	def total(self):
		return sum(r.amount for r in reportAccounts)

class PreReport(SQLObject):

	year = IntCol()
	month = IntCol()
	preAccounts = MultipleJoin("PreAccount")

	def total(self):
		return sum(p.amount for p in preAccounts)

class preAccount(SQLObject):
	name = StringCol()
	code = IntCol(default=0)
	quantity = IntCol()
	amount = CurrencyCol(default=0)
	postReport = ForeignKey("PreReport")

	def add(self, amount):
		self.amount += amount
		self.quantity += 1

class PayedLoan(SQLObject):
	
	affiliate = ForeignKey("Affiliate")
	capital = CurrencyCol(default=0, notNone=True)
	letters = StringCol()
	payment = CurrencyCol(default=0, notNone=True)
	interest = DecimalCol(default=20, notNone=True, size=4, precision=2)
	months = IntCol()
	last = DateCol(default=datetime.now)
	startDate = DateCol(notNone=True, default=datetime.now)
	pays = MultipleJoin("OldPay")
	deductions = MultipleJoin("PayedDeduction")
	
	def to_loan(self):
		
		kw = {}
		kw['affiliate'] = self.affiliate
		kw['capital'] = self.capital
		kw['interest'] = self.interest
		kw['payment'] = self.payment
		kw['months'] = self.months
		kw['last'] = self.last
		kw['startDate'] = self.startDate
		kw['letters'] = self.letters
		kw['number'] = len(self.pays)
		kw['id'] = self.id
		loan = Loan(**kw)
		
		[pay.to_pay(loan) for pay in self.pays]
		[deduction.to_deduction(loan) for deduction in self.deductions]
		
		self.destroySelf()
		return loan

class OldPay(SQLObject):
	
	payedLoan = ForeignKey("PayedLoan")
	day = DateCol(default=datetime.now)
	capital = CurrencyCol(default=0, notNone=True)
	interest = CurrencyCol(default=0, notNone=True)
	amount = CurrencyCol(default=0, notNone=True)
	receipt = StringCol()
	month = StringCol()
	
	def to_pay(self, loan):
		
		kw = {}
		kw['loan'] = loan
		kw['day'] = self.day
		kw['capital'] = self.capital
		kw['interest'] = self.interest
		kw['amount'] = self.amount
		kw['receipt'] = self.receipt
		kw['month'] = self.month
		Pay(**kw)
		self.destroySelf()

class PayedDeduction(SQLObject):
	
	payedLoan = ForeignKey("PayedLoan")
	name = StringCol()
	amount = CurrencyCol()
	account = ForeignKey("Account")
	description = StringCol()
	
	def to_deduction(self, loan):
		
		kw = {}
		kw['loan'] = loan
		kw['name'] = self.name
		kw['amount'] = self.amount
		kw['description'] = self.description
		kw['account'] = self.account
		Deduction(**kw)
		self.destroySelf()

class RefinancedLoan(SQLObject):
	
	"""Data concerning to Loans that have been covered with another loan"""
	
	affiliate = ForeignKey("Affiliate")
	
	capital = CurrencyCol(default=0, notNone=True)
	letters = StringCol()
	debt = CurrencyCol(default=0, notNone=True)
	payment = CurrencyCol(default=0, notNone=True)
	interest = DecimalCol(default=20, notNone=True, size=4, precision=2)
	months = IntCol()
	last = DateCol(default=datetime.now)
	number = IntCol(default=0)
	
	startDate = DateCol(notNone=True, default=datetime.now)
	aproved = BoolCol(default=False)
	
	pays = MultipleJoin("RefinancedPay", orderBy="day")
	deductions = MultipleJoin("RefinancedDeduction")
	
	def get_payment(self):
	
		if self.debt < self.payment:
			return self.debt
		return self.payment
	
	def pay(self, amount, receipt, day=date.today()):
		
		"""Charges a normal payment for the loan
		
		Calculates the composite interest and acredits the made payment
		"""
		
		kw = {}
		kw['amount'] = Decimal(amount).quantize(dot01)
		kw['day'] = day
		kw['receipt'] = receipt
		kw['refinancedLoan'] = self
		
		# When the amount to pay is bigger or equal the debt, it is considered the last payment, so interests are not
		# calculated
		if(self.debt <= amount):
			
			self.last = day
			# Register the payment in the database
			Pay(**kw)
			# Remove the loan and convert it to PayedLoan
			self.remove()
			return True
		
		# Otherwise calculate interest for the loan's payment
		kw['interest'] = (self.debt * self.interest / 1200).quantize(dot01)
		# Increase the loans debt by the interest
		self.debt += kw['interest']
		# Decrease debt by the payment amount
		self.debt -= kw['amount']
		# Calculate how much money was used to pay the capital
		kw['capital'] = kw['amount'] - kw['interest']
		# Change the last payment date
		self.last = day
		# Register the payment in the database
		Pay(**kw)
		# Increase the number of payments by one
		self.number += 1
		
		if self.debt == 0:
			self.remove()
			return True
		
		return False
	
	def payfree(self, amount, receipt, day=date.today()):
		
		"""Creates a new payment for the loan without chargin interests"""
		
		kw = {}
		kw['amount'] = Decimal(amount).quantize(dot01)
		kw['day'] = day
		kw['receipt'] = receipt
		kw['refinancedLoan'] = self
		
		# When the amount to pay is bigger or equal the debt, it is considered the last payment, so interests are not
		# calculated
		if(self.debt <= amount):
			
			self.last = kw['day']
			# Register the payment in the database
			RefinancedPay(**kw)
			# Remove the loan and convert it to PayedLoan
			self.remove()
			return True
		
		# Otherwise calculate interest for the loan's payment
		kw['interest'] = 0
		# Increase the loans debt by the interest
		self.debt += interests
		# Decrease debt by the payment amount
		self.debt -= kw['amount']
		# Calculate how much money was used to pay the capital
		kw['capital'] = kw['amount'] - interests
		# Change the last payment date
		self.last = day
		# Register the payment in the database
		RefinancedPay(**kw)
		# Increase the number of payments by one
		self.number += 1
		
		if self.debt == 0:
			self.remove()
			return True
		
		return False
	
	def remove(self):
		
		kw = {}
		kw['id'] = self.id
		kw['affiliate'] = self.affiliate
		kw['capital'] = self.capital
		kw['letters'] = self.letters
		kw['interest'] = self.interest
		kw['months'] = self.months
		kw['last'] = self.last
		kw['startDate'] = self.startDate
		kw['payment'] = self.payment
		payed = PayedLoan(**kw)
		
		for pay in self.pays:
			pay.remove(payed)
		
		for deduction in self.deductions:
			deduction.remove(payed)
		
		self.destroySelf()

class RefinancedDeduction(SQLObject):
	
	refinancedloan = ForeignKey("RefinancedLoan")
	name = StringCol()
	amount = CurrencyCol()
	account = ForeignKey("Account")
	description = StringCol()
	
	def remove(self, payedLoan):
		
		kw = {}
		kw['payedLoan']
		kw['name'] = self.name
		kw['amount'] = self.amount
		kw['account'] = self.account
		kw['description'] = self.description
		PayedDeduction(**kw)
		deduction.destroySelf()

class RefinancedPay(SQLObject):
	
	refinancedLoan = ForeignKey("RefinancedLoan")
	day = DateCol(default=datetime.now)
	capital = CurrencyCol(default=0, notNone=True)
	interest = CurrencyCol(default=0, notNone=True)
	amount = CurrencyCol(default=0, notNone=True)
	receipt = StringCol()
	month = StringCol(default="")
	
	def remove(self, payedLoan):
		
		kw = {}
		kw['payedLoan'] = payedLoan
		kw['day'] = self.day
		kw['capital'] = self.capital
		kw['interest'] = self.interest
		kw['amount'] = self.amount
		kw['receipt'] = self.receipt
		kw['month'] = self.month
		self.destroySelf()
		OldPay(**kw)

class Deduced(SQLObject):
	
	affiliate = ForeignKey("Affiliate")
	amount = CurrencyCol(default=0)
	account = ForeignKey("Account")
	month = IntCol(default=datetime.today().month)
	year = IntCol(default=datetime.today().year)

class OtherReport(SQLObject):
	
	year = IntCol()
	month = IntCol()
	payment = StringCol(length=15)
	otherAccounts = MultipleJoin("OtherAccount")

	def total(self):
		return sum(r.amount for r in self.otherAccounts)

class OtherAccount(SQLObject):
	
	account = ForeignKey("Account")
	quantity = IntCol(default=0)
	amount = CurrencyCol(default=0)
	otherReport = ForeignKey("OtherReport")

	def add(self, amount):
		self.amount += amount
		self.quantity += 1

class OtherDeduced(SQLObject):
	
	affiliate = ForeignKey("Affiliate")
	amount = CurrencyCol(default=0)
	account = ForeignKey("Account")

# identity models.
class Visit(SQLObject):
	class sqlmeta:
		table = "visit"
	
	visit_key = StringCol(length=40, alternateID=True, 
						  alternateMethodName="by_visit_key")
	created = DateTimeCol(default=datetime.now)
	expiry = DateTimeCol()
	
	def lookup_visit(cls, visit_key):
		try:
			return cls.by_visit_key(visit_key)
		except SQLObjectNotFound:
			return None
	lookup_visit = classmethod(lookup_visit)

class VisitIdentity(SQLObject):
	visit_key = StringCol(length=40, alternateID=True, 
						  alternateMethodName="by_visit_key")
	user_id = IntCol()

class Group(SQLObject):
	"""
	An ultra-simple group definition.
	"""

	# names like "Group", "Order" and "User" are reserved words in SQL
	# so we set the name to something safe for SQL
	class sqlmeta:
		table = "tg_group"
	
	group_name = UnicodeCol(length=16, alternateID=True, 
							alternateMethodName="by_group_name")
	display_name = UnicodeCol(length=255)
	created = DateTimeCol(default=datetime.now)
	
	# collection of all users belonging to this group
	users = RelatedJoin("User", intermediateTable="user_group", 
						joinColumn="group_id", otherColumn="user_id")
	
	# collection of all permissions for this group
	permissions = RelatedJoin("Permission", joinColumn="group_id", 
							  intermediateTable="group_permission", 
							  otherColumn="permission_id")

class User(SQLObject):
	"""
	Reasonably basic User definition. Probably would want additional attributes.
	"""
	# names like "Group", "Order" and "User" are reserved words in SQL
	# so we set the name to something safe for SQL
	class sqlmeta:
		table = "tg_user"
	
	user_name = UnicodeCol(length=16, alternateID=True, 
						   alternateMethodName="by_user_name")
	email_address = UnicodeCol(length=255, alternateID=True, 
							   alternateMethodName="by_email_address")
	display_name = UnicodeCol(length=255)
	password = UnicodeCol(length=40)
	created = DateTimeCol(default=datetime.now)

	# groups this user belongs to
	groups = RelatedJoin("Group", intermediateTable="user_group", 
						 joinColumn="user_id", otherColumn="group_id")
	
	def _get_permissions(self):
		perms = set()
		for g in self.groups:
			perms = perms | set(g.permissions)
		return perms
	
	def _set_password(self, cleartext_password):
		"Runs cleartext_password through the hash algorithm before saving."
		hash = identity.encrypt_password(cleartext_password)
		self._SO_set_password(hash)
	
	def set_password_raw(self, password):
		"Saves the password as-is to the database."
		self._SO_set_password(password)

class Permission(SQLObject):
	permission_name = UnicodeCol(length=16, alternateID=True, 
								 alternateMethodName="by_permission_name")
	description = UnicodeCol(length=255)
	
	groups = RelatedJoin("Group", 
						intermediateTable="group_permission", 
						 joinColumn="permission_id", 
						 otherColumn="group_id")
