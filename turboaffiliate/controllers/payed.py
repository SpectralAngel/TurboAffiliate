# -*- coding: utf8 -*-
#
# payed.py
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

from turbogears import controllers, flash, redirect, identity
from turbogears import expose, validate, validators
from turboaffiliate import model
from datetime import date
from sqlobject.sqlbuilder import AND

class Pay(controllers.Controller):
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.loan.payed.pay")
    @validate(validators=dict(code=validators.Int()))
    def add(self, code):
        
        return dict(loan=model.PayedLoan.get(code))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(code=validators.Int()))
    def remove(self, code):
        
        pay = model.OldPay.get(code)
        loan = pay.payedLoan
        capital = pay.capital
        pay.destroySelf()
        loan = loan.to_loan(identity.current.user)
        loan.debt += capital
        
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Eliminar pago del prestamo {0}".format(loan.id)
        model.Logger(**log)
        
        raise redirect('/payed/{0}'.format(loan.id))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(amount=validators.Number(),
                            day=validators.DateTimeConverter(format='%d/%m/%Y'),
                            payedLoan=validators.Int()
                            ))
    def new(self, payedLoan, **kw):
        
        payedLoan = model.PayedLoan.get(payedLoan)
        
        model.OldPay(payedLoan=payedLoan, **kw)
        
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Agregar pago al prestamo {0}".format(payedLoan.id)
        model.Logger(**log)
        
        flash(u'El pago se ha efecutado')
        raise redirect('/payed/{0}'.format(payedLoan.id))

class PayedLoan(controllers.Controller):
    
    # pay = Pay()
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.loan.payed.payed")
    @validate(validators=dict(loan=validators.Int()))
    def default(self, loan):
        
        return dict(loan=model.PayedLoan.get(loan), day=date.today())
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.loan.payed.list")
    @validate(validators=dict(payment=validators.String(),
                              start=validators.DateTimeConverter(format='%d/%m/%Y'),
                              end=validators.DateTimeConverter(format='%d/%m/%Y')))
    def payment(self, start, end, payment):
        
        loans = model.PayedLoan.select(AND(model.PayedLoan.q.last>=start,
                                      model.PayedLoan.q.last<=end))
        
        loans = [l for l in loans if l.affiliate.payment==payment]
        
        return dict(loans=loans, count=len(loans),
                    payment="Periodo del {0} al {1}".format(payment,
                            start.strftime('%d de %B de %Y'),
                            end.strftime('%d de %B de %Y')),
                    capital=sum(l.capital for l in loans))
    
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.loan.payed.list")
    @validate(validators=dict(start=validators.DateTimeConverter(format='%d/%m/%Y'),
                              end=validators.DateTimeConverter(format='%d/%m/%Y')))
    def period(self, start, end):
        
        loans = model.PayedLoan.select(AND(model.PayedLoan.q.last>=start,
                                      model.PayedLoan.q.last<=end))
        
        return dict(loans=loans, count=loans.count(),
                    payment="Periodo del {0} al {1}".format(start.strftime('%d de %B de %Y'),
                                                        end.strftime('%d de %B de %Y')),
                    capital=sum(l.capital for l in loans))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.payed.pagare')
    @validate(validators=dict(loan=validators.Int()))
    def pagare(self, loan):
        
        return dict(loan=model.PayedLoan.get(loan))
    
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.payed.receipt')
    @validate(validators=dict(loan=validators.Int()))
    def recibo(self, loan):
        
        return dict(loan=model.PayedLoan.get(loan))
    
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(loan=validators.Int()))
    def toLoan(self, loan):
        
        loan = model.PayedLoan.get(loan)
        loan = loan.to_loan(identity.current.user)
        raise redirect('/loan/{0}'.format(loan.id))
    
    @identity.require(identity.All(identity.not_anonymous(), identity.has_permission("delete")))
    @expose()
    @validate(validators=dict(loan=validators.Int()))
    def remove(self, loan):
        
        loan = model.PayedLoan.get(loan)
        affiliate = loan.affiliate
        loan_id = loan.id
        #loan.remove()
        log = dict()
        log['user'] = identity.current.user
        log['action'] = "Prestamo {0} eliminado".format(loan_id)
        model.Logger(**log)
        loan.remove()
        raise redirect('/affiliate/{0}'.format(affiliate.id))
