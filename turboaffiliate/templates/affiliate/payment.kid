<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Afiliados</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print"/>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/style.css')}" media="screen"/>
		<style type="text/css">
			h1
			{
				text-align: center;
			}
		</style>
	</head>
	<body>
		<h3>COPEMH</h3>
		<h1>Afiliados que Cotizan por ${how}</h1>
		<table width="100%">
			<thead>
				<tr>
					<th>Carnet</th>
					<th>Apellido</th>
					<th>Nombre</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="affiliate in affiliates">
					<td>${affiliate.id}</td>
					<td py:content="affiliate.lastName" />
					<td py:content="affiliate.firstName" />
				</tr>
			</tbody>
		</table>
		<strong>Total de Afiliados: </strong><span py:content="count"/>
	</body>
</html>
