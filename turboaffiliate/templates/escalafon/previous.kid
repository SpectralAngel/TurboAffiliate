<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "en-US")
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
					<th>Cdigo</th>
					<th>Cuenta</th>
					<th>Afiliados</th>
					<th>Total</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td>0</td>
					<td>Cuota Aportaciones Ordinarias</td>
					<td py:content="count" />
					<td py:content="'L.', locale.format('%s', count * obligation, True)" />
				</tr>
				<tr>
					<td>3</td>
					<td>Cuota Ordinaria de Pr&eacute;tamo</td>
					<td py:content="loan.qty" />
					<td py:content="'L.', locale.format('%s', loan.amount, True)" />
				</tr>
				<tr py:for="key, value in resume.items()">
					<td py:content="key.code"/>
					<td py:content="key.name" />
					<td py:content="value['number']" />
					<td py:content="'L.', locale.format('%s', value['total'], True)" />
				</tr>
				<tr>
					<td colspan="3">Total</td>
					<td py:content="'L.', locale.format('%s', total, True)" />
				</tr>
			</tbody>
		</table>
	</body>
</html>
