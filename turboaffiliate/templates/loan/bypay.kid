<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Afiliados</title>
	</head>
	<body>
		<h1>Capital e Intereses de Pr&eacute;stamos</h1>
		<table width="100%">
			<thead>
				<tr>
					<th>Pr&eacute;stamo</th>
					<th>COPEMH</th>
					<th>Afiliado</th>
					<th>Capital</th>
					<th>Intereses</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="pay in pays">
					<td>${pay.loan.id}</td>
					<td>${pay.loan.affiliate.id}</td>
					<td>${pay.loan.affiliate.firstName} ${pay.loan.affiliate.lastName}</td>
					<td>${locale.currency(pay.capital, True, True)}</td>
					<td>${locale.currency(pay.interest, True, True)}</td>
				</tr>
			</tbody>
			<tfoot>
				<tr>
					<th colspan="2">Total</td>
					<th>${locale.currency(capital + interest, True, True)}</th>
					<th>${locale.currency(capital, True, True)}</th>
					<th>${locale.currency(interest, True, True)}</th>
				</tr>
			</tfoot>
		</table>
	</body>
</html>
