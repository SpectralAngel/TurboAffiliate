# -*- coding: utf8 -*-
#
# affiliate.py
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

from datetime import date
from decimal import Decimal
import csv

from turbogears import (controllers, flash, redirect, identity, expose,
                        validate, validators, error_handler)
from sqlobject.sqlbuilder import OR, AND
from sqlobject import SQLObjectNotFound

from turboaffiliate import model
from turboaffiliate.controllers import (cuota, extra, billing, deduced,
                                        observacion)


def log(user, message, affiliate):
    """Guarda un mensaje en el registro del sistema"""

    log = {}
    log['user'] = user
    log['action'] = message
    log['affiliate'] = affiliate
    model.Logger(**log)


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

        return dict(cuentas=model.Account.select(), bancos=model.Banco.select())

    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.error')
    def error(self, tg_errors=None):

        if tg_errors:
            errors = [(param, inv.msg, inv.value) for param, inv in
                      tg_errors.items()]
            return dict(errors=errors)

        return dict(errors=u"Desconocido")

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.affiliate')
    @validate(validators=dict(affiliate=validators.Int()))
    def default(self, affiliate):

        """Permite mostrar un afiliado mediante su numero de afiliación
        
        :param affiliate: Número de afiliación
        """

        return dict(affiliate=model.Affiliate.get(affiliate),
                    accounts=model.Account.select(),
                    departamentos=model.Departamento.select(),
                    bancos=model.Banco.select())

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.edit')
    @validate(validators=dict(affiliate=validators.Int()))
    def edit(self, affiliate):

        """Permite mostrar un afiliado mediante su numero de afiliación

        :param affiliate: Número de afiliación
        """

        return dict(affiliate=model.Affiliate.get(affiliate),
                    accounts=model.Account.select(),
                    departamentos=model.Departamento.select(),
                    bancos=model.Banco.select())

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.affiliate')
    @validate(validators=dict(affiliate=validators.Int()))
    def afiliado(self, affiliate):

        """Permite mostrar un afiliado mediante su numero de afiliación
        
        :param affiliate: Número de afiliación
        """

        return self.default(affiliate)

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.autorizacion')
    @validate(validators=dict(affiliate=validators.Int()))
    def autorizacion(self, affiliate):

        """Permite mostrar un afiliado mediante su numero de afiliación
        
        :param affiliate: Número de afiliación
        """

        return dict(affiliate=model.Affiliate.get(affiliate), day=date.today())

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(cardID=validators.String()))
    def card(self, cardID):

        """Permite mostrar un afiliado mediante su numero de Identidad
        
        :param cardID: Número de Identidad
        """
        try:
            affiliate = model.Affiliate.selectBy(cardID=cardID).limit(
                1).getOne()

        except SQLObjectNotFound:
            flash(u'No se encontró la identidad {0}'.format(cardID))
            raise redirect('/affiliate')

        raise redirect('/affiliate/{0}'.format(affiliate.id))

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.search')
    @validate(validators=dict(cobro=validators.String()))
    def cobro(self, cobro):

        """Muestra un afiliado mediante su número de cobro de UPN o INPREMA
        
        :param cobro:    Número de empleado o jubilación a buscar
        """

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
        inprema=validators.UnicodeString(),
        email=validators.UnicodeString(),
        municipio=validators.Int(),
        departamento=validators.Int(),
        cotizacion=validators.Int(),
        banco=validators.Int()
    ))
    def save(self, municipio, departamento, cotizacion, **kw):

        """Permite guardar los datos del afiliado
        
        :param municipio: Código del municipio del afiliado
        :param departamento: Código del departamento del afiliado
        :param kw: Diccionario conteniendo el resto de la información
        """

        municipio = model.Municipio.get(municipio)
        departamento = model.Departamento.get(departamento)
        cotizacion = model.Cotizacion.get(cotizacion)

        if kw['cardID'] == '':
            flash(u'No se escribio un número de identidad')
            raise redirect('/affiliate')
        try:
            # Se esta actualizando un afiliado
            affiliate = model.Affiliate.get(int(kw['affiliate']))

            # Logs del sistema
            log(identity.current.user,
                u"Modificado el afiliado {0}".format(affiliate.id), affiliate)

            del kw['affiliate']

            for key in kw:
                setattr(affiliate, key, kw[key])
            affiliate.departamento = departamento
            affiliate.municipio = municipio
            affiliate.cotizacion = cotizacion
            flash(u'¡El afiliado ha sido actualizado!')

        except KeyError:

            # Se esta creando un nuevo afiliado
            kw['cotizacion'] = cotizacion
            kw['departamento'] = departamento
            kw['municipio'] = municipio
            affiliate = model.Affiliate(**kw)
            affiliate.complete(date.today().year)
            affiliate.departamento = departamento
            affiliate.municipio = municipio
            affiliate.cotizacion = cotizacion

            log(identity.current.user,
                u"Agregado el afiliado {0}".format(affiliate.id), affiliate)

            flash(u'¡El afiliado ha sido guardado!')

        raise redirect('/affiliate/{0}'.format(affiliate.id))

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int()))
    def remove(self, affiliate):

        """Elimina un afiliado permanentemente
        
        :param affiliate:    Número de afiliación a eliminar
        """

        affiliate = model.Affiliate.get(affiliate)

        for loan in affiliate.loans:
            loan.remove()

        for cuota in affiliate.cuotaTables:
            cuota.destroySelf()

        log(identity.current.user,
            u"Eliminado el afiliado {0}".format(affiliate.id), affiliate)

        affiliate.destroySelf()
        flash(u'El afiliado ha sido removido!')

        raise redirect('/affiliate')

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.search')
    @validate(validators=dict(name=validators.UnicodeString()))
    def search(self, name):

        """Permite efectuar una busqueda por nombre o apellido
        
        :param name: El nombre o apellido a buscar 
        """

        if name == '':
            flash(u'Ingrese un nombre')
            raise redirect('/affiliate')

        affiliates = model.Affiliate.select(OR(
            model.Affiliate.q.firstName.contains(name),
            model.Affiliate.q.lastName.contains(name)))
        return dict(result=affiliates)

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.search')
    @validate(validators=dict(cardID=validators.String()))
    def byCardID(self, cardID):

        """Permite buscar afiliados mediante número de identidad
        
        :param cardID: Número de identidad"""

        return dict(affiliates=model.Affiliate.selectBy(cardID=cardID))

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.report')
    @validate(validators=dict(departamento=validators.Int()))
    def departamento(self, departamento):

        """Muestra los afiliados de un departamento seleccionado
        
        :param departamento: Identificador del departamento seleccionado
        """

        departamento = model.Departamento.get(departamento)

        affiliates = model.Affiliate.selectBy(departamento=departamento)
        count = affiliates.count()
        return dict(affiliates=affiliates, departamento=departamento,
                    count=count)

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.card')
    @validate(validators=dict(affiliate=validators.UnicodeString()))
    def byRange(self, cardID):

        """Permite buscar afiliados utilizando números de identidad parciales
        
        :param cardID: Número de identidad
        """

        affiliates = model.Affiliate.select(
            model.Affiliate.q.cardID.contains(cardID))

        return dict(affiliates=affiliates, cardID=cardID,
                    count=affiliates.count())

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.report')
    @validate(validators=dict(affiliate=validators.Int(), end=validators.Int(),
                              begin=validators.Int()))
    def aList(self, begin, end):

        affiliates = model.Affiliate.select(AND(model.Affiliate.q.id >= begin,
                                                model.Affiliate.q.id <= end))
        return dict(affiliates=affiliates, count=affiliates.count())

    @error_handler(index)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.affiliate')
    def last(self):

        """Muestra el último afiliado que se ingreso al sistema"""

        return dict(affiliate=model.Affiliate.select(orderBy="-id"
        ).limit(1).getOne())

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int(),
                              day=validators.DateTimeConverter(
                                  format='%d/%m/%Y'),
                              reason=validators.UnicodeString()))
    def deactivate(self, affiliate, reason, day):

        """Desactiva el afiliado justificando la razon
        
        :param affiliate: Número de afiliación a desactivar
        :param reason:    Justificación de la desactivación
        :param day:       Fecha en que se realiza la desactivación
        """

        affiliate = model.Affiliate.get(affiliate)
        affiliate.active = False
        affiliate.reason = reason
        affiliate.desactivacion = day

        log(identity.current.user,
            u"Desactivado el afiliado {0}".format(affiliate.id), affiliate)

        raise redirect('/affiliate/{0}'.format(affiliate.id))

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int(),
                              muerte=validators.DateTimeConverter(
                                  format='%d/%m/%Y')))
    def fallecimiento(self, affiliate, muerte):

        """Desactiva el Afiliado indicando la fecha de muerte y estableciendo la
        fecha de proceso con el día en que se ingresa el incidente
        
        :param affiliate: El número de afiliación
        :param muerte:    Fecha de fallecimiento del Afiliado
        """

        affiliate = model.Affiliate.get(affiliate)
        affiliate.active = False
        affiliate.reason = "Fallecimiento"
        affiliate.muerte = muerte
        affiliate.desactivacion = date.today()

        log(identity.current.user,
            u"Afiliado {0} reportado como fallecido".format(affiliate.id), affiliate)

        raise redirect('/affiliate/{0}'.format(affiliate.id))

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int()))
    def activate(self, affiliate):

        """Reactiva un afiliado para que pueda continuar participando
        
        :param affiliate: El número de afiliación
        """

        affiliate = model.Affiliate.get(affiliate)
        affiliate.active = True
        log(identity.current.user,
            u"Activado el afiliado {0}".format(affiliate.id), affiliate)

        raise redirect('/affiliate/{0}'.format(affiliate.id))

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.payment')
    @validate(validators=dict(cotizacion=validators.Int()))
    def cotizacion(self, cotizacion):

        cotizacion = model.Cotizacion.get(cotizacion)
        affiliates = model.Affiliate.selectBy(cotizacion=cotizacion).orderBy("lastName")
        return dict(affiliates=affiliates, count=affiliates.count(),
                    cotizacion=cotizacion)

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.age')
    @validate(validators=dict(joined=validators.Int(), age=validators.Int()))
    def age(self, joined, age):

        """Muestra los afiliados por edad hasta un determinado año de afiliacion
        
        :param joined:  El año máximo de afiliación
        :param age:     La edad de los afiliados a buscar
        """

        day = date.today().year - age
        afiliacion = date(joined + 1, 1, 1)
        affiliates = model.Affiliate.select(AND(
            model.Affiliate.q.birthday >= day,
            model.Affiliate.q.joined <= afiliacion))

        return dict(affiliates=affiliates)

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    @validate(
        validators=dict(start=validators.DateTimeConverter(format='%d/%m/%Y'),
                        end=validators.DateTimeConverter(format='%d/%m/%Y')))
    def byDate(self, start, end):

        """Muestra los afiliados que se unieron en un periodo
        
        :param start:  Fecha inicial
        :param end:    Fecha Final 
        """

        affiliates = model.Affiliate.select(AND(
            model.Affiliate.q.joined >= start,
            model.Affiliate.q.joined <= end))
        return dict(affiliates=affiliates, start=start, end=end,
                    show="Fecha de Afiliaci&oacute;n", count=affiliates.count())

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    @validate(validators=dict(town=validators.UnicodeString()))
    def byTown(self, town):

        affiliates = model.Affiliate.selectBy(town=town)
        return dict(affiliates=affiliates, show="Municipio",
                    count=affiliates.count())

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    @validate(validators=dict(school=validators.UnicodeString(),
                              departamento=validators.Int()))
    def bySchool(self, school, departamento):

        """Filtra los afiliados mediante departamento e Instituto
        
        :param school: Nombre del Instituto a buscar
        :param departamento: Código del departamento a buscar
        """

        departamento = model.Departamento.get(departamento)
        affiliates = model.Affiliate.select(
            AND(model.Affiliate.school == school,
                model.Affiliate.q.departamento))

        return dict(affiliates=affiliates, show=u"Instituto",
                    count=affiliates.count())

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    def disabled(self):

        """Muestra los afiliados deshabilitados"""

        affiliates = model.Affiliate.selectBy(active=False)
        return dict(affiliates=affiliates, show="Inhabilitados",
                    count=affiliates.count())

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    def all(self):

        """Muestra todos los afiliados"""

        affiliates = model.Affiliate.select()
        return dict(affiliates=affiliates, show="Todos",
                    count=affiliates.count())

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.planilla')
    @validate(validators=dict(cotizacion=validators.Int(),
                              prestamos=validators.Int(),
                              aportaciones=validators.Int(),
                              excedente=validators.Int(),
                              day=validators.DateTimeConverter(
                                  format='%d/%m/%Y')))
    def planilla(self, cotizacion, day, aportaciones, prestamos, excedente):

        cotizacion = model.Cotizacion.get(cotizacion)
        affiliates = model.Affiliate.select(
            model.Affiliate.q.cotizacion == cotizacion,
            orderBy=cotizacion.ordering)

        return dict(afiliados=affiliates, cotizacion=cotizacion,
                    excedente=excedente, aportaciones=aportaciones,
                    prestamos=prestamos, day=day)

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.debt')
    @validate(validators=dict(payment=validators.UnicodeString()))
    def debt(self, payment):

        affiliates = model.Affiliate.selectBy(payment=payment)
        return dict(affiliates=affiliates, show=payment,
                    count=affiliates.count())

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    @validate(validators=dict(year=validators.Int()))
    def solvent(self, year):

        affiliates = model.Affiliate.select()
        affiliates = [affiliate for affiliate in affiliates
                      if affiliate.multisolvent(year)]
        show = u"Solventes al {0}".format(year)
        return dict(affiliates=affiliates, show=show, count=len(affiliates))

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.year')
    def solventYear(self):

        """Calcula la cantidad de afiliados solventes en todos los años"""

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
        show = u"Sin Año de Afiliación"
        return dict(affiliates=affiliates, show=show, count=affiliates.count())

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.show')
    def noCard(self):

        affiliates = model.Affiliate.selectBy(cardID=None)
        show = u"Sin Número de identidad"
        return dict(affiliates=affiliates, show=show, count=affiliates.count())

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int(),
                              jubilated=validators.DateTimeConverter(
                                  format='%d/%m/%Y'),
                              cobro=validators.Int(),
                              cotizacion=validators.Int()))
    def jubilar(self, affiliate, jubilated, cobro, cotizacion):

        """Permite pasar al afiliado al modo de cobro para jubilados y
        pensionados a los cuales se les deduce una cantidad menor
        
        :param affiliate: Número de afiliación
        """

        affiliate = model.Affiliate.get(affiliate)
        affiliate.jubilated = jubilated
        affiliate.escalafon = str(cobro)
        affiliate.cotizacion = model.Cotizacion.get(cotizacion)
        affiliate.payment = affiliate.cotizacion.nombre
        raise redirect('/affiliate/{0}'.format(affiliate.id))

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.stateSchool')
    @validate(validators=dict(departamento=validators.Int()))
    def stateSchool(self, departamento):

        departamento = model.Departamento.get(departamento)
        affiliates = model.Affiliate.selectBy(departamento=departamento)

        schools = dict()
        for affiliate in affiliates:
            if affiliate.school in schools:
                schools[affiliate.school].append(affiliate)
            else:
                schools[affiliate.school] = list()
                schools[affiliate.school].append(affiliate)

        return dict(departamento=departamento, schools=schools)

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.solvencia')
    @validate(validators=dict(mes=validators.UnicodeString(),
                              anio=validators.Int(),
                              afiliado=validators.Int()))
    def solvencia(self, afiliado, mes, anio):

        return dict(afiliado=model.Affiliate.get(afiliado), mes=mes, anio=anio,
                    dia=date.today())

    @identity.require(identity.not_anonymous())
    @expose('json')
    @validate(validators=dict(afiliado=validators.Int(),
                              amount=validators.UnicodeString(),
                              cuenta=validators.Int(),
                              day=validators.DateTimeConverter(
                                  format='%d/%m/%Y')))
    def devolucionPlanilla(self, afiliado, cuenta, day, amount):

        """Registra Devoluciones Manuales
        
        Permite registrar una devolución de una planilla ingresadamanualmente
        
        :param afiliado: Número de afiliación
        :param cuenta: Código de la cuenta de devoluciones
        :param day: Día en el que se efectuó la deducción
        :param amount: Monto en que consiste la devolución
        """

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

        log(identity.current.user,
            u"Excedente Deducido por planilla afiliado {0}".format(
                affiliate.id), affiliate)

        return dict(pago=affiliate.get_monthly())

    # @expose()
    def cuentas(self):

        afo = model.Affiliate.selectBy(payment='Escalafon')

        afiliados = dict()

        for a in afo:
            if a.cardID == None:
                continue
            afiliados[a.cardID.replace('-', '')] = a

        cuentas = csv.reader(open('cuentas.csv'))

        for linea in cuentas:

            if linea[0] in afiliados:
                afiliado = afiliados[linea[0]]
                banco = int(linea[3])
                cuenta = int(linea[4].strip(
                    'ABCDEFGHIJKMNLOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz- '))

                afiliado.banco = banco
                afiliado.cuenta = cuenta
                print afiliado.banco, afiliado.cuenta

        flash('terminado')

        raise redirect('/affiliate')

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.solvencia')
    @validate(validators=dict(mes=validators.UnicodeString(),
                              cotizacion=validators.Int()))
    def talonarios(self, mes, cotizacion):

        """Permite generar de manera automatizada talonarios de pago que serán
        utilizados por los afiliados para llevar un registro de los pagos que
        deben efectuar"""

        cotizacion = model.Cotizacion.get(cotizacion)
        afiliados = model.Affiliate.selectBy(cotizacion=cotizacion, active=True)

        return dict(afiliados=afiliados)

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(affiliate=validators.Int(), banco=validators.Int(),
                              cuenta=validators.UnicodeString(),
                              bancario=validators.UnicodeString()))
    def autorizar(self, affiliate, banco, cuenta, bancario):

        """Reactiva un afiliado para que pueda continuar participando
        
        :param affiliate: El número de afiliación
        :param banco: El numero del banco de donde se efectuan los debitos
        :param cuenta: El numero de cuenta que se utilizara para deducir
        :param bancario: Codigos internos utilizados por el banco
        """

        affiliate = model.Affiliate.get(affiliate)
        affiliate.autorizacion = True
        affiliate.banco = banco
        affiliate.cuenta = cuenta
        affiliate.bancario = bancario

        autorizacion = model.Autorizacion(affiliate=affiliate, banco=banco)

        log(identity.current.user,
            u"Se registro la autorización del afiliado {0}".format(
                affiliate.id), affiliate)

        flash(u'Se ha registrado la autorización del afiliado {0}'.format(
            affiliate.id))

        raise redirect('/affiliate/')

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose()
    @validate(validators=dict(cardID=validators.String(), banco=validators.Int(),
                              cuenta=validators.UnicodeString(),
                              bancario=validators.UnicodeString()))
    def autorizarIdentidad(self, cardID, banco, cuenta, bancario):

        """Reactiva un afiliado para que pueda continuar participando
        
        :param affiliate: El número de afiliación
        :param banco: El numero del banco de donde se efectuan los debitos
        :param cuenta: El numero de cuenta que se utilizara para deducir
        :param bancario: Codigos internos utilizados por el banco
        """

        try:
            affiliate = model.Affiliate.selectBy(cardID=cardID).limit(
                1).getOne()
            affiliate.autorizacion = True
            affiliate.banco = banco
            affiliate.cuenta = cuenta
            affiliate.bancario = bancario

            autorizacion = model.Autorizacion(affiliate=affiliate)

            log(identity.current.user,
                u"Se registro la autorización del afiliado {0}".format(
                    affiliate.id), affiliate)

            flash(u'Se ha registrado la autorización del afiliado {0}'.format(
                affiliate.id))

            raise redirect('/affiliate/')

        except SQLObjectNotFound:
            flash(u'No se encontró la identidad {0}'.format(cardID))
            raise redirect('/affiliate')

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.search')
    @validate(validators=dict(banco=validators.Int()))
    def bank(self, banco):

        """Permite generar de manera automatizada talonarios de pago que serán
        utilizados por los afiliados para llevar un registro de los pagos que
        deben efectuar"""

        afiliados = model.Affiliate.selectBy(banco=banco)

        return dict(result=afiliados)

    @error_handler(error)
    @identity.require(identity.not_anonymous())
    @expose(template='turboaffiliate.templates.affiliate.autorizaciones')
    @validate(validators=dict(banco=validators.Int(),
                              inicio=validators.DateTimeConverter(format='%d/%m/%Y'),
                              fin=validators.DateTimeConverter(format='%d/%m/%Y')))
    def autorizaciones(self, banco, inicio, fin):

        banco = model.Banco.get(banco)

        return dict(autorizaciones=model.Autorizacion.select(AND(model.Autorizacion.q.banco == banco,
                                                                 model.Autorizacion.q.fecha >= inicio,
                                                                 model.Autorizacion.q.fecha <= fin)),
                    banco=banco)
