#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# status.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2009 Carlos Flores <cafg10@gmail.com>
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

from turbogears import controllers, flash, redirect, identity
from turbogears import expose, validate, validators, error_handler
from cherrypy import request, response, NotFound, HTTPRedirect
from turboaffiliate import model, json
from decimal import *
from datetime import date, datetime

class Elecciones(controllers.Controller):
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.elecciones.index")
    def index(self):
        return dict()
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.listado')
    def all(self):
        
        query = "affiliate.first_name is not null and affiliate.last_name is not null and  affiliate.active = %s" % True
        affiliates = model.Affiliate.select(query)
        return dict(affiliates=affiliates, count=affiliates.count())
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.institutoDepto')
    def stateSchool(self, state):
        
        affiliates = model.Affiliate.select(model.Affiliate.q.state==state)
        
        schools = dict()
        for affiliate in affiliates:
            if affiliate.school in schools:
                if affiliate.active == False:
                    continue
                schools[affiliate.school].append(affiliate)
            else:
                schools[affiliate.school] = list()
                schools[affiliate.school].append(affiliate)
        
        return dict(state=state, schools=schools)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.urnas')
    def urnasDepartamentales(self, departamento):
        
        afiliados = model.Affiliate.selectBy(active=True,state=departamento)
        
        urnas = dict()
        urnas['Sin Instituto'] = 0
        for afiliado in afiliados:
            
            if afiliado.school in urnas:
                urnas[afiliado.school] += 1
            else:
                urnas[afiliado.school] = 1
        
        for instituto in urnas:
            
            if instituto is None:
                urnas['Sin Instituto'] += urnas[instituto]
            
            if instituto == '':
                urnas['Sin Instituto'] += urnas[instituto]
        
        if None in urnas:
            del urnas[None]
        if '' in urnas:
            del urnas['']
        
        return dict(urnas=urnas, cantidad=afiliados.count(), departamento=departamento)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.urnas')
    def urnasDepartamentalesCinco(self, departamento):
        
        afiliados = model.Affiliate.selectBy(active=True,state=departamento)
        
        urnas = dict()
        urnas['Sin Instituto'] = 0
        for afiliado in afiliados:
            
            if afiliado.school in urnas:
                urnas[afiliado.school] += 1
            else:
                urnas[afiliado.school] = 1
        
        for instituto in urnas:
            
            if instituto is None:
                urnas['Sin Instituto'] += urnas[instituto]
            
            if instituto == '':
                urnas['Sin Instituto'] += urnas[instituto]
        
        if None in urnas:
            del urnas[None]
        if '' in urnas:
            del urnas['']
       
        urnas2 = dict()
        for instituto in urnas:
           
            if urnas[instituto] >= 5:
                
                urnas2[instituto] = urnas[instituto]
        
        return dict(urnas=urnas2, cantidad=sum(urnas2[i] for i in urnas2), departamento=departamento)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.acta')
    def actas(self, departamento):
        
        afiliados = model.Affiliate.selectBy(active=True,state=departamento)
        
        urnas = dict()
        urnas['Sin Instituto'] = 0
        for afiliado in afiliados:
            
            if afiliado.school in urnas:
                urnas[afiliado.school] += 1
            else:
                urnas[afiliado.school] = 1
        
        for instituto in urnas:
            
            if instituto is None:
                urnas['Sin Instituto'] += urnas[instituto]
            
            if instituto == '':
                urnas['Sin Instituto'] += urnas[instituto]
        
        if None in urnas:
            del urnas[None]
        if '' in urnas:
            del urnas['']
       
        urnas2 = dict()
        for instituto in urnas:
           
            if urnas[instituto] >= 5:
                
                urnas2[instituto] = urnas[instituto]
        
        return dict(urnas=urnas2, cantidad=sum(urnas2[i] for i in urnas2), departamento=departamento)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.municipios')
    def urnasMunicipio(self, departamento):
        
        afiliados = model.Affiliate.selectBy(active=True,state=departamento)
        urnas = dict()
        
        for afiliado in afiliados:
            
            if not afiliado.town in urnas:
                urnas[afiliado.town] = dict()
            
            if afiliado.school in urnas[afiliado.town]:
            	urnas[afiliado.town][afiliado.school].append(afiliado)
            else:
            	urnas[afiliado.town][afiliado.school] = list()
            	urnas[afiliado.town][afiliado.school].append(afiliado)
        
        return dict(urnas=urnas, departamento=departamento, cantidad=afiliados.count())
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.urnasMunicipios')
    def listaUrnasMunicipio(self, departamento):
        
        afiliados = model.Affiliate.selectBy(active=True,state=departamento)
        urnas = dict()
        
        for afiliado in afiliados:
            
            if not afiliado.town in urnas:
                urnas[afiliado.town] = dict()
            
            if afiliado.school in urnas[afiliado.town]:
            	urnas[afiliado.town][afiliado.school].append(afiliado)
            else:
            	urnas[afiliado.town][afiliado.school] = list()
            	urnas[afiliado.town][afiliado.school].append(afiliado)
        
        return dict(urnas=urnas, departamento=departamento, cantidad=afiliados.count())
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.urnas')
    def totalUrnas(self):
        
        afiliados = model.Affiliate.selectBy(active=True)
        
        urnas = dict()
        urnas['Sin Instituto'] = 0
        for afiliado in afiliados:
            
            if afiliado.school in urnas:
                urnas[afiliado.school] += 1
            else:
                urnas[afiliado.school] = 1
        
        for instituto in urnas:
            
            if instituto is None:
                urnas['Sin Instituto'] += urnas[instituto]
            
            if instituto == '':
                urnas['Sin Instituto'] += urnas[instituto]
        
        if None in urnas:
            del urnas[None]
        if '' in urnas:
            del urnas['']
       
        urnas2 = dict()
        for instituto in urnas:
           
            if urnas[instituto] >= 5:
                
                urnas2[instituto] = urnas[instituto]
        
        return dict(urnas=urnas2, cantidad=sum(urnas2[i] for i in urnas2), departamento="Total de Urnas")
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.listado')
    def cotizacion(self, cotizacion):
        
        afiliados = model.Affiliate.selectBy(active=True,payment=cotizacion)
        
        return dict(affiliates=afiliados, count=afiliados.count())
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.departamento')
    def departamento(self, departamento):
        
        afiliados = model.Affiliate.selectBy(active=True,state=departamento)
        
        return dict(afiliados=afiliados, departamento=departamento, cantidad=afiliados.count())
    
    def sinInstituto(self):
        
        afiliados = model.Affiliate.selectBy(active=True,school=None)
        
        return dict(afiliados=afiliados)
    
    def sinIdentidad(self):
        
        afiliados = model.Affiliate.selectBy(active=True,cardID=None)
        
        return dict(afiliados=afiliados)
