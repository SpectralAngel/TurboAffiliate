# -*- coding: utf8 -*-
#
# elecciones.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2009 - 2012 Carlos Flores <cafg10@gmail.com>
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

from turbogears import controllers, identity, expose, validate, validators
from turboaffiliate import model
from sqlobject.sqlbuilder import AND
from collections import defaultdict


def municipios(urnas, municipio):
    urnas[municipio] = defaultdict(dict)


def asignar(urnas, afiliado):
    if afiliado.school in urnas[afiliado.municipio]:
        urnas[afiliado.municipio][afiliado.school].append(afiliado)
    else:
        urnas[afiliado.municipio][afiliado.school] = list()
        urnas[afiliado.municipio][afiliado.school].append(afiliado)


def filtrar_urnas(afiliados):
    urnas = defaultdict(int)
    urnas['Sin Instituto'] = 0
    for afiliado in afiliados:
        urnas[afiliado.school] += 1

    if None in urnas:
        urnas['Sin Instituto'] += urnas[None]
        del urnas[None]
    if '' in urnas:
        urnas['Sin Instituto'] += urnas['']
        del urnas['']
    return urnas


class Elecciones(controllers.Controller):
    @identity.require(identity.not_anonymous())
    @expose(template="turboaffiliate.templates.elecciones.index")
    def index(self):
        return dict()

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.listado')
    def all(self):

        affiliates = model.Affiliate.select(AND(
            model.Affiliate.q.firstName != None,
            model.Affiliate.q.lastName != None,
            model.Affiliate.q.active == True))
        return dict(affiliates=affiliates, count=affiliates.count())

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.institutoDepto')
    @validate(validators=dict(departamento=validators.Int()))
    def stateSchool(self, departamento):

        departamento = model.Departamento.get(departamento)
        # cambiar por seleccion de cotizacion
        cotizacion = model.Cotizacion.get(1)
        afiliados = model.Affiliate.selectBy(departamento=departamento,
                                             cotizacion=cotizacion,
                                             active=True)

        schools = dict()
        for affiliate in afiliados:
            if affiliate.school in schools:
                schools[affiliate.school].append(affiliate)
            else:
                schools[affiliate.school] = list()
                schools[affiliate.school].append(affiliate)

        return dict(departamento=departamento, schools=schools)

    def urnas_departamentales_interno(self, departamento):
        departamento = model.Departamento.get(departamento)
        # cambiar por seleccion de cotizacion
        cotizacion = model.Cotizacion.get(1)
        afiliados = model.Affiliate.selectBy(departamento=departamento,
                                             cotizacion=cotizacion,
                                             active=True)
        urnas = filtrar_urnas(afiliados)
        return urnas, afiliados, departamento

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.urnas')
    @validate(validators=dict(departamento=validators.Int()))
    def urnasDepartamentales(self, departamento):

        urnas, afiliados, departamento = self.urnas_departamentales_interno(
            departamento)

        return dict(urnas=urnas, cantidad=afiliados.count(),
                    departamento=departamento)

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.urnas')
    @validate(validators=dict(departamento=validators.Int()))
    def urnasDepartamentalesCinco(self, departamento):

        urnas, afiliados, departamento = self.urnas_departamentales_interno(
            departamento)

        for instituto in urnas.keys():

            if urnas[instituto] < 5:
                del urnas[instituto]

        return dict(urnas=urnas, cantidad=sum(urnas[i] for i in urnas),
                    departamento=departamento)

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.acta')
    @validate(validators=dict(departamento=validators.Int()))
    def actas(self, departamento):

        return self.urnasDepartamentalesCinco(departamento)

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.municipios')
    @validate(validators=dict(departamento=validators.Int()))
    def urnasMunicipio(self, departamento):

        departamento = model.Departamento.get(departamento)
        cotizacion = model.Cotizacion.get(1)
        afiliados = model.Affiliate.selectBy(departamento=departamento,
                                             cotizacion=cotizacion,
                                             active=True)
        urnas = defaultdict(lambda: defaultdict(list))

        map(lambda m: municipios(urnas, m), departamento.municipios)

        map(lambda a: asignar(urnas, a), afiliados)

        cantidadUrnas = sum(len(urnas[m]) for m in urnas)

        return dict(urnas=urnas, departamento=departamento,
                    cantidad=afiliados.count(),
                    cantidadUrnas=cantidadUrnas)

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.urnasMunicipios')
    @validate(validators=dict(departamento=validators.Int()))
    def listaUrnasMunicipio(self, departamento):

        departamento = model.Departamento.get(departamento)
        cotizacion = model.Cotizacion.get(1)
        afiliados = model.Affiliate.selectBy(departamento=departamento,
                                             cotizacion=cotizacion,
                                             active=True)
        urnas = defaultdict(lambda: defaultdict(list))

        map(lambda m: municipios(urnas, m), departamento.municipios)

        map(lambda a: asignar(urnas, a), afiliados)

        for municipio in urnas:

            especial = list()
            for instituto in urnas[municipio].keys():
                if len(urnas[municipio][instituto]) < 5:
                    especial.extend(urnas[municipio][instituto])
                    del urnas[municipio][instituto]
            urnas[municipio]['Urna Especial'] = especial

        return dict(urnas=urnas, departamento=departamento,
                    cantidad=afiliados.count())

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.urnas')
    def totalUrnas(self):

        cotizacion = model.Cotizacion.get(1)
        afiliados = model.Affiliate.selectBy(cotizacion=cotizacion,
                                             active=True)

        urnas = filtrar_urnas(afiliados)

        for instituto in urnas.keys():

            if urnas[instituto] < 5:
                del urnas[instituto]

        return dict(urnas=urnas, cantidad=sum(urnas[i] for i in urnas),
                    departamento="Total de Urnas")

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.listado')
    @validate(validators=dict(cotizacion=validators.Int()))
    def cotizacion(self, cotizacion):

        cotizacion = model.Cotizacion.get(cotizacion)
        afiliados = model.Affiliate.selectBy(active=True, cotizacion=cotizacion)
        motivo = u'{0}'.format(cotizacion.nombre)

        return dict(affiliates=afiliados, count=afiliados.count(),
                    motivo=motivo)

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.listado')
    @validate(validators=dict(cotizacion=validators.Int(),
                              departamento=validators.Int()))
    def cotizacionDepto(self, cotizacion, departamento):

        cotizacion = model.Cotizacion.get(cotizacion)
        departamento = model.Departamento.get(departamento)
        afiliados = model.Affiliate.selectBy(active=True, cotizacion=cotizacion,
                                             departamento=departamento)
        motivo = u'{0} {1}'.format(cotizacion.nombre, departamento.nombre)

        return dict(affiliates=afiliados, count=afiliados.count(),
                    motivo=motivo)

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.departamento')
    @validate(validators=dict(departamento=validators.Int()))
    def departamento(self, departamento):

        departamento = model.Departamento.get(departamento)
        afiliados = model.Affiliate.selectBy(departamento=departamento,
                                             active=True)

        return dict(afiliados=afiliados, departamento=departamento,
                    cantidad=afiliados.count())

    def sinInstituto(self):

        afiliados = model.Affiliate.selectBy(active=True, school=None)

        return dict(afiliados=afiliados)

    def sinIdentidad(self):

        afiliados = model.Affiliate.selectBy(active=True, cardID=None)

        return dict(afiliados=afiliados)

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.elecciones.departamentos')
    def resumenUrnas(self):

        departamentos = dict()

        for n in range(1, 19):
            resultado = self.urnasDepartamentalesCinco(n)
            departamentos[resultado['departamento']] = len(resultado['urnas'])

        return dict(departamentos=departamentos)
