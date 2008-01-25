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
		<title>Recibos &bull; Corte de Caja</title>
	</head>
	<body> 
		<h1>Reporte de Cuotas Retrasadas</h1>
		<h2 py:content="'Mes %s A&ntilde;o %s' % (month, year)" />
		<table>
			<thead>
				<th>Cuota</th>
				<th>N&uacute;mero</th>
				<th>Cantidad</th>
			</thead>
			<tbody>
				<tr py:for="key in retrasada.keys()">
					<td py:content="'Cuota Retrasada L. %s' % key" />
					<td py:content="retrasada[key]" />
					<td py:content="locale.currency(key * retrasada[key])" />
				</tr>
			</tbody>
			<tfoot>
				<th colspan="2">Total</th>
				<th py:content="locale.currency(total)" />
			</tfoot>
		</table>
	</body>
</html>
