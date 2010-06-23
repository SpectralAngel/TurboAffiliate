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
        <h1>Deducciones de la cuenta <span py:content="account.name" /></h1>
        <table>
            <thead>
                <tr>
                    <th>N&uacute;mero</th>
                    <th>Nombre</th>
                    <th>Retrasada</th>
                    <th>Mes</th>
                    <th>Anio</th>
                    <th>Cantidad</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="extra in extras">
                    <td>${extra.affiliate.id}</td>
                    <td>${extra.affiliate.firstName} ${extra.affiliate.lastName}</td>
                    <td>${extra.retrasada}</td>
                    <td>${extra.mes}</td>
                    <td>${extra.anio}</td>
                    <td>${locale.currency(extra.amount, True, True)}</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <td>Total:</td>
                    <td>${locale.currency(sum(e.amount for e in extras), True, True)}</td>
                </tr>
            </tfoot>
        </table>
    </body>
</html>
