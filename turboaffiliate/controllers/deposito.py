#-*- coding:utf-8 -*-
#
# deposito.py
# This file is part of TurboAffiliate
#
# Copyright (C) 2011 Carlos Flores
#
# TurboAffiliate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# TurboAffiliate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TurboAffiliate; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, 
# Boston, MA  02110-1301  USA

from turbogears import (controllers, redirect, identity, expose, validate,
                        validators)
from turboaffiliate import model
from decimal import Decimal
from sqlobject.sqlbuilder import OR, AND
from datetime import date

class Deposito(controllers.Controller):
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.deposito.index')
    def index(self):
        
        return dict()
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.deposito.deposito')
    @validate(validators=dict(deposito=validators.Int()))
    def default(self, deposito):
        
        return dict(deposito=model.Deposito.get(deposito))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.deposito.agregar')
    @validate(validators=dict(afiliado=validators.Int()))
    def afiliacion(self, afiliado):
        
        afiliados = list()
        afiliados.append(model.Affiliate.get(afiliado))
        
        return dict(afiliados=afiliados, dia=date.today())
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.deposito.agregar')
    @validate(validators=dict(nombre=validators.UnicodeString()))
    def nombre(self, nombre):
        
        afiliados = model.Affiliate.select(OR(model.Affiliate.q.firstName.contains(nombre),
                                             model.Affiliate.q.lastName.contains(nombre)))
        
        return dict(afiliados=afiliados, dia=date.today())
    
    @expose('json')
    @identity.require(identity.not_anonymous())
    @validate(validators=dict(afiliado=validators.Int(),
                              concepto=validators.UnicodeString(),
                              banco=validators.Int(),
                              monto=validators.UnicodeString(),
                              fecha=validators.DateTimeConverter(format='%d/%m/%Y'),
                              sistema=validators.DateTimeConverter(format='%d/%m/%Y')))
    def agregarAportaciones(self, afiliado, banco, sistema, **kw):
        
        """Permite registrar un deposito que corresponde a pago de aportaciones"""
        
        kw['monto'] = Decimal(kw['monto'].replace(',', '')) 
        kw['afiliado'] = model.Affiliate.get(afiliado)
        kw['banco'] = model.Banco.get(banco)
        deposito = model.Deposito(**kw)
        kw['afiliado'].pay_cuota(sistema.year, sistema.month)
        
        return dict(mensaje=u"Se registró el depósito al afiliado {0}".format(deposito.afiliado.id))
    
    @expose('json')
    @identity.require(identity.not_anonymous())
    @validate(validators=dict(afiliado=validators.Int(),
                              concepto=validators.UnicodeString(),
                              banco=validators.Int(),
                              monto=validators.UnicodeString(),
                              fecha=validators.DateTimeConverter(format='%d/%m/%Y'),
                              sistema=validators.DateTimeConverter(format='%d/%m/%Y')))
    def agregarPrestamo(self, afiliado, banco, sistema, **kw):
        
        """Permite registrar un depósito que corresponde a pago de préstamos"""
        
        kw['monto'] = Decimal(kw['monto'].replace(',', '')) 
        afiliado = kw['afiliado'] = model.Affiliate.get(afiliado)
        kw['banco'] = model.Banco.get(banco)
        banco = kw['cuenta'].banco 
        deposito = model.Deposito(**kw)
        monto = kw['monto']
        while monto > model.Zero:
            
            for prestamo in afiliado.loans:
                
                pago = prestamo.get_payment()
                if monto < pago:
                    pago = monto
                    monto = model.Zero
                else:
                    monto -= pago
                
                prestamo.pagar(pago, banco.nombre, sistema)
        
        return dict(mensaje=u"Se registró el depósito al afiliado {0}".format(deposito.afiliado.id))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.deposito.reporte')
    @validate(validators=dict(inicio=validators.DateTimeConverter(format='%d/%m/%Y'),
                              final=validators.DateTimeConverter(format='%d/%m/%Y')))
    def reporte(self, inicio, fin):
        
        return dict(depositos=model.Deposito.select(AND(model.Loan.q.startDate>=inicio,
                                              model.Loan.q.startDate<=fin)))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.deposito.reporteCuenta')
    @validate(validators=dict(banco=validators.Int(),
                              inicio=validators.DateTimeConverter(format='%d/%m/%Y'),
                              final=validators.DateTimeConverter(format='%d/%m/%Y')))
    def reporteCuenta(self, inicio, fin, banco):
        
        banco = model.Banco.get(banco)
        
        return dict(depositos=model.Deposito.select(AND(model.Deposito.q.startDate>=inicio,
                                              model.Deposito.q.startDate<=fin,
                                              model.Deposito.q.banco==banco)))
    
    @expose()
    @identity.require(identity.not_anonymous())
    @validate(validators=dict(deposito=validators.Int()))
    def eliminar(self, deposito):
        
        deposito = model.Deposito.get(deposito)
        deposito.destroySelf()
        
        raise redirect('/deposito')
