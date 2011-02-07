# -*- coding: utf8 -*-
#
# asamblea.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2010, 2011 Carlos Flores <cafg10@gmail.com>
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

from decimal import Decimal
from turboaffiliate import model
from turbogears import (controllers, identity, expose, validate, validators,
                        redirect, flash)
import locale

def inscripcionRealizada(afiliado):
    
    return u"Se inscribió a {0} - {1} {2}".format(afiliado.id,
                                                  afiliado.firstName,
                                                  afiliado.lastName)

class Banco(controllers.Controller):
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.asamblea.banco.index')
    def index(self):
        
        return dict(bancos=model.Banco.select())
    
    @validate(validators=dict(nombre=validators.Int(),id=validators.Int()))
    @expose()
    def agregar(self, **kw):
        
        model.Banco(**kw)
        
        raise redirect('/banco')

class Viatico(controllers.Controller):
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.asamblea.viatico.index')
    def index(self):
        
        return dict(departamentos=model.Departamento.select(),
                    asambleas=model.Asamblea.select())
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.asamblea.viatico.asamblea')
    @validate(validators=dict(asamblea=validators.Int()))
    def asamblea(self, asamblea):
        
        asamblea = model.Asamblea.get(asamblea)
        
        return dict(viaticos=model.Viatico.selectBy(asamblea=asamblea),
                    asamblea=asamblea)
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(asamblea=validators.Int(),monto=validators.UnicodeString(),
                              municipio=validators.Int()))
    def agregar(self, asamblea, municipio, **kw):
        
        kw['monto'] = Decimal(kw['monto'])
        
        kw['asamblea'] = model.Asamblea.get(asamblea)
        kw['municipio'] = model.Municipio.get(municipio)
        viatico = model.Viatico(**kw)
        
        flash(u'Se agrego el viatico al Municipio de {0}'.format(viatico.municipio.nombre))
        
        raise redirect('/asamblea/viatico')
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(asamblea=validators.Int()))
    def eliminar(self, viatico):
        
        viatico = model.Viatico.get(viatico)
        viatico.destroySelf()
        
        raise redirect('/asamblea/banco')

