<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "en-US")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Volantes y Deducciones</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/status.css')}" media="print"/>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print"/>
	</head>
	<body>
		<h1>Deducciones de <span py:content="account.name" /> para el mes
		<span py:content="month" /> <span py:content="year" /> <span py:content="payment" /></h1>
		<table>
			<thead>
				<tr>
					<th>N&uacute;mero</th>
					<th>Nombre</th>
					<th>Cantidad</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="d in deduced">
					<td py:content="d.affiliate.id" />
					<td py:content="d.affiliate.firstName, ' ', d.affiliate.lastName" />
					<td py:content="locale.currency(d.amount)" />
				</tr>
			</tbody>
			<tfoot>
				<tr>
					<th colspan="2">Total:</th>
					<th py:content="locale.currency(total)" />
				</tr>
			</tfoot>
		</table>
	</body>
</html>
