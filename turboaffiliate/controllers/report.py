# -*- coding: utf8 -*-
#
# report.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2007 - 2013 Carlos Flores <cafg10@gmail.com>
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

from decimal import Decimal
from collections import defaultdict

from turbogears import controllers, expose, identity, validate, validators

from turboaffiliate import model


months = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo',
    4: 'Abril', 5: 'Mayo', 6: 'Junio',
    7: 'Julio', 8: 'Agosto', 9: 'Septiembre',
    10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}


class Report(controllers.Controller):
    """Muestra varios Reportes acerca de los pagos, cuotas y estados financieros
    de los afiliados"""

    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.report.index")
    def index(self):
        return dict(accounts=model.Account.select(),
                    bancos=model.Banco.select(),
                    departamentos=model.Departamento.select())

    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.report.post")
    @validate(validators=dict(year=validators.Int(), month=validators.Int(
        min=1,
        max=12)))
    def postReport(self, year, month):

        """Muestra el reporte de ingresos por los diferentes cargos en un mes
        y año que se han adquirido desde Escalafón"""

        report = model.PostReport.selectBy(month=month, year=year).getOne()

        return dict(month=month, year=year, report=report)

    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.report.report")
    @validate(validators=dict(year=validators.Int(), month=validators.Int(
        min=1,
        max=12),
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
        loans = [loan for loan in loans if loan.affiliate.payment == payment]
        loand = dict()
        loand['amount'] = sum(loan.get_payment() for loan in loans)
        loand['count'] = len(loans)

        kw = dict()
        total = Decimal(0)
        accounts = model.Account.select()
        for account in accounts:
            kw[account] = dict()

            li = [extra for extra in account.extras
                  if extra.affiliate.payment == payment and
                     extra.affiliate.active == True]

            kw[account]['amount'] = sum(e.amount for e in li)
            kw[account]['count'] = len(li)
            total += kw[account]['amount']

        for account in accounts:
            if kw[account]['amount'] == 0:
                del kw[account]

        reintegros = model.Reintegro.selectBy(pagado=False)
        reintegro = dict()
        reintegro['count'] = reintegros.count()
        reintegro['amount'] = sum(r.monto for r in reintegros)
        total += reintegro['amount']

        return dict(deductions=kw, count=affiliates.count(),
                    obligation=obligation, legend=payment, loans=loand,
                    total=total, reintegro=reintegro)

    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.report.extra")
    @validate(validators=dict(account=validators.Int()))
    def extra(self, account):

        """Muestra los cobros a efectuar que corresponden a la cuenta
        especificada
        
        :param account:    Número de la cuenta a mostrar
        """

        account = model.Account.get(account)
        return dict(account=account, extras=account.extras)

    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.report.other")
    @validate(validators=dict(year=validators.Int(), month=validators.Int(
        min=1,
        max=12),
                              cotizacion=validators.String()))
    def cotizacion(self, year, month, cotizacion):

        """Muestra los cobros efectuados correspondientes a un mes y año con
        respecto a un tipo de pago"""

        cotizacion = model.Cotizacion.get(cotizacion)
        report = model.OtherReport.selectBy(cotizacion=cotizacion,
                                            year=year, month=month).getOne()
        return dict(month=month, year=year, report=report,
                    cotizacion=cotizacion)

    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.report.filiales")
    @validate(validators=dict(year=validators.Int(), month=validators.Int(
        min=1,
        max=12)))
    def filiales(self, year, month):

        affiliates = model.Affiliate.selectBy(payment="Escalafon")
        filiales = dict()

        for affiliate in affiliates:
            if affiliate.get_month(year, month):
                if not affiliate.departamento in filiales:
                    filiales[affiliate.departamento] = dict()

                if affiliate.school in filiales[affiliate.departamento]:
                    filiales[affiliate.departamento][affiliate.school] += 1
                    filiales[affiliate.departamento]['total'] += 1
                else:
                    filiales[affiliate.departamento][affiliate.school] = 1
                    filiales[affiliate.departamento]['total'] += 1

        return dict(filiales=filiales)

    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.report.filialres")
    @validate(validators=dict(departamento=validators.Int(),
                              year=validators.Int(),
                              start=validators.Int(min=1, max=12),
                              end=validators.Int(min=1, max=12)))
    def filialesResumen(self, departamento, year, start, end):

        """Muestra un reporte de Filiales de un :class:`Departamento` por mes
        y año de manera resumida"""

        departamento = model.Departamento.get(departamento)
        cotizacion = model.Cotizacion.get(1)
        afiliados = model.Affiliate.selectBy(cotizacion=cotizacion,
                                             departamento=departamento)
        filiales = dict()

        def iniciar_colegio(afiliado):
            filiales[afiliado.school] = defaultdict(int)

        def distribuir(afiliado):
            cantidad = 0
            for month in range(start, end + 1):
                if afiliado.get_month(year, month):
                    filiales[afiliado.school][month] += 1
                    cantidad += 1
            return cantidad

        map(iniciar_colegio, afiliados)

        cantidades = map(distribuir, afiliados)
        return dict(filiales=filiales, year=year, departamento=departamento,
                    start=start, end=end, cantidad=sum(cantidades))


    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.report.listafilial")
    @validate(validators=dict(departamento=validators.Int(),
                              year=validators.Int(),
                              month=validators.Int(min=1, max=12),
                              instituto=validators.UnicodeString()))
    def filialmensual(self, departamento, month, year, instituto):

        """Permite mostrar el listado de afiliados que cotizaron a una filial
        en un determinado mes y año"""

        departamento = model.Departamento.get(departamento)
        afiliados = model.Affiliate.selectBy(school=instituto,
                                             departamento=departamento)
        listado = list()
        for afiliado in afiliados:

            colegiacion = model.CuotaTable.selectBy(affiliate=afiliado,
                                                    year=year).getOne()
            if getattr(colegiacion, "month{0}".format(month)):
                listado.append(afiliado)

        return dict(afiliados=listado, month=month, year=year,
                    instituto=instituto, departamento=departamento)

    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.report.filialesdept")
    @validate(validators=dict(departamento=validators.Int(),
                              year=validators.Int(),
                              month=validators.Int(min=1, max=12)))
    def filialesDept(self, departamento, month, year):

        """Muestra todas las Filiales de un Departamento con sus respectivos
        miembros"""

        departamento = model.Departamento.get(departamento)
        cotizacion = model.Cotizacion.get(1)
        afiliados = model.Affiliate.selectBy(cotizacion=cotizacion,
                                             departamento=departamento)
        filiales = dict()

        for afiliado in afiliados:
            if afiliado.get_month(year, month):
                if afiliado.school in filiales:
                    filiales[afiliado.school].append(afiliado)
                else:
                    filiales[afiliado.school] = list()
                    filiales[afiliado.school].append(afiliado)

        return dict(filiales=filiales, departamento=departamento)

    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.report.planilla")
    @validate(validators=dict(cotizacion=validators.Int(),
                              day=validators.DateTimeConverter(
                                  format='%d/%m/%Y')))
    def planilla(self, cotizacion, day):

        cotizacion = model.Cotizacion.get(cotizacion)

        return dict(cotizacion=cotizacion, day=day,
                    afiliados=model.Affiliate.selectBy(cotizacion=cotizacion,
                                                       active=True))

    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.report.banco")
    @validate(validators=dict(banco=validators.Int(), year=validators.Int(),
                              month=validators.Int(min=1, max=12)))
    def banco(self, banco, month, year):

        banco = model.Banco.get(banco)
        
        deducciones = model.DeduccionBancaria.selectBy(banco=banco, year=year,
                                                       month=month)
        cuentas = dict()

        for deduccion in deducciones:

            if deduccion.account in cuentas:
                cuentas[deduccion.account] += deduccion.amount
            else:
                cuentas[deduccion.account] = deduccion.amount

        total = sum(cuentas[c] for c in cuentas)

        return dict(banco=banco, month=month, year=year, cuentas=cuentas,
                    total=total)


    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.report.deduced")
    @validate(validators=dict(account=validators.Int(), year=validators.Int(),
                              month=validators.Int(min=1, max=12)))
    def deduced(self, account, month, year):

        account = model.Account.get(account)

        deduced = model.Deduced.selectBy(account=account,
                                         year=year, month=month)

        total = sum(d.amount for d in deduced)

        return dict(deduced=deduced, account=account, month=months[month],
                    year=year, total=total)


    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.report.deducedBank")
    @validate(validators=dict(account=validators.Int(), year=validators.Int(),
                              month=validators.Int(min=1, max=12)))
    def deducedBank(self, account, month, year):

        account = model.Account.get(account)

        deduced = model.DeduccionBancaria.selectBy(account=account,
                                                   year=year, month=month)

        total = sum(d.amount for d in deduced)

        return dict(deduced=deduced, account=account, month=months[month],
                    year=year, total=total)

    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.report.payment")
    @validate(validators=dict(account=validators.Int(), year=validators.Int(),
                              month=validators.Int(min=1, max=12),
                              payment=validators.String()))
    def deducedPayment(self, account, month, year, payment):

        deduced = model.Deduced.selectBy(account=account, year=year,
                                         month=month)
        deduced = [d for d in deduced if d.affiliate.payment == payment]
        total = sum(d.amount for d in deduced if d.affiliate.payment == payment)

        return dict(deduced=deduced, account=account, month=months[month],
                    year=year, total=total, payment=payment)

    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.affiliate.show")
    @validate(validators=dict(year=validators.Int(),
                              payment=validators.String()))
    def empty(self, year, payment):

        tables = model.CuotaTable.selectBy(year=year)

        affiliates = list()
        for table in tables:

            if not table.empty() and table.affiliate.payment == payment:
                affiliates.append(table.affiliate)

        return dict(affiliates=affiliates,
                    show="Cotizan por {0} y pagaron un mes en {1}".format(
                        payment,
                        year),
                    count=len(affiliates))

    @expose(template="turboaffiliate.templates.affiliate.show")
    @validate(validators=dict(year=validators.Int(), month=validators.Int(
        min=1,
        max=12)))
    def aportaron(self, year, month):

        cuotas = model.CuotaTable.selectBy(year=year, month=month)
        show = u"que Cotizaron en {0} de {1}".format(month, year)

        affiliates = [c.affiliate for c in cuotas]
        return dict(affiliates=affiliates, show=show, count=len(affiliates))

    @expose(template="turboaffiliate.templates.affiliate.show")
    @validate(validators=dict(year=validators.Int(), month=validators.Int(
        min=1,
        max=12)))
    def noAportaron(self, year, month):

        cuotas = model.CuotaTable.selectBy(year=year, month=month)
        show = u"que no Cotizaron en {0} de {1}".format(month, year)

        affiliates = [c.affiliate for c in cuotas]
        return dict(affiliates=affiliates, show=show, count=len(affiliates))

    @expose(template="turboaffiliate.templates.affiliate.show")
    @validate(validators=dict(year=validators.Int(), month=validators.Int(
        min=1,
        max=12)))
    def conTabla(self, year, month):

        cuotas = model.CuotaTable.selectBy(year=year)

        affiliates = [c.affiliate for c in cuotas if c.affiliate.active]
        show = "que Cotizaron en {0} de {1}".format(month, year)
        return dict(affiliates=affiliates, show=show, count=len(affiliates))

