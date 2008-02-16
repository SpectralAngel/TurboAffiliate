<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Pr&eacute;stamos</title>
	</head>
	<body>
		<h1 py:content="'Cartera Pr&eacute;stamos'" />
		<table>
			<thead>
				<tr>
					<th>Prestamo</th>
					<th>Afiliado</th>
					<th>Afiliaci&oacute;n</th>
					<th>Capital</th>
					<th>Saldo</th>
					<th>Fecha Otorgado</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="loan in loans">
					<td><a href="${tg.url('/loan/%s' % loan.id)}" py:content="loan.id" /></td>
					<td py:content="loan.affiliate.firstName, ' ', loan.affiliate.lastName" />
					<td py:content="loan.affiliate.id" />
					<td py:content="locale.currency(loan.capital, True, True)" />
					<td py:content="locale.currency(loan.debt, True, True)" />
					<td py:content="loan.startDate.strftime('%d/%m/%Y')" />
				</tr>
			</tbody>
		</table>
		<strong>Monto Total:</strong>
		<span py:content="locale.currency(amount, True, True)" />
		<br />
		<strong>Prestamos Otorgados:</strong>
		<span py:content="count" />
	</body>
</html>
