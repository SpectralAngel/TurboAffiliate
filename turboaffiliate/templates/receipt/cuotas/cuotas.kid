<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, """)
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>Recibos &bull; Corte de Caja</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/status.css')}" media="print"/>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print"/>
	</head>
	<body> 
		<h1>Reporte de Cuotas del <span py:content="day" /></h1>
		<div py:for="key in cuotas.keys()">
			<h2 py:content="key.name" />
			<p><strong>Cuotas: </strong><span py:content="cuotas[key]" /></p>
			<table>
				<thead>
					<th>Cuota</th>
					<th>Cantidad</th>
				</thead>
				<tbody>
					<tr py:for="detail in key.details">
						<td py:content="detail.name" />
						<td py:content="'L.', locale.format('%s', detail.amount * cuotas[key], True)" />
					</tr>
				</tbody>
			</table>
		</div>
	</body>
</html>
