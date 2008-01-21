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
					<td py:content="'L.', locale.format('%s', count * obligation, True)" />
				</tr>
				<tr>
					<td>2</td>
					<td>Cuota Pr&eacute;stamo</td>
					<td py:content="loans['count']" />
					<td py:content="'L.', locale.format('%s', loans['amount'], True)" />
				</tr>
				<tr py:for="key, value in deductions.iteritems()">
					<td py:content="key.code"/>
					<td py:content="key.name" />
					<td py:content="locale.format('%s', value['count'], True)" />
					<td py:content="'L.', locale.format('%s', value['amount'], True)" />
				</tr>
			</tbody>
		</table>
		<h2>Total de Ingresos: <span py:replace="'L.', locale.format('%s', total + loans['amount'] + count * obligation, True)" /></h2>
	</body>
</html>
