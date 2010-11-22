#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# cuota.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2008 Carlos Flores <cafg10@gmail.com>
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

from turbogears import (controllers, expose, identity, redirect, validate,
                        validators)
from turboaffiliate import model
from datetime import date

class Cuota(controllers.Controller):
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.cuota.affiliate')
    @validate(validators=dict(affiliate=validators.Int()))
    def default(self, affiliate):
        
        return dict(affiliate=model.Affiliate.get(affiliate), day=date.today())
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int(),start=validators.Int(),
                              end=validators.Int()))
    def fill(self, affiliate, start, end):
        
        affiliate = model.Affiliate.get(affiliate)
        
        for n in range(start, end + 1):
            [affiliate.pay_cuota(n, month) for month in range(1, 13)]
        
        raise redirect('/affiliate/cuota/{0}'.format(affiliate.id))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(id=validators.Int()))
    def remove(self, id):
        
        table = model.CuotaTable.get(id)
        affiliate = table.affiliate
        table.destroySelf()
        raise redirect('/affiliate/cuota/{0}'.format(affiliate.id))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.cuota.edit')
    @validate(validators=dict(code=validators.Int()))
    def edit(self, code):
        
        "Muestra el formulario de edicion de un año de aportaciones"
        
        return dict(table=model.CuotaTable.get(code))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(id=validators.Int(),
                              month1=validators.Bool(),
                              month2=validators.Bool(),
                              month3=validators.Bool(),
                              month4=validators.Bool(),
                              month5=validators.Bool(),
                              month6=validators.Bool(),
                              month7=validators.Bool(),
                              month8=validators.Bool(),
                              month9=validators.Bool(),
                              month10=validators.Bool(),
                              month11=validators.Bool(),
                              month12=validators.Bool()))
    def change(self, id, **kw):
        
        table = model.CuotaTable.get(id)
        for n in range(1, 13):
            try:
                setattr(table, "month{0}".format(n), kw["month{0}".format(n)])
            except KeyError:
                setattr(table, "month{0}".format(n), False)
        
        log = dict()
        log['user'] = identity.current.user
        log['action'] = u"Cambio en aportaciones anio {0} afiliado {1}".format(table.year, table.affiliate.id)
        model.Logger(**log)
        
        raise redirect('/affiliate/cuota/{0}'.format(table.affiliate.id))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int(),year=validators.Int()))
    def addYear(self, affiliate, year):
        
        affiliate = model.Affiliate.get(affiliate)
        affiliate.complete(year)
        
        raise redirect('/affiliate/cuota/{0}'.format(affiliate.id))
    
    @identity.require(identity.not_anonymous())
    @expose('json')
    @validate(validators=dict(afiliado=validators.Int(),cuenta=validators.Int(),
                              day=validators.DateTimeConverter(format='%d/%m/%Y')))
    def pagoPlanilla(self, afiliado, cuenta, day):
        
        affiliate = model.Affiliate.get(afiliado)
        cuenta = model.Account.get(cuenta)
        affiliate.pay_cuota(day.year, day.month)
        
        deduccion = dict()
        deduccion['account'] = cuenta
        deduccion['month'] = day.month
        deduccion['year'] = day.year
        deduccion['affiliate'] = affiliate
        deduccion['amount'] = affiliate.get_cuota(day)
        model.Deduced(**deduccion)
        
        log = dict()
        log['user'] = identity.current.user
        log['action'] = u"Pago por Planilla de cuota de aportaciones afiliado {0}".format(affiliate.id)
        model.Logger(**log)
        
        return dict(pago=affiliate.get_monthly())
