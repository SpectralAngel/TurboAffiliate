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
		<title>TurboAffiliate &bull; Afiliados</title>
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
                <tr py:for="reintegro in afiliado.reintegros" pyif="not reintegro.pagado">
                    <td>${reintegro.emision.strftime('%d/%m/%Y')}</td>
                    <td>${reintegro.cheque}</td>
                    <td>${reintegro.planilla}</td>
                    <td>${locale.currency(reintegro.monto)}</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <th colspan="3">Saldo en Reintegros:</th>
                    <!-- <th>${locale.currency(sum(r.monto in afiliado.reintegros if not r.pagado))}</th> -->
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
                    <td>${locale.currency(reintegro.monto)}</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <th colspan="5">Total Cobrado:</th>
                    <!-- <th>${locale.currency(sum(r.monto in afiliado.reintegros if r.pagado))}</th> -->
                </tr>
            </tfoot>
        </table>
	</body>
</html>
