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
		<title>TurboAffiliate &bull; Pr&eacute;stamos</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print"/>
	</head>
	<body>
		<h1 py:content="'Prestamos Otorgados el dia %s/%s/%s' % (day.day, day.month, day.year)" />
		<div py:for="loan in loans">
		<h3 py:content="'Pr&eacute;stamo N&uacute;mero ', loan.id" />
			<ul>
				<li>
					<strong>Prestatario:</strong>
					<span py:content="loan.affiliate.firstName, ' ', loan.affiliate.lastName" />
					<span py:content="loan.affiliate.cardID" />
				</li>
				<li>
					<strong>Monto Original:</strong>
					<span py:content="'L.', locale.format('%s',loan.capital, True)" />
				</li>
			</ul>
		</div>
		<strong>Monto Total:</strong>
		<span py:content="'L.', locale.format('%s',amount, True)" />
	</body>
</html>
