<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Reporte de Ingresos</title>
	</head>
	<body>
		<h1>Reporte de Ingresos ${payment} de ${month} de ${year}</h1>
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
					<td py:content="locale.currency(account.amount, True, True)" />
				</tr>
			</tbody>
		</table>
		<h2>Total de Ingresos: <span py:replace="locale.currency(report.total(), True, True)" /></h2>
	</body>
</html>
