<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
    locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../../master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Pr&eacute;stamos</title>
        <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/status.css')}" media="print"/>
        <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print"/>
    </head>
    <body>
        <ul class="toolbox ui-widget ui-widget-header ui-corner-all noprint">
            <li><a class="ui-state-default ui-corner-all ui-button" href="${tg.url('/payed/view/%s' % loan.id)}">Modificar Datos del Pr&eacute;stamo</a></li>
            <li><a class="ui-state-default ui-corner-all ui-button" href="${tg.url('/payed/toLoan/%s' % loan.id)}">Enviar a Pr&eacute;stamos Normales</a></li>
            <li><a class="ui-state-default ui-corner-all ui-button" href="javascript:print();">Imprimir</a></li>
            <li py:if="'delete' in tg.identity.permissions"><a class="ui-state-default ui-corner-all ui-button" href="${'/payed/remove/%s' % loan.id}">Eliminar</a></li>
        </ul>
        <div class="noprint">&nbsp;</div>
        <div style="text-align: center;">
            <div style="font-weight: bold; font-size: 180%">COPEMH</div>
            <div style="font-weight: bold; font-size: 180%">Estado de Cuenta Pr&eacute;stamos Pagados</div>
            <div>Pr&eacute;stamo N&uacute;mero ${loan.id}</div>
            <span>Al: ${day.strftime('%d de %B de %Y')}</span>
        </div>
        <ul>
            <li>
                <strong>Prestatario:</strong>
                <a class="print" href="${tg.url('/affiliate/%s' % loan.affiliate.id)}">${loan.affiliate.id}</a> ${loan.affiliate.firstName} ${loan.affiliate.lastName}
            </li>
            <li>
                <strong>Fecha de Otorgamiento:</strong> ${loan.startDate}
            </li>
            <li>
                <strong>Monto Original:</strong> ${locale.currency(loan.capital, True, True)}
            </li>
        </ul>
        <table width="100%">
            <caption>Deducciones</caption>
            <tbody>
                <tr py:for="d in loan.deductions">
                    <td>${d.account.name}</td>
                    <td>${locale.currency(d.amount, True, True)}</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <td>Total deducciones</td>
                    <td><strong py:content="locale.currency(sum(d.amount for d in loan.deductions), True, True)" /></td>
                </tr>
                <tr>
                    <td>Remanente o Monto Liquidado</td>
                    <td><strong py:content="locale.currency(loan.capital - sum(d.amount for d in loan.deductions), True, True)" /></td>
                </tr>
            </tfoot>
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
                </tr>
            </thead>
            <tbody>
                <?python i = 1 ?>
                <tr py:for="pay in loan.pays">
                    <td>${pay.day.strftime('%d de %B de %Y')}</td>
                    <td>${i}/${loan.months}</td>					
                    <?python i += 1 ?>
                    <td>${locale.currency(pay.interest, True, True)}</td>
                    <td>${locale.currency(pay.capital, True, True)}</td>
                    <td>${locale.currency(pay.amount, True, True)}</td>
                    <td>${pay.receipt}</td>
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
