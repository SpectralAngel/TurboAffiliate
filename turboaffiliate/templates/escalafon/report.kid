<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Afiliados</title>
    </head>
    <body>
        <h1>Reporte de Ingresos ${legend}</h1>
        <table>
            <thead>
                <tr>
                    <th>C&oacute;digo</th>
                    <th>Cuenta</th>
                    <th>Afiliados</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>Aportaciones Ordinarias</td>
                    <td>${count}</td>
                    <td>${locale.currency(count * obligation, True, True)}</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>Cuota Pr&eacute;stamo</td>
                    <td>${loans['count']}</td>
                    <td>${locale.currency(loans['amount'], True, True)}</td>
                </tr>
                <tr py:for="deduccion in deductions">
                    <td>${deduccion.code}</td>
                    <td>${deduccion.name}</td>
                    <td>${deductions[deduccion]['count']" />
                    <td py:content="locale.currency(deductions[deduccion]['amount'], True, True)" />
                </tr>
            </tbody>
        </table>
        <h2>Total de Ingresos: ${(total + loans['amount'] + count * obligation, True, True)}</h2>
    </body>
</html>
