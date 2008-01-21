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
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/status.css')}" />
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" />
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
					<td py:content="pay.loan.id" />
					<td py:content="pay.loan.affiliate.id" />
					<td py:content="pay.loan.affiliate.firstName, ' ', pay.loan.affiliate.lastName" />
					<td py:content="locale.format('%s', pay.capital, True)" />
					<td py:content="locale.format('%s', pay.interest, True)" />
				</tr>
			</tbody>
			<tfoot>
				<tr>
					<td colspan="2">Total</td>
					<td py:content="locale.format('%s', capital + interest, True)" />
					<td py:content="locale.format('%s', capital, True)" />
					<td py:content="locale.format('%s', interest, True)" />
				</tr>
			</tfoot>
		</table>
	</body>
</html>
