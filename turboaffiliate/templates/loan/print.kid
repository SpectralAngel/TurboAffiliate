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
		<title>TurboAffiliate &bull; Pr&eacute;stamos</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print"/>
	</head>
	<body>
		<h2 py:content="'Pr&eacute;stamo N&uacute;mero ', loan.id" />
		<ul>
			<li>
				<strong>Prestatario:</strong>
				<span py:content="loan.affiliate.firstName, ' ', loan.affiliate.lastName" />
				<span py:content="loan.affiliate.cardID" />
			</li>
			<li>
				<strong>Cuotas:</strong>
				<span>${loan.number}/${loan.months}</span>
			</li>
			<li>
				<strong>&Uacute;ltimo Pago:</strong>
				<span>${loan.last}</span>
			</li>
			<li>
				<strong>Fecha de Inicio:</strong>
				<span py:content="loan.startDate" />
			</li>
			<li>
				<strong>Pago Mensual:</strong>
				<span py:content="locale.currency(loan.payment)" />
			</li>
			<li>
				<strong>Monto Original:</strong>
				<span py:content="locale.currency(loan.capital)" />
			</li>
			<li>
				<strong>Monto Debido</strong>
				<span py:content="locale.currency(loan.debt)" />
			</li>
		</ul>
		<ul>
			<li class="link">
				<a href="${tg.url('/loan/pay/add/%s' % loan.id)}">Agregar un Pago</a>
			</li>
			<li class="link">
				<a py:if="loan.refinance()" href="${'/loan/remove/%s' % loan.id}">Eliminar</a>
			</li>
			<li class="link">
				<a href="${tg.url('/loan/pagare/%s' % loan.id)}">Ver Pagar&eacute;</a>
			</li>
			<li class="link">
				<a href="${tg.url('/loan/receipt/%s' % loan.id)}">Ver Liquidaci&oacute;n</a>
			</li>
			<li class="link">
				<a href="${tg.url('/loan/deduction/add/%s' % loan.id)}">A&ntilde;adir Deducci&oacute;n</a>
			</li>
		</ul>
		<h3>Pagos Efectuados</h3>
		<table class="pay" py:if="len(loan.pays) != 0">
			<thead>
				<tr>
					<th>Fecha</th>
					<th>Intereses</th>
					<th>Capital</th>
					<th>Valor</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="pay in loan.pays">
					<th py:content="pay.day" />
					<th py:content="locale.currency(pay.interest)" />
					<th py:content="locale.currency(pay.capital)" />
					<th py:content="locale.currency(pay.amount)" />
				</tr>
			</tbody>
		</table>
	</body>
</html>