class Asamblea(controllers.Controller):
    
    banco = Banco()
    viatico = Viatico()
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.asamblea.index')
    def index(self):
        
        return dict(asambleas=model.Asamblea.select(), departamentos=model.Departamento.select())
    
    @expose()
    @validate(validators=dict(departamento=validators.Int(), nombre=validators.UnicodeString(),
                              numero=validators.Int()))
    def agregar(self, departamento, **kw):
        
        kw['departamento'] = model.Departamento.get(departamento)
        
        asamblea = model.Asamblea(**kw)
        
        raise redirect('/asamblea/{0}'.format(asamblea.id))
    
    @identity.require(identity.not_anonymous())
    @expose('turboaffiliate.templates.asamblea.inscripcion')
    @validate(validators=dict(asamblea=validators.Int()))
    def inscripcion(self, asamblea):
        
        return dict(asamblea=model.Asamblea.get(asamblea),
                    bancos=model.Banco.select(),
                    departamentos=model.Departamento.select())
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.asamblea.asamblea')
    @validate(validators=dict(asamblea=validators.Int()))
    def default(self, asamblea):
        
        return dict(departamentos=model.Departamento.select(),
                    bancos=model.Banco.select(),
                    asamblea=model.Asamblea.get(asamblea))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.asamblea.confirmar')
    @validate(validators=dict(asamblea=validators.Int(),
                              afiliado=validators.Int()))
    def confirmar(self, afiliado, asamblea):
        
        afiliado = model.Affiliate.get(afiliado)
        banco = None
        deshabilitado = False
        
        if afiliado.tiempo() < 1 and identity.current.user.user_name != 'asura10':
            deshabilitado = True
            flash(u'El afiliado no tiene un año desde su afiliación: {0}'.format(afiliado.joined))
        
        if afiliado.debt() > 1000 and identity.current.user.user_name != 'asura10':
            deshabilitado = True
            flash(u'El afiliado no se encuentra solvente. Deuda {0}'.format(
                                locale.currency(afiliado.debt(), True, True)
            ))
        
        if afiliado.banco != None:
            banco = model.Banco.get(afiliado.banco)
        
        return dict(deshabilitado=deshabilitado,
                    afiliado=afiliado,banco=banco,
                    asamblea=model.Asamblea.get(asamblea),
                    bancos=model.Banco.select(),
                    departamentos=model.Departamento.select())
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.asamblea.confirmar')
    @validate(validators=dict(asamblea=validators.Int(),
                              identidad=validators.UnicodeString()))
    def confirmarIdentidad(self, identidad, asamblea):
        
        afiliado = model.Affiliate.selectBy(cardID=identidad).limit(1).getOne()
        banco = None
        deshabilitado = False
        
        if afiliado.tiempo() < 1 and identity.current.user.user_name != 'asura10':
            deshabilitado = True
            flash(u'El afiliado no tiene un año desde su afiliación: {0}'.format(afiliado.joined))
        
        if afiliado.debt() > 1000 and identity.current.user.user_name != 'asura10':
            deshabilitado = True
            flash(u'El afiliado no se encuentra solvente. Deuda {0}'.format(
                                locale.currency(afiliado.debt(), True, True)
            ))
        
        if afiliado.banco != None:
            banco = model.Banco.get(afiliado.banco)
        
        return dict(deshabilitado=deshabilitado,
                    afiliado=afiliado,banco=banco,
                    asamblea=model.Asamblea.get(asamblea),
                    bancos=model.Banco.select(),
                    departamentos=model.Departamento.select())
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(asamblea=validators.Int(),
                              afiliado=validators.Int()))
    def inscribir(self, afiliado, asamblea):
        
        if identity.current.user.user_name != 'asura10':
            raise redirect('/asamblea/inscripcion/{0}'.format(asamblea.id))
        
        kw = dict()
        afiliado = model.Affiliate.get(afiliado)
        asamblea = model.Asamblea.get(asamblea)
        
        if afiliado.tiempo() < 1 and identity.current.user.user_name != 'asura10':
            raise redirect('/asamblea/inscripcion/{0}'.format(asamblea.id))
        
        if afiliado.debt() > 1000 and identity.current.user.user_name != 'asura10':
            raise redirect('/asamblea/inscripcion/{0}'.format(asamblea.id))
        
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Inscrito afiliado {0} en asamblea {1}".format(afiliado.id, asamblea.id)
        model.Logger(**log)
        
        kw['afiliado'] = afiliado
        kw['asamblea'] = asamblea
        kw['viatico'] = model.Viatico.selectBy(asamblea=asamblea,
                        municipio=afiliado.municipio).limit(1).getOne()
        
        model.Inscripcion(**kw)
        flash(inscripcionRealizada(afiliado))
        
        raise redirect('/asamblea/inscripcion/{0}'.format(asamblea.id))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(afiliado=validators.Int(),
                              banco=validators.Int(),
                              departamento=validators.Int(),
                              cuenta=validators.Int(),
                              asamblea=validators.Int(),
                              municipio=validators.Int()))
    def corregir(self, afiliado, asamblea, departamento, banco, cuenta, municipio):
        
        if identity.current.user.user_name != 'asura10':
            raise redirect('/asamblea/inscripcion/{0}'.format(asamblea.id))
        
        kw = dict()
        afiliado = model.Affiliate.get(afiliado)
        asamblea = model.Asamblea.get(asamblea)
        
        departamento = model.Departamento.get(departamento)
        afiliado.departamento = departamento
        afiliado.municipio = model.Municipio.get(municipio)
        
        if afiliado.tiempo() < 1 and identity.current.user.user_name != 'asura10':
            raise redirect('/asamblea/inscripcion/{0}'.format(asamblea.id))
        
        if afiliado.debt() > 1000 and identity.current.user.user_name != 'asura10':
            raise redirect('/asamblea/inscripcion/{0}'.format(asamblea.id))
        
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Inscrito afiliado {0} en asamblea {1}".format(afiliado.id, asamblea.id)
        model.Logger(**log)
        
        banco = model.Banco.get(banco)
        afiliado.banco = banco.id
        afiliado.cuenta = cuenta
        kw['afiliado'] = afiliado
        kw['asamblea'] = asamblea
        kw['viatico'] = model.Viatico.selectBy(asamblea=asamblea,
                                               municipio=afiliado.municipio
                                               ).limit(1).getOne()
        
        model.Inscripcion(**kw)
        flash(inscripcionRealizada(afiliado))
        
        raise redirect('/asamblea/inscripcion/{0}'.format(asamblea.id))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(afiliado=validators.Int(),
                              departamento=validators.Int(),
                              asamblea=validators.Int(),
                              municipio=validators.Int()))
    def corregirDepto(self, afiliado, asamblea, departamento, municipio):
        
        if identity.current.user.user_name != 'asura10':
            raise redirect('/asamblea/inscripcion/{0}'.format(asamblea.id))
        
        kw = dict()
        afiliado = model.Affiliate.get(afiliado)
        asamblea = model.Asamblea.get(asamblea)
        departamento = model.Departamento.get(departamento)
        afiliado.departamento = departamento
        municipio = model.Municipio.get(municipio)
        kw['afiliado'] = afiliado
        kw['asamblea'] = asamblea
        kw['viatico'] = model.Viatico.selectBy(asamblea=asamblea,
                                               departamento=departamento,
                                               municipio=municipio
                                               ).limit(1).getOne()
        
        model.Inscripcion(**kw)
        flash(inscripcionRealizada(afiliado))
        
        raise redirect('/asamblea/inscripcion/{0}'.format(asamblea.id))
    
    @expose()
    def ingresar(self):
        
        ninguno = model.Municipio.get(299)
        ndepto = model.Departamento.get(19)
        
        afiliados = model.Affiliate.select(model.Affiliate.q.municipio==ninguno)
        
        for afiliado in afiliados:
            if afiliado.departamento != ndepto:
                
                if afiliado.departamento == None:
                    afiliado.departamento = ndepto
                    continue
                
                afiliado.municipio = afiliado.departamento.municipios[1]
        
        afiliados = model.Affiliate.select()
        
        for afiliado in afiliados:
            
            if afiliado.town == None:
                if afiliado.municipio == None:
                    afiliado.municipio = ninguno
                continue
            
            if afiliado.departamento == None:
                afiliado.departamento = ndepto
            
            municipios = dict()
            for m in afiliado.departamento.municipios:
                municipios[m.nombre.lower()] = m
            
            if afiliado.town.lower() in municipios:
                afiliado.municipio = municipios[afiliado.town.lower()]
            else:
                for m in municipios:
                    if m.find(afiliado.town.lower()) != -1:
                        afiliado.municipio = municipios[m]
        
        flash('Registrados los municipos de los afiliados')
        
        raise redirect('/asamblea')
