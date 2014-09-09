# -*- coding: utf8 -*-
#
# loan.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2007 - 2014 Carlos Flores <cafg10@gmail.com>
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

from datetime import date, timedelta
from decimal import Decimal

from turbogears import controllers, flash, redirect, identity
from turbogears import expose, validate, validators
from sqlobject.sqlbuilder import AND
from sqlobject.main import SQLObjectNotFound
from cherrypy import request

from turboaffiliate import model, wording
from affiliate import log


def daterange(start_date, end_date):
    """Crea un rango de fechas para efectuar cálculos"""

    for n in range((end_date - start_date).days):
        yield (start_date + timedelta(n)).date()


def separacion(loan):
    papeleo = 0
    intereses = 0
    retencion = 0
    aportaciones = 0
    reintegros = 0
    neto = loan.net()
    monto = loan.capital
    for d in loan.deductions:
        if d.account.id == 660:
            papeleo += d.amount
        elif d.account.id == 658:
            intereses += d.amount
        elif d.account.id == 659:
            retencion += d.amount
        elif d.account.id == 665:
            aportaciones += d.amount
        elif d.account.id == 678:
            reintegros += d.amount

    afiliado = loan.affiliate
    return model.AuxiliarPrestamo(loan.id, afiliado, monto, neto, papeleo,
                                  aportaciones, intereses, retencion,
                                  reintegros)


def deduccionesInterno(loans, payedLoans, start, end):
    prestamos = map(separacion, loans)
    prestamos.extend(map(separacion, payedLoans))

    papeleo = sum(p.papeleo for p in prestamos)
    intereses = sum(p.intereses for p in prestamos)
    retencion = sum(p.retencion for p in prestamos)
    aportaciones = sum(p.aportaciones for p in prestamos)
    reintegros = sum(p.reintegros for p in prestamos)
    neto = sum(p.neto for p in prestamos)
    monto = sum(p.monto for p in prestamos)

    return dict(loans=prestamos, start=start, end=start, monto=monto,
                neto=neto, papeleo=papeleo, aportaciones=aportaciones,
                intereses=intereses, retencion=retencion, reintegros=reintegros)


class Deduction(controllers.Controller):
    require = identity.require(identity.not_anonymous())

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(loan=validators.Int(), account=validators.Int(),
                              amount=validators.UnicodeString(),
                              description=validators.UnicodeString()))
    def save(self, **kw):
        kw['loan'] = model.Loan.get(kw['loan'])
        kw['account'] = model.Account.get(kw['account'])
        kw['amount'] = Decimal(kw['amount'].replace(',', ''))

        deduction = model.Deduction(**kw)

        log(u"Deduccion de {0} al prestamo {1}".format(kw['amount'],
                                                       kw['loan'].id),
            identity.current.user, deduction.loan.affiliate)

        raise redirect('/loan/{0}'.format(kw['loan'].id))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(deduction=validators.Int()))
    def remove(self, deduction):
        deduction = model.Deduction.get(deduction)
        loan = deduction.loan
        deduction.destroySelf()

        log(
            u"Eliminada deducción préstamo {0}".format(loan.id),
            identity.current.user, loan.affiliate)

        raise redirect('/loan/{0}'.format(loan.id))


