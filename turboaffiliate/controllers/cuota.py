# -*- coding: utf8 -*-
#
# cuota.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2009 - 2011 Carlos Flores <cafg10@gmail.com>
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

from datetime import date

from turbogears import (controllers, expose, identity, redirect, validate,
                        validators, flash)

from turboaffiliate import model


def log(user, message, affiliate):
    """Guarda un mensaje en el registro del sistema"""

    log = {'user': user, 'action': message, 'affiliate': affiliate}
    model.Logger(**log)


class Cuota(controllers.Controller):
    def log(self, message, user):
        log = dict()
        log['user'] = user
        log['action'] = message
        model.Logger(**log)

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.cuota.affiliate')
    @validate(validators=dict(affiliate=validators.Int()))
    def default(self, affiliate):

        return dict(affiliate=model.Affiliate.get(affiliate), day=date.today())

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(
        validators=dict(affiliate=validators.Int(), start=validators.Int(),
                        end=validators.Int()))
    def fill(self, affiliate, start, end):

        affiliate = model.Affiliate.get(affiliate)
        if end > date.today().year:
            end = start

        log(identity.current.user,
            u"Posteo aportaciones de  {0} a {1} afiliado {2}".format(start, end,
                                                                     affiliate.id),
            affiliate)

        for n in range(start, end + 1):
            [affiliate.pay_cuota(n, month) for month in range(1, 13)]

        raise redirect('/affiliate/cuota/{0}'.format(affiliate.id))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(id=validators.Int()))
    def remove(self, id):

        table = model.CuotaTable.get(id)
        affiliate = table.affiliate
        table.destroySelf()
        raise redirect('/affiliate/cuota/{0}'.format(affiliate.id))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(id=validators.Int()))
    def removecompliment(self, id):

        table = model.AutoSeguro.get(id)
        affiliate = table.affiliate
        table.destroySelf()
        raise redirect('/affiliate/cuota/{0}'.format(affiliate.id))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose(template='turboaffiliate.templates.affiliate.cuota.edit')
    @validate(validators=dict(code=validators.Int()))
    def edit(self, code):

        """Muestra el formulario de edicion de un año de aportaciones
        
        :param code: identificador de la Tabla de Aportaciones
        """

        return dict(table=model.CuotaTable.get(code))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose(template='turboaffiliate.templates.affiliate.cuota.editcompliment')
    @validate(validators=dict(code=validators.Int()))
    def editcompliment(self, code):

        """Muestra el formulario de edicion de un año de aportaciones

        :param code: identificador de la Tabla de Aportaciones
        """

        return dict(table=model.AutoSeguro.get(code))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(id=validators.Int(),
                              month1=validators.Bool(),
                              month2=validators.Bool(),
                              month3=validators.Bool(),
                              month4=validators.Bool(),
                              month5=validators.Bool(),
                              month6=validators.Bool(),
                              month7=validators.Bool(),
                              month8=validators.Bool(),
                              month9=validators.Bool(),
                              month10=validators.Bool(),
                              month11=validators.Bool(),
                              month12=validators.Bool()))
    def change(self, id, **kw):

        table = model.CuotaTable.get(id)
        for n in range(1, 13):
            try:
                setattr(table, "month{0}".format(n), kw["month{0}".format(n)])
            except KeyError:
                setattr(table, "month{0}".format(n), False)

        log(identity.current.user,
            u"Cambio en aportaciones año {0} afiliado {1} {2}".format(
                table.year,
                table.affiliate.id, table),
            table.affiliate)

        raise redirect('/affiliate/cuota/{0}'.format(table.affiliate.id))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(validators=dict(id=validators.Int(),
                              month1=validators.Bool(),
                              month2=validators.Bool(),
                              month3=validators.Bool(),
                              month4=validators.Bool(),
                              month5=validators.Bool(),
                              month6=validators.Bool(),
                              month7=validators.Bool(),
                              month8=validators.Bool(),
                              month9=validators.Bool(),
                              month10=validators.Bool(),
                              month11=validators.Bool(),
                              month12=validators.Bool()))
    def changecompliment(self, id, **kw):

        table = model.AutoSeguro.get(id)
        for n in range(1, 13):
            try:
                setattr(table, "month{0}".format(n), kw["month{0}".format(n)])
            except KeyError:
                setattr(table, "month{0}".format(n), False)

        log(identity.current.user,
            u"Cambio en complemento año {0} afiliado {1} {2}".format(
                table.year,
                table.affiliate.id, table),
            table.affiliate)

        raise redirect('/affiliate/cuota/{0}'.format(table.affiliate.id))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(
        validators=dict(affiliate=validators.Int(), year=validators.Int()))
    def addYear(self, affiliate, year):

        affiliate = model.Affiliate.get(affiliate)
        affiliate.complete(year)

        raise redirect('/affiliate/cuota/{0}'.format(affiliate.id))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose()
    @validate(
        validators=dict(affiliate=validators.Int(), year=validators.Int()))
    def addcompliment(self, affiliate, year):

        affiliate = model.Affiliate.get(affiliate)
        affiliate.complete_compliment(year)

        raise redirect('/affiliate/cuota/{0}'.format(affiliate.id))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose('json')
    @validate(validators=dict(afiliado=validators.Int(), anio=validators.Int(),
                              mes=validators.Int(),
                              redir=validators.UnicodeString()))
    def pagar(self, afiliado, mes, anio, redir):

        afiliado = model.Affiliate.get(afiliado)
        afiliado.pay_cuota(anio, mes)
        log(identity.current.user,
            u"Pago Aportaciones año {0} mes {1} afiliado {2} "
            u"0".format(anio, mes, afiliado.id),
            afiliado)

        flash(u'Pagadas Aportaciones de {0} de {1}'.format(mes, anio))

        raise redirect('/affiliate/{0}{1}'.format(redir, afiliado.id))

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose('json')
    @validate(validators=dict(afiliado=validators.Int(), anio=validators.Int(),
                              meses=validators.UnicodeString(),
                              redir=validators.UnicodeString()))
    def pagarVarias(self, afiliado, meses, anio, redir):

        """Permite pagar varios meses en una sola operación"""

        afiliado = model.Affiliate.get(afiliado)
        for mes in meses.split():
            afiliado.pay_cuota(anio, int(mes))
            log(identity.current.user,
                u"Pago Aportaciones año {0} mes {1} afiliado {2} "
                u"0".format(anio, mes, afiliado.id), afiliado)

        flash(u'Pagadas Aportaciones de {0} de {1}'.format(meses, anio))

        raise redirect(redir)

    @identity.require(identity.All(identity.in_any_group('admin', 'operarios'),
                                   identity.not_anonymous()))
    @expose('json')
    @validate(
        validators=dict(afiliado=validators.Int(), cuenta=validators.Int(),
                        day=validators.DateTimeConverter(format='%d/%m/%Y')))
    def pagoPlanilla(self, afiliado, cuenta, day):

        """Permite registrar un pago mediante planilla utilizando llamadas
        en JSON"""

        affiliate = model.Affiliate.get(afiliado)
        cuenta = model.Account.get(cuenta)
        affiliate.pay_cuota(day.year, day.month)

        deduccion = {'account': cuenta, 'month': day.month, 'year': day.year,
                     'affiliate': affiliate, 'amount': affiliate.get_cuota(day),
                     'cotizacion': affiliate.cotizacion}
        model.Deduced(**deduccion)

        log(identity.current.user,
            u"Pago por Planilla de cuota de aportaciones afiliado {0}".format(
                affiliate.id), affiliate)

        return dict(pago=affiliate.get_cuota(day))
