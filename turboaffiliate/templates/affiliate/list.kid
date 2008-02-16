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
		<h3>COPEMH</h3>
		<p>Hoja de deducciones a Afiliados de Educaci&oacute;n Media Solicitamos deducir:</p>
		<h1><center>Planilla ${how}</center></h1>
		<p>Al: </p>
		<table width="100%">
			<thead>
				<tr>
					<th>Carnet</th>
					<th>N&ordm; Empleado</th>
					<th>Nombre</th>
					<th>Deducci&oacute;n</th>
					<th class="noprint">Postear</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="affiliate in affiliates">
				<!-- filtro para inprema <tr py:for="affiliate in affiliates" py:if="affiliate.total(month, year) != 250"> -->
					<td><a href="${tg.url('/affiliate/edit/%s' % affiliate.id)}">${affiliate.id}</a></td>
					<td py:content="affiliate.escalafon" />
					<td py:content="affiliate.lastName, ' ', affiliate.firstName" />
					<td py:content="locale.currency(affiliate.total(month, year), True, True)" />
					<td class="noprint"><a href="${affiliate.link(year, month)}">X</a></td>
				</tr>
			</tbody>
		</table>
		<strong>Total de Afiliados: </strong><span py:content="count"/>
	</body>
</html>
