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
		<h1>Deducciones de la cuenta <span py:content="account.name" /></h1>
		<table>
			<thead>
				<tr>
					<th>N&uacute;mero</th>
					<th>Nombre</th>
                    <th>Retrasada</th>
                    <th>Mes</th>
                    <th>Anio</th>
					<th>Cantidad</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="extra in extras">
					<td py:content="extra.affiliate.id" />
					<td py:content="extra.affiliate.firstName, ' ', extra.affiliate.lastName" />
                    <td>${extra.retrasada}</td>
                    <td>${extra.mes}</td>
                    <td>${extra.anio}</td>
					<td py:content="locale.currency(extra.amount, True, True)" />
				</tr>
			</tbody>
			<tfoot>
				<tr>
					<td>Total:</td>
					<td py:content="locale.currency(sum(e.amount for e in extras), True, True)" />
				</tr>
			</tfoot>
		</table>
	</body>
</html>
