# -*- coding: utf8 -*-
#
# model.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2007 - 2011 Carlos Flores <cafg10@gmail.com>
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

from turbogears.database import PackageHub
from sqlobject import (SQLObject, UnicodeCol, StringCol, DateCol, CurrencyCol,
                       MultipleJoin, ForeignKey, IntCol, DecimalCol, BoolCol,
                       DatabaseIndex, DateTimeCol, RelatedJoin,
                       SQLObjectNotFound, BigIntCol)
from decimal import Decimal
from datetime import date, datetime
import wording
import math, copy

from turbogears import identity
import calendar

dot01 = Decimal(".01")
Zero = Decimal(0)
Zeros = Decimal(0)

hub = PackageHub("turboaffiliate")
__connection__ = hub

# identity models.
class Visit(SQLObject):
    class sqlmeta:
        table = "visit"
    
    visit_key = StringCol(length=40, alternateID=True, 
                          alternateMethodName="by_visit_key")
    created = DateTimeCol(default=datetime.now)
    expiry = DateTimeCol()
    
    def lookup_visit(cls, visit_key):
        try:
            return cls.by_visit_key(visit_key)
        except SQLObjectNotFound:
            return None
    lookup_visit = classmethod(lookup_visit)

class VisitIdentity(SQLObject):
    visit_key = StringCol(length=40, alternateID=True, 
                          alternateMethodName="by_visit_key")
    user_id = IntCol()

class Group(SQLObject):
    """
    An ultra-simple group definition.
    """

    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table = "tg_group"
    
    group_name = UnicodeCol(length=16, alternateID=True, 
                            alternateMethodName="by_group_name")
    display_name = UnicodeCol(length=255)
    created = DateTimeCol(default=datetime.now)
    
    # collection of all users belonging to this group
    users = RelatedJoin("User", intermediateTable="user_group", 
                        joinColumn="group_id", otherColumn="user_id")
    
    # collection of all permissions for this group
    permissions = RelatedJoin("Permission", joinColumn="group_id", 
                              intermediateTable="group_permission", 
                              otherColumn="permission_id")

class User(SQLObject):
    """
    Reasonably basic User definition. Probably would want additional attributes.
    """
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table = "tg_user"
    
    user_name = UnicodeCol(length=16, alternateID=True, 
                           alternateMethodName="by_user_name")
    email_address = UnicodeCol(length=255, alternateID=True, 
                               alternateMethodName="by_email_address")
    display_name = UnicodeCol(length=255)
    password = UnicodeCol(length=40)
    created = DateTimeCol(default=datetime.now)

    # groups this user belongs to
    groups = RelatedJoin("Group", intermediateTable="user_group", 
                         joinColumn="user_id", otherColumn="group_id")
    
    loans = MultipleJoin("Loan", joinColumn="aproval_id")
    logs = MultipleJoin("Logger", joinColumn="user_id")
    casa = ForeignKey("Casa")
    departamentos = RelatedJoin("Departamento")
    cotizaciones = RelatedJoin("Cotizacion")
    
    def _get_permissions(self):
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms
    
    def has_permission(self, permission):
        
        perms = (p.permission_name for p in self._get_permissions())
        if permission in perms: return True
        else: return False
    
    def _set_password(self, cleartext_password):
        "Runs cleartext_password through the hash algorithm before saving."
        hash = identity.encrypt_password(cleartext_password)
        self._SO_set_password(hash)
    
    def set_password_raw(self, password):
        "Saves the password as-is to the database."
        self._SO_set_password(password)
    
    def cotizar(self):
        
        return (c.nombre for c in self.cotizaciones)

class Permission(SQLObject):
    permission_name = UnicodeCol(length=16, alternateID=True, 
                                 alternateMethodName="by_permission_name")
    description = UnicodeCol(length=255)
    
    groups = RelatedJoin("Group", 
                        intermediateTable="group_permission", 
                         joinColumn="permission_id", 
                         otherColumn="group_id")

class Logger(SQLObject):
    
    user = ForeignKey("User")
    action = UnicodeCol(default="")
    day = DateTimeCol(default=datetime.now)

################################################################################
# Clases Especificas del Negocio
################################################################################

months = {
    1:'Enero', 2:'Febrero', 3:'Marzo', 
    4:'Abril', 5:'Mayo', 6:'Junio', 
    7:'Julio', 8:'Agosto', 9:'Septiembre', 
    10:'Octubre', 11:'Noviembre', 12:'Diciembre'
}

class Departamento(SQLObject):
    
    nombre = UnicodeCol(length=50,default=None)
    
    municipios = MultipleJoin('Municipio')
    afiliados = MultipleJoin('Affiliate')
    usuarios = RelatedJoin("User")

class Municipio(SQLObject):
    
    departamento = ForeignKey('Departamento')
    nombre = UnicodeCol(length=50,default=None)
    afiliados = MultipleJoin('Affiliate')

class Casa(SQLObject):
    
    """Sucursal del COPEMH
    
    Representa un lugar físico donde se encuentra una sede del COPEMH.
    """
    
    nombre = UnicodeCol(length=20, default=None)
    direccion = UnicodeCol(length=255)
    telefono = UnicodeCol(length=11)
    activa = BoolCol(default=True)
    prestamos = MultipleJoin("Loan")
    usuarios = MultipleJoin("User")

