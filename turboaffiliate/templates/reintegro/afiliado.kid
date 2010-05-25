<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
    locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Reintegros &bull; ${afiliado.id}</title>
        <script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
        <script type="text/javascript">
        <![CDATA[
        $(document).ready(function(e)
        {
            $('input.datepicker').datepicker({
                dateFormat: 'dd/mm/yy',
                changeMonth: true,
                changeYear: true,
            });
        });
        ]]>
        </script>
    </head>
    <body>
        <h1>Estado de Cuenta de Reintegros</h1>
        <h2>${afiliado.id} - ${afiliado.firstName} ${afiliado.lastName}</h2>
        <table>
            <caption>Reintegros por Efectuar</caption>
            <thead>
                <tr>
                    <th>Emisi&oacute;n</th>
                    <th>Cheque</th>
                    <th>Planilla</th>
                    <th>Monto</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="reintegro in afiliado.reintegros" py:if="not reintegro.pagado">
                    <td>${reintegro.emision.strftime('%d/%m/%Y')}</td>
                    <td>${reintegro.cheque}</td>
                    <td>${reintegro.planilla}</td>
                    <td>${locale.currency(reintegro.monto, True, True)}</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <th colspan="3">Saldo en Reintegros:</th>
                    <th>${locale.currency(sum(r.monto for r in afiliado.reintegros if not r.pagado))}</th>
                </tr>
            </tfoot>
        </table>
        <table>
            <caption>Reintegros Cancelados</caption>
            <thead>
                <tr>
                    <th>Emisi&oacute;n</th>
                    <th>Cheque</th>
                    <th>Planilla</th>
                    <th>Forma de Pago</th>
                    <th>Fecha de Pago</th>
                    <th>Monto</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="reintegro in afiliado.reintegros" py:if="reintegro.pagado">
                    <td>${reintegro.emision.strftime('%d/%m/%Y')}</td>
                    <td>${reintegro.cheque}</td>
                    <td>${reintegro.planilla}</td>
                    <td>${reintegro.formaPago.nombre}</td>
                    <td>${reintegro.cancelacion.strftime('%d/%m/%Y')}</td>
                    <td>${locale.currency(reintegro.monto, True, True)}</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <th colspan="5">Total Cobrado:</th>
                    <th>${locale.currency(sum(r.monto for r in afiliado.reintegros if r.pagado))}</th>
                </tr>
            </tfoot>
        </table>
        <form class="AgregarReintegro" action="${tg.url('/reintegro/agregar')}">
            <fieldset>
                <input type="hidden" value="${afiliado.id}" name="affiliate" />
                <input type="hidden" value="${cuenta.id}" name="cuenta" />
                <ol>
                    <li>
                        <label>Fecha de Emisi&oacute;n</label>
                        <input class="datepicker" name="emision" />
                    </li>
                    <li>
                        <label>Motivo:</label>
                        <input name="motivo" />
                    </li>
                    <li>
                        <label>Cheque</label>
                        <input name="cheque" />
                    </li>
                    <li>
                        <label>Planilla</label>
                        <input name="planilla" />
                    </li>
                    <li>
                        <label>Monto:</label>
                        <input name="monto" />
                    </li>
                </ol>
            </fieldset>
        </form>
        <form action="${tg.url('/reintegro/pagar')}">
            <input type="hidden" name="reintegro" />
            <fieldset>
                <ol>
                    <li>
                        <label>Forma de Pago:</label>
                        <select name="forma">
                            <option py:for="forma in formas" value="${forma.id}">${forma.nombre}</option>
                        </select>
                    </li>
                    <li>
                        <label>Fecha de Pago</label>
                        <input class="datepicker" name="fecha" />
                    </li>
                </ol>
            </fieldset>
        </form>
    </body>
</html>
