# -*- coding: utf8 -*-
#
# elecciones.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2009 - 2011 Carlos Flores <cafg10@gmail.com>
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

from turbogears import controllers, identity, expose, validate, validators
from turboaffiliate import model
from sqlobject.sqlbuilder import AND

class Elecciones(controllers.Controller):
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.elecciones.index")
    def index(self):
        return dict()
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.listado')
    def all(self):
        
        affiliates = model.Affiliate.select(AND(model.Affiliate.q.firstName!=None,
                                                model.Affiliate.q.lastName!=None,
                                                model.Affiliate.q.active==True))
        return dict(affiliates=affiliates, count=affiliates.count())
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.institutoDepto')
    @validate(validators=dict(departamento=validators.Int()))
    def stateSchool(self, departamento):
        
        departamento = model.Departamento.get(departamento)
        affiliates = model.Affiliate.selectBy(departamento=departamento)
        
        schools = dict()
        for affiliate in affiliates:
            if affiliate.school in schools:
                if affiliate.active == False:
                    continue
                schools[affiliate.school].append(affiliate)
            else:
                schools[affiliate.school] = list()
                schools[affiliate.school].append(affiliate)
        
        return dict(departamento=departamento, schools=schools)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.urnas')
    @validate(validators=dict(departamento=validators.Int()))
    def urnasDepartamentales(self, departamento):
        
        departamento = model.Departamento.get(departamento)
        afiliados = model.Affiliate.selectBy(departamento=departamento,active=True)
        
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
    @validate(validators=dict(departamento=validators.Int()))
    def urnasDepartamentalesCinco(self, departamento):
        
        departamento = model.Departamento.get(departamento)
        afiliados = model.Affiliate.selectBy(departamento=departamento,active=True)
        
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
    @validate(validators=dict(departamento=validators.Int()))
    def actas(self, departamento):
        
        departamento = model.Departamento.get(departamento)
        afiliados = model.Affiliate.selectBy(departamento=departamento,active=True)
        
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
    @validate(validators=dict(departamento=validators.Int()))
    def urnasMunicipio(self, departamento):
        
        departamento = model.Departamento.get(departamento)
        afiliados = model.Affiliate.selectBy(departamento=departamento,active=True)
        urnas = dict()
        cantidadUrnas = 0
        
        for afiliado in afiliados:
            
            if not afiliado.municipio in urnas:
                urnas[afiliado.municipio] = dict()
            
            if afiliado.school in urnas[afiliado.municipio]:
                urnas[afiliado.municipio][afiliado.school].append(afiliado)
            else:
                urnas[afiliado.municipio][afiliado.school] = list()
                urnas[afiliado.municipio][afiliado.school].append(afiliado)
                cantidadUrnas += 1
        
        return dict(urnas=urnas, departamento=departamento, cantidad=afiliados.count(), cantidadUrnas=cantidadUrnas)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.urnasMunicipios')
    @validate(validators=dict(departamento=validators.Int()))
    def listaUrnasMunicipio(self, departamento):
        
        departamento = model.Departamento.get(departamento)
        afiliados = model.Affiliate.selectBy(departamento=departamento,active=True)
        urnas = dict()
        
        for afiliado in afiliados:
            
            if not afiliado.municipio in urnas:
                urnas[afiliado.municipio] = dict()
            
            if afiliado.school in urnas[afiliado.municipio]:
                urnas[afiliado.municipio][afiliado.school].append(afiliado)
            else:
                urnas[afiliado.municipio][afiliado.school] = list()
                urnas[afiliado.municipio][afiliado.school].append(afiliado)
        
        for municipio in urnas:
            
            especial = list()
            for instituto, v in urnas[municipio].items():
                if len(urnas[municipio][instituto]) < 5:
                    especial.extend(urnas[municipio][instituto])
                    del urnas[municipio][instituto]
            urnas[municipio]['Urna Especial'] = especial
        
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
    @validate(validators=dict(cotizacion=validators.Int()))
    def cotizacion(self, cotizacion):
        
        cotizacion = model.Cotizacion.get(cotizacion)
        afiliados = model.Affiliate.selectBy(active=True,cotizacion=cotizacion)
        
        return dict(affiliates=afiliados, count=afiliados.count())
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.listado')
    @validate(validators=dict(cotizacion=validators.Int(), departamento=validators.Int()))
    def cotizacionDepto(self, cotizacion, departamento):
        
        cotizacion = model.Cotizacion.get(cotizacion)
        departamento = model.Departamento.get(departamento)
        afiliados = model.Affiliate.selectBy(active=True,cotizacion=cotizacion,
                                             departamento=departamento)
        
        return dict(affiliates=afiliados, count=afiliados.count())
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.departamento')
    @validate(validators=dict(departamento=validators.Int()))
    def departamento(self, departamento):
        
        departamento = model.Departamento.get(departamento)
        afiliados = model.Affiliate.selectBy(departamento=departamento,active=True)
        
        return dict(afiliados=afiliados, departamento=departamento, cantidad=afiliados.count())
    
    def sinInstituto(self):
        
        afiliados = model.Affiliate.selectBy(active=True,school=None)
        
        return dict(afiliados=afiliados)
    
    def sinIdentidad(self):
        
        afiliados = model.Affiliate.selectBy(active=True,cardID=None)
        
        return dict(afiliados=afiliados)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.departamentos')
    def resumenUrnas(self):
        
        departamentos = dict()
        for n in range(1, 19):
            resultado = self.urnas_depto(n)
            print resultado
            
            
            departamentos[resultado['departamento']] = len(resultado['urnas'])
         
        return dict(departamentos=departamentos)
    
    def urnas_depto(self, departamento):
        departamento = model.Departamento.get(departamento)
        afiliados = model.Affiliate.selectBy(departamento=departamento,active=True)
        
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
    