class Cotizacion(SQLObject):
    
    nombre = UnicodeCol(length=50,default=None)
    jubilados = BoolCol(default=True)
    usuarios = RelatedJoin("User")

class Affiliate(SQLObject):

    """Representa un miembro de la institución, cada afiliado puede tener
    Prestamos, tiene Cuota mensual que es Deducido por planilla o pagado en
    ventanilla en algunos casos.
    
    Ademas, puede deducirsele por diferentes métodos, como ser:
        
        * Escalafon
        * UPN
        * INPREMA
        * Ventanilla
        * Ministerio de Educación.
    
    El afiliado puede asistir a diferentes eventos de la institucion como ser
    asambleas, elecciones u otras actividades extraordinarias que se programen.
    
    Es necesario para efectuar los diversos cobros:
        
        1. Escalafon: Número de Identidad.
        2. INPREMA: Número de cobro.
        3. UPN: Número de empleado.
    
    Algunos datos son requeridos para obtener información estadística acerca de
    la institución.
    """

    firstName = UnicodeCol(length=100)
    """Nombre del Afiliado"""
    lastName = UnicodeCol(length=100)
    """Apellidos del Afiliado"""
    cardID = UnicodeCol(length=15, default=None)
    """Identidad del afiliado"""
    gender = UnicodeCol(length=1, varchar=False)
    birthday = DateCol(default=date.today)
    birthPlace = UnicodeCol(length=100, default=None)
    
    address = UnicodeCol(default=None)
    phone = UnicodeCol(default=None)
    
    departamento = ForeignKey('Departamento', default=Departamento.get(19))
    municipio = ForeignKey('Municipio', default=Municipio.get(299))
    state = UnicodeCol(length=50, default=None)
    school = UnicodeCol(length=255, default=None)
    town = UnicodeCol(length=50, default=None)
    
    joined = DateCol(default=date.today)
    """Fecha en que se unio a la organización"""
    active = BoolCol(default=True, notNone=True)
    """Indica si el afiliado se encuentra activo o no"""
    reason = UnicodeCol(default=None, length=50)
    """Razon por la que fue desactivado el afiliado"""
    escalafon = UnicodeCol(length=11, default=None)
    inprema = UnicodeCol(length=11, default=None)
    jubilated = DateCol(default=None)
    
    payment = UnicodeCol(default="Ventanilla", length=20)
    cotizacion = ForeignKey('Cotizacion')
    """Método de Cotización"""
    
    cuotaTables = MultipleJoin("CuotaTable", orderBy='year')
    """Historial de aportaciones"""
    loans = MultipleJoin("Loan", orderBy='startDate')
    """Préstamos activos"""
    payedLoans = MultipleJoin("PayedLoan", orderBy='startDate')
    """Préstamos cancelados"""
    extras = MultipleJoin("Extra")
    """Deducciones extra a efectuar"""
    deduced = MultipleJoin("Deduced", orderBy=['-year', '-month'])
    """Deducciones efectuadas por planilla en un mes y año"""
    observaciones = MultipleJoin('Observacion')
    """Observaciones acerca de actividad en un afiliado"""
    solicitudes = MultipleJoin('Solicitud')
    """Solicitudes de Préstamo ingresada"""
    reintegros = MultipleJoin('Reintegro')
    """Reintegros a efectuar"""
    muerte = DateCol(default=date.today)
    """Fecha de Fallecimiento"""
    desactivacion = DateCol(default=date.today)
    """Fecha de Desactivación"""
    cuenta = BigIntCol(default=None)
    """Número de cuenta bancaria"""
    banco = IntCol(default=None)
    """Código del Banco"""
    sobrevivencias = MultipleJoin("Sobrevivencia", joinColumn="afiliado_id")
    devoluciones = MultipleJoin("Devolucion", joinColumn="afiliado_id")
    funebres = MultipleJoin("Funebre", joinColumn="afiliado_id")
    seguros = MultipleJoin("Seguro", joinColumn="afiliado_id")
    inscripciones = MultipleJoin("Inscripcion", joinColumn="afiliado_id")
    depositos = MultipleJoin("Deposito", joinColumn="afiliado_id")
    
    def tiempo(self):
        
        """Permite mostrar el tiempo que tiene el afiliado de ser parte de la
        organizacion"""
        
        if self.joined == None:
            
            return 1
        
        return (date.today() - self.joined).days / 365
    
    def get_monthly(self):
        
        """Obtiene el pago mensual que debe efectuar el afiliado"""
        
        extras = sum(e.amount for e in self.extras)
        loans = Decimal(0)
        #loans = sum(l.get_payment() for l in self.loans)
        #reintegros = sum(r.monto for r in self.reintegros if not r.pagado)
        reintegros = Decimal(0)
        for r in self.reintegros:
            if r.pagado:
                break
            reintegros += r.monto
            break
        
        # Cobrar solo el primer préstamo
        for loan in self.loans:
            
            loans = loan.get_payment()
            break
        
        return extras + loans + reintegros + self.get_cuota()
    
    def get_cuota(self, hoy=date.today()):
        
        """Obtiene la cuota de aportación que el :class:`Affiliate` debera pagar
        en el mes actual"""
        
        obligations = Obligation.selectBy(month=hoy.month, year=hoy.year)
        
        obligation = Decimal(0)
        obligation += sum(o.amount for o in obligations
                          if not self.cotizacion.jubilados)
        
        obligation += sum(o.inprema for o in obligations
                          if self.cotizacion.jubilados)
        
        return obligation
    
    def populate(self, year):
        
        kw = dict()
        for n in range(1, 13):
            kw["month{0}".format(n)] = False
        return kw
    
    def complete(self, year):
        
        """Agrega un año de aportaciones al estado de cuenta del afiliado"""
        
        kw = dict()
        kw['affiliate'] = self
        kw['year'] = year
        CuotaTable(**kw)
    
    def get_delayed(self):
        
        for cuota in self.cuotaTables:
            if cuota.delayed() != Zero:
                return cuota
        return None
    
    def obtenerAportaciones(self, year):
        cuota = None
        try:
            cuota = CuotaTable.selectBy(affiliate=self, year=year).getOne()
        except SQLObjectNotFound:
            
            # Esto evita crear un año de aportaciones incorrecto
            if year < self.joined.year:
                return None
            
            kw = dict()
            kw['affiliate'] = self
            kw['year'] = year
            cuota = CuotaTable(**kw)
        return cuota
    
    def pagar_cuota(self, mes, anio):
        
        self.obtenerAportaciones(anio).pagar_mes(mes)
    
    def pay_cuota(self, year, month):
        
        self.obtenerAportaciones(year).pagar_mes(month)
    
    def remove_cuota(self, year, month):
        
        self.obtenerAportaciones(year).remove_month(month)
    
    def aportaciones(self):
    
        return sum(table.pagado() for table in self.cuotaTables)
    
    def deuda_prestamo(self):
        
        """Muestra la deuda por préstamos"""
        
        return sum(loan.debt() for loan in self.loans)
    
    def debt(self):
        
        return sum(table.deuda() for table in self.cuotaTables)
    
    def solvent(self, year):
        
        return self.obtenerAportaciones(year).all()
    
    def multisolvent(self, year):
        
        for cuota in self.cuotaTables:
            if cuota.year > year:
                break
            if not cuota.todos():
                return False
        return True
    
    def remove(self):
        
        for table in self.cuotaTables:
            table.destroySelf()
        
        for loan in self.loans:
            loan.remove()
        
        self.destroySelf()
    
    def get_month(self, year, month):
        
        table = self.obtenerAportaciones(year)
        
        # en caso que el afiliado sea de afiliación más reciente que el año
        # solicitado
        if table == None:
            return False
        
        return getattr(table, "month{0}".format(month))
    
    def get_age(self):
        
        return (date.today() - self.birthday).days / 365

