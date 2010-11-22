#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# asamblea.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2010 Carlos Flores <cafg10@gmail.com>
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
from sqlobject import SQLObjectNotFound
from turboaffiliate import model
from turbogears import (controllers, identity, expose, validate, validators,
                        redirect, flash)

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
                              departamento=validators.Int()))
    def agregar(self, asamblea, departamento, **kw):
        
        kw['monto'] = Decimal(kw['monto'])
        
        kw['asamblea'] = model.Asamblea.get(asamblea)
        kw['departamento'] = model.Departamento.get(departamento)
        viatico = model.Viatico(**kw)
        
        flash(u'Se agrego el viatico al Departamento de {0}'.format(viatico.departamento.nombre))
        
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
    @expose()
    @validate(validators=dict(afiliado=validators.Int(),
                              banco=validators.Int(),
                              departamento=validators.Int(),
                              cuenta=validators.Int(),
                              asamblea=validators.Int()))
    def inscribir(self, afiliado, banco, departamento, cuenta, asamblea):
        
        kw = dict()
        kw['afiliado'] = model.Affiliate.get(afiliado)
        kw['afiliado'].banco = model.Banco.get(banco).id
        kw['afiliado'].cuenta = cuenta
        
        kw['departamento'] = model.Departamento.get(departamento)
        kw['asamblea'] = model.Asamblea.get(asamblea)
        
        kw['viatico'] = model.Viatico.selectBy(asamblea=kw['asamblea'],
                            departamento=kw['departamento']).limit(1).getOne()
        
        model.Inscripcion(**kw)
        
        flash(inscripcionRealizada(kw['afiliado']))
        
        raise redirect('/asamblea/inscripcion/{0}'.format(kw['asamblea'].id))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(identidad=validators.UnicodeString(),
                              banco=validators.Int(),
                              departamento=validators.Int(),
                              cuenta=validators.Int(),
                              asamblea=validators.Int()))
    def identidad(self, identidad, banco, departamento, cuenta, asamblea):
        
        kw = dict()
        kw['afiliado'] = model.Affiliate.selectBy(cardID=identidad).limit(1).getOne()
        kw['afiliado'].banco = model.Banco.get(banco).id
        kw['afiliado'].cuenta = cuenta
        kw['departamento'] = model.Departamento.get(departamento)
        kw['asamblea'] = model.Asamblea.get(asamblea)
        
        kw['viatico'] = model.Viatico.selectBy(asamblea=kw['asamblea'],
                            departamento=kw['departamento']).limit(1).getOne()
        
        model.Inscripcion(**kw)
        
        flash(inscripcionRealizada(kw['afiliado']))
        
        raise redirect('/asamblea/inscripcion/{0}'.format(asamblea.id))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(afiliado=validators.Int(),
                              departamento=validators.Int(),
                              asamblea=validators.Int()))
    def inscripcionRapida(self, afiliado, departamento, asamblea):
        
        kw = dict()
        kw['afiliado'] = model.Affiliate.get(afiliado)
        
        kw['departamento'] = model.Departamento.get(departamento)
        kw['asamblea'] = model.Asamblea.get(asamblea)
        
        kw['viatico'] = model.Viatico.selectBy(asamblea=kw['asamblea'],
                            departamento=kw['departamento']).limit(1).getOne()
        
        model.Inscripcion(**kw)
        
        flash(inscripcionRealizada(kw['afiliado']))
        
        raise redirect('/asamblea/inscripcion/{0}'.format(kw['asamblea'].id))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(identidad=validators.UnicodeString(),
                              departamento=validators.Int(),
                              asamblea=validators.Int()))
    def inscripcionRapidaI(self, identidad, departamento, asamblea):
        
        kw = dict()
        kw['afiliado'] = model.Affiliate.selectBy(cardID=identidad).limit(1).getOne()
        
        kw['departamento'] = model.Departamento.get(departamento)
        kw['asamblea'] = model.Asamblea.get(asamblea)
        
        kw['viatico'] = model.Viatico.selectBy(asamblea=kw['asamblea'],
                            departamento=kw['departamento']).limit(1).getOne()
        
        model.Inscripcion(**kw)
        
        flash(inscripcionRealizada(kw['afiliado']))
        
        raise redirect('/asamblea/inscripcion/{0}'.format(kw['asamblea'].id))
    
    @expose()
    @validate(validators=dict(departamento=validators.Int(),
                              nombre=validators.UnicodeString(),
                              numero=validators.Int()))
    def agregar(self, departamento, **kw):
        
        kw['departamento'] = model.Departamento.get(departamento)
        
        asamblea = model.Asamblea(**kw)
        
        raise redirect('/asamblea/{0}'.format(asamblea.id))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(afiliado=validators.Int(), banco=validators.Int(),
                              departamento=validators.Int(), cuenta=validators.Int()))
    def corregir(self, afiliado, banco, asamblea, cuenta, departamento):
        
        try:
            afiliado = model.Affiliate.get(afiliado)
            afiliado.banco = model.Banco.get(banco).id
            afiliado.cuenta = cuenta
            departamento = model.Departamento.get(departamento)
            asamblea = model.Asamblea.get(asamblea)
            inscripcion = model.Inscripcion.selectBy(afiliado=afiliado,
                                            asamblea=asamblea).limit(1).getOne()
            inscripcion.departamento = departamento
            inscripcion.viatico = model.Viatico.selectBy(asamblea=asamblea,
                            departamento=departamento).limit(1).getOne()
            inscripcion.enviado = False
        
        except SQLObjectNotFound:
            
            flash('El afiliado {0} no se encuentra inscrito'.format(afiliado))
            raise redirect('/asamblea/inscripcion/{0}'.format(asamblea))
        
        flash('Corregida la inscripcion del afiliado {0}'.format(afiliado.id))
        
        raise redirect('/asamblea/inscripcion/{0}'.format(asamblea))
