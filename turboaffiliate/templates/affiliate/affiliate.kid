<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
    locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Afiliado ${affiliate.id}</title>
        <script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/afiliado.js')}" type="text/javascript"> </script>
    </head>
    <body>
        <div class="noprint" id="breadcrum">
            <a class="previous" href="${tg.url('/affiliate/%s' % (affiliate.id - 1))}">Anterior</a>
            <a class="next" href="${tg.url('/affiliate/%s' % (affiliate.id + 1))}">Siguiente</a>
        </div>
        <h1 class="afiliado">${affiliate.id} - ${affiliate.firstName} ${affiliate.lastName}</h1>
        <ul class="toolbox ui-widget ui-widget-header ui-corner-all noprint">
            <li><a class="ui-state-default ui-corner-all ui-button" href="#" onclick="javascript:$('.editar').dialog('open');">Editar</a></li>
            <li py:if="'admin' in tg.identity.groups"><a class="ui-state-default ui-corner-all ui-button" href="${tg.url('/affiliate/remove/%s' % affiliate.id)}">Borrar</a></li>
            <li><a href="#" class="ui-state-default ui-corner-all ui-button" onclick="javascript:$('.extra').dialog('open');">Agregar Deducci&oacute;n</a></li>
            <li><a href="#" class="ui-state-default ui-corner-all ui-button" onclick="javascript:$('.jubilar').dialog('open');">Jubilar</a></li>
            <li><a href="#" class="ui-state-default ui-corner-all ui-button" onclick="javascript:$('.desactivar').dialog('open');">Desactivar</a><a class="ui-state-default ui-corner-all ui-button" py:if="not affiliate.active" href="${tg.url('/affiliate/activate/%s' % affiliate.id)}">Activar Afiliado</a></li>
            <li><a href="#" class="ui-state-default ui-corner-all ui-button" onclick="javascript:$('.agregarSolicitud').dialog('open');">Agregar Solicitud</a></li>
            <li><a href="#" class="ui-state-default ui-corner-all ui-button" onclick="javascript:$('.verDeducciones').dialog('open');">Mostrar Deducciones</a></li>
            <li><a href="#" class="ui-state-default ui-corner-all ui-button" onclick="javascript:$('.agregarObservacion').dialog('open');">Observaci&oacute;n</a></li>
        </ul>
        <h3>ID: ${affiliate.cardID} <span class="pago">${affiliate.payment}</span>
        <span class="pago" py:if="affiliate.payment != 'Escalafon'">N&uacute;mero de Cobro:
        ${affiliate.escalafon}</span> Afiliado desde <span py:if="not affiliate.joined is None">${affiliate.joined.strftime('%d de %B de %Y')}</span></h3>
        <ul class="toolbox ui-widget ui-widget-header ui-corner-all noprint">
            <li>Estados de Cuenta:</li>
            <li><a class="ui-state-default ui-corner-all ui-button" href="${tg.url('/affiliate/status/%s' % affiliate.id)}">Aportaciones</a></li>
            <li><a class="ui-state-default ui-corner-all ui-button" href="${tg.url('/reintegro/%s' % affiliate.id)}">Reintegros</a></li>
            <li><a class="ui-state-default ui-corner-all ui-button" href="${tg.url('/affiliate/deduced/%s' % affiliate.id)}">Deducciones</a></li>
        </ul>
        <h4 py:if="affiliate.payment == 'INPREMA' and affiliate.jubilated != None">
                Jubilado desde ${affiliate.jubilated.strftime('%d de %B de %Y')}
        </h4>
        <span class="flash">
            <span py:if="affiliate.payment == 'INPREMA' and affiliate.jubilated == None">
            Este Afiliado requiere Actualizar sus datos de Jubilaci&oacute;n haga
            <a class="ui-state-default ui-corner-all ui-button" href="${tg.url('/affiliate/jubilate/%s' % affiliate.id)}">click aqu&iacute;</a>
            actualizarlos</span>
            <span py:if="affiliate.cardID == None">Este afiliado no
            tiene tarjeta de identidad ingresada haga
            <a href="${tg.url('/affiliate/edit/%s' % affiliate.id)}">click aqu&iacute;</a>
            para ingresarla</span>
            <span py:if="affiliate.state == None or affiliate.state ==''">Este afiliado no
            tiene Departamento
            <a class="ui-state-default ui-corner-all ui-button"  href="${tg.url('/affiliate/edit/%s' % affiliate.id)}">Ingresar</a></span>
            <span py:if="affiliate.town == None or affiliate.town ==''">Este afiliado no
            tiene Ciudad
            <a class="ui-state-default ui-corner-all ui-button"  href="${tg.url('/affiliate/edit/%s' % affiliate.id)}">Ingresar</a></span>
        </span>
        <h3 class="flash" py:if="not affiliate.active">Afiliado desactivado, razon:<strong><span class="flash" py:if="not affiliate.active" py:content="affiliate.reason" /></strong></h3>
        <h3>Informaci&oacute;n Personal</h3>
        <ul>
            <li>
                <strong>Lugar de Nacimiento: </strong>
                <span py:content="affiliate.birthPlace" />
            </li>
            <li>
                <strong>Fecha de Nacimiento: </strong>
                <span py:if="not affiliate.birthday is None" py:content="affiliate.birthday.strftime('%d de %B de %Y')" />
            </li>
            <li>
                <strong>G&eacute;nero:</strong>
                <span py:if="affiliate.gender == 'M'">Masculino</span>
                <span py:if="affiliate.gender == 'F'">Femenino</span>
            </li>
            <li>
                <strong>Tel&eacute;fono: </strong>
                <span py:content="affiliate.phone" />
            </li>
            <li>
                <strong>Instituto: </strong>
                <span py:content="affiliate.school" />
            </li>
            <li>
                <strong>Instituto: </strong>
                <span py:content="affiliate.school2" />
            </li>
            <li>
                <strong>Municipio: </strong>
                <span py:content="affiliate.town" />
            </li>
            <li>
                <strong>Departamento: </strong>
                <span py:content="affiliate.state" />
            </li>
        </ul>
        <table>
            <caption>Cobros a Efectuar</caption>
            <thead>
                <th>Concepto</th>
                <th>Retrasada</th>
                <th>Mes</th>
                <th>A&ntilde;o</th>
                <th>Cantidad</th>
                <th>Borrar</th>
            </thead>
            <tbody>
                <tr>
                    <td>Aportaci&oacute;n Ordinaria</td>
                    <td>No</td>
                    <td></td>
                    <td></td>
                    <td>${locale.currency(affiliate.get_cuota(), True, True)}</td>
                    <td></td>
                </tr>
                <tr py:for="loan in affiliate.loans">
                    <td>Cuota de Pr&eacute;stamo</td>
                    <td>No</td>
                    <td></td>
                    <td></td>
                    <td>${locale.currency(loan.get_payment(), True, True)}</td>
                    <td></td>
                </tr>
                <tr py:for="extra in affiliate.extras">
                    <td>${extra.account.name}</td>
                    <td py:if="extra.retrasada">S&iacute;</td>
                    <td py:if="not extra.retrasada">No</td>
                    <td>${extra.mes}</td>
                    <td>${extra.anio}</td>
                    <td>${locale.currency(extra.amount, True, True)}</td>
                    <td><a class="ui-state-default ui-corner-all ui-button" href="${tg.url('/affiliate/extra/delete/%s' % extra.id)}">X</a></td>
                </tr>
                <tr py:for="reintegro in affiliate.reintegros" py:if="not reintegro.pagado">
                    <td>Reintegro</td>
                    <td>No</td>
                    <td>${reintegro.motivo}</td>
                    <td>${reintegro.emision.strftime('%d/%m/%Y')}</td>
                    <td>${locale.currency(reintegro.monto, True, True)}</td>
                    <td>X</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="4">Total de Deducciones</td>
                    <td>${locale.currency(affiliate.get_monthly(), True, True)}</td>
                </tr>
            </tfoot>
        </table>
        <table class="ui-widget" py:if="len(affiliate.loans) != 0">
            <caption>Pr&eacute;stamos Personales</caption>
            <thead>
                <tr>
                    <th>Solicitud</th>
                    <th>Monto</th>
                    <th>Deuda</th>
                    <th>Cuota</th>
                    <th>Ultimo Pago</th>
                    <th>Ver</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="loan in affiliate.loans">
                    <td><a href="${tg.url('/loan/%s' % loan.id)}" >${loan.id}</a></td>
                    <td>${locale.currency(loan.capital, True, True)}</td>
                    <td>${locale.currency(loan.debt, True, True)}</td>
                    <td>${locale.currency(loan.payment, True, True)}</td>
                    <td>${loan.last.strftime('%d de %B de %Y')}</td>
                    <td><a href="${tg.url('/loan/%s' % loan.id)}" >Ver</a></td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <th colspan="6"><a href="${tg.url('/loan/add/%s' % affiliate.id)}">Agregar Pr&eacute;stamo</a></th>
                </tr>
            </tfoot>
        </table>
        <a py:if="len(affiliate.loans) == 0" href="${tg.url('/loan/add/%s' % affiliate.id)}">Agregar Pr&eacute;stamo</a>
        <table py:if="len(affiliate.solicitudes) != 0">
            <caption>Solicitudes de Pr&eacute;stamo</caption>
            <thead>
                <tr>
                    <th>Monto</th>
                    <th>Periodo</th>
                    <th>Recibido</th>
                    <th>Entrega</th>
                    <th>Liquidar</th>
                    <th>Eliminar</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="solicitud in affiliate.solicitudes">
                    <td>${locale.currency(solicitud.monto, True, True)}</td>
                    <td>${solicitud.periodo}</td>
                    <td>${solicitud.ingreso.strftime('%d de %B de %Y')}</td>
                    <td>${solicitud.entrega.strftime('%d de %B de %Y')}</td>
                    <td><a href="${tg.url('/solicitud/convertir/%s' % solicitud.id)}">Liquidar</a></td>
                    <td><a href="${tg.url('/solicitud/eliminar/%s' % solicitud.id)}">Eliminar</a></td>
                </tr>
            </tbody>
        </table>
        <table py:if="len(affiliate.payedLoans) != 0">
            <caption>Historial de Pr&eacute;stamos Cancelados</caption>
            <thead>
                <tr>
                    <th>Solicitud</th>
                    <th>Monto</th>
                    <th>Cuota</th>
                    <th>Ultimo Pago</th>
                    <th>Ver</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="loan in affiliate.payedLoans">
                    <td><a href="${tg.url('/payed/%s' % loan.id)}">${loan.id}</a></td>
                    <td>${locale.currency(loan.capital, True, True)}</td>
                    <td>${locale.currency(loan.payment, True, True)}</td>
                    <td>${loan.last.strftime('%d de %B de %Y')}</td>
                    <td><a href="${tg.url('/payed/%s' % loan.id)}" >Ver</a></td>
                </tr>
            </tbody>
        </table>
        <table py:if="len(affiliate.observaciones) != 0">
            <caption>Observaciones</caption>
            <thead>
                <tr>
                    <th>Descripci&oacute;n</th>
                    <th>Fecha</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="observacion in affiliate.observaciones">
                    <td>${observacion.texto}</td>
                    <td py:if="observacion.fecha != None">${observacion.fecha.strftime('%d/%m/%Y')}</td>
                </tr>
            </tbody>
        </table>
        <form class="verDeducciones" action="${tg.url('/affiliate/deduced/mostrar')}" method="get">
            <div>
                <ul>
                    <input type="hidden" value="${affiliate.id}" name="afiliado" />
                    <li>
                        <label>Mes:</label>
                        <input name="mes" />
                    </li>
                    <li>
                        <label>A&ntilde;o:</label>
                        <input name="anio" />
                    </li>
                </ul>
            </div>
        </form>
        <form class="agregarSolicitud" action="${tg.url('/solicitud/agregar')}">
            <div>
                <ol>
                    <li>
                        <input name="affiliate" value="${affiliate.id}" type="hidden" />
                        <label>Monto</label>
                        <input name="monto" />
                    </li>
                    <li>
                        <label>Periodo</label>
                        <input name="periodo" />
                    </li>
                    <li>
                        <label>Entrega</label>
                        <input name="entrega" class="datepicker" />
                    </li>
                    <li>
                        <label>Ingreso</label>
                        <input name="ingreso" class="datepicker" />
                    </li>
                </ol>
            </div>
        </form>
        <form class="agregarObservacion" action="${tg.url('/affiliate/observacion/add')}">
            <div>
                <ol>
                    <li>
                        <input name="affiliate" value="${affiliate.id}" type="hidden" />
                        <label>Observaci&oacute;n</label>
                        <textarea name="texto" cols="18"></textarea>
                    </li>
                </ol>
            </div>
        </form>
        <form class="desactivar" action="${tg.url('/affiliate/deactivate')}" method="post">
            <div>
                <input value="${affiliate.id}" name="affiliate" type="hidden" />
                <ul>
                    <li>
                        <label>Raz&oacute;n</label>
                        <select name="reason">
                            <option>Retiro</option>
                            <option>Fallecimiento</option>
                            <option>Renuncia</option>
                            <option>No es Afiliado</option>
                            <option>Suspendido</option>
                        </select>
                    </li>
                </ul>
            </div>
        </form>
        <form class="editar" action="${tg.url('/affiliate/save')}" method="post">
            <div>
                <input type="hidden" value="${affiliate.id}" name="affiliate" />
                <ul>
                    <li>
                        <label for="firstName">Nombre:</label>
                        <input name="firstName" value="${affiliate.firstName}" />
                    </li>
                    <li>
                        <label for="lastName">Apellido:</label>
                        <input name="lastName" value="${affiliate.lastName}" />
                    </li>
                    <li>
                        <label for="birthPlace">Lugar de Nacimiento:</label>
                        <input name= "birthPlace" value="${affiliate.birthPlace}" />
                    </li>
                    <li>
                        <label for="phone">Tel&eacute;fono:</label>
                        <input name="phone" value="${affiliate.phone}"/>
                    </li>
                    <li>
                        <label>Identidad:</label>
                        <input name="cardID" value="${affiliate.cardID}" maxlength="15"/>
                    </li>
                    <li>
                        <label for="birthday">Fecha de Nacimiento</label>
                        <input name="birthday" value="${affiliate.birthday.strftime('%d/%m/%Y')}" class="datepicker" />
                    </li>
                    <li>
                        <label for="payment">Cotiza por:</label>
                        <select name="payment">
                            <option py:if="affiliate.payment == 'Escalafon'" selected="">Escalafon</option>
                            <option py:if="not affiliate.payment == 'Escalafon'">Escalafon</option>
                            <option py:if="affiliate.payment == 'UPN'" selected="">UPN</option>
                            <option py:if="not affiliate.payment == 'UPN'">UPN</option>
                            <option py:if="affiliate.payment == 'INPREMA'" selected="">INPREMA</option>
                            <option py:if="not affiliate.payment == 'INPREMA'">INPREMA</option>
                            <option py:if="affiliate.payment == 'Ventanilla'" selected="">Ventanilla</option>
                            <option py:if="not affiliate.payment == 'Ventanilla'">Ventanilla</option>
                            <option py:if="affiliate.payment == 'Ministerio'" selected="">Ministerio</option>
                            <option py:if="not affiliate.payment == 'Ministerio'">Ministerio</option>
                            <option py:if="affiliate.payment == 'Retirado'" selected="">Retirado</option>
                            <option py:if="not affiliate.payment == 'Retirado'">Retirado</option>
                        </select>
                    </li>
                    <li>
                        <label for="escalafon">Escalaf&oacute;n:</label>
                        <input name="escalafon" value="${affiliate.escalafon}" />
                    </li>
                    <li>
                        <label for="school">Instituto:</label>
                        <input name="school" value="${affiliate.school}" />
                    </li>
                    <li>
                        <label for="town">Municipio:</label>
                        <input name="town" value="${affiliate.town}" />
                    </li>
                    <li>
                        <label for="state">Departamento:</label>
                        <input name="state" value="${affiliate.state}" />
                    </li>
                </ul>
            </div>
        </form>
        <form class="extra" action="${tg.url('/affiliate/extra/save')}" method="post">
            <div>
                <input type="hidden" name="affiliate" value="${affiliate.id}" />
                <ul>
                    <li>
                        <label for="amount">Cantidad:</label>
                        <input name="amount" />
                    </li>
                    <li>
                        <label for="account">Cuenta:</label>
                        <select name="account">
                            <option py:for="account in accounts" value="${account.id}">${account.name}</option>
                        </select>
                    </li>
                    <li>
                        <label for="months">Meses</label>
                        <input name="months" />
                    </li>
                    <li>
                        <label>Es Retrasada</label>
                        <input name="retrasada" type="checkbox" />
                    </li>
                </ul>
            </div>
        </form>
        <form class="jubilar" action="/affiliate/jubilar" method="post">
			<div>
				<ul>
					<li>
						<label for="jubilated">Fecha de Jubilaci&oacute;n</label>
						<input py:if="affiliate.jubilated != None" name="jubilated" value="${affiliate.jubilated.strftime('%d/%m/%Y')}" class="datepicker" />
                        <input py:if="affiliate.jubilated == None" name="jubilated" class="datepicker" />
						<input type="hidden" value="${affiliate.id}" name="affiliate" />
					</li>
                    <li>
                        <label for="cobro">N&uacute;mero de Cobro:</label>
                        <input name="cobro" value="${affiliate.escalafon}" />
                    </li>
				</ul>
			</div>
		</form>
    </body>
</html>
