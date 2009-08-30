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
	</head>
	<body>
		<h1>Afiliados de <span py:replace="payment" /> con Cuotas Retrasadas</h1>
		<table width="100%">
			<thead>
				<tr>
					<th>Afiliado</th>
					<th>Nombre</th>
					<th>Mes</th>
					<th>A&ntilde;o</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="affiliate in affiliates">
					<td><a href="${tg.url('/affiliate/%s' % affiliate.id)}" py:content="affiliate.id"</td>
					<td py:content="affiliate.lastName, ' ', affiliate.firstName" />
					<td py:content="affiliate.delayed().delayed()" />
					<td py:content="affiliate.delayed().year" />
				</tr>
			</tbody>
		</table>
		<strong>Total de Afiliados: </strong><span py:content="count"/>
	</body>
</html>

