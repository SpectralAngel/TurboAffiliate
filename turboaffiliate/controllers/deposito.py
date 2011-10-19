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
    
    """Permite registrar depósitos que los afiliados han efectuado en una
    institución bancaria"""
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.deposito.index')
    def index(self):
        
        return dict()
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.error')
    def error(self, tg_errors=None):
        
        if tg_errors:
            errors = [(param,inv.msg,inv.value) for param, inv in
                      tg_errors.items()]
            return dict(errors=errors)
        
        return dict(errors=u"Desconocido")
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.deposito.deposito')
    @validate(validators=dict(deposito=validators.Int()))
    def default(self, deposito):
        
        return dict(deposito=model.Deposito.get(deposito))
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose(template='turboaffiliate.templates.deposito.agregar')
    @validate(validators=dict(afiliado=validators.Int()))
    def afiliacion(self, afiliado):
        
        """Muestra la interfaz de registro de depositos mediante el número de
        afiliación
        
        :param afiliado: El número de afiliación a mostrar
        """
        
        afiliados = list()
        afiliados.append(model.Affiliate.get(afiliado))
        
        return dict(afiliados=afiliados, dia=date.today())
    
    @expose(template='turboaffiliate.templates.deposito.agregar')
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @validate(validators=dict(nombre=validators.UnicodeString()))
    def nombre(self, nombre):
        
        """Muestra la interfaz de registro de depositos mediante el nombre o los
        apellidos del afiliado
        
        :param nombre: El nombre o apellidos del afiliado a buscar
        """
        
        afiliados = model.Affiliate.select(OR(
                                model.Affiliate.q.firstName.contains(nombre),
                                model.Affiliate.q.lastName.contains(nombre)))
        
        return dict(afiliados=afiliados, dia=date.today())
    
    @expose('json')
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @validate(validators=dict(afiliado=validators.Int(),
                              concepto=validators.UnicodeString(),
                              banco=validators.Int(),
                              monto=validators.UnicodeString(),
                              fecha=validators.DateTimeConverter(
                                                            format='%d/%m/%Y'),
                              sistema=validators.DateTimeConverter(
                                                            format='%d/%m/%Y')))
    def agregarAportaciones(self, afiliado, banco, sistema, **kw):
        
        """Permite registrar un deposito que corresponde a pago de aportaciones
        
        :param afiliado: El número de afiliación
        :param banco:    El código del banco en que se efectuó el depósito
        :param sistema:  La fecha en la que se esta registrando el pago
        :param kw:       Incluye el resto de los datos del depósito
        """
        
        kw['monto'] = Decimal(kw['monto'].replace(',', '')) 
        kw['afiliado'] = model.Affiliate.get(afiliado)
        kw['banco'] = model.Banco.get(banco)
        deposito = model.Deposito(**kw)
        kw['afiliado'].pay_cuota(sistema.year, sistema.month)
        
        return dict(mensaje=u"Se registró el depósito al afiliado {0}".format(
                                                        deposito.afiliado.id))
    
    @expose('json')
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @validate(validators=dict(prestamo=validators.Int(),
                              concepto=validators.UnicodeString(),
                              banco=validators.Int(),
                              monto=validators.UnicodeString(),
                              fecha=validators.DateTimeConverter(
                                                            format='%d/%m/%Y'),
                              sistema=validators.DateTimeConverter(
                                                            format='%d/%m/%Y')))
    def agregarPrestamo(self, banco, sistema, prestamo, **kw):
        
        """Permite registrar un depósito que corresponde a pago de préstamos
        
        :param prestamo: El número de préstamo que se va a pagar
        :param banco:    El código del banco en que se efectuó el depósito
        :param sistema:  La fecha en la que se esta registrando el pago
        :param kw:       Incluye el resto de los datos del depósito
        """
        
        prestamo = model.Loan.get(prestamo)
        kw['monto'] = Decimal(kw['monto'].replace(',', '')) 
        kw['afiliado'] = prestamo.affiliate
        kw['banco'] = model.Banco.get(banco)
        banco = kw['banco']
        deposito = model.Deposito(**kw)
        monto = kw['monto']
        prestamo.pagar(amount=monto, receipt=banco.nombre, day=sistema,
                       remove=False)
        
        return dict( mensaje=u"Se registró el depósito al afiliado {0}".format(
                                                        deposito.afiliado.id))
    
    @expose('json')
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @validate(validators=dict(afiliado=validators.Int(),
                              banco=validators.Int(),
                              monto=validators.UnicodeString(),
                              fecha=validators.DateTimeConverter(
                                                        format='%d/%m/%Y'),
                              cuenta=validators.Int()))
    def agregarOtros(self, afiliado, banco, cuenta, **kw):
        
        """Permite registrar un deposito que corresponde a pago de aportaciones
        
        :param afiliado: El número de afiliación
        :param banco:    El código del banco en que se efectuó el depósito
        :param kw:       Diccionario que incluye el resto de los datos del
                         depósito
        """
        
        cuenta = model.Account.get(cuenta)
        kw['monto'] = Decimal(kw['monto'].replace(',', ''))
        kw['afiliado'] = model.Affiliate.get(afiliado)
        kw['banco'] = model.Banco.get(banco)
        kw['concepto'] = cuenta.name
        deposito = model.Deposito(**kw)
        
        return dict(mensaje=u"Se registró el depósito al afiliado {0}".format(
                                                        deposito.afiliado.id))
    
    @expose('json')
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @validate(validators=dict(referencia=validators.UnicodeString(),
                              concepto=validators.UnicodeString(),
                              banco=validators.Int(),
                              monto=validators.UnicodeString(),
                              fecha=validators.DateTimeConverter(
                                                            format='%d/%m/%Y')))
    def agregarAnonimo(self, banco, **kw):
        
        """Permite registrar un deposito al que no se le puede encontrar
        afiliado"""
        
        kw['monto'] = Decimal(kw['monto'].replace(',', ''))
        kw['banco'] = model.Banco.get(banco)
        deposito = model.DepositoAnonimo(**kw)
        
        return dict(
            mensaje=u"Se registró el deposito con referencia {0}".format(
                                                        deposito.referencia))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.deposito.reporte')
    @validate(validators=dict(inicio=validators.DateTimeConverter(
                                                            format='%d/%m/%Y'),
                              final=validators.DateTimeConverter(
                                                           format='%d/%m/%Y')))
    def reporte(self, inicio, fin):
        
        return dict(depositos=model.Deposito.select(AND(
                                                    model.Loan.q.fecha>=inicio,
                                                    model.Loan.q.fecha<=fin)))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.deposito.reporteBanco')
    @validate(validators=dict(banco=validators.Int(),
                              inicio=validators.DateTimeConverter(
                                                             format='%d/%m/%Y'),
                              final=validators.DateTimeConverter(
                                                            format='%d/%m/%Y')))
    def reporteBanco(self, inicio, final, banco):
        
        banco = model.Banco.get(banco)
        
        return dict(depositos=model.Deposito.select(AND(
                                              model.Deposito.q.fecha>=inicio,
                                              model.Deposito.q.fecha<=final,
                                              model.Deposito.q.banco==banco)),
                                              banco=banco,inicio=inicio,
                                              final=final)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.deposito.reporteAnonimo')
    @validate(validators=dict(banco=validators.Int(),
                              inicio=validators.DateTimeConverter(
                                                            format='%d/%m/%Y'),
                              final=validators.DateTimeConverter(
                                                            format='%d/%m/%Y')))
    def reporteAnonimo(self, inicio, final, banco):
        
        banco = model.Banco.get(banco)
        
        return dict(depositos=model.DepositoAnonimo.select(AND(
                                        model.DepositoAnonimo.q.fecha>=inicio,
                                        model.DepositoAnonimo.q.fecha<=final,
                                        model.DepositoAnonimo.q.banco==banco)),
                                        banco=banco,inicio=inicio, final=final)
    
    @expose()
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @validate(validators=dict(deposito=validators.Int()))
    def eliminar(self, deposito):
        
        deposito = model.Deposito.get(deposito)
        deposito.destroySelf()
        
        raise redirect('/deposito')
    
    @expose()
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @validate(validators=dict(deposito=validators.Int()))
    def eliminarAnonimo(self, deposito):
        
        deposito = model.DepositoAnonimo.get(deposito)
        deposito.destroySelf()
        
        raise redirect('/deposito')
