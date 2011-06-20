#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# account.py
# This file is part of TurboAffiliate
#
# Copyright © 2007 - 2010 Carlos Flores <cafg10@gmail.com>
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

from turboaffiliate import model
from turbogears import (controllers, identity, expose, validate, validators,
                        redirect, flash)

class Account(controllers.Controller):
    
    """Controller for Accounts in Affiliate Program"""
    
    @identity.require(identity.not_anonymous())
    #@expose(template="turboaffiliate.templates.account.index")
    def index(self):
        return dict()
    
    @identity.require(identity.not_anonymous())
    #@expose(template="turboaffiliate.templates.account.account")
    @expose("json")
    @validate(validators=dict(code=validators.Int()))
    def default(self, code):
    
        account = model.Account.get(code)
        return dict(account=account)
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.account.add")
    def add(self):
        return dict()
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(code=validators.Int(),name=validators.String()))
    def save(self, **kw):
        
        account = model.Account(**kw)
        flash(u"La cuenta ha sido grabada")
        
        log = dict()
        log['user'] = identity.current.user
        log['action'] = u"Agregada cuenta {0} {1}".format(account.id, account.name)
        model.Logger(**log)
        raise redirect('/account/{0}'.format(account.id))
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose(template="turboaffiliate.templates.account.retrasada")
    def retrasada(self):
        
        return dict(accounts=model.Account.select())
    
    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(mes=validators.Int(), anio=validators.Int(),
                              account=validators.Int()))
    def agregarRetrasada(self, account, **kw):
        
        account = model.Account.get(account)
        kw['account'] = account
        retrasada = model.CuentaRetrasada(**kw)
        retrasada.account = account
        
        flash(u"La cuenta para restradas ha sido grabada")
        raise redirect('/account/retrasada')
