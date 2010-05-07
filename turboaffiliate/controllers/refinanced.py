#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# refinanced.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2008 - 2009 Carlos Flores <cafg10@gmail.com>
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
from turbogears import expose, validate, validators
from turboaffiliate import model

class Refinanced(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.refinanced.refinanced")
	@validate(validators=dict(loan=validators.Int()))
	def default(self, loan):
		
		return dict(loan=model.RefinancedLoan.get(loan))
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(loan=validators.Int()))
	def recover(self, loan):
		
		loan = model.RefinancedLoan.get(loan)
		loan = loan.recover()
		
		raise redirect('/loan/%s' % loan.id)
	
	@identity.require(identity.not_anonymous())
	@expose()
	@validate(validators=dict(loan=validators.Int()))
	def remove(self, loan):
		
		loan = model.RefinancedLoan.get(loan)
		payed = loan.remove()
		flash("Prestamo pagado")
		raise redirect(url('/loan/payed/%s' % payed.id))
