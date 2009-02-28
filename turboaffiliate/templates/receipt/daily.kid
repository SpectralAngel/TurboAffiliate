<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Recibos</title>
	</head>
	<body>
		<h1 py:content="'Recibos del D&iacute;a ', day.strftime('%d de %B de %Y')" />
		<table>
			<thead>
				<tr>
					<th>Recibo</th>
					<th>Cantidad</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="receipt in receipts">
					<td py:content="receipt.id" />
					<td py:content="locale.currency(receipt.amount, True, True)" />
				</tr>
			</tbody>
			<tfoot>
				<tr>
					<th>Total</th>
					<th py:content="locale.currency(sum(r.amount for r in receipts), True, True)" />
				</tr>
			</tfoot>
		</table>
	</body>
</html>
