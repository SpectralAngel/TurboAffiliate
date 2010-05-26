<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
    locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Reintegros</title>
        <script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/reintegro.js')}" type="text/javascript"></script>
    </head>
    <body>
        <table>
            <caption>Reintegros por Periodo</caption>
            <thead>
                <tr>
                    <th>Emisi&oacute;n</th>
                    <th>Cheque</th>
                    <th>Planilla</th>
                    <th>Motivo</th>
                    <th>Monto</th>
                    <th>Afiliado</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="reintegro in reintegros">
                    <td>${reintegro.emision.strftime('%d/%m/%Y')}</td>
                    <td>${reintegro.cheque}</td>
                    <td>${reintegro.planilla}</td>
                    <td>${reintegro.motivo}</td>
                    <td>${locale.currency(reintegro.monto, True, True)}</td>
                    <td>
                        <a href="${tg.url('/affiliate/%s' % reintegro.affiliate.id)}">
                            ${reintegro.affiliate.id}</a>
                        ${reintegro.affiliate.firstName} ${reintegro.affiliate.lastName}
                    </td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <th></th>
                    <th colspan="3">Monto Total de Reintegros:</th>
                    <th>${locale.currency(sum(r.monto for r in reintegros))}</th>
                    <th></th>
                </tr>
            </tfoot>
        </table>
    </body>
</html>
