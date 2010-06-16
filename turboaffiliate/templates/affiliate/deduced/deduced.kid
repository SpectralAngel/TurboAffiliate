<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
    locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../../master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Afiliados</title>
    </head>
    <body>
        <table>
            <thead>
                <tr>
                    <th>Deducci&oacute;n</th>
                    <th>Cantidad</th>
                    <th>Detalle</th>
                    <th>Mes</th>
                    <th>A&ntilde;o</th>
                    <th py:if="tg.identity.user.has_permission('Deductor')">Eliminar</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="d in affiliate.deduced">
                    <td py:content="d.account.name" />
                    <td py:content="locale.currency(d.amount, True, True)" />
                    <td py:content="d.detail" />
                    <td py:content="d.month" />
                    <td py:content="d.year" />
                    <th py:if="tg.identity.user.has_permission('Deductor')">
                        <a href="${tg.url('/affiliate/deduced/delete/%s' % d.id)}" >X</a>
                    </th>
                </tr>
            </tbody>
        </table>
        <a py:if="tg.identity.user.has_permission('Deductor')" href="${tg.url('/affiliate/deduced/add/%s' % affiliate.id)}">Agregar Deducci&oacute;n</a>
    </body>
</html>