class Pay(controllers.Controller):
    require = identity.require(identity.not_anonymous())

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(code=validators.Int()))
    def remove(self, code):

        pay = model.Pay.get(code)
        loan = pay.loan
        pay.revert()
        raise redirect('/loan/{0}'.format(loan.id))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(amount=validators.UnicodeString(),
                              loan=validators.Int(),
                              receipt=validators.String(),
                              free=validators.Bool(),
                              deposito=validators.Bool(),
                              redir=validators.UnicodeString(),
                              description=validators.UnicodeString(),
                              day=validators.DateTimeConverter(
                                  format='%d/%m/%Y')))
    def agregar(self, amount, day, loan, receipt, redir, **kw):

        amount = Decimal(amount.replace(',', ''))
        loan = model.Loan.get(loan)
        id = loan.id

        free = False
        deposito = False

        if 'free' in kw:
            free = kw['free']

        if 'deposito' in kw:
            deposito = kw['deposito']

        if day is None:
            day = date.today()

        log(
            u"Pago de {0} al prestamo {1}".format(amount, loan.id),
            identity.current.user, loan.affiliate)

        if loan.pagar(amount, receipt, day, free, deposito=deposito,
                      descripcion=kw['description']):
            raise redirect('/payed/{0}'.format(id))

        raise redirect(redir)

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(amount=validators.UnicodeString(),
                              loan=validators.Int(),
                              receipt=validators.String(),
                              free=validators.Bool(),
                              deposito=validators.Bool(),
                              redir=validators.UnicodeString(),
                              description=validators.UnicodeString(),
                              day=validators.DateTimeConverter(
                                  format='%d/%m/%Y'),
                              numero=validators.Int()))
    def agregarVarios(self, amount, day, loan, receipt, redir, numero, **kw):

        amount = Decimal(amount.replace(',', ''))
        loan = model.Loan.get(loan)
        id = loan.id

        free = False
        deposito = False

        if 'free' in kw:
            free = kw['free']

        if 'deposito' in kw:
            deposito = kw['deposito']

        if day is None:
            day = date.today()

        log(
            u"{0} Pagos de {1} al prestamo {2}".format(numero,
                                                       amount,
                                                       loan.id),
            identity.current.user, loan.affiliate)

        for n in range(numero):

            if loan.pagar(amount, receipt, day, free, deposito=deposito,
                          descripcion=kw['description']):
                raise redirect('/payed/{0}'.format(id))

        raise redirect(redir)

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.pay.resume')
    @validate(
        validators=dict(start=validators.DateTimeConverter(format='%d/%m/%Y'),
                        end=validators.DateTimeConverter(format='%d/%m/%Y')))
    def resume(self, start, end):

        pays = model.Pay.select(
            AND(model.Pay.q.day >= start, model.Pay.q.day <= end))
        oldpays = model.OldPay.select(
            AND(model.OldPay.q.day >= start, model.OldPay.q.day <= end))
        count = pays.count() + oldpays.count()
        capital = sum(pay.capital for pay in pays) + sum(
            pay.capital for pay in oldpays)
        interest = sum(pay.interest for pay in pays) + sum(
            pay.interest for pay in oldpays)

        return dict(start=start, end=end, pays=pays, count=count,
                    capital=capital,
                    interest=interest, oldpays=oldpays)

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose('json')
    @validate(validators=dict(amount=validators.UnicodeString(),
                              loan=validators.Int(), free=validators.Bool(),
                              cuenta=validators.Int(),
                              day=validators.DateTimeConverter(
                                  format='%d/%m/%Y')))
    def agregarPlanilla(self, loan, day, cuenta, amount, **kw):

        amount = Decimal(amount.replace(',', ''))
        loan = model.Loan.get(loan)
        cuenta = model.Account.get(cuenta)
        id = loan.id

        free = False;

        if 'free' in kw:
            free = kw['free']

        if day is None:
            day = date.today()

        deduccion = {}
        deduccion['account'] = cuenta
        deduccion['month'] = day.month
        deduccion['year'] = day.year
        deduccion['affiliate'] = loan.affiliate
        deduccion['amount'] = amount
        model.Deduced(**deduccion)

        log(
            u"Pago por Planilla de {0} al prestamo {1}".format(
                amount, loan.id),
            identity.current.user, loan.affiliate)

        loan.pagar(amount, u'Planilla', day, free)

        return dict(pago=loan.affiliate.get_monthly())


