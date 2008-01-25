#!/usr/bin/python
# -*- coding: utf8 -*-
#
# account.py
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
from datetime import date
from mx.DateTime import *

class Reinteger(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.reinteger.index")
	def index(self):
		return dict()
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.reinteger.add")
	def default(self, code):
		
		try:
			reinteger = model.Reinteger.get(int(code))
			return dict(reinteger=reinteger)
		
		except model.SQLObjectNotFound:
			flash('No existe el reintegro %s' % code)
			raise redirect('/reinteger')
		
		except ValueError:
			flash(u'Número de Reintegro invalido')
			raise redirect('/reinteger')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def save(self, **kw):
		
		try:
			if kw['amount'] == '':
				flash(u'Cantidad invalida')
				raise redirect('/reinteger/add')
			
			kw['affiliate'] = model.Affiliate.get(int(kw['affiliate']))
			reinteger = model.Reinteger(**kw)
			raise redirect('/reinteger/%s' % reinteger.id)
		
		except model.SQLObjectNotFound:
			flash('No existe el Afiliado %s' % code)
			raise redirect('/reinteger')
		
		except ValueError:
			flash(u'Número de Afiliado invalido')
			raise redirect('/reinteger')
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.reinteger.search")
	def search(self, code):
		try:
			affiliate = model.Affiliate.get(int(code))
			reintegers = model.Reinteger.select(model.Reinteger.q.affiliate==affiliate)
			return dict(reintegers=reintegers)
		
		except model.SQLObjectNotFound:
			flash('No existe el Afiliado %s' % code)
			raise redirect('/affiliate')
		
		except ValueError:
			flash(u'Número de Afiliado invalido')
			raise redirect('/affiliate')

class Funebre(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.funebre.index")
	def index(self):
		return dict()
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.funebre.add")
	def add(self, code):
		
		try:
			affiliate = model.Affiliate.get(int(code))
		
		except model.SQLObjectNotFound:
			flash('No se encontro el afiliado con el número %s' % code)
			raise redirect('/affiliate')
		
		except ValueError:
			flash('Número de afiliado invalido')
			raise redirect('/affiliate')
		
		return dict(affiliate=affiliate)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.funebre.funebre")
	def default(self, code):
		
		try:
			funebre = model.Funebre.get(int(code))
			return dict(funebre=funebre)
		
		except model.SQLObjectNotFound:
			flash('No existe la Ayuda Funebre %s' % code)
			raise redirect('/funebre')
		
		except ValueError:
			flash(u'Número de Ayuda invalido')
			raise redirect('/funebre')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def save(self, **kw):
		
		try:
			if kw['amount'] == '':
				flash(u'Cantidad invalida')
				raise redirect('/funebre/add')
			
			kw['affiliate'] = model.Affiliate.get(int(kw['affiliate']))
			kw['cheque'] = int(kw['cheque'])
			funebre = model.Funebre(**kw)
			raise redirect('/funebre/%s' % funebre.id)
		
		except model.SQLObjectNotFound:
			flash('No existe el Afiliado %s' % code)
			raise redirect('/funebre')
		
		except ValueError:
			flash(u'Número de Afiliado invalido')
			raise redirect('/funebre')
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.funebre.search")
	def search(self, code):
		try:
			affiliate = model.Affiliate.get(int(code))
			query = "funebre.affiliate_id = %s" % (affiliate.id)
			funebres = model.Funebre.select(query)
			return dict(funebres=funebres)
		
		except model.SQLObjectNotFound:
			flash('No existe el Afiliado %s' % code)
			raise redirect('/affiliate')
		
		except ValueError:
			flash(u'Número de Afiliado invalido')
			raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def delete(self, code):
		
		try:
			funebre = model.Funebre.get(int(code))
			funebre.destroySelf()
			flash("Ayuda Funebre Eliminada")
			raise redirect('/funebre')
		except:
			raise redirect('/funebre')

class Survival(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.survival.index")
	def index(self):
		return dict()
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.survival.add")
	def add(self, code):
		
		try:
			affiliate = model.Affiliate.get(int(code))
		
		except model.SQLObjectNotFound:
			flash('No se encontro el afiliado con el número %s' % code)
			raise redirect('/affiliate')
		
		except ValueError:
			flash('Número de afiliado invalido')
			raise redirect('/affiliate')
		
		return dict(affiliate=affiliate)
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.survival.survival")
	def default(self, code):
		
		try:
			survival = model.Survival.get(int(code))
			return dict(survival=survival)
		
		except model.SQLObjectNotFound:
			flash('No existe la Ayuda de Sobrevivencia %s' % code)
			raise redirect('/survival')
		
		except ValueError:
			flash(u'Número de Ayuda invalido')
			raise redirect('/survival')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def save(self, **kw):
		
		try:
			if kw['amount'] == '':
				flash(u'Cantidad invalida')
				raise redirect('/survival/add/%' % kw['affiliate'])
			
			kw['affiliate'] = model.Affiliate.get(int(kw['affiliate']))
			kw['cheque'] = int(kw['chueque'])
			survival = model.Survival(**kw)
			raise redirect('/survival/%s' % survival.id)
		
		except model.SQLObjectNotFound:
			flash('No existe el Afiliado %s' % code)
			raise redirect('/affiliate')
		
		except ValueError:
			flash(u'Número de Afiliado invalido')
			raise redirect('/survival')
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.survival.search")
	def search(self, code):
		try:
			affiliate = model.Affiliate.get(int(code))
			query = "survival.affiliate_id = %s" % (affiliate.id)
			survivals = model.Survival.select(query)
			return dict(survivals=survivals)
		
		except model.SQLObjectNotFound:
			flash('No existe el Afiliado %s' % code)
			raise redirect('/affiliate')
		
		except ValueError:
			flash(u'Número de Afiliado invalido')
			raise redirect('/affiliate')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def delete(self, code):
		
		try:
			survival = model.Survival.get(int(code))
			survival.destroySelf()
			flash("Ayuda de Sobrevivencia Eliminada")
			raise redirect('/survival')
		except:
			raise redirect('/survival')

class Devolution(controllers.Controller):
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.devolution.index")
	def index(self):
		return dict()
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.devolution.add")
	def default(self, code):
		
		try:
			survival = model.Devolution.get(int(code))
			return dict(survival=survival)
		
		except model.SQLObjectNotFound:
			flash('No existe la Devolucion %s' % code)
			raise redirect('/devolution')
		
		except ValueError:
			flash(u'Número de Ayuda invalido')
			raise redirect('/devolution')
	
	@identity.require(identity.not_anonymous())
	@expose()
	def save(self, **kw):
		
		try:
			if kw['amount'] == '':
				flash(u'Cantidad invalida')
				raise redirect('/devolution/add/%' % kw['affiliate'])
			
			if kw['affiliate'] != '':
				kw['affiliate'] = model.Affiliate.get(int(kw['affiliate'])).id
			else:
				kw['affiliate'] = 0
			
			devolution = model.Devolution(**kw)
			raise redirect('/devolution/%s' % devolution.id)
		
		except model.SQLObjectNotFound:
			flash('No existe el Afiliado %s' % code)
			raise redirect('/devolution')
		
		except ValueError:
			flash(u'Número de Afiliado invalido')
			raise redirect('/devolution')
	
	@identity.require(identity.not_anonymous())
	@expose(template="turboaffiliate.templates.survival.search")
	def search(self, code):
		
		code = code.replace('*', '%')
		query = "devolution.name LIKE %%%s%%" % (code)
		devolutions = model.Devolution.select(query)
		return dict(devolutions=devolutions)
