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
		<title>Caja &bull; Corte</title>
		<style type="text/css">
			table { width: 100%; }
			.total { font-weight: bold; }
			.amount { text-align: right; }
		</style>
	</head>
	<body>
		<h1>Corte de Caja <span py:content="title" /></h1>
		<h2 py:content="house.name" />
		<h3 py:content="'D�a ', day.strftime('%A %d de %B de %Y')" />
		<table>
			<thead>
				<tr>
					<th>Cuenta</th>
					<th>Cantidad</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="account, amount in accounts.items()">
					<td py:content="account.name" />
					<td class="amount" py:content="locale.currency(amount)" />
				</tr>
                <tr class="total">
                    <td>Total:</td>
                    <td class="amount" py:content="locale.currency(total)" />
                </tr>
			</tbody>
		</table>
		<h2>Reporte de Cuotas</h2>
		<div py:for="key in cuotas.keys()">
			<h3 py:content="key.name" />
			<p><strong>Cuotas: </strong><span py:content="cuotas[key]" /></p>
			<table>
				<thead>
					<th>Cuota</th>
					<th>Cantidad</th>
				</thead>
				<tbody>
					<tr py:if="detail.company == company" py:for="detail in key.details">
						<td py:content="detail.name" />
						<td py:content="locale.currency(detail.amount * cuotas[key])" />
					</tr>
				</tbody>
				<tfoot>
					<tr>
						<th>Total:</th>
						<th py:content="locale.currency(cuotaTotal[key])" />
					</tr>
				</tfoot>
			</table>
		</div>
	</body>
</html>
