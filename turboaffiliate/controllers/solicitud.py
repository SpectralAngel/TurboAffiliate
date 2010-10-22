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

from turbogears import controllers, flash, redirect, identity
from turbogears import expose, validate, validators
from turboaffiliate import model
from decimal import Decimal

class Solicitud(controllers.Controller):
    
    @expose()
    @validate(validators=dict(affiliate=validators.Int(), periodo=validators.Int(),
                              entrega=validators.DateTimeConverter(format='%d/%m/%Y'),
                              ingreso=validators.DateTimeConverter(format='%d/%m/%Y'),
                              monto=validators.String()))
    @identity.require(identity.not_anonymous())
    def agregar(self, affiliate, **kw):
        
        kw['affiliate'] = model.Affiliate.get(affiliate)
        kw['monto'] = Decimal(kw['monto'])
        model.Solicitud(**kw)
        
        flash('Agregada la solicitud')
        
        raise redirect('/affiliate/{0}'.format(kw['affiliate'].id))
    
    @expose()
    @validate(validators=dict(solicitud=validators.Int()))
    def convertir(self, solicitud):
        
        solicitud = model.Solicitud.get(solicitud)
        prestamo = solicitud.prestamo(identity.current.user)
        solicitud.destroySelf()
        
        raise redirect('/loan/{0}'.format(prestamo.id))
    
    @expose()
    @identity.require(identity.not_anonymous())
    @validate(validators=dict(solicitud=validators.Int()))
    def eliminar(self, solicitud):
        
        solicitud = model.Solicitud.get(solicitud)
        affiliate = solicitud.affiliate
        solicitud.destroySelf()
        
        raise redirect('/affiliate/{0}'.format(affiliate.id))
    
    @expose(template='turboaffiliate.templates.solicitud.dia')
    @identity.require(identity.not_anonymous())
    @validate(validators=dict(dia=validators.DateTimeConverter(format='%d/%m/%Y')))
    def dia(self, dia):
        
        solicitudes = model.Solicitud.selectBy(entrega=dia)
        
        return dict(solicitudes=solicitudes, dia=dia)
