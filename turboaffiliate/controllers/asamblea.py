#!/usr/bin/env python
# -*- coding: utf-8 -*-

from turbogears import controllers, flash, redirect, identity
from turbogears import expose, validate, validators, error_handler
from cherrypy import request, response, NotFound, HTTPRedirect
from turboaffiliate import model

class Asamblea(controllers.Controller):
	
	"""Se encarga de controlar los afiliados que asistiran a una asamblea"""
	
	@expose(template='turboaffiliate.templates.asamblea.index')
	def index(self):
		
		return dict()
	
	@expose()
	@validate(validators=dict(anio=validators.Int()))
	def agregar(self, anio):
		
		asamblea = model.Asamblea()
		asamblea.id = anio
		
		raise redirect('/asamblea/%' % asamblea)
	
	@expose(template="turboaffiliate.templates.asamblea.asamblea")
	@validate(validators=dict(asamblea=validators.Int()))
	def default(self, asamblea):
		
		return dict(asamblea=model.Asamblea.get(asamblea))
	
	@expose()
	@validate(validators=dict(asamblea=validators.Int(), afiliado=validators.Int(), municipio=validators.String()))
	def asistente(self, afiliado, asamblea):
		
		asistente = model.Asistente()
		asistente.afiliado = model.Affiliate.get(afiliado)
		asistente.asamblea = model.Asamblea.get(asamblea)
		asistente.municipio = municipio
		
		raise redirect('/asamblea')
