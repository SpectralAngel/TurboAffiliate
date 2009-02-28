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
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/status.css')}" />
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" />
	</head>
	<body>
		
		<table width="100%">
			<thead>
				<tr>
					<th>Pr&eacute;stamo</th>
					<th>COPEMH</th>
					<th>Afiliado</th>
					<th>Cuota Pr&eacute;stamo Anterior</th>
					<th>Cuota Pr&eacute;stamo Nuevo</th>
					<th>Otorgado Anterior</th>
					<th>Otorgado Nuevo</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="p in payed">
					<td><a class="print" href="${tg.url('/payed/%s' % p.id)}" py:content="p.id"  /></td>
					<td><a class="print" href="${tg.url('/affiliate/%s' % p.affiliate.id)}" py:content="p.affiliate.id" /></td>
					<td py:content="p.affiliate.firstName, ' ', p.affiliate.lastName" />
					<td py:content="locale.currency(p.payment, True, True)" />
					<td py:content="locale.currency(p.affiliate.loans[0].get_payment(), True, True)" />
					<td py:content="p.startDate" />
					<td py:content="p.affiliate.loans[0].startDate" />
				</tr>
			</tbody>
		</table>
	</body>
</html>
