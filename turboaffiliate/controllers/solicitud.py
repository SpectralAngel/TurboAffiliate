#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# affiliate.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2007, 2008, 2009 Carlos Flores <cafg10@gmail.com>
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
from decimal import *
from datetime import date, datetime

class Solicitud(controllers.Controller):
    
    @expose()
    @validate(validators=dict(affiliate=validators.Int(), periodo=validators.Int(),
                              entrega=validators.DateTimeConverter(format='%Y-%m-%d'),
                              ingreso=validators.DateTimeConverter(format='%Y-%m-%d'),
                              monto=validators.String()))
    def agregar(self, affiliate, **kw):
        
        kw['affiliate'] = model.Affiliate.get(affiliate)
        kw['monto'] = Decimal(kw['monto'])
        model.Solicitud(**kw)
        
        raise redirect('/affiliate/%s' % kw['affiliate'].id)
    
    @expose()
    @validate(validators=dict(solicitud=validators.Int()))
    def eliminar(self, solicitud):
        
        solicitud = model.Solicitud.get(solicitud)
        affiliate = solicitud.affiliate
        solicitud.destroySelf()
        
        raise redirect('/loan/%s' % affiliate.id)
