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
		<h1>Reporte de Ingresos ${legend}</h1>
		<table>
			<thead>
				<tr>
					<th>C&oacute;digo</th>
					<th>Cuenta</th>
					<th>Afiliados</th>
					<th>Total</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td>1</td>
					<td>Aportaciones Ordinarias</td>
					<td py:content="count" />
					<td py:content="locale.currency(count * obligation, True, True)" />
				</tr>
				<tr>
					<td>2</td>
					<td>Cuota Pr&eacute;stamo</td>
					<td py:content="loans['count']" />
					<td py:content="locale.currency(loans['amount'], True, True)" />
				</tr>
				<tr py:for="deduccion in deductions">
					<td py:content="deduccion.code"/>
					<td py:content="deduccion.name" />
					<td py:content="deductions[deduccion]['count']" />
					<td py:content="locale.currency(deductions[deduccion]['amount'], True, True)" />
				</tr>
			</tbody>
		</table>
		<h2>Total de Ingresos: <span py:replace="locale.currency(total + loans['amount'] + count * obligation, True, True)" /></h2>
	</body>
</html>