class CuentaRetrasada(SQLObject):
    
    account = ForeignKey('Account')
    mes = IntCol()
    anio = IntCol()

class CuotaTable(SQLObject):
    
    """Contains the payed months as Boolean values"""
    
    affiliate = ForeignKey("Affiliate")
    year = IntCol()
    affiliateYear = DatabaseIndex("affiliate", "year", unique=True)
    
    month1 = BoolCol(default=False)
    month2 = BoolCol(default=False)
    month3 = BoolCol(default=False)
    month4 = BoolCol(default=False)
    month5 = BoolCol(default=False)
    month6 = BoolCol(default=False)
    month7 = BoolCol(default=False)
    month8 = BoolCol(default=False)
    month9 = BoolCol(default=False)
    month10 = BoolCol(default=False)
    month11 = BoolCol(default=False)
    month12 = BoolCol(default=False)
    
    def periodo(self, retrasada=False):
        
        (start, end) = (1, 13)
        
        if self.affiliate.joined.year == self.year:
            start = self.affiliate.joined.month
        
        if self.year == date.today().year:
            if retrasada:
                end = date.today().month
            else:
                end = date.today().month + 1
        
        if end == 0:
            end = 1
        
        return start, end
    
    def todos(self):
        
        """Verifica si el afiliado ha realizado todos los pagos del año"""
        
        inicio, fin = self.periodo()
        for n in range(inicio, fin):
            if not getattr(self, 'month{0}'.format(n)):
                return False
        
        return True
    
    def vacio(self):
        
        """Responde si el afiliado no ha realizado pagos durante el año"""
        
        inicio, fin = self.periodo()
        for n in range(inicio, fin):
            if getattr(self, 'month{0}'.format(n)):
                return False
        
        return True
    
    def cantidad(self, mes):
        
        total = Zero
        os = Obligation.selectBy(year=self.year,month=mes)
        
        if (self.affiliate.cotizacion.jubilados and
            not self.affiliate.jubilated is None):
        
            if self.affiliate.jubilated.year < self.year:
                total = sum(o.inprema for o in os)
            
            elif self.affiliate.jubilated.year == self.year:
                total += sum(o.amount for o in os
                             if mes < self.affiliate.jubilated.month)
                
                total += sum(o.inprema for o in os
                             if mes >= self.affiliate.jubilated.month)
            
            elif self.affiliate.jubilated.year > self.year:
                total = sum(o.amount for o in os)
        
        else:
            total = sum(o.amount for o in os)
        
        return total
    
    def pago_mes(self, mes, periodo=None):
        
        """Muestra la cantidad pagada en el mes especificado"""
        
        if periodo == None:
            inicio, fin = self.periodo()
            periodo = range(inicio, fin)
        
        if not mes in periodo:
            return Zero
        
        if not getattr(self, 'month{0}'.format(mes)):
            return Zero
        
        return self.cantidad(mes)
    
    def deuda_mes(self, mes, periodo=None):
        
        """Muestra la cantidad debida en el mes especificado"""
        
        if periodo == None:
            inicio, fin = self.periodo()
            periodo = range(inicio, fin)
        
        if not mes in periodo:
            return Zero
        
        if getattr(self, 'month{0}'.format(mes)):
            return Zero
        
        return self.cantidad(mes)
    
    def deuda(self):
        
        """Obtiene la cantidad total debida durante el año"""
        
        inicio, fin = self.periodo()
        periodo = range(inicio, fin)
        return sum(self.deuda_mes(mes, periodo) for mes in periodo)
    
    def pagado(self):
        
        """Obtiene la cantidad total pagada durante el año"""
        
        inicio, fin = self.periodo()
        periodo = range(inicio, fin)
        return sum(self.pago_mes(mes, periodo) for mes in periodo)
    
    def delayed(self):
        
        if self.affiliate.joined == None:
            return Zero
        
        """Obtiene el primer mes en el que no se haya efectuado un pago en las
        aportaciones.
        """
        
        inicio, fin = self.periodo(retrasada=True)
        for n in range(inicio, fin):
            if not getattr(self, 'month{0}'.format(n)):
                return n
        
        return Zero
    
    def edit_line(self, month):
        text = ' name="month{0}"'.format(month)
        if getattr(self, 'month{0}'.format(month)):
            return text + ' checked'
        else:
            return text + ' '
    
    def pagar_mes(self, mes):
        setattr(self, 'month{0}'.format(mes), True)
    
    def pay_month(self, month):
        setattr(self, 'month{0}'.format(month), True)
    
    def remove_month(self, month):
        setattr(self, 'month{0}'.format(month), False)
    
    def all(self):
        
        return self.todos()
    
    def empty(self):
        
        return self.vacio()

