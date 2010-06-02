#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# loan.py
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
from turbogears import expose, validate, validators
from turboaffiliate import model, wording
from datetime import date
from decimal import Decimal

class Deduction(controllers.Controller):
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(loan=validators.Int(),account=validators.Int(),
                              amount=validators.String(),
                              description=validators.String()))
    def save(self, **kw):
        
        kw['loan'] = model.Loan.get(kw['loan'])
        kw['account'] = model.Account.get(kw['account'])
        kw['amount'] = Decimal(kw['amount'])
        kw['name'] = kw['account'].name
        
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Deduccion de %s al prestamo %s" % (kw['amount'], kw['loan'].id)
        model.Logger(**log)
        
        model.Deduction(**kw)
        raise redirect('/loan/%s' % kw['loan'].id)
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(deduction=validators.Int()))
    def remove(self, deduction):
        
        deduction = model.Deduction.get(deduction)
        loan = deduction.loan
        deduction.destroySelf()
        
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Eliminada deduccion prestamo %s" % loan.id
        model.Logger(**log)
        
        raise redirect('/loan/%s' % loan.id)

class Pay(controllers.Controller):
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(code=validators.Int()))
    def remove(self, code):
        
        pay = model.Pay.get(code)
        loan = pay.loan
        pay.revert()
        raise redirect('/loan/%s' % loan.id)
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(amount=validators.String(),loan=validators.Int(),
                          receipt=validators.String(), free=validators.Bool(),
                          day=validators.DateTimeConverter(format='%d/%m/%Y')))
    def agregar(self, amount, day, loan, receipt, **kw):
        
        amount = Decimal(amount)
        loan = model.Loan.get(loan)
        id = loan.id
        
        free = False;
        
        if 'free' in kw:
            free = kw['free']
        
        if day == None:
            day = date.today()
        
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Pago de %s al prestamo %s" % (amount, loan.id)
        model.Logger(**log)
        
        if loan.pagar(amount, receipt, day, free):
            raise redirect('/payed/%s' % id)
        
        raise redirect(url('/loan/%s' % loan.id))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.pay.resume')
    @validate(validators=dict(start=validators.DateTimeConverter(format='%Y-%m-%d'),
                              end=validators.DateTimeConverter(format='%Y-%m-%d')))
    def resume(self, start, end):
        
        query = "pay.day >= '%s' and pay.day <= '%s'" % (start, end)
        
        pays = model.Pay.select(query)
        count = pays.count()
        capital = sum(pay.capital for pay in pays)
        interest = sum(pay.interest for pay in pays)
        
        return dict(start=start, end=end, pays=pays, count=count, capital=capital,
                    interest=interest)

