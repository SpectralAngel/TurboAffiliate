# -*- coding: utf8 -*-
#
# asamblea.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2010 - 2012 Carlos Flores <cafg10@gmail.com>
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
from sqlobject.sqlbuilder import *
from datetime import date

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
                    asambleas=model.Asamblea.select(),
                    bancos=model.Banco.select())
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.asamblea.viatico.asamblea')
    @validate(validators=dict(asamblea=validators.Int()))
    def asamblea(self, asamblea):
        
        asamblea = model.Asamblea.get(asamblea)
        
        return dict(viaticos=model.Viatico.selectBy(asamblea=asamblea),
                    asamblea=asamblea)
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(asamblea=validators.Int(),
                              monto=validators.UnicodeString(),
                              transporte=validators.UnicodeString(),
                              previo=validators.UnicodeString(),
                              posterior=validators.UnicodeString(),
                              municipio=validators.Int()))
    def agregar(self, asamblea, municipio, **kw):
        
        kw['monto'] = Decimal(kw['monto'])
        kw['transporte'] = Decimal(kw['transporte'])
        kw['previo'] = Decimal(kw['previo'])
        kw['posterior'] = Decimal(kw['posterior'])
        
        kw['asamblea'] = model.Asamblea.get(asamblea)
        kw['municipio'] = model.Municipio.get(municipio)
        viatico = model.Viatico(**kw)
        
        flash(u'Se agrego el viatico al Municipio de {0}'.format(
                                                    viatico.municipio.nombre))
        
        raise redirect('/asamblea/viatico')
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(asamblea=validators.Int(),
                              monto=validators.UnicodeString(),
                              transporte=validators.UnicodeString(),
                              previo=validators.UnicodeString(),
                              posterior=validators.UnicodeString(),
                              departamento=validators.Int()))
    def agregarDepto(self, asamblea, departamento, **kw):
        
        kw['monto'] = Decimal(kw['monto'])
        kw['transporte'] = Decimal(kw['transporte'])
        kw['previo'] = Decimal(kw['previo'])
        kw['posterior'] = Decimal(kw['posterior'])
        
        kw['asamblea'] = model.Asamblea.get(asamblea)
        departamento = model.Departamento.get(departamento)
        for municipio in departamento.municipios:
            kw['municipio'] = municipio
            model.Viatico(**kw)
        
        flash(u'Se agrego el viatico al Departamento de {0}'.format(
                                                    departamento.nombre))
        
        raise redirect('/asamblea/viatico')
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(asamblea=validators.Int()))
    def eliminar(self, viatico):
        
        viatico = model.Viatico.get(viatico)
        asamblea = viatico.asamblea
        viatico.destroySelf()
        
        raise redirect('/asamblea/{0}'.format(asamblea.id))

class Inscripcion(controllers.Controller):
    
    @identity.require(identity.not_anonymous())
    @expose('turboaffiliate.templates.asamblea.inscripcion')
    @validate(validators=dict(asamblea=validators.Int()))
    def default(self, asamblea):
        
        return dict(asamblea=model.Asamblea.get(asamblea),
                    bancos=model.Banco.selectBy(asambleista=True),
                    departamentos=model.Departamento.select())
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(inscripcion=validators.Int()))
    def reenviar(self, inscripcion):
        
        inscripcion = model.Inscripcion.get(inscripcion)
        inscripcion.enviado = False
        
        raise redirect('/affiliate/{0}'.format(inscripcion.afiliado.id))
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(viatico=validators.Int()))
    def enviar(self, inscripcion):
        
        """Cambia el estado de una inscripción a enviada"""
        
        inscripcion = model.Inscripcion.get(inscripcion)
        inscripcion.enviado = True
        inscripcion.envio = date.today()
        
        return dict(inscripcion=inscripcion)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.asamblea.pendientes')
    @validate(validators=dict(asamblea=validators.Int()))
    def pendientes(self, asamblea):
        
        """Muestra las inscripciones que estan pendientes de pago"""
        
        asamblea = model.Asamblea.get(asamblea)
        inscripciones = model.Inscripcion.selectBy(asamblea=asamblea, enviado=False)
        
        return dict(asamblea=asamblea, inscripciones=inscripciones)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.asamblea.pendientes')
    @validate(validators=dict(asamblea=validators.Int(),
                              departamento=validators.Int()))
    def pendientesDepartamento(self, asamblea, departamento):
        
        """Muestra las inscripciones que estan pendientes de pago"""
        
        asamblea = model.Asamblea.get(asamblea)
        departamento = model.Departamento.get(departamento)
        viaticos = model.Municipio.selectBy(departamento=departamento).throughTo.viaticos
        inscripciones = viaticos.throughTo.inscripciones.filter(AND(
                                    model.Inscripcion.q.asamblea==asamblea,
                                    model.Inscripcion.q.enviado==False))
        return dict(asamblea=asamblea, inscripciones=inscripciones)
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(asamblea=validators.Int(),
                              municipio=validators.Int()))
    def enviarDepartamento(self, asamblea, departamento):
        
        asamblea = model.Asamblea.get(asamblea)
        departamento = model.Departamento.get(departamento)
        viaticos = model.Municipio.selectBy(departamento=departamento).throughTo.viaticos
        inscripciones = viaticos.throughTo.inscripciones.filter(AND(
                                    model.Inscripcion.q.asamblea==asamblea,
                                    model.Inscripcion.q.enviado==False))
        
        for inscripcion in inscripciones:
            
            inscripcion.enviado = True
        
        flash(u'Marcadas como enviadas todas las Inscripciones de {0} en {1}'.format(asamblea.nombre, departamento.nombre))
        
        raise redirect('/asamblea/{0}'.format(asamblea.id))