class Loan(SQLObject):

    """Guarda los datos que pertenecen a un préstamo personal otorgado a un
    :class:`Affiliate` de la organización"""
    
    affiliate = ForeignKey("Affiliate")
    casa = ForeignKey("Casa")
    
    capital = CurrencyCol(default=0, notNone=True)
    letters = UnicodeCol(default=None, length=100)
    debt = CurrencyCol(default=0, notNone=True)
    payment = CurrencyCol(default=0, notNone=True)
    interest = DecimalCol(default=20, notNone=True, size=4, precision=2)
    months = IntCol()
    last = DateCol(default=date.today)
    number = IntCol(default=0)
    offset = IntCol(default=0)
    
    startDate = DateCol(notNone=True, default=date.today)
    aproved = BoolCol(default=False)
    fecha_mora = DateCol(notNone=True, default=date.today)
    
    pays = MultipleJoin("Pay", orderBy="day")
    deductions = MultipleJoin("Deduction")
    aproval = ForeignKey("User")
    
    def percent(self):
        
        """Calcula cuanto de la deuda se ha cubierto con los pagos"""
        
        x = (Decimal(self.debt) * Decimal(100)).quantize(dot01)
        total = x / Decimal(self.capital).quantize(dot01)
        return total
    
    def mora_mensual(self):
        
        """Calcula el monto que se acumula mensualmente por mora"""
        
        return self.debt * Decimal("0.02")
    
    def inicio_mora(self):
        
        """Calcula la fecha de inicio de cobro de intereses moratorios de
        manera.
        Utiliza la fecha de inicio de mora almacenada en el prestamo en caso
        que esta sea mayor que la fecha en que se inició.
        """
        
        ultimo = calendar.monthrange(self.fecha_mora.year,
                                     self.fecha_mora.month)[1]
        inicio = date(self.fecha_mora.year, self.fecha_mora.month, ultimo)
        
        if self.startDate < inicio:
            
            return self.fecha_mora
        
        return self.startDate
    
    def prediccion_pagos_actuales(self):
        
        """Calcula la cantidad de pagos que el :class:`Loan` deberia tener a
        la fecha de hoy
        """
        
        return (date.today() - self.inicio_mora()).days / 30
    
    def pagos_en_mora(self):
        
        """Calcula la cantidad de pagos que el :class:`Affiliate` no ha
        efectuado desde que se le otorgo el :class:`Loan`"""
        
        pagos = self.prediccion_pagos_actuales()
        # Utilizar el número de pagos almacenado, para evitar calcular intereses
        # sobre cuotas pagadas y eliminadas accidentalmente.
        return pagos - self.number + 1
    
    def obtener_mora(self):
        
        """Calcula el monto a pagar por mora en la siguiente cuota"""
        
        return self.mora_mensual() * self.pagos_en_mora()
    
    def get_payment(self):
        
        """Obtiene el cobro a efectuar del prestamo"""
    
        if self.debt < self.payment and self.number != self.months - 1:
            return self.debt
        
        return self.payment
    
    def start(self):
        
        """Inicia el saldo del préstamo al capital"""
    
        self.debt = self.capital
    
    def pagar(self, amount, receipt, day=date.today(), libre=False, remove=True,
              deposito=False, descripcion=None):
        
        """Carga un nuevo pago para el préstamo
        
        Dependiendo de si se marca como libre de intereses o no, calculará el
        interés compuesto a pagar.
        
        En caso de ingresar un pago mayor que la deuda actual del préstamo,
        ingresará el sobrante como intereses y marcará el préstamo como
        pagado.
        """
        
        kw = dict()
        kw['amount'] = amount = Decimal(amount).quantize(dot01)
        kw['day'] = day
        kw['receipt'] = receipt
        kw['loan'] = self
        kw['deposito'] = deposito
        kw['description'] = descripcion
        
        # La cantidad a pagar es igual que la deuda del préstamo, por
        # lo tanto se considera la ultima cuota y no se cargaran intereses
        if(self.debt == amount):
           
            self.last = kw['day']
            kw['capital'] = kw['amount']
            kw['interest'] = 0
            # Register the payment in the database
            Pay(**kw)
            # Remove the loan and convert it to PayedLoan
            if remove:
                self.remove()
            else:
                self.debt -= kw['amount']
            return True
        
        if libre:
            kw['interest'] = 0
        else:
            kw['interest'] = (self.debt * self.interest / 1200).quantize(dot01)
        
        # Registra cualquier cantidad mayor a los intereses
        if(self.debt < amount):
            
            kw['interest'] = amount - self.debt
        
        # Calculate how much money was used to pay the capital
        kw['capital'] = kw['amount'] - kw['interest']
        # Decrease debt by the amount of the payed capital
        self.debt -= kw['capital']
        # Change the last payment date
        #if day.date > self.last:
        self.last = day
        # Register the payment in the database
        Pay(**kw)
        # Increase the number of payments by one
        self.number += 1
        
        if self.debt <= 0 and remove:
            self.remove()
            return True
        
        self.compensar()
        
        return False
    
    def refinanciar(self, pago, solicitud, cuenta, usuario, descripcion):
        
        self.pagar(pago, "Liquidacion", solicitud.entrega, True)
        
        prestamo = solicitud.prestamo(usuario)
        
        kw = dict()
        kw['account'] = cuenta
        kw['amount'] = pago
        kw['name'] = kw['account'].name
        kw['loan'] = prestamo
        kw['description'] = descripcion
        
        Deduction(**kw)
        
        return prestamo
    
    def net(self):
        
        """Obtains the amount that was given to the affiliate in the check"""
        
        return self.capital - sum(d.amount for d in self.deductions)
    
    def total_deductions(self):
        
        return sum(d.amount for d in self.deductions)
    
    def remove(self):
        
        """Convierte un :class:`Loan` en un :class:`PayedLoan`"""
        
        kw = dict()
        kw['id'] = self.id
        kw['affiliate'] = self.affiliate
        kw['capital'] = self.capital
        kw['letters'] = self.letters
        kw['interest'] = self.interest
        kw['months'] = self.months
        kw['last'] = self.last
        kw['startDate'] = self.startDate
        kw['payment'] = self.payment
        kw['casa'] = self.casa
        payed = PayedLoan(**kw)
        
        for pay in self.pays:
            pay.remove(payed)
        
        for deduction in self.deductions:
            deduction.remove(payed)
        
        self.destroySelf()
        
        return payed
    
    def future(self):
        
        """Calcula la manera en que se pagará el préstamo basado en los
        intereses y los pagos actuales"""
        
        debt = copy.copy(self.debt)
        li = list()
        start = self.startDate.month + self.offset
        if self.startDate.day == 24 and self.startDate.month == 8:
            start += 1
        year = self.startDate.year
        n = 1
        while debt > 0:
            kw = dict()
            # calcular el número de pago
            kw['number'] = "{0}/{1}".format(n + self.number, self.months)
            kw['month'] = self.number + n + start
            kw['enum'] = self.number + n
            kw['year'] = year
            
            # Normalizar Meses
            while kw['month'] > 12:
                kw['month'] = kw['month'] - 12
                kw['year'] += 1
            
            # colocar el mes y el año
            kw['month'] = "{0} {1}".format(months[kw['month']], kw['year'])
            # calcular intereses
            kw['interest'] = Decimal(debt * self.interest / 1200).quantize(dot01)
            
            if debt <= self.payment:
                kw['amount'] = 0
                kw['capital'] = debt
                kw['payment'] = kw['interest'] + kw['capital']
                li.append(kw)
                break
            
            kw['capital'] = self.payment - kw['interest']
            debt = debt + kw['interest'] - self.payment
            kw['amount'] = debt
            kw['payment'] = kw['interest'] + kw['capital']
            li.append(kw)
            n += 1
            
        return li
    
    def compensar(self):
        
        """Recalcula la deuda final utilizando el calculo de pagos futuros
        para evitar perdidas por pagos finales menores a la cuota de préstamo
        pero que deberian mantenerse en el valor de la cuota de préstamo"""
        
        futuro = self.future()
        if futuro == list():
            return
        
        ultimo_pago = futuro[-1]['payment']
        ultimo_mes = futuro[-1]['enum']
        if ultimo_pago < self.payment and ultimo_mes == self.months:
            self.debt += ((self.payment - ultimo_pago) * 2 / 3).quantize(dot01)
    
    def totaldebt(self):
        
        return self.debt
    
    def capitalPagado(self):
        
        return sum(p.capital for p in self.pays)
    
    def pagado(self):
        
        return sum(p.amount for p in self.pays)
    
    def interesesPagados(self):
        
        return sum(p.interest for p in self.pays)
    
    def reconstruirSaldo(self):
        
        """Recalcula el valor de la deuda del préstamo en base a los pagos
        efectuados"""
        
        self.debt = self.capital - self.capitalPagado()

