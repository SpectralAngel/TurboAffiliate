#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# affiliate.py
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

from turbogears import controllers, flash, redirect, identity, url
from turbogears import expose, validate, validators
from turboaffiliate import model
from decimal import Decimal

class Reintegro(controllers.Controller):
    
    """Permite realizar acciones sobre los Reintegros"""
    
    @expose()
    @identity.require(identity.not_anonymous())
    @validate(validators=dict(affiliate=validators.Int(),cuenta=validators.Int(),
                              emision=validators.DateTimeConverter(format='%d/%m/%Y'),
                              motivo=validators.UnicodeString(),
                              cheque=validators.UnicodeString(),
                              planilla=validators.UnicodeString(),
                              monto=validators.UnicodeString()))
    def agregar(self, affiliate, cuenta, **kw):
        
        """Ingresa un nuevo reintegro a la base de datos"""
        
        kw['affiliate'] = model.Affiliate.get(affiliate)
        kw['cuenta'] = model.Account.get(cuenta)
        kw['monto'] = Decimal(kw['monto'])
        
        reintegro = model.Reintegro(**kw)
        
        flash("Se agrego el reintegro al afiliado")
        
        raise redirect(url('/reintegro/afiliado/%' % reintegro.affiliate.id))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.reintegro.afiliado')
    @validate(validators=dict(afiliado=validators.Int()))
    def afiliado(self, afiliado): 
        
        """Muestra el estado de cuenta de reintegros de un afiliado"""
        
        return dict(afiliado=model.Affiliate.get(afiliado),
                    cuenta=model.Account.get(678),
                    formas=model.FormaPago.select())
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(reintegro=validators.Int()))
    def eliminar(self, reintegro):
        
        """Elimina un reintegro"""
        
        reintegro = model.Reintegro.get(reintegro)
        
        afiliado = reintegro.afiliado
        
        reintegro.DestroySelf()
        
        raise redirect(url('/reintegro/afiliado/%s' % afiliado.id))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(reintegro=validators.Int(),forma=validators.Int(),
                              fecha=validators.DateTimeConverter(format='%d/%m/%Y')))
    def pagar(self, reintegro, forma, fecha):
        
        """Registra un pago de reintegro"""
        
        reintegro = model.Reintegro.get(reintegro)
        
        reintegro.formaPago = model.FormaPago.get(forma)
        reintegro.pagado = True
        reintegro.cancelacion = fecha
        
        flash("Se ha pagado el Reintegro")
        
        raise redirect(url('/reintegro/afiliado/%s' % reintegro.affiliate.id))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.reintegro.pagados')
    @validate(validators=dict(inicio=validators.DateTimeConverter(format='%d/%m/%Y'),
                              fin=validators.DateTimeConverter(format='%d/%m/%Y')))
    def pagados(self, inicio, fin):
        
        """Muestra los reintegros pagados durante un periodo"""
        
        query = "reintegro.cancelacion >= %s and reintregro.cancelacion <= %s and pagado = true" (inicio, fin)
        
        return dict(reintegros=model.Reintegro.select(query))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.reintegro.emision')
    @validate(validators=dict(inicio=validators.DateTimeConverter(format='%d/%m/%Y'),
                              fin=validators.DateTimeConverter(format='%d/%m/%Y')))
    def emision(self, inicio, fin):
        
        """Muestra los reintegros emitidos en un periodo"""
        
        query = "reintegro.emision >= %s and reintregro.emision <= %s" (inicio, fin)
        
        return dict(reintegros=model.Reintegro.select(query))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.reintegro.cobros')
    def cobros(self):
        
        """Muestra los cobros a efectuar por concepto de reintegros"""
        
        return dict(reintegros=model.Reintegro.selectBy(pagado=False))
