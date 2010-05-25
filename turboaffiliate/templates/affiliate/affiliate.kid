<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
    locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Afiliado ${affiliate.id}</title>
        <script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
        <script type="text/javascript">
        <![CDATA[
        $(document).ready(function(e)
        {
            $('input.date-picker').datepicker({
                dateFormat: 'yy-mm-dd',
                changeMonth: true,
                changeYear: true,
                yearRange: '1940:2010'
            });
        });
        ]]>
        </script>
    </head>
    <body>
        <div id="breadcrum">
            <a class="previous" href="${tg.url('/affiliate/%s' % (affiliate.id - 1))}">Anterior</a>
            <a class="next" href="${tg.url('/affiliate/%s' % (affiliate.id + 1))}">Siguiente</a>
        </div>
        <ul class="toolbox">
            <li>
                <a class="edit" href="${tg.url('/affiliate/edit/%s' % affiliate.id)}">Editar</a>
            </li>
            <li py:if="'admin' in tg.identity.groups">
                <a class="delete" href="${tg.url('/affiliate/remove/%s' % affiliate.id)}">Borrar</a>
            </li>
            <li>
                <a class="add" href="${tg.url('/affiliate/extra/add/%s' % affiliate.id)}">A&ntilde;adir Deducci&oacute;n Extra</a>
            </li>
            <li>
                <a class="add" href="${tg.url('/affiliate/jubilate/%s' % affiliate.id)}">Editar Fecha de Jubilaci&oacute;n</a>
            </li>
            <li>
                <a py:if="affiliate.active" class="delete" href="${tg.url('/affiliate/deactivate/%s' % affiliate.id)}">Desactivar Afiliado</a>
                <a py:if="not affiliate.active" class="delete" href="${tg.url('/affiliate/activate/%s' % affiliate.id)}">Activar Afiliado</a>
            </li>
            <li>
                <a class="view" href="${tg.url('/affiliate/deduced/%s' % affiliate.id)}">Ver detalle de Deducciones</a>
            </li>
        </ul>
        <h1 class="afiliado">${affiliate.id} - ${affiliate.firstName} ${affiliate.lastName}</h1>
        <h3>ID: ${affiliate.cardID}   <span class="pago">${affiliate.payment}</span>
        <span class="pago" py:if="affiliate.payment == 'INPREMA'">N&uacute;mero de Cobro:
        ${affiliate.escalafon}</span>
        </h3>
        
        <h3>Afiliado desde <span py:if="not affiliate.joined is None">${affiliate.joined.strftime('%d de %B de %Y')}</span>
            <a href="${tg.url('/affiliate/status/%s' % affiliate.id)}">Aportaciones</a> &bull;
            <a href="${tg.url('/reintegro/afiliado/%s' % affiliate.id)}">Reintegros</a>
        </h3>
        
        <h4 py:if="affiliate.payment == 'INPREMA' and affiliate.jubilated != None">
                Jubilado desde ${affiliate.jubilated.strftime('%d de %B de %Y')}
        </h4>
        <span class="flas">
            <span py:if="affiliate.payment == 'INPREMA' and affiliate.jubilated == None">
            Este Afiliado requiere Actualizar sus datos de Jubilaci&oacute;n haga
            <a href="${tg.url('/affiliate/jubilate/%s' % affiliate.id)}">click aqu&iacute;</a>
            actualizarlos</span>
            <span py:if="affiliate.cardID == None">Este afiliado no
            tiene tarjeta de identidad ingresada haga
            <a href="${tg.url('/affiliate/edit/%s' % affiliate.id)}">click aqu&iacute;</a>
            para ingresarla</span>
            <span py:if="affiliate.state == None or affiliate.state ==''">Este afiliado no
            tiene Departamento
            <a href="${tg.url('/affiliate/edit/%s' % affiliate.id)}">Ingresar</a></span>
            <span py:if="affiliate.town == None or affiliate.town ==''">Este afiliado no
            tiene Ciudad
            <a href="${tg.url('/affiliate/edit/%s' % affiliate.id)}">Ingresar</a></span>
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
                <th>Anio</th>
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
                    <td><a href="${tg.url('/affiliate/extra/delete/%s' % extra.id)}">X</a></td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="4">Total de Deducciones</td>
                    <td>${locale.currency(affiliate.get_monthly(), True, True)}</td>
                </tr>
            </tfoot>
        </table>
        <table>
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
                    <td>${loan.id}</td>
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
        <table>
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
        <form action="${tg.url('/solicitud/agregar')}">
                <fieldset>
                    <legend>Agregar Solicitud</legend>
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
                            <input name="entrega" class="date-picker" />
                        </li>
                        <li>
                            <label>Ingreso</label>
                            <input name="ingreso" class="date-picker" />
                        </li>
                        <li>
                            <input type="submit" value="Agregar" />
                        </li>
                    </ol>
                </fieldset>
            </form>
        <table>
            <caption>Historial de Pr&eacute;stamos</caption>
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
                <tr py:for="loan in affiliate.payedLoans">
                    <td>${loan.id}</td>
                    <td>${locale.currency(loan.capital, True, True)}</td>
                    <td>${locale.currency(0)}</td>
                    <td>${locale.currency(loan.payment, True, True)}</td>
                    <td>${loan.last.strftime('%d de %B de %Y')}</td>
                    <td><a href="${tg.url('/payed/%s' % loan.id)}" >Ver</a></td>
                </tr>
            </tbody>
        </table>
        <form action="${tg.url('/affiliate/deduced/mostrar')}" method="get">
            <fieldset>
                <legend>Ver Deducciones Realizadas</legend>
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
                    <li><input value="Mostrar" type="submit" /></li>
                </ul>
            </fieldset>
        </form>
        <div id="observaciones">
            <h2>Observaciones</h2>
            <p py:for="observacion in affiliate.observaciones" py:content="observacion.texto" />
            <form action="${tg.url('/affiliate/observacion/add')}">
                <fieldset>
                    <legend>Agregar Observaci&oacute;n</legend>
                    <ol>
                        <li>
                            <input name="affiliate" value="${affiliate.id}" type="hidden" />
                            <label>Observaci&oacute;n</label>
                            <textarea name="texto"></textarea>
                        </li>
                        <li>
                            <input type="submit" value="Agregar" />
                        </li>
                    </ol>
                </fieldset>
            </form>
        </div>
    </body>
</html>