class Pay(SQLObject):
    
    loan = ForeignKey("Loan")
    day = DateCol(default=date.today)
    capital = CurrencyCol(default=0, notNone=True)
    interest = CurrencyCol(default=0, notNone=True)
    amount = CurrencyCol(default=0, notNone=True)
    deposito = BoolCol(default=False)
    receipt = UnicodeCol(length=50)
    description = UnicodeCol(length=100)
    
    def remove(self, payedLoan):
        
        kw = dict()
        kw['payedLoan'] = payedLoan
        kw['day'] = self.day
        kw['capital'] = self.capital
        kw['interest'] = self.interest
        kw['amount'] = self.amount
        kw['receipt'] = self.receipt
        kw['description'] = self.description
        self.destroySelf()
        OldPay(**kw)
    
    def revert(self):
        
        self.loan.debt = self.loan.capital - self.loan.capitalPagado() \
                       + self.capital
        self.loan.number -= 1
        self.destroySelf()

class Account(SQLObject):
    
    """Simple Account made for affiliate handling"""
    
    name = StringCol()
    loan = BoolCol(default=False)
    
    extras = MultipleJoin("Extra")
    retrasadas = MultipleJoin("CuentaRetrasada")

class Extra(SQLObject):
    
    """Represents a Deduction that will be made"""
    
    affiliate = ForeignKey("Affiliate")
    amount = CurrencyCol(default=0)
    months = IntCol(default=1)
    retrasada = BoolCol(default=False)
    account = ForeignKey("Account")
    mes = IntCol(default=None)
    anio = IntCol(default=None)
    
    def act(self, decrementar=True, day=date.today()):
        
        """Registra que la deducción se efectuó y disminuye la cantidad"""
        
        self.to_deduced(day=day)
        if decrementar and self.months == 1:
            self.destroySelf()
        if decrementar:
            self.months -= 1
        if self.months == 0:
            self.destroySelf()
    
    def to_deduced(self, day=date.today()):
        
        """Registra la deducción convirtiendola en :class:`Deduced`"""
        
        kw = dict()
        kw['amount'] = self.amount
        kw['affiliate'] = self.affiliate
        kw['account'] = self.account
        kw['month'] = day.month
        kw['year'] = day.year
        
        if self.retrasada:
            
            cuota = self.affiliate.get_delayed()
            month, year = (None, None)
            if not cuota is None:
                month = cuota.delayed()
                year = cuota.year
                cuota.pay_month(month)
            kw['detail'] = "Cuota Retrasada {0} de {1}".format(month, year)
        
        Deduced(**kw)
    
    def manual(self):
        
        self.act()

