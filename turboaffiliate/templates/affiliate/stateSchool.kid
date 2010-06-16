<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
    locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Filiales</title>
        <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/form.css')}" media="screen" />
         <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print" />
         <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/billing.css')}" />
    </head>
    <body>
        <h1>Afiliados de ${state}</h1>
        <table class="page" py:for="school in schools" style="width: 100%">
            <caption>${school}</caption>
            <thead>
                <tr>
                    <th>Afiliaci&oacute;n</th>
                    <th>Apellidos</th>
                    <th>Nombre</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="affiliate in schools[school]">
                    <td>${affiliate.id}</td>
                    <td>${affiliate.lastName}</td>
                    <td>${affiliate.firstName}</td>
                </tr>
            </tbody>
            <tfoot>
                <th colspan="2">Total de Afiliados</th>
                <th>${len(schools[school])}</th>
            </tfoot>
        </table>
    </body>
</html>
