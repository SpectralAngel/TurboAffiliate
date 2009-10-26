#!/usr/bin/env python
# -*- coding: utf-8 -*-

from turbogears import controllers, flash, redirect, identity
from turbogears import expose, validate, validators
from turboaffiliate import model

class Asamblea(controllers.Controller):
	
	"""Se encarga de controlar los afiliados que asistiran a una asamblea"""
	
	@expose(template='turboaffiliate.templates.asamblea.index')
	def index(self):
		
		return dict()
	
	@expose()
	@validate(validators=dict(anio=validators.Int()))
	def agregar(self, anio):
		
		"""Agrega una Asamblea a la existencia del COPEMH"""
		
		asamblea = model.Asamblea()
		asamblea.id = anio
		
		raise redirect('/asamblea/%' % asamblea)
	
	@expose(template="turboaffiliate.templates.asamblea.asamblea")
	@validate(validators=dict(asamblea=validators.Int()))
	def default(self, asamblea):
		
		"""Muestra los datos de una Asamblea"""
		
		return dict(asamblea=model.Asamblea.get(asamblea))
	
	@expose()
	@validate(validators=dict(asamblea=validators.Int(), afiliado=validators.Int(),
							  municipio=validators.String(), cuenta=validators.String(),
							  banco=validators.Int(), departamento=validators.String()))
	def asistente(self, afiliado, asamblea, municipio, banco, cuenta, departamento):
		
		"""Agrega un Asistente a la asamblea"""
		
		asistencia = model.Asistencia()
		asistencia.afiliado = model.Affiliate.get(afiliado)
		asistencia.asamblea = model.Asamblea.get(asamblea)
		asistencia.municipio = municipio
		asistencia.banco = model.Banco.get(banco)
		asistencia.cuenta = cuenta
		asistencia.departamento = departamento
		
		raise redirect('/asamblea')
