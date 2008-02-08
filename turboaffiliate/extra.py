#!/usr/bin/python
# -*- coding: utf8 -*-
#
# affiliate.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2008 Carlos Flores <cafg10@gmail.com>
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
from turboaffiliate import model
from decimal import *

class Extra(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.extra.index')
	def index(self):
		return dict(accounts=model.Account.select())
	
	@identity.require(identity.not_anonymous())
	@expose(template='turboaffiliate.templates.affiliate.extra.add')
	def add(self, affiliate):
		
		try:
			affiliate = model.Affiliate.get(int(affiliate))
			accounts = model.Account.select()
		except model.SQLObjectNotFound:
			raise redirect('/affiliate')
		except ValueError:
			raise redirect('/affiliate')
		return dict(affiliate=affiliate, accounts=accounts)
	
	@identity.require(identity.not_anonymous())
	@expose()
	def save(self, **kw):
		
		try:
			kw['affiliate'] = model.Affiliate.get(int(kw['affiliate']))
			kw['account'] = model.Account.get(int(kw['account']))
			kw['months'] = int(kw['months'])
			extra = model.Extra(**kw)
			raise redirect('/affiliate/%s' % kw['affiliate'].id)
		except model.SQLObjectNotFound:
			raise redirect('/affiliate')
		except ValueError:
			raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def many(self, **kw):
		try:
			kw['account'] = model.Account.get(int(kw['account']))
			kw['months'] = int(kw['months'])
			first = int(kw['first'])
			last = int(kw['last']) + 1
			del kw['last']
			del kw['first']
			for n in range(first, last):
				try:
					kw['affiliate'] = model.Affiliate.get(n)
				except model.SQLObjectNotFound:
					pass
				extra = model.Extra(**kw)
			raise redirect('/affiliate')
		except model.SQLObjectNotFound:
			raise redirect('/affiliate')
		except ValueError:
			raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def delete(self, code):
		
		try:
			extra = model.Extra.get(int(code))
			extra.destroySelf()
		except:
			raise redirect('/affiliate')
