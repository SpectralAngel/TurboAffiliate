#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# observacion.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2009,2010 Carlos Flores <cafg10@gmail.com>
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

from turbogears import controllers, redirect, url
from turbogears import expose, validate, validators
from turboaffiliate import model

class Observacion(controllers.Controller):
    
    def index(self):
        
        return dict()
    
    @expose()
    @validate(validators=dict(affiliate=validators.Int(),
                              texto=validators.String()))
    def add(self, affiliate, texto):
        
        affiliate = model.Affiliate.get(affiliate)
        model.Observacion(affiliate=affiliate, texto=texto)
        
        raise redirect('/affiliate/{0}'.format(affiliate.id))
