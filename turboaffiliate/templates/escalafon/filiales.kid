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
		<h1>Filiales Departamentales</h1>
		<div py:for="department in filiales.keys()">
			<h2 py:content="department" />
			<table>
				<thead>
					<tr>
						<th>Instituto</th>
						<th>Afiliados</th>
					</tr>
				</thead>
				<tbody>
					<tr py:for="school in filiales[department].keys()">
						<td py:content="school" />
						<td py:content="filiales[department][school]" />
					</tr>
				</tbody>
			</table>
		</div>
	</body>
</html>

