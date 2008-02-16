<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Filiales</title>
	</head>
	<body>
		<h1>Aportaciones a Filiales</h1>
		<table>
			<thead>
				<tr>
					<th>Instituto</th>
					<th>Afiliados</th>
					<th>Cantidad</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="name in filiales.keys()">
					<td py:content="name" />
					<td py:content="filiales[name]" />
					<td py:content="locale.currency(filiales[name] * obligation.filiales, True, True)" />
				</tr>
				<tr>
					<td colspan="3">Total</td>
					<td py:content="locale.currency(total, True, True)" />
				</tr>
			</tbody>
		</table>
	</body>
</html>
