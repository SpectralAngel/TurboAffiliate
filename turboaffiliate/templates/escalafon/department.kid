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
		<h1>Filiales <span py:content="state" /></h1>
			<table>
				<thead>
					<tr>
						<th>Instituto</th>
						<th>Afiliados</th>
					</tr>
				</thead>
				<tbody>
					<tr py:for="school in filiales.keys()">
						<td py:content="school" />
						<td py:content="filiales[school]" />
					</tr>
					<tr>
						<td colspan="3">Total</td>
						<td py:content="sum(filiales[school] for school in filiales.keys())" />
					</tr>
				</tbody>
			</table>
	</body>
</html>

