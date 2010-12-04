#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# affiliate.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2007 - 2010 Carlos Flores <cafg10@gmail.com>
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

from turbogears import (controllers, flash, redirect, identity, expose,
                        validate, validators, error_handler)
from turboaffiliate import model
from turboaffiliate.controllers import cuota, extra, billing, deduced, observacion
from datetime import date
from sqlobject.sqlbuilder import OR, AND
from decimal import Decimal
import csv

class Affiliate(controllers.Controller):
    
    """Permite administrar la información de los afiliados"""
    
    cuota = cuota.Cuota()
    extra = extra.Extra()
    billing = billing.Billing()
    deduced = deduced.Deduced()
    observacion = observacion.Observacion()
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.index')
    def index(self):
        
        return dict(cuentas=model.Account.select())
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.error')
    def error(self, tg_errors=None):
        
        if tg_errors:
            errors = [(param,inv.msg,inv.value) for param, inv in
                      tg_errors.items()]
            return dict(errors=errors)
        
        return dict(errors=u"Desconocido")
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.affiliate')
    @validate(validators=dict(affiliate=validators.Int()))
    def default(self, affiliate):
        
        """Permite mostrar un afiliado mediante su numero de afiliación"""
        
        return dict(affiliate=model.Affiliate.get(affiliate),accounts=model.Account.select())
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(cardID=validators.String()))
    def card(self, cardID):
        
        affiliate = model.Affiliate.selectBy(cardID=cardID).limit(1).getOne()
        
        raise redirect('/affiliate/{0}'.format(affiliate.id))
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.search')
    @validate(validators=dict(cobro=validators.String()))
    def cobro(self, cobro):
        
        """Muestra un afiliado mediante su número de cobro de UPN o INPREMA"""
        
        return dict(result=model.Affiliate.selectBy(escalafon=cobro))
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.affiliate')
    @validate(validators=dict(carnet=validators.Int()))
    def carnet(self, carnet):
        
        """Permite utilizar un numero de afiliacion en un formulario"""
        
        raise redirect('/affiliate/{0}'.format(carnet))
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(
            cardID=validators.UnicodeString(),
            birthday=validators.DateTimeConverter(format='%d/%m/%Y'),
            escalafon=validators.UnicodeString(),
            phone=validators.UnicodeString(),
            birthPlace=validators.UnicodeString(),
            gender=validators.UnicodeString(),
            payment=validators.UnicodeString(),
            school=validators.UnicodeString(),
            school2=validators.UnicodeString(),
            inprema=validators.UnicodeString(),
            municipio=validators.Int(),
            departamento=validators.Int()
    ))
    def save(self, municipio, departamento, **kw):
        
        """Permite guardar los datos del afiliado"""
        
        municipio = model.Municipio.get(municipio)
        departamento = model.Departamento.get(departamento)
        
        if kw['cardID'] == '':
            flash(u'No se escribio un número de identidad')
            raise redirect('/affiliate')
        try:            
            affiliate = model.Affiliate.get(int(kw['affiliate']))
            
            # Logs del sistema
            log = dict()
            log['user'] = identity.current.user
            log['action'] = u"Modificado el afiliado {0}".format(affiliate.id)
            model.Logger(**log)
            
            del kw['affiliate']
            
            for key in kw:
                setattr(affiliate, key, kw[key])
            affiliate.departamento = departamento
            affiliate.municipio = municipio
            flash(u'¡El afiliado ha sido actualizado!')
        
        except KeyError:
            
            affiliate = model.Affiliate(**kw)
            affiliate.complete(date.today().year)
            affiliate.departamento = departamento
            affiliate.municipio = municipio
            
            log = dict()
            log['user'] = identity.current.user
            log['action'] = u"Agregado el afiliado {0}".format(affiliate.id)
            model.Logger(**log)
            
            flash(u'¡El afiliado ha sido guardado!')
        
        raise redirect('/affiliate/{0}'.format(affiliate.id))
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int()))
    def remove(self, affiliate):
        
        affiliate = model.Affiliate.get(affiliate)
        
        for loan in affiliate.loans:
            loan.remove()
        
        for cuota in affiliate.cuotaTables:
            cuota.destroySelf()
        
        affiliate.destroySelf()
        flash(u'El afiliado ha sido removido!')
        
        raise redirect('/affiliate')
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.search')
    @validate(validators=dict(name=validators.UnicodeString()))
    def search(self, name):
        
        if name == '':
            raise redirect('/affiliate')
        affiliates = model.Affiliate.select(OR(model.Affiliate.q.firstName.contains(name),
                                               model.Affiliate.q.lastName.contains(name)))
        return dict(result=affiliates)
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.search')
    @validate(validators=dict(cardID=validators.String()))
    def byCardID(self, cardID):
        
        """Permite buscar afiliados mediante número de identidad"""
        
        return dict(affiliates=model.Affiliate.selectBy(cardID=cardID))
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.report')
    @validate(validators=dict(departamento=validators.Int()))
    def departamento(self, departamento):
        
        departamento = model.Departamento.ge(departamento)
        
        affiliates = model.Affiliate.selectBy(departamento=departamento)
        count = affiliates.count()
        return dict(affiliates=affiliates,departamento=departamento,count=count)
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.card')
    @validate(validators=dict(affiliate=validators.UnicodeString()))
    def byRange(self, cardID):
        
        affiliates = model.Affiliate.select("affiliate.card_id like '%{0}%'".format(cardID))
        return dict(affiliates=affiliates, cardID=cardID, count=affiliates.count())
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.report')
    @validate(validators=dict(affiliate=validators.Int(),end=validators.Int(), begin=validators.Int()))
    def aList(self, begin, end):
        
        affiliates = model.Affiliate.select(AND(model.Affiliate.q.id>=begin,model.Affiliate.q.id<=end))
        return dict(affiliates=affiliates, count=affiliates.count())
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.affiliate')
    def last(self):
        
        return dict(affiliate=model.Affiliate.select(orderBy="-id").limit(1).getOne())
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int(), reason=validators.UnicodeString()))
    def deactivate(self, affiliate, reason):
        
        affiliate = model.Affiliate.get(affiliate)
        affiliate.active = False
        affiliate.reason = reason
        log = dict()
        affiliate.desactivacion = date.today()
        log['user'] = identity.current.user
        log['action'] = u"Desactivado el afiliado {0}".format(affiliate.id)
        model.Logger(**log)
        raise redirect('/affiliate/{0}'.format(affiliate.id))
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int(),
                              muerte=validators.DateTimeConverter(format='%d/%m/%Y')))
    def fallecimiento(self, affiliate, muerte):
        
        """Desactiva el Afiliado indicando la fecha de muerte y estableciendo la
        fecha de proceso con el día en que se ingresa el incidente"""
        
        affiliate = model.Affiliate.get(affiliate)
        affiliate.active = False
        affiliate.reason = "Fallecimiento"
        affiliate.muerte = muerte
        affiliate.desactivacion = date.today()
        log = dict()
        log['user'] = identity.current.user
        log['action'] = u"Afiliado {0} reportado como fallecido".format(affiliate.id)
        model.Logger(**log)
        raise redirect('/affiliate/{0}'.format(affiliate.id))
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int()))
    def activate(self, affiliate):
        
        affiliate = model.Affiliate.get(int(affiliate))
        affiliate.active = True
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Activado el afiliado {0}".format(affiliate.id)
        model.Logger(**log)
        raise redirect('/affiliate/{0}'.format(affiliate.id))
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.payment')
    @validate(validators=dict(how=validators.UnicodeString()))
    def payment(self, how):
        
        affiliates = model.Affiliate.selectBy(model.Affiliate.q.payment==how, orderBy="lastName")
        return dict(affiliates=affiliates, count=affiliates.count(), how=how)
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.age')
    @validate(validators=dict(joined=validators.Int(),age=validators.Int()))
    def age(self, joined, age):
        
        """Muestra los afiliados por edad hasta un determinado año de afiliacion
        
        :param joined:  El año máximo de afiliación
        :param age:     La edad de los afiliados a buscar
        """
        
        day = date.today().year - age
        afiliacion = date(joined + 1, 1, 1)
        affiliates = model.Affiliate.select(AND(model.Affiliate.q.birthday>=day,
                                                model.Affiliate.q.joined<=afiliacion))
        
        return dict(affiliates=affiliates)
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    @validate(validators=dict(start=validators.DateTimeConverter(format='%d/%m/%Y'),
                              end=validators.DateTimeConverter(format='%d/%m/%Y')))
    def byDate(self, start, end):
        
        affiliates = model.Affiliate.select(AND(model.Affiliate.q.joined>=start,
                                                model.Affiliate.q.joined<=end))
        return dict(affiliates=affiliates, start=start, end=end, show="Fecha de Afiliaci&oacute;n", count=affiliates.count())
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    @validate(validators=dict(town=validators.UnicodeString()))
    def byTown(self, town):
        
        affiliates = model.Affiliate.selectBy(town=town)
        return dict(affiliates=affiliates, show="Municipio", count=affiliates.count())
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    @validate(validators=dict(school=validators.UnicodeString(),state=validators.UnicodeString()))
    def bySchool(self, school, state):
        
        affiliates = model.Affiliate.select(OR(model.Affiliate.school==school,model.Affiliate.school2==school))
        affiliates = [a for a in affiliates if a.state == state]
        return dict(affiliates=affiliates, show=u"Instituto", count=len(affiliates))
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    def disabled(self):
        
        affiliates = model.Affiliate.selectBy(active=False)
        return dict(affiliates=affiliates, show="Inhabilitados", count=affiliates.count())
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    def all(self):
        
        affiliates = model.Affiliate.select()
        return dict(affiliates=affiliates, show="Todos", count=affiliates.count())
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.planilla')
    @validate(validators=dict(payment=validators.UnicodeString(),
                              prestamos=validators.Int(),
                              aportaciones=validators.Int(),
                              excedente=validators.Int(),
                              day=validators.DateTimeConverter(format='%d/%m/%Y')))
    def planilla(self, payment, day, aportaciones, prestamos, excedente):
        
        affiliates = model.Affiliate.select(model.Affiliate.q.payment==payment, orderBy="lastName")
        
        return dict(afiliados=affiliates, cotizacion=payment, excedente=excedente,
                    aportaciones=aportaciones, prestamos=prestamos,day=day)
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.debt')
    @validate(validators=dict(payment=validators.UnicodeString()))
    def debt(self, payment):
        
        affiliates = model.Affiliate.selectBy(payment=payment)
        return dict(affiliates=affiliates, show=payment, count=affiliates.count())
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    @validate(validators=dict(year=validators.Int()))
    def solvent(self, year):
        
        affiliates = model.Affiliate.select()
        affiliates = [affiliate for affiliate in affiliates if affiliate.multisolvent(year)]
        show = "Solventes al %s" % year
        return dict(affiliates=affiliates, show=show, count=len(affiliates))
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.year')
    def solventYear(self):
        
        years = dict()
        tables = model.CuotaTable.select()
        
        for table in tables:
            if table.all():
                if table.year in years:
                    years[table.year] += 1
                else:
                    years[table.year] = 1
        
        return dict(years=years)
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    def none(self):
        
        affiliates = model.Affiliate.selectBy(joined=None)
        show = "Sin Año de Afiliación"
        return dict(affiliates=affiliates, show=show, count=affiliates.count())
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    def noCard(self):
        
        affiliates = model.Affiliate.selectBy(cardID=None)
        show = "Sin Número de identidad"
        return dict(affiliates=affiliates, show=show, count=affiliates.count())
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int(),
                              jubilated=validators.DateTimeConverter(format='%d/%m/%Y'),
                              cobro=validators.Int()))
    def jubilar(self, affiliate, jubilated, cobro):
        
        affiliate = model.Affiliate.get(affiliate)
        affiliate.jubilated = jubilated
        affiliate.escalafon = str(cobro)
        affiliate.payment = "INPREMA"
        return self.default(affiliate.id)
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.delayed')
    @validate(validators=dict(payment=validators.String()))
    def delayed(self, payment):
        
        affiliates = model.Affiliate.selectBy(payment=payment)
        affiliates =[a for a in affiliates if a.get_delayed() != None]
        
        return dict(affiliates=affiliates,count=len(affiliates),payment=payment)
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.stateSchool')
    @validate(validators=dict(state=validators.UnicodeString()))
    def stateSchool(self, state):
        
        affiliates = model.Affiliate.selectBy(state=state)
        
        schools = dict()
        for affiliate in affiliates:
            if affiliate.school in schools:
                schools[affiliate.school].append(affiliate)
            else:
                schools[affiliate.school] = list()
                schools[affiliate.school].append(affiliate)
        
        return dict(state=state, schools=schools)
    
    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.solvencia')
    @validate(validators=dict(mes=validators.UnicodeString(),anio=validators.Int(),
                              afiliado=validators.Int()))
    def solvencia(self, afiliado, mes, anio):
        
        return dict(afiliado=model.Affiliate.get(afiliado),mes=mes,anio=anio,
                    dia=date.today())
    
    @identity.require(identity.not_anonymous())
    @expose('json')
    @validate(validators=dict(afiliado=validators.Int(),
                              amount=validators.UnicodeString(),
                              cuenta=validators.Int(),
                              day=validators.DateTimeConverter(format='%d/%m/%Y')))
    def devolucionPlanilla(self, afiliado, cuenta, day, amount):
        
        affiliate = model.Affiliate.get(afiliado)
        cuenta = model.Account.get(cuenta)
        affiliate.pay_cuota(day.year, day.month)
        
        deduccion = dict()
        deduccion['account'] = cuenta
        deduccion['month'] = day.month
        deduccion['year'] = day.year
        deduccion['affiliate'] = affiliate
        deduccion['amount'] = Decimal(amount)
        model.Deduced(**deduccion)
        
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Excedente Deducido por planilla afiliado {0}".format(affiliate.id)
        model.Logger(**log)
        
        return dict(pago=affiliate.get_monthly())
    
    @expose()
    def cuentas(self):
        
        afo = model.Affiliate.selectBy(payment='Escalafon')
    
        afiliados = dict()
        
        for a in afo:
            if a.cardID == None:
                continue
            afiliados[a.cardID.replace('-','')] = a
        
        cuentas = csv.reader(open('cuentas.csv'))
        
        for linea in cuentas:
            
            if linea[0] in afiliados:
                afiliado = afiliados[linea[0]]
                banco = int(linea[3])
                cuenta = int(linea[4].strip('ABCDEFGHIJKMNLOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz- '))
                
                afiliado.banco = banco
                afiliado.cuenta = cuenta
                print afiliado.banco, afiliado.cuenta
        
        flash('terminado')
        
        raise redirect('/affiliate')