class Loan(controllers.Controller):
    
    pay = Pay()
    deduction = Deduction()
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.index')
    def index(self):
        return dict()
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.loan')
    @expose("json")
    @validate(validators=dict(code=validators.Int()))
    def default(self, code):
        
        return dict(loan=model.Loan.get(code), day=date.today(),
                    accounts=model.Account.selectBy(loan=True))
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.loan.pay")
    def payment(self, code):
    
        return dict(loan=model.Loan.get(code))
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.loan.list")
    @validate(validators=dict(start=validators.DateTimeConverter(format='%Y-%m-%d'),
                              end=validators.DateTimeConverter(format='%Y-%m-%d'),
                              payment=validators.String()))
    def cotizacion(self, start, end, payment):
        
        query = "loan.start_date >= '%s' and loan.start_date <= '%s'" % (start, end)
        
        loans = model.Loan.select(query)
        
        loans = [l for l in loans if l.affiliate.payment==payment]
        
        return dict(loans=loans, count=len(loans),
                    payment="de %s Periodo del %s al %s" % (payment,
                            start.strftime('%d de %B de %Y'),
                            end.strftime('%d de %B de %Y')),
                    capital=sum(l.capital for l in loans),
                    debt=sum(l.debt for l in loans))
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.loan.list")
    @validate(validators=dict(depto=validators.String(),cotizacion=validators.String()))
    def cotizacionDepto(self, depto, cotizacion):
        
        loans = model.Loan.select()
        l = [loan for loan in loans if loan.affiliate.state == depto
             and loan.affiliate.payment == cotizacion]
        
        return dict(loans=l, count=len(l), payment=cotizacion,
                debt=sum(loan.debt for loan in l), capital=sum(loan.capital for loan in l))
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.loan.list")
    def dobles(self):
        
        loans = model.Loan.select()
        
        l = [loan for loan in loans if len(loan.affiliate.loans) > 1]
        
        return dict(loans=l, count=len(l), payment='',
                debt=sum(loan.debt for loan in l), capital=sum(loan.capital for loan in l))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.add')
    @validate(validators=dict(affiliate=validators.Int()))
    def add(self, affiliate):

        affiliate = model.Affiliate.get(affiliate)
        #if (date.today() - affiliate.joined).days < 365:
        #    flash(u"El afiliado a￺n no tiene un año de afiliación")
        #    raise redirect('/affiliate/%s' % affiliate.id)
        #if len(affiliate.loans) > 0:
        #    
        #    for loan in affiliate.loans:
        #        
        #        if loan.percent() < 59:
        #            
        #            flash("El Afiliado no ha pagado el 60% del préstamo anterior")
        #            raise redirect('/affiliate/%s' % affiliate.id)
            
        return dict(affiliate=affiliate)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.edit')
    @validate(validators=dict(loan=validators.Int()))
    def edit(self, loan):
        
        return dict(loan=model.Loan.get(loan))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(loan=validators.Int(),
                              months=validators.Int(),
                              capital=validators.Number(),
                              payment=validators.String()))
    def save(self, loan, capital, months, payment):
        
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Modificacion al prestamo %s" % loan.id
        model.Logger(**log)
        
        loan = model.Loan.get(loan)
        loan.capital = capital
        loan.months = months
        loan.payment = Decimal(payment).quantize(Decimal("0.01"))
        return self.default(loan.id)
        
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int(),
                              months=validators.Int(),
                              capital=validators.Number(),
                              payment=validators.String(),
                              startDate=validators.DateTimeConverter(format='%Y-%m-%d'),
                              id=validators.String()))
    def new(self, affiliate, **kw):
        
        affiliate = model.Affiliate.get(affiliate)
        kw['payment'] = Decimal(kw['payment']).quantize(Decimal("0.01"))
        kw['debt'] = kw['capital']
        kw['letters'] = wording.parse(kw['capital']).capitalize()
        
        if kw['id'] == '':
            del kw['id']
            
        if kw['capital'] < 0:
            raise redirect('/loan/add/%s' % affiliate.id)
        
        kw["aproval"] = identity.current.user
        
        loan = model.Loan(affiliate=affiliate, **kw)
        
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Otorgar prestamo al afiliado %s" % affiliate.id
        model.Logger(**log)
        
        raise redirect(url("/loan/%s" % loan.id))
    
    @identity.require(identity.All(identity.not_anonymous(),
                                   identity.has_permission("delete")))
    @expose()
    @validate(validators=dict(code=validators.Int()))
    def remove(self, code):
        
        loan = model.Loan.get(code)
        loan.remove()
        flash('El prestamo ha sido removido')
        raise redirect('/payed/%s' % code)
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(loan=validators.Int(),months=validators.Int(),
             payment=validators.String()))
    def month(self, loan, months, payment):
        
        loan = model.Loan.get(loan)
        loan.months = months
        loan.payment = Decimal(payment).quantize(Decimal("0.01"))
        raise redirect('/loan/%s' % loan.id)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.pagare')
    @validate(validators=dict(loan=validators.Int()))
    def pagare(self, loan):
    
        return dict(loan=model.Loan.get(loan))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.receipt')
    @validate(validators=dict(loan=validators.Int()))
    def receipt(self, loan):
        
        return dict(loan=model.Loan.get(loan))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(loan=validators.Int()))
    def search(self, loan):
        raise redirect('/loan/%s' % loan)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.day')
    @validate(validators=dict(day=validators.DateTimeConverter(format='%Y-%m-%d')))
    def day(self, day):
        
        loans = model.Loan.selectBy(startDate=day)
        amount = sum(l.capital for l in loans)
        return dict(amount=amount, loans=loans,day=day)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.list')
    @validate(validators=dict(first=validators.DateTimeConverter(format='%Y-%m-%d'),
                              last=validators.DateTimeConverter(format='%Y-%m-%d')))
    def period(self, first, last):
                
        loans = list()
        query = "loan.start_date >= '%s' and loan.start_date <= '%s' order by start_date" % (first, last)
        adeudados = [loan for loan in model.Loan.select(query)]
        
        query = "payed_loan.start_date >= '%s' and payed_loan.start_date <= '%s'" % (first, last)
        pagados = [loan for loan in model.PayedLoan.select(query)]
        
        for n in range(first.day, last.day + 1):
            loans.extend(loan for loan in adeudados if loan.startDate.day == n)
            loans.extend(loan for loan in pagados if loan.startDate.day == n)
        
        debt =0
        for l in loans:
            
            debt += l.totaldebt()
        
        return dict(loans=loans, count=len(loans),
                    payment="Periodo del %s al %s" % (first.strftime('%d de %B de %Y'),
                                                        last.strftime('%d de %B de %Y')),
                    capital=sum(l.capital for l in loans),
                    debt=debt)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.cartera')
    @validate(validators=dict(first=validators.DateTimeConverter(format='%Y-%m-%d'),
                              last=validators.DateTimeConverter(format='%Y-%m-%d')))
    def cartera(self, first, last):
        
        loans = list()
        query = "loan.start_date >= '%s' and loan.start_date <= '%s' order by start_date" % (first, last)
        adeudados = [loan for loan in model.Loan.select(query)]
        
        query = "payed_loan.start_date >= '%s' and payed_loan.start_date <= '%s'" % (first, last)
        pagados = [loan for loan in model.PayedLoan.select(query)]
        
        for n in range(first.day, last.day + 1):
            loans.extend(loan for loan in adeudados if loan.startDate.day == n)
            loans.extend(loan for loan in pagados if loan.startDate.day == n)
        
        amount = sum(l.capital for l in loans)
        return dict(amount=amount, loans=loans, first=first, last=last, count=len(loans))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.view')
    @validate(validators=dict(loan=validators.Int()))
    def view(self, loan):
        
        return dict(loan=model.Loan.get(loan))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(loan=validators.Int(),payment=validators.String()))
    def modify(self, loan, payment):
        
        loan = model.Loan.get(loan)
        loan.payment = Decimal(payment)
        
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Cambio de cuota de prestamo %s a %s" % (loan.id, payment)
        model.Logger(**log)
        
        raise redirect('/loan/%s' % loan.id)
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(loan=validators.Int(),debt=validators.String()))
    def debt(self, loan, debt):
        
        loan = model.Loan.get(loan)
        loan.debt = Decimal(debt)
        raise redirect('/loan/%s' % loan.id)
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(loan=validators.Int(),amount=validators.String()))
    def capital(self, loan, amount):
        
        loan = model.Loan.get(loan)
        loan.amount = Decimal(amount)
        raise redirect('/loan/%s' % loan.id)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.monthly')
    @validate(validators=dict(start=validators.DateTimeConverter(format='%Y-%m-%d'),
                              end=validators.DateTimeConverter(format='%Y-%m-%d')))
    def monthly(self, start, end):
        
        query = "loan.start_date >= '%s' and loan.start_date <= '%s'" % (start, end)
        
        loans = model.Loan.select(query)
        
        li = list()
        
        for n in range(start.month, end.month + 1):
            
            month = dict()
            month['month'] = n
            month['amount'] = sum(l.capital for l in loans if l.startDate.month == n)
            month['net'] = sum(l.net() for l in loans if l.startDate.month == n)
            month['number'] = len(list(l for l in loans if l.startDate.month == n))
            li.append(month)
        
        total = sum(m['amount'] for m in li)
        net = sum(m['net'] for m in li)
        
        return dict(months=li, total=total, start=start, end=end, net=net)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.list')
    @validate(validators=dict(payment=validators.String()))
    def bypayment(self, payment):
        
        affiliates = model.Affiliate.selectBy(payment=payment)
        
        loans = list()
        for a in affiliates:
            loans.extend(l for l in a.loans)
        
        debt = sum(l.debt for l in loans)
        capital = sum(l.capital for l in loans)
        
        count = len(loans)
        
        return dict(loans=loans, count=count, debt=debt, capital=capital, payment=payment)
        
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.list')
    @validate(validators=dict(start=validators.DateTimeConverter(format='%Y-%m-%d'),
                              end=validators.DateTimeConverter(format='%Y-%m-%d'),
                              payment=validators.String()))
    def paymentDate(self, payment, start, end):
        
        query = "loan.start_date >= '%s' and loan.start_date <= '%s'" % (start, end)
        
        loans = model.Loan.select(query)
        
        loans = [l for l in loans if l.affiliate.payment==payment]
        
        debt = sum(l.debt for l in loans)
        capital = sum(l.capital for l in loans)
        
        count = len(loans)
        
        return dict(loans=loans, count=count, debt=debt, capital=capital, payment=payment)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.liquid')
    @validate(validators=dict(start=validators.DateTimeConverter(format='%Y-%m-%d'),
                              end=validators.DateTimeConverter(format='%Y-%m-%d')))
    def liquid(self, start, end):
        
        query = "loan.start_date >= '%s' and loan.start_date <= '%s'" % (start, end)
        
        loans = model.Loan.select(query)
        debt = sum(l.net() for l in loans)
        capital = sum(l.capital for l in loans)
        count = loans.count()
        
        return dict(loans=loans, count=count, debt=debt, capital=capital, payment="")
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(loan=validators.Int()))
    def increase(self, loan):
        
        loan = model.Loan.get(loan)
        loan.offset += 1
        
        return self.default(loan.id)
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(loan=validators.Int()))
    def decrease(self, loan):
        
        loan = model.Loan.get(loan)
        loan.offset -= 1
        return self.default(loan.id)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.bypay')
    @validate(validators=dict(day=validators.DateTimeConverter(format='%Y-%m-%d')))
    def byCapital(self, day):
        
        pays = model.Pay.selectBy(day=day)
        
        capital = sum(pay.capital for pay in pays)
        interest = sum(pay.interest for pay in pays)
        
        return dict(pays=pays, capital=capital, interest=interest)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.resume')
    @validate(validators=dict(start=validators.DateTimeConverter(format='%Y-%m-%d'),
                              end=validators.DateTimeConverter(format='%Y-%m-%d')))
    def resume(self, start, end):
        
        query = "pay.day >= '%s' and pay.day <= '%s'" % (start, end)
        
        pays = model.Pay.select(query)
        capital = sum(pay.capital for pay in pays)
        interest = sum(pay.interest for pay in pays)
        
        query = "old_pay.day >= '%s' and old_pay.day <= '%s'" % (start, end)
        pays = model.OldPay.select(query)
        capital += sum(pay.capital for pay in pays)
        interest += sum(pay.interest for pay in pays)
        
        return dict(capital=capital, interest=interest, start=start, end=end)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.diverge')
    @validate(validators=dict(payment=validators.String(),
                              start=validators.DateTimeConverter(format='%d/%m/%Y'),
                              end=validators.DateTimeConverter(format='%d/%m/%Y')))
    def diverge(self, payment, start, end):
        
        query = "payed_loan.last >= '%s' and payed_loan.last <= '%s'" % (start, end)
        payed = model.PayedLoan.select(query)
        
        payed = [p for p in payed if len(p.affiliate.loans) > 0]
        
        payed = [p for p in payed if p.affiliate.loans[0].get_payment() != p.payment]
        
        payed = [p for p in payed if p.affiliate.payment == payment]
        
        return dict(payed=payed)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.payment')
    @validate(validators=dict(payment=validators.String()))
    def listPayment(self, payment):
        
        loans = model.Loan.select()
        
        return dict(loans=[l for l in loans if l.affiliate.payment == payment])
    
    def calcular_deducciones(self, loans):
        
        prestamos = list()
        
        for loan in loans:
            papeleo = 0
            intereses = 0
            retencion = 0
            aportaciones = 0
            neto = loan.net()
            monto = loan.capital
            for d in loan.deductions:
                if d.account.id == 660:
                    papeleo = d.amount
                elif d.account.id == 658:
                    intereses = d.amount
                elif d.account.id == 659:
                    retencion = d.amount
                elif d.account.id == 665:
                    aportaciones = d.amount
                elif d.account.id == 678:
                    reintegros = d.amount
            
            afiliado = loan.affiliate
            prestamo = model.AuxiliarPrestamo(loan.id, afiliado, monto, neto, papeleo, aportaciones, intereses, retencion, reintegros)
            prestamos.append(prestamo)
        
        return prestamos
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.deducciones')
    @validate(validators=dict(start=validators.DateTimeConverter(format='%Y-%m-%d'),
                              end=validators.DateTimeConverter(format='%Y-%m-%d')))
    def deducciones(self, start, end):
        
        query = "loan.start_date >= '%s' and loan.start_date <= '%s'" % (start, end)
        query2 = "payed_loan.start_date >= '%s' and payed_loan.start_date <= '%s'" % (start, end)
        
        loans = model.Loan.select(query)
        payedLoans = model.PayedLoan.select(query2)
        
        prestamos = list()
        
        prestamos.extend(self.calcular_deducciones(loans))
        prestamos.extend(self.calcular_deducciones(payedLoans))
        
        papeleo = 0
        intereses = 0
        retencion = 0
        aportaciones = 0
        reintegros =0 
        neto = 0
        monto = 0
        
        for p in prestamos:
            
            papeleo += p.papeleo
            intereses += p.intereses
            retencion += p.retencion
            aportaciones += p.aportaciones
            neto += p.neto
            reintegros += p.reintegros
            monto += p.monto
        
        return dict(loans=prestamos, start=start, end=end, monto=monto,
                    neto=neto, papeleo=papeleo, aportaciones=aportaciones,
                    intereses=intereses, retencion=retencion, reintegros=reintegros)
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.deducciones')
    @validate(validators=dict(start=validators.DateTimeConverter(format='%Y-%m-%d')))
    def deduccionesDia(self, start):
        
        loans = model.Loan.selectBy(startDate=start)
        payedLoans = model.PayedLoan.selectBy(startDate=start)
        
        prestamos = list()
        
        prestamos.extend(self.calcular_deducciones(loans))
        prestamos.extend(self.calcular_deducciones(payedLoans))
        
        papeleo = 0
        intereses = 0
        retencion = 0
        aportaciones = 0
        reintegros =0 
        neto = 0
        monto = 0
        
        for p in prestamos:
            
            papeleo += p.papeleo
            intereses += p.intereses
            retencion += p.retencion
            aportaciones += p.aportaciones
            neto += p.neto
            reintegros += p.reintegros
            monto += p.monto
        
        return dict(loans=prestamos, start=start, end=start, monto=monto,
                    neto=neto, papeleo=papeleo, aportaciones=aportaciones,
                    intereses=intereses, retencion=retencion, reintegros=reintegros)

