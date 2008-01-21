<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "en-US")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Afiliados</title>
		<style type="text/css">
			table
			{
				width: 100%;
			}
			.total
			{
				font-weight: bold;
			}
			.amount
			{
				text-align: right;
			}
		</style>
	</head>
	<body>
		<h1> Reporte de Afiliados con C&oacute;digo de Identidad ${code}</h1>
		<table>
			<thead>
				<tr>
					<th>Carnet</th>
					<th>Nombre</th>
					<th>Ingreso</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="affiliate in affiliates">
					<td><a href="${tg.url('/affiliate/%s' % affiliate.id)}" py:content="affiliate.id" /></td>
					<td py:content="affiliate.firstName, ' ', affiliate.lastName" />
					<td py:content="affiliate.joined" />
				</tr>
			</tbody>
		</table>
		<strong>Total de Afiliados: </strong><span py:content="count"/>
	</body>
</html>
