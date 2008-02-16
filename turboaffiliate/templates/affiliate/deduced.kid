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
		<title>TurboAffiliate &bull; Afiliados</title>
	</head>
	<body>
		<table>
			<thead>
				<tr>
					<th>Deducci&oacute;n</th>
					<th>Cantidad</th>
					<th>Mes</th>
					<th>A&ntilde;o</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="d in deduced">
					<td py:content="d.account.name" />
					<td py:content="locale.currency(d.amount, True, True)" />
					<td py:content="d.month" />
					<td py:content="d.year" />
				</tr>
			</tbody>
		</table>
	</body>
</html>
