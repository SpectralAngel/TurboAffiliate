<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "en-US")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Recibos</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/status.css')}" media="print" />
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print" />
	</head>
	<body>
		<h1 py:content="'Recibos del D&iacute;a %s/%s/%s' % (day.day, day.month, day.year)" />
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
					<td py:content="'L. ', locale.format('%s', receipt.amount, True)" />
				</tr>
			</tbody>
			<tfoot>
				<tr>
					<th>Total</th>
					<th py:content="'L. ', locale.format('%s', sum(r.amount for r in receipts), True)" />
				</tr>
			</tfoot>
		</table>
	</body>
</html>
