<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "en-US")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Reporte de Ingresos</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/status.css')}" media="print"/>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print"/>
	</head>
	<body>
		<h1>Reporte de Ingresos <span py:content="payment" /> de <span py:content="month" /> <span py:content="year" /></h1>
		<table class="pay">
			<thead>
				<tr>
					<th>C&oacute;digo</th>
					<th>Cuenta</th>
					<th>Afiliados</th>
					<th>Total</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="account in report.otherAccounts">
					<td py:content="account.account.code"/>
					<td py:content="account.account.name" />
					<td py:content="account.quantity" />
					<td py:content="'L.', locale.format('%s', account.amount, True)" />
				</tr>
			</tbody>
		</table>
		<h2>Total de Ingresos: <span py:replace="'L.', locale.format('%s', report.total(), True)" /></h2>
	</body>
</html>
