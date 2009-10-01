#!/usr/bin/env python
# -*- coding: utf-8 -*-

from turbogears import controllers, flash, redirect, identity
from turbogears import expose, validate, validators, error_handler
from cherrypy import request, response, NotFound, HTTPRedirect
from turboaffiliate import model

class Asamblea(controllers.Controller):
	
	"""Se encarga de controlar los afiliados que asistiran a una asamblea"""

