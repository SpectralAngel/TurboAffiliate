# -*- coding: utf8 -*-
#
# json.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2010, 2011 Carlos Flores <cafg10@gmail.com>
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

from turbogears import controllers, expose, validate, validators
from turboaffiliate import model

class JSON(controllers.Controller):
    
    @expose('json')
    def departamentos(self):
        
        """Regresa una lista de departamentos en formato JSON"""
        
        return dict(departamentos=model.Departamento.select())
    
    @expose('json')
    @validate(validators=dict(departamento=validators.Int()))
    def municipios(self, departamento):
        
        """Regresa una lista de municipios en fromato JSON"""
        
        departamento = model.Departamento.get(departamento)
        
        return dict(municipios=model.Municipio.selectBy(departamento=departamento))
    
    @expose('json')
    def cuentas(self):
        
        """Muestra una lista de las cuentas del sistema"""
        
        return dict(cuentas=model.Account.select())
    
    @expose('json')
    def cotizacion(self):
        
        """Muestra una lista de los métodos de cotización"""
        
        return dict(cotizaciones=model.Cotizacion.select())
    
    @expose('json')
    def bancos(self):
        
        """Muestra una lista con todos los bancos disponibles"""
        
        return dict(bancos=model.Banco.selectBy(depositable=True))
    
    @expose('json')
    def jubilados(self):
        
        return dict(cotizaciones=model.Cotizacion.selectBy(jubilados=True))
