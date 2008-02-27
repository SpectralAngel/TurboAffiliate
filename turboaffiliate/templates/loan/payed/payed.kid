<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, """)
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Pr&eacute;stamos</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/status.css')}" media="print"/>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print"/>
	</head>
	<body>
		<div style="text-align: center;">
			<div style="font-weight: bold; font-size: 180%">COPEMH</div>
			<div style="font-weight: bold; font-size: 180%">Estado de Cuenta Pr&eacute;stamos Pagados</div>
			<div py:content="'Pr&eacute;stamo N&uacute;mero ', loan.id" />
		</div>
		<ul>
			<li>
				<strong>Prestatario:</strong>
				<a href="${tg.url('/affiliate/%s' % loan.affiliate.id)}">
					<span py:content="loan.affiliate.id" />
				</a>
				<span py:content="loan.affiliate.id" /> <span py:content="loan.affiliate.firstName, ' ', loan.affiliate.lastName" />
			</li>
			<li>
				<strong>Fecha de Otorgamiento:</strong>
				<span py:content="loan.startDate" />
			</li>
			<li>
				<strong>Monto Original:</strong>
				<span py:content="'L.', locale.format('%s', loan.capital, True)" />
			</li>
			<li>
				<a href="${tg.url('/payed/view/%s' % loan.id)}">
					Modificar Datos
				</a>
			</li>
		</ul>
		<table width="100%">
			<tr>
				<td colspan="2">Deducciones</td>
			</tr>
			<tr py:for="d in loan.deductions">
				<td>${d.name}</td>
				<td>L. ${locale.format('%s', d.amount, True)}</td>
			</tr>
			<tr>
				<td>Total deducciones</td>
				<td><strong>L. ${locale.format('%s', sum([d.amount for d in loan.deductions]), True)}</strong></td>
			</tr>
			<tr>
				<td>Remanente o Monto Liquidado</td>
				<td><strong>L. ${locale.format('%s', loan.capital - sum([d.amount for d in loan.deductions]), True)}</strong></td>
			</tr>
		</table>
		<h4 py:if="len(loan.pays) != 0">Pagos Efectuados</h4>
		<table class="pay" py:if="len(loan.pays) != 0">
			<thead>
				<tr>
					<th>Fecha</th>
					<th>N&uacute;mero</th>
					<th>Intereses</th>
					<th>Capital</th>
					<th>Valor</th>
					<th>Recibo</th>
				</tr>
			</thead>
			<tbody>
				<?python i = 1 ?>
				<tr py:for="pay in loan.pays">
					<td py:content="pay.day.day, '/', pay.day.month, '/', pay.day.year" />
					<td py:content="i, '/', loan.months" />					
					<?python i += 1 ?>
					<td py:content="'L. ', locale.format('%s', pay.interest, True)" />
					<td py:content="'L. ', locale.format('%s', pay.capital, True)" />
					<td py:content="'L. ', locale.format('%s', pay.amount, True)" />
					<td py:content="pay.receipt" />
				</tr>
			</tbody>
		</table>
	</body>
</html>
