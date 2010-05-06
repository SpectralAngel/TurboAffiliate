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
		<h1>Pr&eacute;stamos por Liquidaci&oacute;n</h1>
		<table width="100%">
			<thead>
				<tr>
					<th>Pr&eacute;stamo</th>
					<th>COPEMH</th>
					<th>Afiliado</th>
					<th>Capital</th>
					<th>Liquidado</th>
					<th>Fecha de Inicio</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="loan in loans">
					<td py:content="loan.id" />
					<td py:content="loan.affiliate.id" />
					<td py:content="loan.affiliate.firstName, ' ', loan.affiliate.lastName" />
					<td py:content="locale.currency(loan.capital, True, True)" />
					<td py:content="locale.currency(loan.net(), True, True)" />
					<td py:content="loan.startDate" />
				</tr>
			</tbody>
			<tfoot>
				<tr>
					<td>Cantidad</td>
					<td py:content="count" />
					<td></td>
					<td py:content="locale.currency(capital, True, True)" />
					<td py:content="locale.currency(debt, True, True)" />
					<td></td>
				</tr>
			</tfoot>
		</table>
	</body>
</html>
