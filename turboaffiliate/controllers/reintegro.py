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
    @validate(validators=dict(afiliado=validators.Int(),cuenta=validators.Int(),
                              emision=validators.DateTimeConverter(format='%d/%m/%Y'),
                              motivo=validators.UnicodeString(),
                              monto=validators.UnicodeString()))
    def agregar(self, afiliado, cuenta, **kw):
        
        """Ingresa un nuevo reintegro a la base de datos"""
        
        kw['afiliado'] = model.Affiliate.get(afiliado)
        kw['cuenta'] = model.Account.get(cuenta)
        kw['monto'] = Decimal(kw['monto'])
        
        model.Reintegro(**kw)
        
        flash("Se agrego el reintegro al afiliado")
        
        raise redirect(url('/reintegro'))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.reintegro.afiliado')
    @validate(validators=dict(afiliado=validators.Int()))
    def afiliado(self, afiliado): 
        
        return dict(afiliado=model.Affiliate.get(afiliado), cuenta=model.Account.get())
    