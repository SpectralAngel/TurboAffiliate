# -*- coding: utf8 -*-
#
# billing.py
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

from turbogears import controllers, identity
from turbogears import expose, validate, validators
from sqlobject.sqlbuilder import AND

from turboaffiliate import model


class Billing(controllers.Controller):
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.billing.index')
    def index(self):

        return dict()

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.billing.status')
    @validate(validators=dict(departamento=validators.Int()))
    def state(self, departamento):

        """Muestra los estados de cuenta de aportaciones de los afiliados de un
        Departamento

        :param departamento: El identificador del :class:`Departamento` a
        mostrar
        """

        departamento = model.Departamento.get(departamento)
        affiliates = model.Affiliate.selectBy(departamento=departamento)

        return dict(affiliates=affiliates, day=date.today())

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.billing.status')
    @validate(validators=dict(payment=validators.String()))
    def payment(self, payment):

        affiliates = model.Affiliate.selectBy(payment=payment)
        affiliates = (a for a in affiliates if a.joined != None)

        return dict(affiliates=affiliates, day=date.today())

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.billing.status')
    @validate(validators=dict(school=validators.String()))
    def school(self, school):

        affiliates = model.Affiliate.selectBy(school=school)
        affiliates = (a for a in affiliates if a.joined != None)

        return dict(affiliates=affiliates, day=date.today())

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.billing.status')
    @validate(validators=dict(start=validators.Int(), end=validators.Int))
    def rango(self, start, end):

        affiliates = model.Affiliate.select(AND(model.Affiliate.q.id >= start,
                                                model.Affiliate.q.id <= end))
        affiliates = (a for a in affiliates if a.joined != None)

        return dict(affiliates=affiliates, day=date.today())

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.billing.loans')
    @validate(validators=dict(departamento=validators.Int()))
    def loanState(self, departamento):

        """Muestra los estados de cuenta préstamos de los afiliados de un
        departamento

        :param departamento: El identificador del :class:`Departamento` a
        mostrar"""

        departamento = model.Departamento.get(departamento)
        affiliates = model.Affiliate.selectBy(departamento=departamento)
        loans = list()
        for affiliate in affiliates:
            loans.extend(affiliate.loans)

        return dict(loans=loans, day=date.today())

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.billing.loans')
    @validate(validators=dict(school=validators.String()))
    def loanSchool(self, school):

        """Muestra los estados de cuenta préstamos de los afiliados de un
        departamento

        :param school: El colegio a mostrar """

        affiliates = model.Affiliate.selectBy(school=school)
        loans = list()
        for affiliate in affiliates:
            loans.extend(affiliate.loans)

        return dict(loans=loans, day=date.today())
