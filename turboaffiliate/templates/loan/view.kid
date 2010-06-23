<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Pr&eacute;stamos</title>
        <script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/jquery.date.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/prestamo.js')}" type="text/javascript"></script>
    </head>
    <body>
        <div style="text-align: center;">
            <h1>COPEMH</h1>
            <h2>Estado de Cuenta P&eacute;stamos</h2>
            <h3>Pr&eacute;stamo N&uacute;mero ${loan.id}</h3>
        </div>
        <ul>
            <li>
                <strong>Prestatario:</strong> <a href="${tg.url('/affiliate/%s' % loan.affiliate.id)}">${loan.affiliate.id}</a>
                ${loan.affiliate.firstName} ${loan.affiliate.lastName}
            </li>
            <li>
                <strong>Fecha de Inicio:</strong> ${loan.startDate.strftime('%d/%m/%Y')}
            </li>
            <li>
                <strong>Pago Mensual:</strong> ${locale.currency(loan.payment, True, True)}
            </li>
            <li>
                <strong>Monto Original:</strong> ${locale.currency(loan.capital, True, True)"}
            </li>
            <li>
                <strong>Monto Debido:</strong> ${locale.currency(loan.debt, True, True)}
            </li>
        </ul>
        <ul>
            <li class="add">
                <a href="${tg.url('/loan/pay/add/%s' % loan.id)}">Agregar un Pago</a>
            </li>
            <li class="delete">
                <a href="${'/loan/remove/%s' % loan.id}">Eliminar</a>
            </li>
            <li class="add">
                <a href="${tg.url('/loan/deduction/add/%s' % loan.id)}">A&ntilde;adir Deducci&oacute;n</a>
            </li>
            <li>
                <a href="${tg.url('/loan/increase/%s' % loan.id)}">Corregir Mes +1</a>
            </li>
            <li>
                <a href="${tg.url('/loan/decrease/%s' % loan.id)}">Corregir Mes -1</a>
            </li>
        </ul>
        <form action="${tg.url('/loan/modify')}">
            <fieldset>
                <legend>Cambiar Cuota</legend>
                <ul>
                    <li>
                        <label for="payment">Cuota:</label>
                        <input name="payment" />
                        <input type="hidden" name="loan" value="${loan.id}" />
                    </li>
                    <li>
                        <input value="Modificar"  type="submit" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('/loan/debt')}">
            <fieldset>
                <legend>Cambiar Saldo</legend>
                <ul>
                    <li>
                        <label for="debt">Nuevo Saldo:</label>
                        <input name="debt" />
                        <input type="hidden" name="loan" value="${loan.id}" />
                    </li>
                    <li>
                        <input value="Modificar"  type="submit" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('/loan/capital')}">
            <fieldset>
                <legend>Cambiar Monto</legend>
                <ul>
                    <li>
                        <label for="amount">Nuevo Monto:</label>
                        <input name="amount" />
                        <input type="hidden" name="loan" value="${loan.id}" />
                    </li>
                    <li>
                        <input value="Modificar"  type="submit" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('/loan/month')}">
            <fieldset>
                <legend>Cambiar Periodo de Pago</legend>
                <ul>
                    <li>
                        <label for="months">Meses:</label>
                        <input name="months" id="months" />
                        <input type="hidden" name="loan" value="${loan.id}" />
                    </li>
                    <li>
                        <label for="payment">Cuota:</label>
                        <input name="payment" id="payment" />
                    </li>
                    <li>
                        <input value="Modificar"  type="submit" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <h4>Deducciones Aplicadas</h4>
        <table>
            <thead>
                <tr>
                    <th>Concepto</th>
                    <th>Cantidad</th>
                    <th>Descripci&oacute;n</th>
                    <th py:if="tg.identity.user.has_permission('delete')">Borrar</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="deduction in loan.deductions">
                    <td>${deduction.account.name}</td>
                    <td>${locale.currency(deduction.amount, True, True)}</td>
                    <td>${deduction.description}</td>
                    <td py:if="'delete' in tg.identity.permissions">
                        <a href="${tg.url('/loan/deduction/remove/%s' % deduction.id)}">Borrar</a>
                    </td>
                </tr>
            </tbody>
        </table>
        <table class="pay" py:if="len(loan.pays) != 0">
            <caption>Pagos Efectuados</caption>
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
            <tfoot class="noprint">
                <tr>
                    <th colspan="2">Total Pagado:</th>
                    <th>${locale.currency(loan.interesesPagados(), True, True)}</th>
                    <th>${locale.currency(loan.capitalPagado(), True, True)}</th>
                    <th>${locale.currency(loan.pagado(), True, True)}</th>
                    <th></th>
                    <th class="noprint"></th>
                </tr>
            </tfoot>
        </table>
    </body>
</html>