class Loan(controllers.Controller):
    pay = Pay()
    deduction = Deduction()

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.index')
    def index(self):

        return dict(casas=model.Casa.select())

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.loan')
    @expose("json")
    @validate(validators=dict(code=validators.Int()))
    def default(self, code):

        loan = None
        try:
            loan = model.Loan.get(code)
        except SQLObjectNotFound:
            flash(u'No se encuentra el préstamo con Solicitud {0}'.format(code))
            raise redirect(request.headers.get("Referer", "/"))

        return dict(loan=loan, day=date.today(),
                    accounts=model.Account.selectBy(loan=True))

    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.loan.list")
    @validate(
        validators=dict(start=validators.DateTimeConverter(format='%d/%m/%Y'),
                        end=validators.DateTimeConverter(format='%d/%m/%Y'),
                        payment=validators.String()))
    def cotizacion(self, start, end, payment):

        loans = model.Loan.select(AND(model.Loan.q.startDate >= start,
                                      model.Loan.q.startDate <= end))

        loans = [l for l in loans if l.affiliate.payment == payment]

        return dict(loans=loans, count=len(loans),
                    payment=u"de {0} Periodo del {1} al {2}".format(payment,
                                                                    start.strftime(
                                                                        '%d de %B de %Y'),
                                                                    end.strftime(
                                                                        '%d de %B de %Y')),
                    capital=sum(l.capital for l in loans),
                    debt=sum(l.debt for l in loans))

    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.loan.list")
    @validate(validators=dict(depto=validators.UnicodeString(),
                              cotizacion=validators.UnicodeString()))
    def cotizacionDepto(self, depto, cotizacion):

        loans = model.Loan.select()
        l = [loan for loan in loans if loan.affiliate.state == depto
        and loan.affiliate.payment == cotizacion]

        return dict(loans=l, count=len(l), payment=cotizacion,
                    debt=sum(ln.debt for ln in l),
                    capital=sum(ln.capital for ln in l))

    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.loan.list")
    def dobles(self):

        loans = model.Loan.select()

        l = [loan for loan in loans if len(loan.affiliate.loans) > 1]

        return dict(loans=l, count=len(l), payment=u'',
                    debt=sum(loan.debt for loan in l),
                    capital=sum(loan.capital for loan in l))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(loan=validators.Int(),
                              months=validators.Int(),
                              capital=validators.Number(),
                              payment=validators.UnicodeString()))
    def save(self, loan, capital, months, payment):

        log(u"Modificaciones al prestamo {0}".format(loan.id),
            identity.current.user, loan.affiliate)

        loan = model.Loan.get(loan)
        loan.capital = capital.replace(',', '')
        loan.months = months
        loan.payment = Decimal(payment).quantize(Decimal("0.01"))
        return self.default(loan.id)

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(affiliate=validators.Int(),
                              months=validators.Int(),
                              capital=validators.UnicodeString(),
                              payment=validators.UnicodeString(),
                              interest=validators.Int(),
                              startDate=validators.DateTimeConverter(
                                  format='%d/%m/%Y'),
                              id=validators.String()))
    def new(self, affiliate, **kw):

        affiliate = model.Affiliate.get(affiliate)
        kw['capital'] = Decimal(kw['capital'].replace(',', '')).quantize(
            Decimal("0.01"))
        kw['payment'] = Decimal(kw['payment'].replace(',', '')).quantize(
            Decimal("0.01"))
        kw['debt'] = kw['capital']
        kw['letters'] = wording.parse(kw['capital']).capitalize()

        if kw['id'] == '':
            del kw['id']

        if kw['capital'] < 0:
            flash(u"El capital no puede ser menor que 0")
            raise redirect('/loan/add/{0}'.format(affiliate.id))

        kw["aproval"] = identity.current.user
        kw["casa"] = kw["aproval"].casa

        loan = model.Loan(affiliate=affiliate, **kw)
        log(
            u"Otorgar préstamo al afiliado {0}".format(affiliate.id),
            identity.current.user, loan.affiliate)

        raise redirect("/loan/{0}".format(loan.id))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(loan=validators.Int(), solicitud=validators.Int(),
                              cuenta=validators.Int(),
                              pago=validators.UnicodeString(),
                              descripcion=validators.UnicodeString()))
    def refinanciar(self, loan, pago, solicitud, cuenta, descripcion):

        pago = Decimal(pago.replace(',', ''))
        solicitud = model.Solicitud.get(solicitud)
        cuenta = model.Account.get(cuenta)
        loan = model.Loan.get(loan)

        prestamo = loan.refinanciar(pago, solicitud, cuenta,
                                    identity.current.user,
                                    descripcion)

        raise redirect('/loan/{0}'.format(prestamo.id))

    @identity.require(identity.All(identity.not_anonymous(),
                                   identity.has_permission("delete")))
    @expose()
    @validate(validators=dict(code=validators.Int()))
    def remove(self, code):

        loan = model.Loan.get(code)
        loan = loan.remove()

        log(u"Enviado el prestamo {0} a pagados".format(loan.id),
            identity.current.user, loan.affiliate)

        flash('El prestamo ha sido removido')
        raise redirect('/payed/{0}'.format(loan.id))

    @expose()
    def limpiar(self):

        loans = model.Loan.select(model.Loan.q.debt == 0)
        map(model.Loan.remove, loans)
        flash('Se han trasladado los Préstamos sin saldo pendiente')
        raise redirect('/loan')

    @expose()
    @validate(validators=dict(loan=validators.Int()))
    def calibrar(self, loan):

        """Permite efectuar la calibración de un :class:`Loan` en especifico
        desde la interfaz de usuario"""

        loan = model.Loan.get(loan)
        loan.calibrar()
        flash(u'Se han corregido los intereses de los pagos al Préstamo')
        raise redirect('/loan/{0}'.format(loan.id))

    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(loan=validators.Int(), months=validators.Int(),
                              payment=validators.String()))
    def month(self, loan, months, payment):

        loan = model.Loan.get(loan)
        loan.months = months
        loan.payment = Decimal(payment).quantize(Decimal("0.01"))
        raise redirect('/loan/{0}'.format(loan.id))

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
        raise redirect('/loan/{0}'.format(loan))

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.day')
    @validate(
        validators=dict(day=validators.DateTimeConverter(format='%d/%m/%Y')))
    def day(self, day):

        loans = model.Loan.selectBy(startDate=day)
        amount = sum(l.capital for l in loans)
        return dict(amount=amount, loans=loans, day=day)

    def carteraInterna(self, first, last, adeudados, pagados):

        """Calcula los montos de Prestamo Pagados y Corrientes, ordenandolos
        por fecha"""

        loans = list()

        for n in daterange(first, last + timedelta(1)):
            loans.extend(loan for loan in adeudados if loan.startDate == n)
            loans.extend(loan for loan in pagados if loan.startDate == n)

        amount = sum(l.capital for l in loans)
        deuda = sum(l.debt for l in loans)
        net = sum(l.net() for l in loans)

        return loans, amount, deuda, net

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.cartera')
    @validate(
        validators=dict(first=validators.DateTimeConverter(format='%d/%m/%Y'),
                        last=validators.DateTimeConverter(format='%d/%m/%Y')))
    def cartera(self, first, last):

        adeudados = model.Loan.select(AND(model.Loan.q.startDate >= first,
                                          model.Loan.q.startDate <= last))

        pagados = model.PayedLoan.select(
            AND(model.PayedLoan.q.startDate >= first,
                model.PayedLoan.q.startDate <= last))

        loans, amount, deuda, net = self.carteraInterna(first, last, adeudados,
                                                        pagados)

        return dict(amount=amount, deuda=deuda, net=net, loans=loans,
                    first=first, last=last, count=len(loans))

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.carteraCasa')
    @validate(
        validators=dict(first=validators.DateTimeConverter(format='%d/%m/%Y'),
                        last=validators.DateTimeConverter(format='%d/%m/%Y'),
                        casa=validators.Int()))
    def carteraCasa(self, first, last, casa):

        casa = model.Casa.get(casa)
        adeudados = model.Loan.select(AND(model.Loan.q.startDate >= first,
                                          model.Loan.q.startDate <= last,
                                          model.Loan.q.casa == casa))

        pagados = model.PayedLoan.select(
            AND(model.PayedLoan.q.startDate >= first,
                model.PayedLoan.q.startDate <= last,
                model.PayedLoan.q.casa == casa))

        loans, amount, deuda, net = self.carteraInterna(first, last, adeudados,
                                                        pagados)

        return dict(amount=amount, deuda=deuda, net=net, loans=loans,
                    first=first, last=last, count=len(loans), casa=casa)


    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.carteraDepartamento')
    @validate(
        validators=dict(first=validators.DateTimeConverter(format='%d/%m/%Y'),
                        last=validators.DateTimeConverter(format='%d/%m/%Y'),
                        departamento=validators.Int()))
    def carteraDepartamento(self, first, last, departamento):

        departamento = model.Departamento.get(departamento)

        adeudados = model.Affiliate.selectBy(
            departamento=departamento).throughTo.loans.filter(
            AND(model.Loan.q.startDate >= first,
                model.Loan.q.startDate <= last))

        pagados = model.Affiliate.selectBy(
            departamento=departamento).throughTo.payedLoans.filter(
            AND(model.PayedLoan.q.startDate >= first,
                model.PayedLoan.q.startDate <= last))

        loans, amount, deuda, net = self.carteraInterna(first, last, adeudados,
                                                        pagados)

        return dict(amount=amount, deuda=deuda, net=net, loans=loans,
                    departamento=departamento, first=first, last=last,
                    count=len(loans))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(
        validators=dict(loan=validators.Int(), payment=validators.String()))
    def modify(self, loan, payment):

        loan = model.Loan.get(loan)
        loan.payment = Decimal(payment.replace(',', ''))

        log(
            u"Cambio de cuota de prestamo {0} a {1}".format(loan.id,
                                                            payment),
            identity.current.user, loan.affiliate)

        raise redirect('/loan/{0}'.format(loan.id))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(loan=validators.Int(),
                              debt=validators.UnicodeString()))
    def debt(self, loan, debt):

        loan = model.Loan.get(loan)
        loan.debt = Decimal(debt.replace(',', ''))
        log(
            u"Cambio de deuda de prestamo {0} a {1}".format(loan.id,
                                                            debt),
            identity.current.user, loan.affiliate)
        raise redirect('/loan/{0}'.format(loan.id))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(
        validators=dict(loan=validators.Int(), amount=validators.String()))
    def capital(self, loan, amount):

        loan = model.Loan.get(loan)
        loan.amount = Decimal(amount.replace(',', ''))
        log(
            u"Cambio de capital de prestamo {0} a {1}".format(loan.id,
                                                            amount),
            identity.current.user, loan.affiliate)
        raise redirect('/loan/{0}'.format(loan.id))

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.monthly')
    @validate(
        validators=dict(start=validators.DateTimeConverter(format='%d/%m/%Y'),
                        end=validators.DateTimeConverter(format='%d/%m/%Y')))
    def monthly(self, start, end):

        loans = model.Loan.select(AND(model.Loan.q.startDate >= start,
                                      model.Loan.q.startDate <= end))
        prestamos = dict()

        for l in loans:
            if not (l.startDate.year in prestamos):
                prestamos[l.startDate.year] = dict()

        if l.startDate.month in prestamos[l.startDate.year]:
            prestamos[l.startDate.year][l.startDate.month][
                'capital'] += l.capital
            prestamos[l.startDate.year][l.startDate.month]['cantidad'] += 1
            prestamos[l.startDate.year][l.startDate.month]['neto'] += l.net()
        else:
            prestamos[l.startDate.year][l.startDate.month] = dict()
            prestamos[l.startDate.year][l.startDate.month][
                'capital'] += l.capital
            prestamos[l.startDate.year][l.startDate.month]['cantidad'] += 1
            prestamos[l.startDate.year][l.startDate.month]['neto'] += l.net()

        return dict(prestamos=loans, start=start, end=end)

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.list')
    @validate(validators=dict(payment=validators.UnicodeString()))
    def bypayment(self, payment):

        affiliates = model.Affiliate.selectBy(payment=payment)

        loans = list()
        for a in affiliates:
            loans.extend(l for l in a.loans)

        debt = sum(l.debt for l in loans)
        capital = sum(l.capital for l in loans)

        count = len(loans)

        return dict(loans=loans, count=count, debt=debt, capital=capital,
                    payment=payment)

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.list')
    @validate(
        validators=dict(start=validators.DateTimeConverter(format='%d/%m/%Y'),
                        end=validators.DateTimeConverter(format='%d/%m/%Y'),
                        payment=validators.String()))
    def paymentDate(self, payment, start, end):

        loans = model.Loan.select(AND(model.Loan.q.startDate >= start,
                                      model.Loan.q.startDate <= end))

        loans = [l for l in loans if l.affiliate.payment == payment]

        debt = sum(l.debt for l in loans)
        capital = sum(l.capital for l in loans)

        count = len(loans)

        return dict(loans=loans, count=count, debt=debt, capital=capital,
                    payment=payment)

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.liquid')
    @validate(
        validators=dict(start=validators.DateTimeConverter(format='%d/%m/%Y'),
                        end=validators.DateTimeConverter(format='%d/%m/%Y')))
    def liquid(self, start, end):

        loans = model.Loan.select(AND(model.Loan.q.startDate >= start,
                                      model.Loan.q.startDate <= end))
        debt = sum(l.net() for l in loans)
        capital = sum(l.capital for l in loans)
        count = loans.count()

        return dict(loans=loans, count=count, debt=debt, capital=capital,
                    payment=u"")

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(loan=validators.Int()))
    def increase(self, loan):

        loan = model.Loan.get(loan)
        loan.offset += 1

        raise redirect('/loan/{0}'.format(loan.id))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(loan=validators.Int()))
    def decrease(self, loan):

        loan = model.Loan.get(loan)
        loan.offset -= 1

        raise redirect('/loan/{0}'.format(loan.id))

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.bypay')
    @validate(
        validators=dict(day=validators.DateTimeConverter(format='%d/%m/%Y')))
    def byCapital(self, day):

        pays = model.Pay.selectBy(day=day)

        capital = sum(pay.capital for pay in pays)

        interest = sum(pay.interest for pay in pays)

        return dict(pays=pays, capital=capital, interest=interest)

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.resume')
    @validate(
        validators=dict(start=validators.DateTimeConverter(format='%d/%m/%Y'),
                        end=validators.DateTimeConverter(format='%d/%m/%Y')))
    def resume(self, start, end):

        """Crea un reporte de capital e intereses de todos los préstamos,
        incluidos los pagados"""

        pagos = list()
        pagos.extend(model.Pay.select(
            AND(model.Pay.q.day >= start, model.Pay.q.day <= end)))
        pagos.extend(model.OldPay.select(
            AND(model.OldPay.q.day >= start, model.OldPay.q.day <= end)))
        capital = sum(pay.capital for pay in pagos)
        interest = sum(pay.interest for pay in pagos)

        return dict(capital=capital, interest=interest, start=start, end=end)

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.diverge')
    @validate(validators=dict(payment=validators.String(),
                              start=validators.DateTimeConverter(
                                  format='%d/%m/%Y'),
                              end=validators.DateTimeConverter(
                                  format='%d/%m/%Y')))
    def diverge(self, payment, start, end):

        payed = model.PayedLoan.select(AND(model.PayedLoan.q.last >= start,
                                           model.PayedLoan.q.last <= end))

        payed = [p for p in payed if
                 len(p.affiliate.loans) > 0 and p.affiliate.payment == payment]

        payed = [p for p in payed if
                 p.affiliate.loans[0].get_payment() != p.payment]

        return dict(payed=payed)

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.payment')
    @validate(validators=dict(payment=validators.String()))
    def listPayment(self, payment):

        loans = model.Loan.select()

        return dict(loans=[l for l in loans if l.affiliate.payment == payment])

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.deducciones')
    @validate(
        validators=dict(start=validators.DateTimeConverter(format='%d/%m/%Y'),
                        end=validators.DateTimeConverter(format='%d/%m/%Y'),
                        casa=validators.Int()))
    def deducciones(self, start, end, casa):

        casa = model.Casa.get(casa)
        loans = model.Loan.select(AND(model.Loan.q.startDate >= start,
                                      model.Loan.q.startDate <= end,
                                      model.Loan.q.casa == casa))
        payedLoans = model.PayedLoan.select(
            AND(model.PayedLoan.q.startDate >= start,
                model.PayedLoan.q.startDate <= end,
                model.PayedLoan.q.casa == casa))

        interno = deduccionesInterno(loans, payedLoans, start, end)
        interno['casa'] = casa
        return interno

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.loan.deducciones')
    @validate(
        validators=dict(start=validators.DateTimeConverter(format='%d/%m/%Y')))
    def deduccionesDia(self, start):

        loans = model.Loan.selectBy(startDate=start)
        payedLoans = model.PayedLoan.selectBy(startDate=start)

        return deduccionesInterno(loans, payedLoans, start, start)

    @expose()
    def reconstruirSaldo(self):

        loans = model.Loan.select()

        for loan in loans:
            anterior = loan.debt
            loan.reconstruirSaldo()

        flash(u'Operacion Completada Exitósamente!')
        raise redirect('/loan')
