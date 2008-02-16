<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "S")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Afiliados</title>
	</head>
	<body>

		<h2 py:content="affiliate.id" />
		<h2 py:content="affiliate.firstName, ' ', affiliate.lastName" />
		<p><strong>Monto Total: </strong><span py:content="locale.format('%s', obligation + affiliate.get_monthly(), True)" />
		<a href="${tg.url('/affiliate/complete?affiliate=%s&amp;year=%s&amp;month=%s' % (affiliate.id, year, month))}">Posteo Completo</a></p>
		<a href="${tg.url('/affiliate/postobligation?affiliate=%s&amp;year=%s&amp;month=%s' % (affiliate.id, year, month))}">Postear solo Aportaciones</a>
		<h3>Detalle Deducciones Extra</h3>
		<table>
			<thead>
				<tr>
					<th>Cuenta</th>
					<th>Monto</th>
					<th>Postear</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="extra in affiliate.extras">
					<td py:content="extra.account.name" />
					<td py:content="locale.currency(extra.amount, True, True)" />
					<td><a href="${tg.url('/affiliate/postextra/%s' % extra.id)}">X</a></td>
				</tr>
			</tbody>
		</table>
		<h3>Detalle Pr&eacute;stamo</h3>
		<table>
			<thead>
				<tr>
					<th>Pr&eacute;stamo</th>
					<th>Cuota</th>
					<th>Postear</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="loan in affiliate.loans">
					<td py:content="loan.id" />
					<td py:content="locale.currency(loan.get_payment(), True, True)" />
					<td><a href="${tg.url('/affiliate/postloan/%s' % loan.id)}">X</a></td>
				</tr>
			</tbody>
		</table>
	</body>
</html>