class Asamblea(controllers.Controller):
    
    banco = Banco()
    viatico = Viatico()
    inscripcion = Inscripcion()
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.asamblea.index')
    def index(self):
        
        return dict(asambleas=model.Asamblea.select(),
                    departamentos=model.Departamento.select(),
                    bancos=model.Banco.select())
    
    @identity.require(identity.All(identity.in_any_group('admin', 'junta'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(departamento=validators.Int(),
                              nombre=validators.UnicodeString(),
                              numero=validators.Int()))
    def agregar(self, departamento, **kw):
        
        kw['departamento'] = model.Departamento.get(departamento)
        
        asamblea = model.Asamblea(**kw)
        
        raise redirect('/asamblea/{0}'.format(asamblea.id))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.asamblea.asamblea')
    @validate(validators=dict(asamblea=validators.Int()))
    def default(self, asamblea):
        
        return dict(departamentos=model.Departamento.select(),
                    bancos=model.Banco.selectBy(asambleista=True),
                    asamblea=model.Asamblea.get(asamblea))
    
    def confirmacion(self, asamblea, afiliado):
        
        """Muestra una interfaz para confirmar los datos del afiliado antes de
        inscribir su participación en la asamblea"""
        
        banco = None
        deshabilitado = False
        asamblea = model.Asamblea.get(asamblea)
        inscripciones = model.Inscripcion.selectBy(asamblea=asamblea, afiliado=afiliado)
        msg = u"Inscribiendo en asamblea {0}".format(asamblea.nombre)
        
        if inscripciones.count() > 0:
            deshabilitado = True
            msg = u"Ya esta inscrito en asamblea {0}".format(asamblea.nombre)
        
        if afiliado.banco != None:
            banco = model.Banco.get(afiliado.banco)
        
        return deshabilitado, msg, afiliado, banco, asamblea

    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose(template='turboaffiliate.templates.asamblea.confirmar')
    @validate(validators=dict(asamblea=validators.Int(),
                              afiliado=validators.Int()))
    def confirmar(self, afiliado, asamblea):
        
        """Confirmar los datos de inscripción mediante el número de afiliación
        
        Permite confirmar los datos del afiliado antes de inscribirlo a la
        asamblea correspondiente, mostrando un mensaje acerca del estado de la
        inscripcion del afiliado en la asamblea"""
        
        afiliado = model.Affiliate.get(afiliado)
        deshabilitado, msg, afiliado, banco, asamblea = self.confirmacion(asamblea, afiliado)
        
        return dict(deshabilitado=deshabilitado, msg=msg,
                    afiliado=afiliado, banco=banco, asamblea=asamblea,
                    bancos=model.Banco.selectBy(asambleista=True), 
                    departamentos=model.Departamento.select())
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose(template='turboaffiliate.templates.asamblea.confirmar')
    @validate(validators=dict(asamblea=validators.Int(),
                              identidad=validators.UnicodeString()))
    def confirmarIdentidad(self, identidad, asamblea):
        
        """Confirmar los datos de inscripción mediante la identidad
        
        Permite confirmar los datos del afiliado antes de inscribirlo a la
        asamblea correspondiente, mostrando un mensaje acerca del estado de la
        inscripcion del afiliado en la asamblea"""
        
        afiliado = model.Affiliate.selectBy(cardID=identidad).limit(1).getOne()
        deshabilitado, msg, afiliado, banco, asamblea = self.confirmacion(asamblea, afiliado)
        
        return dict(deshabilitado=deshabilitado, msg=msg,
                    afiliado=afiliado,banco=banco, asamblea=asamblea,
                    bancos=model.Banco.selectBy(asambleista=True), 
                    departamentos=model.Departamento.select())
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(asamblea=validators.Int(),
                              afiliado=validators.Int()))
    def inscribir(self, afiliado, asamblea):
        
        asamblea = model.Asamblea.get(asamblea)
        
        kw = dict()
        afiliado = model.Affiliate.get(afiliado)
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Inscrito afiliado {0} en asamblea {1}".format(
                                                                afiliado.id,
                                                                asamblea.id)
        model.Logger(**log)
        
        kw['afiliado'] = afiliado
        kw['asamblea'] = asamblea
        kw['viatico'] = model.Viatico.selectBy(asamblea=asamblea,
                        municipio=afiliado.municipio).limit(1).getOne()
        
        model.Inscripcion(**kw)
        
        flash(inscripcionRealizada(afiliado))
        
        raise redirect('/asamblea/inscripcion/{0}'.format(asamblea.id))
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(afiliado=validators.Int(),
                              banco=validators.Int(),
                              departamento=validators.Int(),
                              cuenta=validators.UnicodeString(),
                              asamblea=validators.Int(),
                              municipio=validators.Int()))
    def corregir(self, afiliado, asamblea, departamento, banco, cuenta,
                 municipio):
        
        kw = dict()
        afiliado = model.Affiliate.get(afiliado)
        asamblea = model.Asamblea.get(asamblea)
        
        departamento = model.Departamento.get(departamento)
        afiliado.departamento = departamento
        afiliado.municipio = model.Municipio.get(municipio)
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Inscrito afiliado {0} en asamblea {1}".format(
                                                                afiliado.id,
                                                                asamblea.id)
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
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(afiliado=validators.Int(),
                              departamento=validators.Int(),
                              asamblea=validators.Int(),
                              municipio=validators.Int()))
    def corregirDepto(self, afiliado, asamblea, departamento, municipio):
        
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
    
    @identity.require(identity.All(identity.in_group('admin'),
                                   identity.not_anonymous()))
    @expose()
    def ingresar(self):
        
        ninguno = model.Municipio.get(299)
        ndepto = model.Departamento.get(19)
        
        afiliados = model.Affiliate.selectBy(municipio=ninguno)
        
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
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose(template='turboaffiliate.templates.asamblea.departamento')
    @validate(validators=dict(departamento=validators.Int(),
                              asamblea=validators.Int()))
    def departamento(self, departamento, asamblea):
        
        """Muestra un reporte de los montos de en pago"""
        
        clause1 = model.Inscripcion.q.viatico == model.Viatico.q.id
        clause2 = model.Viatico.q.municipio == model.Municipio.q.id
        clause3 = model.Municipio.q.departamento == model.Departamento.q.id
        clause4 = model.Departamento.q.id == departamento
        clause5 = model.Inscripcion.q.asamblea == asamblea
        anded = AND(clause1, clause2, clause3, clause4, clause5)
        select = Select([model.Municipio.q.nombre,
                         func.COUNT(model.Inscripcion.q.id),
                         func.SUM(model.Viatico.q.monto)],
                        staticTables=['inscripcion', 'departamento',
                                      'municipio', 'viatico'],
                        where=anded,
                        groupBy='municipio.id')
        query = model.__connection__.sqlrepr(select)
        municipios = model.__connection__.queryAll(query)
        
        return dict(municipios=municipios, asamblea=model.Asamblea.get(asamblea),
                    departamento=model.Departamento.get(departamento))
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose(template='turboaffiliate.templates.asamblea.ach')
    @validate(validators=dict(banco=validators.Int(),
                              asamblea=validators.Int()))
    def ach(self, asamblea, banco):
        
        clause1 = model.Inscripcion.q.asamblea == asamblea
        clause2 = model.Inscripcion.q.afiliado == model.Affiliate.q.id
        clause3 = model.Inscripcion.q.viatico == model.Viatico.q.id
        clause4 = model.Inscripcion.q.enviado == False
        clause5 = model.Affiliate.q.banco != banco
        
        select = Select([model.Affiliate.q.banco,
                         model.Affiliate.q.cuenta,
                         model.Viatico.q.monto],
                        where=AND(clause1, clause2, clause3, clause4, clause5),
                        orderBy=model.Affiliate.q.banco)
        query = model.__connection__.sqlrepr(select)
        pagos = model.__connection__.queryAll(query)
        
        asamblea = model.Asamblea.get(asamblea)
        banco = model.Banco.get(banco)
        
        return dict(pagos=pagos, asamblea=asamblea, banco=banco)
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose(template='turboaffiliate.templates.asamblea.ach')
    @validate(validators=dict(banco=validators.Int(),
                              asamblea=validators.Int()))
    def achBanco(self, asamblea):
        
        clause1 = model.Inscripcion.q.asamblea == asamblea
        clause2 = model.Inscripcion.q.afiliado == model.Affiliate.q.id
        clause3 = model.Inscripcion.q.viatico == model.Viatico.q.id
        clause4 = model.Inscripcion.q.enviado == False
        clause5 = model.Affiliate.q.banco == banco
        
        select = Select([model.Affiliate.q.banco,
                         model.Affiliate.q.cuenta,
                         model.Viatico.q.monto],
                        where=AND(clause1, clause2, clause3, clause4, clause5),
                        orderBy=model.Affiliate.q.banco)
        query = model.__connection__.sqlrepr(select)
        pagos = model.__connection__.queryAll(query)
        
        asamblea = model.Asamblea.get(asamblea)
        banco = model.Banco.get(banco)
        
        return dict(pagos=pagos, asamblea=asamblea, banco=banco)
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose(template='turboaffiliate.templates.asamblea.planilla')
    @validate(validators=dict(banco=validators.Int(),
                              asamblea=validators.Int()))
    def planilla(self, asamblea, banco):
        
        clause1 = model.Inscripcion.q.asamblea == asamblea
        clause2 = model.Inscripcion.q.afiliado == model.Affiliate.q.id
        clause3 = model.Inscripcion.q.viatico == model.Viatico.q.id
        clause4 = model.Inscripcion.q.enviado == False
        clause5 = model.Affiliate.q.banco == banco
        
        select = Select([model.Affiliate.q.cuenta,
                         model.Viatico.q.monto],
                        where=AND(clause1, clause2, clause3, clause4, clause5),
                        orderBy=model.Affiliate.q.banco)
        query = model.__connection__.sqlrepr(select)
        pagos = model.__connection__.queryAll(query)
        
        asamblea = model.Asamblea.get(asamblea)
        banco = model.Banco.get(banco)
        
        return dict(pagos=pagos, asamblea=asamblea, banco=banco)
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(asamblea=validators.Int(),
                              enviado=validators.Bool(),
                              municipio=validators.Int()))
    def asistentes(self, asamblea, municipio, enviado):
        
        asamblea = model.Asamblea.get(asamblea)
        municipio = model.Municipio.get(municipio)
        
        viaticos = model.Viatico.selectBy(asamblea=asamblea, municipio=municipio,
                                          enviado=enviado)
        
        return dict(asamblea=asamblea, municipio=municipio, viaticos=viaticos)
    
    @identity.require(identity.All(identity.in_any_group('admin'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(asamblea=validators.Int()))
    def enviarMasa(self, asamblea):
        
        update = Update('inscripcion',
                        values={'enviado':True,'envio':date.today()},
                        where='asamblea_id={0} and enviado=false'.format(asamblea))
        query = model.__connection__.sqlrepr(update)
        model.__connection__.query(query)
        asamblea = model.Asamblea.get(asamblea)
        
        flash(u'Marcadas como enviadas todas las Inscripciones de {0}'.format(asamblea.nombre))
        
        raise redirect('/asamblea')
