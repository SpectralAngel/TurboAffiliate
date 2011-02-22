# -*- coding: utf8 -*-
#
# extra.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2008 - 2011 Carlos Flores <cafg10@gmail.com>
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

from turbogears import (controllers, redirect, identity,expose, validate,
                        validators, flash)
from turboaffiliate import model
from decimal import Decimal

class Extra(controllers.Controller):
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.extra.index')
    def index(self):
        return dict(accounts=model.Account.select())
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int(),
                              account=validators.Int(),
                              months=validators.Int(),
                              retrasada=validators.Bool(),
                              amount=validators.String()))
    def save(self, affiliate, account, **kw):
        
        kw['affiliate'] = model.Affiliate.get(affiliate)
        kw['account'] = model.Account.get(account)
        kw['amount'] = Decimal(kw['amount'].replace(',', ''))
        model.Extra(**kw)
        raise redirect('/affiliate/{0}'.format(kw['affiliate'].id))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(account=validators.Int(), months=validators.Int(),
                              first=validators.Int(), last=validators.Int(),
                              amount=validators.Number()))
    def many(self, first, last, account, **kw):
        
        kw['account'] = model.Account.get(account)
        for n in range(first, last +1):
            kw['affiliate'] = model.Affiliate.get(n)
            kw['amount'] = Decimal(kw['amount'].replace(',', ''))
            model.Extra(**kw)
        raise redirect('/affiliate')
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(code=validators.Int()))
    def delete(self, code):
        
        extra = model.Extra.get(code)
        affiliate = extra.affiliate
        extra.destroySelf()
        
        raise redirect('/affiliate/{0}'.format(affiliate.id))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(account=validators.Int(), months=validators.Int(),
                              payment=validators.String(),
                              amount=validators.String()))
    def payment(self, payment, account, amount, **kw):
        
        kw['account'] = model.Account.get(account)
        kw['amount'] = Decimal(kw['amount'])
        
        afiliados = model.Affiliate.selectBy(payment=payment)
        
        for afiliado in afiliados:
            
            kw['affiliate'] = afiliado
            model.Extra(**kw)
        
        flash(u'Se agrego la deducción a los afiliados')
        
        raise redirect('/affiliate/extra')
    
    @identity.require(identity.not_anonymous())
    @expose('json')
    @validate(validators=dict(extra=validators.Int(),
                              day=validators.DateTimeConverter(format='%d/%m/%Y')))
    def pagarPlanilla(self, extra, day):
    
        extra = model.Extra.get(extra)
        pago = extra.amount
        extra.act(day=day)
        
        return dict(pago=pago)
