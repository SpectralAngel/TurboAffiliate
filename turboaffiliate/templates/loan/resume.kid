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
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/status.css')}" />
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" />
	</head>
	<body>
		<h1 py:content="'Pagos de Pr&eacute;stamos Efectuados entre %s/%s/%s y %s/%s/%s' % (start.day, start.month, start.year, end.day, end.month, end.year)" />
		<table>
			<thead>
				<tr>
					<th>Concepto</th>
					<th>Cantidad</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td>Capital</td>
					<td py:content="'L. ', locale.format('%s', capital, True)" />
				</tr>
				<tr>
					<td>Intereses</td>
					<td py:content="'L. ', locale.format('%s', interest, True)" />
				</tr>
				<tr>
					<td>Total</td>
					<td py:content="'L. ', locale.format('%s', capital + interest, True)" />
				</tr>
			</tbody>
		</table>
	</body>
</html>
