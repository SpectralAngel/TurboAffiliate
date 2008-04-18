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
		<title>TurboAffiliate &bull; Afiliados</title>
	</head>
	<body>
		 <h2 py:content="affiliate.id, ' ', affiliate.firstName, ' ', affiliate.lastName" />
		 <p><strong>Monto Total: </strong><span py:content="locale.currency(obligation + affiliate.get_monthly(), True, True)" />
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
		<h4>Detalle de Pr&eacute;tamos</h4>
		<div py:for="loan in affiliate.loans">
			<h4 py:content="'Préstamo ', loan.id" />
			<span py:content="locale.currency(loan.get_payment(), True, True)" />
			<a href="${tg.url('/affiliate/postloan/%s' % loan.id)}">Postear</a>
			<form action="${tg.url('/affiliate/prestamo')}">
				<fieldset>
					<legend>Postear otro Pago</legend>
					<ul>
						<li>
							<label>Cuota:</label>
							<input name="amount" />
							<input name="year" value="${year}" type="hidden" />
							<input name="month" value="${month}" type="hidden" />
							<input name="loan" value="${loan.id}" type="hidden" />
						</li>
					</ul>
				</fieldset>
			</form>
		</div>
		<a href="${tg.url('/affiliate/listmanual?payment=%s&amp;month=%s&amp;year=%s' % (affiliate.payment, month, year))}">Regresar</a>
	</body>
</html>
