#!/usr/bin/python
#
# refinanced.py
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
from turboaffiliate import model, json
from datetime import date
from decimal import *

class Refinanced(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.loan.refinanced.refinanced")
	def  default(self, loan):
		
		try:
			loan = model.RefinancedLoan.get(int(loan))
		except model.SQLObjectNotFound:
			flash("Prestamo no encontrado")
			raise redirect('/loan')
		
		return dict(loan=loan)
	
	@identity.require(identity.not_anonymous())
	@expose()
	def  remove(self, loan):
		
		try:
			loan = model.RefinancedLoan.get(int(loan))
			loan.remove()
		except model.SQLObjectNotFound:
			flash("Prestamo no encontrado")
			raise redirect('/loan')
		
		return dict(loan=loan)
		
		flash("Prestamo pagado")
		raise redirect('/loan')
