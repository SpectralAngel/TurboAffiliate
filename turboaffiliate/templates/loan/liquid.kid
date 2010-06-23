<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Afiliados</title>
    </head>
    <body>
        <h1>Pr&eacute;stamos por Liquidaci&oacute;n</h1>
        <table width="100%">
            <thead>
                <tr>
                    <th>Pr&eacute;stamo</th>
                    <th>COPEMH</th>
                    <th>Afiliado</th>
                    <th>Capital</th>
                    <th>Liquidado</th>
                    <th>Fecha de Inicio</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="loan in loans">
                    <td>${loan.id}</td>
                    <td>${loan.affiliate.id}</td>
                    <td>${loan.affiliate.firstName} ${loan.affiliate.lastName}</td>
                    <td>${locale.currency(loan.capital, True, True)}</td>
                    <td>${locale.currency(loan.net(), True, True)}</td>
                    <td>${loan.startDate}</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <td>Cantidad</td>
                    <td>${count}</td>
                    <td></td>
                    <td>${locale.currency(capital, True, True)}</td>
                    <td>${locale.currency(debt, True, True)}</td>
                    <td></td>
                </tr>
            </tfoot>
        </table>
    </body>
</html>
