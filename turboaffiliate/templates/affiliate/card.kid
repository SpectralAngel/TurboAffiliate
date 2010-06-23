<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Afiliados</title>
        <style type="text/css">
            table
            {
                width: 100%;
            }
            .total
            {
                font-weight: bold;
            }
            .amount
            {
                text-align: right;
            }
        </style>
    </head>
    <body>
        <h1> Reporte de Afiliados con C&oacute;digo de Identidad ${cardID}</h1>
        <table>
            <thead>
                <tr>
                    <th>Carnet</th>
                    <th>Nombre</th>
                    <th>Ingreso</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="affiliate in affiliates">
                    <td><a href="${tg.url('/affiliate/%s' % affiliate.id)}">${affiliate.id}</a></td>
                    <td>${affiliate.firstName} ${affiliate.lastName}</td>
                    <td>${affiliate.joined}</td>
                </tr>
            </tbody>
        </table>
        <strong>Total de Afiliados: </strong>${count}
    </body>
</html>