class Deduction(SQLObject):
    
    loan = ForeignKey("Loan")
    amount = CurrencyCol()
    account = ForeignKey("Account")
    description = UnicodeCol(length=100)
    
    def remove(self, payedLoan):
        
        kw = dict()
        kw['payedLoan'] = payedLoan
        kw['amount'] = self.amount
        kw['account'] = self.account
        kw['description'] = self.description
        PayedDeduction(**kw)
        self.destroySelf()

class PayedLoan(SQLObject):
    
    affiliate = ForeignKey("Affiliate")
    casa = ForeignKey("Casa")
    capital = CurrencyCol(default=0, notNone=True)
    letters = StringCol()
    payment = CurrencyCol(default=0, notNone=True)
    interest = DecimalCol(default=20, notNone=True, size=4, precision=2)
    months = IntCol()
    last = DateCol(default=date.today)
    startDate = DateCol(notNone=True, default=date.today)
    pays = MultipleJoin("OldPay")
    deductions = MultipleJoin("PayedDeduction")
    debt = CurrencyCol(default=0, notNone=True)
    
    def remove(self):
        
        [pay.destroySelf() for pay in self.pays]
        [deduction.destroySelf() for deduction in self.deductions]
        self.destroySelf()
    
    def to_loan(self, user):
        
        kw = dict()
        kw['aproval'] = user
        kw['affiliate'] = self.affiliate
        kw['capital'] = self.capital
        kw['interest'] = self.interest
        kw['payment'] = self.payment
        kw['months'] = self.months
        kw['last'] = self.last
        kw['startDate'] = self.startDate
        kw['letters'] = self.letters
        kw['number'] = len(self.pays)
        kw['id'] = self.id
        kw['casa'] = self.casa
        loan = Loan(**kw)
        
        [pay.to_pay(loan) for pay in self.pays]
        [deduction.to_deduction(loan) for deduction in self.deductions]
        
        self.destroySelf()
        return loan
    
    def net(self):
        
        """Obtains the amount that was given to the affiliate in the check"""
        
        return self.capital - sum(d.amount for d in self.deductions)
    
    def capitalPagado(self):
        
        return sum(p.capital for p in self.pays)
    
    def pagado(self):
        
        return sum(p.amount for p in self.pays)
    
    def interesesPagados(self):
        
        return sum(p.interest for p in self.pays)

class OldPay(SQLObject):
    
    payedLoan = ForeignKey("PayedLoan")
    day = DateCol(default=date.today)
    capital = CurrencyCol(default=0, notNone=True)
    interest = CurrencyCol(default=0, notNone=True)
    amount = CurrencyCol(default=0, notNone=True)
    receipt = UnicodeCol(length=50)
    description = UnicodeCol(length=100)
    
    def to_pay(self, loan):
        
        kw = dict()
        kw['loan'] = loan
        kw['day'] = self.day
        kw['capital'] = self.capital
        kw['interest'] = self.interest
        kw['amount'] = self.amount
        kw['receipt'] = self.receipt
        kw['description'] = self.description
        Pay(**kw)
        self.destroySelf()

