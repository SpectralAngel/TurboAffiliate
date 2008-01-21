#!/usr/bin/python
# -*- coding: utf8 -*-
#
# translator.py
# This file is part of WebAc
#
# Copyright © 2007 Carlos Flores <cafg10@gmail.com>
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

from turboaffiliate import model
from decimal import *

class Translator(object):
	
	"""A standard translator class that defines the interface between the
	exporting/importing of data inside TurboAffiliate and WebAc.
	"""
	
	def __init__(self, filename):
		self.file = filename
		self.payments = []
	
	def decode(self):
		pass
	
	def encode(self):
		pass
	
	def result(self):
		return self.payments
	
	def update(self):
		for payment in self.payments:
			try:
				affiliate = model.Affiliate.byCardID(payment['affiliate'])
				affiliate.pay_coutas(payment['money'])
				print payment['affiliate']
			except model.SQLObjectNotFound:
				pass

class Bank(Translator):
	
	"""This class takes an input file and translates it into the database"""
	
	def __init__(self, filename):
		self.Translator.__init__(self, filename)
	
	def decode(self):
		for line in self.file:
			payment = {}
			year = line[:4]
			month = line[4:6]
			payment['date'] = year + '-' + month + '-' + '01'
			payment['affiliate'] = line[6:10] + '-' + line[10:14] + '-' + line[14:19]
			cash = line[24:]
			payment['money'] = Decimal(cash) / Decimal(100)
			self.payments.append(payment)

class Escalafon(Translator):
	
	"""Translates an Escalafon input file
	
	Takes a file made by Escalaon and decodes it for updating Affiliate payment
	status.
	"""
	
	def __init__(self, f):
		self.payments = []
		self.decode(f)
	
	def decode(self, f):
		for line in f:
			print 'decoding %s' % line
			if line[90:94] == '0000':
				continue
			payment = {}
			year = line[:4]
			month = line[4:6]
			payment['date'] = year + '-' + month + '-' + '01'
			payment['affiliate'] = line[6:10] + '-' + line[10:14] + '-' + line[14:19]
			cash = line[94:111]
			payment['money'] = Decimal(cash) / Decimal(100)
			self.payments.append(payment)
	
	def update(self):
		failed = []
		for payment in self.payments:
			try:
				affiliate = model.Affiliate.byCardID(payment['affiliate'])
				affiliate.pay_cuotas(payment['money'])
			except model.SQLObjectNotFound:
				failed.append(payment)
		return failed
