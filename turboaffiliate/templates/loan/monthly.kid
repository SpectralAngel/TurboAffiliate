<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "en-US")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Pr&eacute;stamos</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/status.css')}" media="print"/>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print"/>
	</head>
	<body>
		<h1>Pr&eacute;stamos Activos Otorgados</h1>
		<table>
			<thead>
				<tr>
					<th>Mes</th>
					<th>Cantidad</th>
					<th>Monto</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="month in months">
					<td py:content="month['month']" />
					<td py:content="month['number']" />
					<td py:content="'L. ', locale.format('%s', month['amount'], True)" />
				</tr>
			</tbody>
			<tfoot>
				<tr>
					<th colspan="2">Total:</th>
					<th py:content="'L. ', locale.format('%s', total, True)" />
				</tr>
			</tfoot>
		</table>
	</body>
</html>
