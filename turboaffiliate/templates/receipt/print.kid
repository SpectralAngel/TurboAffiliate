<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "en-US")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Afiliados</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print"/>
		<style type="text/css">
		body
		{
			font-size: 75%;
			margin-left: 5px;
		}
		</style>
	</head>
	<body background="/static/images/recibo.png">
		<div style="height: 70px; padding-left: 80px;">&nbsp;</div>
		<!--<span py:content="receipt.id" /> -->
		<span style="padding-left: 80px;" py:content="receipt.affiliate" />
		<div style="height: 20px;">&nbsp;</div>
		<span style="padding-left: 80px;" py:content="receipt.name" />
		<div style="height: 40px;">&nbsp;</div>
		<table width="100%">
			<tbody>
				<tr py:for="line in receipt.lines">
					<td class="first" width="50" style="text-align: right;" py:content="line.qty" />
					<td class="second" width="450" style="text-align: center;" py:content="line.account.name" />
					<td class="third" width="450" py:content="line.detail" />
					<td class="first" width="50" style="text-align: right;" py:content="'L.', locale.format('%s', line.unit, True)" />
					<td class="last" style="text-align: right;" py:content="'L.', locale.format('%s',line.value(), True)" />
				</tr>
			</tbody>
		</table>
		<div style="position: absolute; top: 420px; right: 10px;" py:content="'L. ', locale.format('%s', sum([l.value() for l in receipt.lines]), True)" />
		<div style="position: absolute; top: 440px; left: 100px;" py:content="receipt.day.day, '/', receipt.day.month, '/', receipt.day.year" />
	</body>
</html>
