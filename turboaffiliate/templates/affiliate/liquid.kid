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
    </head>
    <body>
        <h1>Liquidaciones de Pr&eacute;stamos</h1>
        <table>
            <thead>
                <tr>
                    <th>Prestamo</th>
                    <th>Afiliado</th>
                    <th>Afiliacion</th>
                    <th>Capital</th>
                    <th>Liquidado</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="loan in loans">
                    <td>${loan.id}</td>
                    <td>${loan.affiliate.firstName} ${loan.affiliate.lastName}</td>
                    <td>${loan.affiliate.id}</td>
                    <td>${loan.capital}</td>
                    <td>${locale.currency(loan.net(), True, True)}</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <th>Monto Total:</th>
                    <th>${locale.currency(amount, True, True)}</th>
                    <th colspan="2">Otorgados:</th>
                    <th>${count}</th>
                </tr>
            </tfoot>
        </table>
    </body>
</html>
