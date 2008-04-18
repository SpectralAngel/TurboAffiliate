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
		<title>TurboAffiliate &bull; Pr&eacute;stamos</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/status.css')}" />
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" />
	</head>
	<body>
		<h1 py:content="'Pagos de Pr&eacute;stamos Efectuados entre', start.strftime('%d/%m/%Y'), 'y ', end.strftime('%d/%m/%Y') " />
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
					<td py:content="locale.currency(capital, True, True)" />
				</tr>
				<tr>
					<td>Intereses</td>
					<td py:content="locale.currency(interest, True, True)" />
				</tr>
				<tr>
					<td>Total</td>
					<td py:content="locale.currency(capital + interest, True, True)" />
				</tr>
			</tbody>
		</table>
	</body>
</html>
