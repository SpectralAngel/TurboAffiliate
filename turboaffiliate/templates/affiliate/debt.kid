<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
    locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Afiliados &bull; ${show}</title>
        <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print"/>
        <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/style.css')}" media="screen"/>
        <style type="text/css">
            h1
            {
                text-align: center;
            }
        </style>
    </head>
    <body>
        <h3>COPEMH</h3>
        <h1>Afiliados por ${show}</h1>
        <table width="100%">
            <thead>
                <tr>
                    <th>Carnet</th>
                    <th>Apellido</th>
                    <th>Nombre</th>
                    <th>Deuda Aportaciones</th>
                    <th>Deuda Pr&eacute;stamos</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="affiliate in affiliates">
                    <td><a href="${tg.url('/affiliate/%s' % affiliate.id)}">${affiliate.id}</a></td>
                    <td>${affiliate.lastName}</td>
                    <td>${affiliate.firstName}</td>
                    <td>${locale.currency(affiliate.debt(), True, True)}</td>
                    <td>${locale.currency(affiliate.loan(), True, True)}</td>
                </tr>
            </tbody>
        </table>
        <strong>Total de Afiliados: </strong>${count}
    </body>
</html>
