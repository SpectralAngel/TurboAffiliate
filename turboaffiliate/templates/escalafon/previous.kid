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
                    <td>0</td>
                    <td>Cuota Aportaciones Ordinarias</td>
                    <td>${count}</td>
                    <td>${locale.currency(count * obligation)}</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>Cuota Ordinaria de Pr&eacute;tamo</td>
                    <td>${loan.qty}</td>
                    <td>${locale.currency(loan.amount)}</td>
                </tr>
                <tr py:for="key, value in resume.items()">
                    <td>${key.code}</td>
                    <td>${key.name}</td>
                    <td>${value['number']}</td>
                    <td>${locale.currency(value['total'])}</td>
                </tr>
                <tr>
                    <td colspan="3">Total</td>
                    <td>${locale.currency(totale)}</td>
                </tr>
            </tbody>
        </table>
    </body>
</html>
