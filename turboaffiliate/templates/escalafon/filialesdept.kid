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
		<h1>Filiales Departamentales <span py:content="state" /></h1>
		<table>
			<tr>
				<th>Departamento</th>
				<th>Afiliados</th>
			</tr>
			<tr py:for="instituto in filiales.keys()">
				<td py:content="instituto" />
				<td py:content="filiales[instituto]" />
			</tr>
			<tr>
				<th>Total</th>
				<th py:content="sum(filiales.values())" />
			</tr>
		</table>
	</body>
</html>
