<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
    locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Afiliados</title>
    </head>
    <body>
        <h3>COPEMH</h3>
        <p>Hoja de deducciones a Afiliados de Educaci&oacute;n Media Solicitamos deducir:</p>
        <h1><center>Planilla ${how}</center></h1>
        <p>Al: </p>
        <table width="100%">
            <thead>
                <tr>
                    <th>Carnet</th>
                    <th>N&ordm; Empleado</th>
                    <th>Nombre</th>
                    <th>Deducci&oacute;n</th>
                    <th class="noprint">Postear</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="affiliate in affiliates">
                <!-- filtro para inprema <tr py:for="affiliate in affiliates" py:if="affiliate.total(month, year) != 250"> -->
                    <td><a href="${tg.url('/affiliate/edit/%s' % affiliate.id)}">${affiliate.id}</a></td>
                    <td>${affiliate.escalafon}</td>
                    <td>${affiliate.lastName} ${affiliate.firstName}</td>
                    <td>${locale.currency(affiliate.total(month, year), True, True)}</td>
                    <td class="noprint"><a href="${tg.url('/affiliate/posteo/?how=%s&amp;year=%s&amp;month=%s&amp;code=%s' % (self.payment, year, month, affiliate.id))}">X</a></td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <th colspan="5">Total de Afiliados: ${count}</th>
                </tr>
            </tfoot>
        </table>
    </body>
</html>
