<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
    locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>COPEMH &bull; Pr&eacute;stamo ${loan.id}</title>
        <script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/prestamo.js')}" type="text/javascript"></script>
    </head>
    <body>
        <ul class="toolbox ui-widget ui-widget-header ui-corner-all noprint">
            <li><a class="ui-state-default ui-corner-all ui-button" href="#" onclick="javascript:$('.pagar').dialog('open');">Agregar un Pago</a></li>
            <li><a class="ui-state-default ui-corner-all ui-button" href="#" onclick="javascript:$('.deduccion').dialog('open');">Agregar una Deducci&oacute;n</a></li>
            <li><a class="ui-state-default ui-corner-all ui-button" href="#" onclick="javascript:$('#refinanciar').dialog('open');">Refinanciar</a></li>
            <li><a class="ui-state-default ui-corner-all ui-button" href="${tg.url('/loan/view/%s' % loan.id)}">Modificar Datos del Pr&eacute;stamo</a></li>
            <li><a class="ui-state-default ui-corner-all ui-button" href="${tg.url('/loan/pagare/%s' % loan.id)}">Ver Pagar&eacute;</a></li>
            <li><a class="ui-state-default ui-corner-all ui-button" href="${tg.url('/loan/receipt/%s' % loan.id)}">Ver Liquidaci&oacute;n</a></li>
            <li><a class="ui-state-default ui-corner-all ui-button" href="javascript:print();">Imprimir</a></li>
            <li py:if="'delete' in tg.identity.permissions"><a class="ui-state-default ui-corner-all ui-button" href="${'/loan/remove/%s' % loan.id}">Eliminar</a></li>
        </ul>
        <div class="noprint">&nbsp;</div>
        <div style="text-align: center;">
            <div style="font-weight: bold; font-size: 180%">COPEMH</div>
            <div style="font-weight: bold; font-size: 180%">Estado de Cuenta Pr&eacute;stamos</div>
            <div>Pr&eacute;stamo N&uacute;mero ${loan.id}</div>
            <span>Al: ${day.strftime('%d de %B de %Y')}</span>
        </div>
        <ul>
            <li>
                <strong>Prestatario:</strong>
                <a href="${tg.url('/affiliate/%s' % loan.affiliate.id)}">${loan.affiliate.id}</a>
                ${loan.affiliate.firstName} ${loan.affiliate.lastName}
            </li>
            <li>
                <strong>Fecha de Otorgamiento:</strong>
                ${loan.startDate.strftime('%d de %B de %Y')}
            </li>
            <li>
                <strong>Monto Original:</strong>
                ${locale.currency(loan.capital, True, True)}
            </li>
        </ul>
        <table width="100%">
            <caption>Deducciones</caption>
            <tr py:for="d in loan.deductions">
                <td>${d.name}</td>
                <td>${locale.currency(d.amount, True, True)}</td>
            </tr>
            <tr>
                <td>Total deducciones</td>
                <td><strong>${locale.currency(sum(d.amount for d in loan.deductions), True, True)}</strong></td>
            </tr>
            <tr>
                <td>Remanente o Monto Liquidado</td>
                <td><strong>${locale.currency(loan.capital - sum(d.amount for d in loan.deductions), True, True)}</strong></td>
            </tr>
        </table>
        <table class="pay" py:if="len(loan.future()) != 0">
            <caption>Pagos a Efectuar</caption>
            <thead>
                <tr>
                    <th colspan="5">Abono</th>
                    <th>&nbsp;
                    </th>
                </tr>
                <tr>
                    <th>Mes</th>
                    <th>Pago N&ordm;</th>
                    <th>Intereses</th>
                    <th>Cuota</th>
                    <th>Capital</th>
                    <th>Saldo</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td colspan="5">&nbsp;</td>
                    <td><strong>${locale.currency(loan.debt, True, True)}</strong></td>
                </tr>
                <tr py:for="pay in loan.future()">
                    <td>${pay['month']}</td>
                    <td>${pay['number']}</td>
                    <td>${locale.currency(pay['interest'], True, True)}</td>
                    <td>${locale.currency(pay['payment'], True, True)}</td>
                    <td>${locale.currency(pay['capital'], True, True)}</td>
                    <td>${locale.currency(pay['amount'], True, True)}</td>
                </tr>
            </tbody>
        </table>
        <table class="pay" py:if="len(loan.pays) != 0">
            <caption>Pagos Efectuados
            </caption>
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>N&uacute;mero</th>
                    <th>Intereses</th>
                    <th>Capital</th>
                    <th>Valor</th>
                    <th>Recibo</th>
                    <th class="noprint">Borrar</th>
                </tr>
            </thead>
            <tbody>
                <?python i = 1 ?>
                <tr py:for="pay in loan.pays">
                    <td py:content="pay.day.strftime('%d de %B de %Y')" />
                    <td>${i}/${loan.months}</td>
                    <?python i += 1 ?>
                    <td>${locale.currency(pay.interest, True, True)}</td>
                    <td>${locale.currency(pay.capital, True, True)}</td>
                    <td>${locale.currency(pay.amount, True, True)}</td>
                    <td>${pay.receipt}</td>
                    <td class="noprint"><a href="${tg.url('/loan/pay/remove/%s' % pay.id)}">X</a></td>
                </tr>
            </tbody>
        </table>
        <form class="pagar" action="${tg.url('/loan/pay/agregar')}" method="post">
            <div>
                <ul>
                    <li>
                        <label for="amount">Monto:</label>
                        <input name="amount" />
                    </li>
                    <li>
                        <label for="day">Fecha:</label>
                        <input name="day" class="datepicker" /><input type="hidden" name="loan" value="${loan.id}" />
                    </li>
                    <li>
                        <label for="receipt">Recibo:</label>
                        <input name="receipt" />
                    </li>
                    <li>
                        <label for="free">Libre de Intereses:</label>
                        <input name="free" type="checkbox" />
                    </li>
                </ul>
            </div>
        </form>
        <form class="deduccion" action="${tg.url('/loan/deduction/save')}" method="post">
            <div>
                <input type="hidden" name="loan" value="${loan.id}" />
                <ul>
                    <li>
                        <label for="name">Concepto:</label>
                        <input name="name" />
                    </li>
                    <li>
                        <label for="amount">Monto:</label>
                        <input name="amount" />
                    </li>
                    <li>
                        <label for="account">Cuenta:</label>
                        <select name="account">
                            <option py:for="account in accounts" py:content="account.code, ' - ', account.name" value="${account.id}" />
                        </select>
                    </li>
                    <li>
                        <label for="description">Descripci&oacute;n:</label>
                        <textarea name="description" />
                    </li>
                </ul>
            </div>
        </form>
        <form id="refinanciar" action="${tg.url('/loan/refinanciar')}" method="post">
            <div>
                <input type="hidden" name="loan" value="${loan.id}" />
                <ul>
                    <li>
                        <label for="solicitud">Solicitud:</label>
                        <select name="solicitud">
                            <option py:for="s in loan.affiliate.solicitudes" value="${s.id}">N&ordm; ${s.id} - ${locale.currency(s.monto, True, True)} ${s.entrega.strftime('%d de %B de %Y')}</option>
                        </select>
                    </li>
                    <li>
                        <label for="pago">Monto a Pagar:</label>
                        <input name="pago" />
                    </li>
                    <li>
                        <label for="cuenta">Cuenta para Deducir:</label>
                        <select name="cuenta">
                            <option py:for="account in accounts" py:content="account.code, ' - ', account.name" value="${account.id}" />
                        </select>
                    </li>
                    <li>
                        <label for="descripcion">Descripci&oacute;n deducci&oacute;n:</label>
                        <textarea name="descripcion" />
                    </li>
                </ul>
            </div>
        </form>
    </body>
</html>
