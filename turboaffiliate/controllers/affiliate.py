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

from turbogears import controllers, flash, redirect, identity, url
from turbogears import expose, validate, validators, error_handler
from turboaffiliate import model
from turboaffiliate.controllers import cuota, extra, billing, deduced, observacion
from datetime import date
from sqlobject.sqlbuilder import OR

class Affiliate(controllers.Controller):
    
    """Permite administrar la información de los afiliados"""
    
    cuota = cuota.Cuota()
    extra = extra.Extra()
    billing = billing.Billing()
    deduced = deduced.Deduced()
    observacion = observacion.Observacion()
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.index')
    def index(self, tg_errors=None):
        
        if tg_errors:
            errors = [(param,inv.msg,inv.value) for param, inv in
                      tg_errors.items()]
            flash(errors)
        
        return dict()
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.affiliate')
    @validate(validators=dict(affiliate=validators.Int()))
    def default(self, affiliate):
        
        """Permite mostrar un afiliado mediante su numero de afiliación"""
        
        return dict(affiliate=model.Affiliate.get(affiliate),accounts=model.Account.select())
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(cardID=validators.String()))
    def card(self, cardID):
        
        affiliate = model.Affiliate.selectBy(cardID=cardID).limit(1).getOne()
        
        raise redirect(url('/affiliate/%s' % affiliate.id))
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.search')
    @validate(validators=dict(cobro=validators.String()))
    def cobro(self, cobro):
        
        """Muestra un afiliado mediante su número de cobro de UPN o INPREMA"""
        
        return dict(result=model.Affiliate.selectBy(escalafon=cobro))
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.affiliate')
    @validate(validators=dict(carnet=validators.Int()))
    def carnet(self, carnet):
        
        """Permite utilizar un numero de afiliacion en un formulario"""
        
        raise redirect(url('/affiliate/%s' % carnet))
    
    @identity.require(identity.has_permission("afiliar"))
    @expose(template="turboaffiliate.templates.affiliate.add")
    def add(self):
        return dict()
    
    @error_handler(index)
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
            town=validators.UnicodeString(),
            state=validators.UnicodeString(),
    ))
    def save(self, **kw):
        
        if kw['cardID'] == '':
            flash(u'No se escribio un número de identidad')
            flash(u'Al afiliado no se le podra cobrar si cotiza por escalafon')
        try:            
            affiliate = model.Affiliate.get(int(kw['affiliate']))
            
            # Logs del sistema
            log = dict()
            log['user'] = identity.current.user
            log['action'] = "Modificado el afiliado %s" % affiliate.id
            model.Logger(**log)
            
            del kw['affiliate']
            
            for key in kw.keys():
                setattr(affiliate, key, kw[key])
            
            flash('El afiliado ha sido actualizado!')
        
        except KeyError:
            
            affiliate = model.Affiliate(**kw)
            affiliate.complete(date.today().year)
            
            log = dict()
            log['user'] = identity.current.user
            log['action'] = "Agregado el afiliado %s" % affiliate.id
            model.Logger(**log)
            
            flash('El afiliado ha sido guardado!')
        
        raise redirect(url('/affiliate/%s' % affiliate.id))
    
    @error_handler(index)
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
        flash('El afiliado ha sido removido')
        
        raise redirect(url('/affiliate'))
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.search')
    @validate(validators=dict(name=validators.UnicodeString()))
    def search(self, name):
        
        if name == '':
            raise redirect(url('/affiliate'))
        affiliates = model.Affiliate.select(OR(model.Affiliate.q.firstName.contains(name),
											   model.Affiliate.q.lastName.contains(name)))
        return dict(result=affiliates)
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.search')
    @validate(validators=dict(cardID=validators.String()))
    def byCardID(self, cardID):
        
        """Permite buscar afiliados mediante número de identidad"""
        
        return dict(affiliates=model.Affiliate.selectBy(cardID=cardID))
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.report')
    @validate(validators=dict(state=validators.UnicodeString()))
    def department(self, state):
        
        affiliates = model.Affiliate.selectBy(state=state)
        count = affiliates.count()
        return dict(affiliates=affiliates, state=state, count=count)
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.card')
    @validate(validators=dict(affiliate=validators.UnicodeString()))
    def byRange(self, cardID):
        
        affiliates = model.Affiliate.select("affiliate.card_id like '%%%s%%'" % cardID)
        return dict(affiliates=affiliates, cardID=cardID, count=affiliates.count())
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.list')
    @validate(validators=dict(year=validators.Int(),month=validators.Int(), how=validators.UnicodeString()))
    def cotization(self, how, year, month):
        
        affiliates = model.Affiliate.select(model.Affiliate.q.payment==how, orderBy="lastName")
        total = sum(a.total(year, month) for a in affiliates)
        return dict(affiliates=affiliates, count=affiliates.count(), year=year, month=month, how=how, total=total)
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.report')
    @validate(validators=dict(affiliate=validators.Int(),end=validators.Int(), begin=validators.Int()))
    def aList(self, begin, end):
        
        query = "affiliate.id <= %s and affiliate.id >= %s" % (begin, end)
        affiliates = model.Affiliate.select(query)
        return dict(affiliates=affiliates, count=affiliates.count())
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.affiliate')
    def last(self):
        
        return dict(affiliate=model.Affiliate.select(orderBy="-id").limit(1).getOne())
    
    @error_handler(index)
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
        log['action'] = "Desactivado el afiliado %s" % affiliate.id
        model.Logger(**log)
        raise redirect(url('/affiliate/%s' % affiliate.id))
    
    @error_handler(index)
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
        log['action'] = "Desactivado el afiliado %s" % affiliate.id
        model.Logger(**log)
        raise redirect(url('/affiliate/%s' % affiliate.id))
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int()))
    def activate(self, affiliate):
        
        affiliate = model.Affiliate.get(int(affiliate))
        affiliate.active = True
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Activado el afiliado %s" % affiliate.id
        model.Logger(**log)
        raise redirect(url('/affiliate/%s' % affiliate.id))
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.payment')
    @validate(validators=dict(how=validators.UnicodeString()))
    def payment(self, how):
        
        affiliates = model.Affiliate.select(model.Affiliate.q.payment==how, orderBy="lastName")
        return dict(affiliates=affiliates, count=affiliates.count(), how=how)
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.age')
    @validate(validators=dict(joined=validators.Int(),age=validators.Int()))
    def age(self, joined, age):
        
        day = date.today().year - age
        affiliates = model.Affiliate.select(model.Affiliate.birthday>=day)
        affiliates = [affiliate for affiliate in affiliates if affiliate.joined.year <= joined]
        
        return dict(affiliates=affiliate)
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    @validate(validators=dict(start=validators.DateTimeConverter(format='%d/%m/%Y'),
                              end=validators.DateTimeConverter(format='%d/%m/%Y')))
    def byDate(self, start, end):
        
        query = "affiliate.joined >= '%s' and affiliate.joined <= '%s'" % (start, end)
        affiliates = model.Affiliate.select(query)
        return dict(affiliates=affiliates, start=start, end=end, show="Fecha de Afiliaci&oacute;n", count=affiliates.count())
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    @validate(validators=dict(town=validators.UnicodeString()))
    def byTown(self, town):
        
        affiliates = model.Affiliate.selectBy(town=town)
        return dict(affiliates=affiliates, show="Municipio", count=affiliates.count())
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    @validate(validators=dict(school=validators.UnicodeString(),state=validators.UnicodeString()))
    def bySchool(self, school, state):
        
        query = "affiliate.school = '%s' or affiliate.school2 = '%s'" % (school, school)
        affiliates = model.Affiliate.select(query)
        affiliates = [a for a in affiliates if a.state == state]
        return dict(affiliates=affiliates, show="Instituto", count=len(affiliates))
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    def disabled(self):
        
        affiliates = model.Affiliate.selectBy(active=False)
        return dict(affiliates=affiliates, show="Inhabilitados", count=affiliates.count())
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    def all(self):
        
        affiliates = model.Affiliate.select()
        return dict(affiliates=affiliates, show="Todos", count=affiliates.count())
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int(),how=validators.UnicodeString(),
                              year=validators.Int(),month=validators.Int()))
    def posteo(self, affiliate, how, year, month):
        
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Posteado el afiliado %s" % affiliate.id
        model.Logger(**log)
        
        affiliate = model.Affiliate.get(affiliate)
        affiliate.pay_cuota(year, month)
        
        for loan in affiliate.loans:
            loan.pay(loan.get_payment(), "Planilla", date.today())
        
        raise redirect(url('/affiliate/cotization/?how=%s&year=%s&month=%s' % (how, year, month)))
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.planilla')
    @validate(validators=dict(payment=validators.String(),year=validators.Int(),
                              month=validators.Int(), day=validators.DateTimeConverter(format='%Y-%m-%d')))
    def listmanual(self, payment, month, year, day):
        
        affiliates = model.Affiliate.select(model.Affiliate.q.payment==payment, orderBy="lastName")
        return dict(affiliates=affiliates, count=affiliates.count(), how=payment, year=year, month=month, day=day.date())
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.debt')
    @validate(validators=dict(payment=validators.String()))
    def debt(self, payment):
        
        affiliates = model.Affiliate.selectBy(payment=payment)
        return dict(affiliates=affiliates, show=payment, count=affiliates.count())
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    @validate(validators=dict(year=validators.Int()))
    def solvent(self, year):
        
        affiliates = model.Affiliate.select()
        affiliates = [affiliate for affiliate in affiliates if affiliate.multisolvent(year)]
        show = "Solventes al %s" % year
        return dict(affiliates=affiliates, show=show, count=len(affiliates))
    
    @error_handler(index)
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
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    def none(self):
        
        affiliates = model.Affiliate.selectBy(joined=None)
        show = "Sin Año de Afiliación"
        return dict(affiliates=affiliates, show=show, count=affiliates.count())
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    def noCard(self):
        
        affiliates = model.Affiliate.selectBy(cardID=None)
        show = "Sin Número de identidad"
        return dict(affiliates=affiliates, show=show, count=affiliates.count())
    
    @error_handler(index)
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
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.delayed')
    @validate(validators=dict(payment=validators.String()))
    def delayed(self, payment):
        
        affiliates = model.Affiliate.selectBy(payment=payment)
        affiliates =[a for a in affiliates if a.get_delayed() != None]
        
        return dict(affiliates=affiliates,count=len(affiliates),payment=payment)
    
    @error_handler(index)
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
    
    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.solvencia')
    @validate(validators=dict(mes=validators.UnicodeString(),anio=validators.Int(),
                              afiliado=validators.Int()))
    def solvencia(self, afiliado, mes, anio):
        
        return dict(afiliado=model.Affiliate.get(afiliado),mes=mes,anio=anio, dia=date.today())