class PayedDeduction(SQLObject):
    
    payedLoan = ForeignKey("PayedLoan")
    amount = CurrencyCol()
    account = ForeignKey("Account")
    description = StringCol()
    
    def to_deduction(self, loan):
        
        kw = dict()
        kw['loan'] = loan
        kw['amount'] = self.amount
        kw['description'] = self.description
        kw['account'] = self.account
        Deduction(**kw)
        self.destroySelf()

class Obligation(SQLObject):
    
    """The description of the Cuota payment"""
    
    name = UnicodeCol(length=50)
    amount = CurrencyCol(default=0, notNone=True)
    inprema = CurrencyCol(default=0, notNone=True)
    month = IntCol()
    year = IntCol()
    account = ForeignKey("Account")
    filiales = CurrencyCol(default=4, notNone=True)

class ReportAccount(SQLObject):
    
    name = name = UnicodeCol(length=100)
    quantity = IntCol()
    amount = CurrencyCol(default=0)
    postReport = ForeignKey("PostReport")

    def add(self, amount):
        self.amount += amount
        self.quantity += 1

class PostReport(SQLObject):

    year = IntCol()
    month = IntCol()
    reportAccounts = MultipleJoin("ReportAccount", orderBy="name")

    def total(self):
        return sum(r.amount for r in self.reportAccounts)

class Deduced(SQLObject):
    
    affiliate = ForeignKey("Affiliate")
    amount = CurrencyCol(default=0)
    account = ForeignKey("Account")
    detail = UnicodeCol(default="")
    month = IntCol(default=date.today().month)
    year = IntCol(default=date.today().year)

class OtherReport(SQLObject):
    
    year = IntCol()
    month = IntCol()
    otherAccounts = MultipleJoin("OtherAccount")
    cotizacion = ForeignKey("Cotizacion")

    def total(self):
        return sum(r.amount for r in self.otherAccounts)

class OtherAccount(SQLObject):
    
    account = ForeignKey("Account")
    quantity = IntCol(default=0)
    amount = CurrencyCol(default=0)
    otherReport = ForeignKey("OtherReport")

    def add(self, amount):
        self.amount += amount
        self.quantity += 1

class AuxiliarPrestamo(object):
    
    def __init__(self, id, afiliado, monto, neto, papeleo, aportaciones,
                 intereses, retencion, reintegros):
        
        self.id = id
        self.afiliado = afiliado
        self.monto = monto
        self.neto = neto
        self.papeleo = papeleo
        self.aportaciones = aportaciones
        self.intereses = intereses
        self.retencion = retencion
        self.reintegros = reintegros

class Observacion(SQLObject):
    
    affiliate = ForeignKey("Affiliate")
    texto = UnicodeCol()
    fecha = DateCol(default=date.today)

class Solicitud(SQLObject):
    
    affiliate = ForeignKey("Affiliate")
    ingreso = DateCol(default=date.today)
    entrega = DateCol(default=date.today)
    monto = CurrencyCol(default=0, notNone=True)
    periodo = IntCol(default=12)
    
    def prestamo(self, user):
        
        tipo = Decimal(20) / 1200
        numerado = str(1 - math.pow(tipo + 1, -self.periodo))
        cuota = self.monto * Decimal(tipo / Decimal(numerado))
        
        kw = dict()
        kw['aproval'] = user
        kw['affiliate'] = self.affiliate
        kw['capital'] = self.monto
        kw['interest'] = 20
        kw['payment'] = cuota
        kw['months'] = self.periodo
        kw['last'] = self.entrega
        kw['startDate'] = self.entrega
        kw['letters'] = wording.parse(self.monto).capitalize()
        kw['number'] = 0
        prestamo = Loan(**kw)
        prestamo.start()
        
        return prestamo

class FormaPago(SQLObject):
    
    """Maneras en que se puede efectuar un pago"""
    
    nombre = UnicodeCol(length=15)
    """Nombre de la forma de pago"""

class Reintegro(SQLObject):
    
    """Cobros que debieron regresarse al empleador del afiliado y que deben ser
    cobrados de nuevo"""
    
    affiliate = ForeignKey('Affiliate')
    """:class:`Affiliate` al que pertenece el cobro"""
    emision = DateCol(default=date.today)
    """Fecha en que se emitio el pago del empleador"""
    monto = CurrencyCol()
    """Monto que debe cobrarse"""
    cheque = UnicodeCol(length=10)
    """Cheque bancario utilizado por el empleador para pagar"""
    planilla = UnicodeCol(length=10)
    """Codigo de la planilla enviado por el empleador"""
    motivo = UnicodeCol(length=100)
    """Razón por la cual se debe efectuar el cobro de nuevo"""
    formaPago = ForeignKey("FormaPago")
    """Modo en que se efectuó el cobro"""
    pagado = BoolCol(default=False)
    """Identifica si el reintegro ya ha sido pagado"""
    cancelacion = DateCol(default=date.today)
    """Indica el día en que se efectuó el cobro"""
    cuenta = ForeignKey('Account')
    """Cuenta a la que pertenece el reintegro"""
    
    def cancelar(self, dia=date.today()):
        
        """Marca el :class:`Reintegro` como pagado"""
        
        self.pagado = True
        self.cancelacion = dia
    
    def deduccion(self, dia=date.today()):
        
        """Efectua el pago del :class:`Reintegro` mediante una planilla"""
        
        self.cancelar(dia)
        self.formaPago = FormaPago.get(1)
        
        kw = dict()
        kw['amount'] = self.monto
        kw['affiliate'] = self.afiliado
        kw['account'] = self.cuenta
        kw['month'] = dia.month
        kw['year'] = dia.year
        
        kw['detail'] = "Reintegro {0} por {0}".format(
                                            self.emision.strftime('%d/%m/%Y'),
                                            self.motivo)
        
        Deduced(**kw)
    
    def revertir(self):
        
        """Revierte el pago del :class:`Reintegro`"""
        
        self.pagado = False

