#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# flyer.py
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

from turbogears import controllers, expose, flash, identity, redirect, url
from turbogears import validate, validators
from turboaffiliate import model
from decimal import Decimal

months = {
            1:'Enero', 2:'Febrero', 3:'Marzo',
            4:'Abril', 5:'Mayo', 6:'Junio',
            7:'Julio', 8:'Agosto', 9:'Septiembre',
            10:'Octubre', 11:'Noviembre', 12:'Diciembre'
         }

filiales = {"Atlantida":{'total':0},"Choluteca":{'total':0},"Colon":{'total':0},
            "Comayagua":{'total':0},"Copan":{'total':0}, "Cortes":{'total':0},
            "El Paraiso":{'total':0}, "Francisco Morazan":{'total':0},
            "Gracias a Dios":{'total':0}, "Intibuca":{'total':0},
            "Islas de la Bahia":{'total':0},"La Paz":{'total':0},
            "Lempira":{'total':0},"Olancho":{'total':0},"Ocotepeque":{'total':0},
            "Santa Barbara":{'total':0},"Valle":{'total':0},"Yoro":{'total':0}}

class Flyer(controllers.Controller):
    
    """Muestra varios Reportes acerca de los pagos, cuotas y estados financieros
    de los afiliados"""
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.escalafon.index")
    def index(self):
        return dict(accounts=model.Account.select())
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.escalafon.post")
    @validate(validators=dict(year=validators.Int(), month=validators.Int(min=1,max=12)))
    def postReport(self, year, month):
        
        """Muestra el reporte de ingresos por los diferentes cargos en un mes
        y año que se han adquirido desde Escalafón"""
        
        report = model.PostReport.selectBy(month=month, year=year).getOne()
        
        return dict(month=month, year=year, report=report)
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.escalafon.report")
    @validate(validators=dict(year=validators.Int(), month=validators.Int(min=1,max=12),
                              payment=validators.String()))
    def report(self, payment, year, month):
        
        """Muestra los cobros a efectuar correspondientes a un mes y año con
        respecto a un tipo de pago"""
        
        affiliates = model.Affiliate.selectBy(payment=payment, active=True)
        
        obligations = model.Obligation.selectBy(month=month, year=year)
        obligation = 0
        if payment == 'INPREMA':
            obligation = sum(o.inprema for o in obligations)
        else:
            obligation = sum(o.amount for o in obligations)
        
        loans = model.Loan.select()
        loans = [loan for loan in loans if loan.affiliate.payment==payment]
        loand = dict()
        loand['amount'] = sum(loan.get_payment() for loan in loans)
        loand['count'] = len(loans)
        
        kw = dict()
        total = Decimal(0)
        accounts = model.Account.select()
        for account in accounts:
            kw[account] = dict()
            li = [extra for extra in account.extras if extra.affiliate.payment==payment]
            kw[account]['amount'] = sum(e.amount for e in li)
            kw[account]['count'] = len(li)
            total += kw[account]['amount']
        
        for account in accounts:
            if kw[account]['amount'] == 0:
                del kw[account]
        
        return dict(deductions=kw, count=affiliates.count(), obligation=obligation, legend=payment, loans=loand, total=total)
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.escalafon.extra")
    @validate(validators=dict(account=validators.Int()))
    def extra(self, account):
        
        """Muestra los cobros a efectuar que corresponden a la cuenta especificada"""
        
        account = model.Account.get(account)
        return dict(account=account, extras=account.extras)
    
    @identity.require(identity.not_anonymous())
    @validate(validators=dict(year=validators.Int(), month=validators.Int(min=1,max=12),
                              payment=validators.String()))
    def OtherReport(self, payment, month, year):
        
        """Genera un reporte para otras deducciones"""
        
        otherDeduced = model.Deduced.selectBy(year=year,month=month)
        otherDeduced = [o for o in otherDeduced if o.affiliate.payment == payment]
        
        kw = dict()
        init = dict()
        i = {"payment":payment, "month":month, "year":year}
        init["otherReport"] = model.OtherReport(**i)
        for other in otherDeduced:
            
            try:
                # The account is already in the report, just add the amount
                kw[other.account].add(other.amount)
            except KeyError:
                init['account'] = other.account
                kw[other.account] = model.OtherAccount(**init)
                kw[other.account].add(other.amount)
            
            other.destroySelf()
        
        flash('Reporte Generado')
        raise redirect(url('/escalafon'))
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.escalafon.other")
    @validate(validators=dict(year=validators.Int(), month=validators.Int(min=1,max=12),
                              payment=validators.String()))
    def showReport(self, year, month, payment):
        
        """Muestra los cobros efectuados correspondientes a un mes y año con
        respecto a un tipo de pago"""
        
        report = model.OtherReport.selectBy(payment=payment).getOne()
        return dict(month=month, year=year, report=report, payment=payment)
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.escalafon.filiales")
    @validate(validators=dict(year=validators.Int(), month=validators.Int(min=1,max=12)))
    def filiales(self, year, month):
        
        affiliates = model.Affiliate.selectBy(payment="Escalafon")
        
        for affiliate in affiliates:
            if affiliate.get_month(year, month):
                if affiliate.school in filiales[affiliate.state]:
                    filiales[affiliate.state][affiliate.school] += 1
                    filiales[affiliate.state]['total'] += 1
                else:
                    filiales[affiliate.state][affiliate.school] = 1
                    filiales[affiliate.state]['total'] += 1
        
        return dict(filiales=filiales)
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.escalafon.aportaciones")
    @validate(validators=dict(year=validators.Int(), month=validators.Int(min=1,max=12)))
    def aportaciones(self, year, month):
        
        """Muestra las deducciones realizadas por concepto de aportaciones
        en un mes y año"""
        
        account = model.Account.get(1)
        deduced = model.Deduced.selectBy(year=year,month=month,account=account)
        
        return dict(deduced=deduced, year=year, month=month)
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.escalafon.filialesdept")
    @validate(validators=dict(state=validators.String(),year=validators.Int(),
                              month=validators.Int(min=1,max=12)))
    def filialesDept(self, state, month, year):
        
        """Muestra todas las Filiales de un Departamento con sus respectivos miembros"""
        
        afiliados = model.Affiliate.selectBy(payment="Escalafon",state=state)
        filiales = dict()
        
        for afiliado in afiliados:
            if afiliado.get_month(year, month):
                if afiliado.school in filiales:
                    filiales[afiliado.school].append(afiliado)
                else:
                    filiales[afiliado.school] = list()
                    filiales[afiliado.school].append(afiliado)
        
        return dict(filiales=filiales, state=state)
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.escalafon.deduced")
    @validate(validators=dict(account=validators.Int(),year=validators.Int(),
                              month=validators.Int(min=1,max=12)))
    def deduced(self, account, month, year):
        
        account = model.Account.get(account)
        
        deduced = model.Deduced.selectBy(account=account, year=year, month=month)
        
        total = sum(d.amount for d in deduced)
        
        return dict(deduced=deduced, account=account, month=months[month], year=year, total=total)
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.escalafon.payment")
    @validate(validators=dict(account=validators.Int(),year=validators.Int(),
                              month=validators.Int(min=1,max=12),payment=validators.String()))
    def deducedPayment(self, account, month, year, payment):
        
        deduced = model.Deduced.selectBy(account=account, year=year, month=month)
        total = sum(d.amount for d in deduced if d.affiliate.payment == payment)
        return dict(deduced=deduced, account=account, month=months[month], year=year, total=total, payment=payment)
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.affiliate.show")
    @validate(validators=dict(year=validators.Int(), payment=validators.String()))
    def empty(self, year, payment):
        
        tables = model.CuotaTable.selectBy(year=year)
        
        affiliates = list()
        for table in tables:
            
            if not table.empty() and table.affiliate.payment == payment:
                
                affiliates.append(table.affiliate)
        
        return dict(affiliates=affiliates, show="Cotizan por %s y pagaron un mes en %s" % (payment, year), count=len(affiliates))
    
    @expose(template="turboaffiliate.templates.affiliate.show")
    @validate(validators=dict(year=validators.Int(), month=validators.Int(min=1,max=12)))
    def aportaron(self, year, month):
        
        query = "cuota_table.month%s = true AND cuota_table.year = %s" % (month, year)
        cuotas = model.CuotaTable.select(query)
        show = "que Cotizaron en %s de %s" % (month, year)
        
        affiliates = [c.affiliate for c in cuotas]
        return dict(affiliates=affiliates,show=show, count=len(affiliates))
    
    @expose(template="turboaffiliate.templates.affiliate.show")
    @validate(validators=dict(year=validators.Int(), month=validators.Int(min=1,max=12)))
    def noAportaron(self, year, month):
        
        query = "cuota_table.month%s = 0 AND cuota_table.year = %s" % (month, year)
        cuotas = model.CuotaTable.select(query)
        show = "que no Cotizaron en %s de %s" % (month, year)
        
        affiliates = [c.affiliate for c in cuotas]
        return dict(affiliates=affiliates,show=show, count=len(affiliates))
    
    @expose(template="turboaffiliate.templates.affiliate.show")
    @validate(validators=dict(year=validators.Int(), month=validators.Int(min=1,max=12)))
    def conTabla(self, year, month):
        
        cuotas = model.CuotaTable.selectBy(year=year)
        
        affiliates = [c.affiliate for c in cuotas if c.affiliate.active]
        show = "que Cotizaron en %s de %s" % (month, year)
        return dict(affiliates=affiliates,show=show,count=len(affiliates))
