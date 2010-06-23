<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Afiliados</title>
    </head>
    <body>
         <h2>${affiliate.id} ${affiliate.firstName} ${affiliate.lastName}</h2>
         <p><strong>Monto Total: </strong><span py:content="locale.currency(obligation + affiliate.get_monthly(), True, True)" />
         <form action="${tg.url('/affiliate/complete')}" method="post">
                <input name="year" value="${year}" type="hidden" />
                <input name="affiliate" value="${affiliate.id}" type="hidden" />
                <input name="month" value="${month}" type="hidden" />
                <input name="day" value="${day.date().strftime('%Y-%m-%d')}" type="hidden" />
                <input value="Posteo Completo" type="submit" />
        </form>
        <form action="${tg.url('/affiliate/postobligation')}" method="post">
                <input name="year" value="${year}" type="hidden" />
                <input name="affiliate" value="${affiliate.id}" type="hidden" />
                <input name="month" value="${month}" type="hidden" />
                <input name="day" value="${day.date().strftime('%Y-%m-%d')}" type="hidden" />
                <input value="Postear Solo Aportaciones" type="submit" />
        </form>
        </p>
        <h3>Detalle Deducciones Extra</h3>
        <table>
            <thead>
                <tr>
                    <th>Cuenta</th>
                    <th>Monto</th>
                    <th>Postear</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="extra in affiliate.extras">
                    <td py:content="extra.account.name" />
                    <td py:content="locale.currency(extra.amount, True, True)" />
                    <td>
                        <form action="${tg.url('/affiliate/postextra')}" method="post">
                            <input name="year" value="${year}" type="hidden" />
                            <input name="extra" value="${extra.id}" type="hidden" />
                            <input name="month" value="${month}" type="hidden" />
                            <input value="Postear" type="submit" />
                        </form>
                    </td>
                </tr>
            </tbody>
        </table>
        <h4>Detalle de Pr&eacute;tamos</h4>
        <div py:for="loan in affiliate.loans">
            <h4 py:content="'Préstamo ', loan.id" />
            <form action="${tg.url('/affiliate/postloan')}" method="post">
                <fieldset>
                    <legend>Posteo de Pr&eacute;stamo</legend>
                    <label for="amount">Cantidad</label><input name="amount" readonly="readonly" value="${loan.get_payment()}" />
                    <input name="loan" value="${loan.id}" type="hidden" />
                    <input name="year" value="${year}" type="hidden" />
                    <input name="month" value="${month}" type="hidden" />
                    <input name="day" value="${day.date().strftime('%Y-%m-%d')}" type="hidden" />
                    <input value="Postear" type="submit" />
                </fieldset>
            </form>
            <form action="${tg.url('/affiliate/prestamo')}">
                <fieldset>
                    <legend>Postear otro Pago</legend>
                    <ul>
                        <li>
                            <label>Cuota:</label>
                            <input name="amount" />
                            <input name="year" value="${year}" type="hidden" />
                            <input name="month" value="${month}" type="hidden" />
                            <input name="loan" value="${loan.id}" type="hidden" />
                        </li>
                    </ul>
                </fieldset>
            </form>
        </div>
        <a href="${tg.url('/affiliate/listmanual?payment=%s&amp;month=%s&amp;year=%s&amp;day=%s' % (affiliate.payment, month, year, day.date()))}">Regresar</a>
    </body>
</html>