class Sobrevivencia(SQLObject):
    
    afiliado = ForeignKey("Affiliate")
    fecha = DateCol(default=date.today)
    monto = CurrencyCol(default=0)
    cheque = UnicodeCol(length=20, default=None)
    banco = UnicodeCol(length=50)

class Devolucion(SQLObject):
    
    afiliado = ForeignKey("Affiliate")
    """:class:`Afiliado` a quien se entrega"""
    concepto = UnicodeCol(length=200)
    """razon por la que se entrega la devolucion"""
    fecha = DateCol(default=date.today)
    """Día en cual se entrego el cheque"""
    monto = CurrencyCol()
    """Monto entregado"""
    cheque = UnicodeCol(length=20)
    """Referencia al cheque emitido"""
    banco = UnicodeCol(length=50)

class Funebre(SQLObject):
    
    """Ayuda funebre en caso de fallecimiento de un familiar"""
    
    class sqlmeta:
        table = 'ayuda_funebre'
    
    afiliado = ForeignKey("Affiliate")
    """:class:`Afiliado` a quien se entrega"""
    fecha = DateCol(default=date.today)
    """Día en cual se entrego el cheque"""
    monto = CurrencyCol()
    """Cantidad que se entrego"""
    cheque = UnicodeCol(length=20)
    """Referencia al cheque emitido"""
    pariente = UnicodeCol(length=100)
    """Familiar que fallecio"""
    banco = UnicodeCol(length=50)

class Indemnizacion(SQLObject):
    
    nombre = UnicodeCol(length=50)
    seguros = MultipleJoin("Seguro")

class Seguro(SQLObject):
    
    afiliado = MultipleJoin("Affiliate")
    indemnizacion = ForeignKey("Indemnizacion")
    fecha = DateCol(default=datetime.now)
    fallecimiento = DateCol(default=datetime.now)
    beneficiarios = MultipleJoin("Beneficiario")
    
    def monto(self):
        
        return sum(beneficiario.monto for beneficiario in self.beneficiarios)

class Beneficiario(SQLObject):
    
    seguro = ForeignKey("Seguro")
    nombre = UnicodeCol(length=50)
    monto = CurrencyCol()
    cheque = UnicodeCol(length=20)
    banco = UnicodeCol(length=50)
    fecha = DateCol(default=datetime.now)

class Asamblea(SQLObject):
    
    """Representación de asambleas efectuadas por la organización"""
    
    numero = IntCol()
    nombre = UnicodeCol(length=100)
    departamento = ForeignKey('Departamento')
    habilitado = BoolCol(default=False)

class Banco(SQLObject):
    
    """Instituciones bancarías a través de las cuales se efectuan los pagos de
    :class:`Viaticos`"""
    
    nombre = UnicodeCol(length=100)
    depositable = BoolCol(default=False)
    asambleista = BoolCol(default=False)
    depositos = MultipleJoin("Deposito")
    depositosAnonimos = MultipleJoin("DepositoAnonimo")

class Viatico(SQLObject):
    
    """Describe las cantidades a pagar por departamento para cada
    :class:`Asamblea`"""
    
    asamblea = ForeignKey('Asamblea')
    municipio = ForeignKey('Municipio')
    monto = CurrencyCol()

class Inscripcion(SQLObject):
    
    """Pagos a efectuar por concepto de :class:`Viaticos` a un
    :class:`Affiliate`"""
    
    afiliado = ForeignKey('Affiliate')
    """:class:`Afiliado` que se inscribio"""
    asamblea = ForeignKey('Asamblea')
    viatico = ForeignKey('Viatico')
    enviado = BoolCol(default=False)
    envio = DateCol(default=date.today)

class Deposito(SQLObject):
    
    """Pagos efectuados mediante un deposito bancario"""
    
    afiliado = ForeignKey("Affiliate")
    """:class:`Afiliado` que realizó el :class:`Deposito`"""
    banco = ForeignKey("Banco")
    concepto = UnicodeCol(length=50)
    fecha = DateCol(default=date.today)
    monto = CurrencyCol()

class DepositoAnonimo(SQLObject):
    
    """Depositos efectuados en el :class:`Banco` que no pueden ser rastreados
    a su depositante"""
    
    referencia = UnicodeCol(length=100)
    banco = ForeignKey("Banco")
    concepto = UnicodeCol(length=50)
    fecha = DateCol(default=date.today)
    monto = CurrencyCol()
