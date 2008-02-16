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
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/status.css')}" media="print"/>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print"/>
	</head>
	<body>
		<div style="text-align: center;">
			<div style="font-weight: bold; font-size: 180%">COPEMH</div>
			<div style="font-weight: bold; font-size: 180%">Estado de Cuenta Pr&eacute;stamos Refinanciados</div>
			<div py:content="'Pr&eacute;stamo N&uacute;mero ', loan.id" />
			<span>Al: <span py:content="day.strftime('%d de %B de %Y')" /></span>
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
				<span py:content="locale.currency(loan.capital)" />
			</li>
		</ul>
		<ul class="noprint">
			<li class="link">
				<a href="${tg.url('pay/add/%s' % loan.id)}">Agregar un Pago</a>
			</li>
			<li class="link">
				<a href="${tg.url('/loan/pay/addfree/%s' % loan.id)}">Agregar un Pago sin Intereses</a>
			</li>
			<li class="link">
				<a href="${'remove/%s' % loan.id}">Eliminar</a>
			</li>
			<li class="link">
				<a href="${tg.url('view/%s' % loan.id)}">Modificar Datos del Pr&eacute;stamo</a>
			</li>
		</ul>
		<table width="100%">
			<tr>
				<td colspan="2">Deducciones</td>
			</tr>
			<tr py:for="d in loan.deductions">
				<td py:content="d.name" />
				<td py:content="locale.currency(d.amount)" />
			</tr>
			<tr>
				<td>Total deducciones</td>
				<td><strong py:content="locale.currency(sum(d.amount for d in loan.deductions)" /></td>
			</tr>
			<tr>
				<td>Remanente o Monto Liquidado</td>
				<td><strong py:content="locale.currency(loan.net())" /></td>
			</tr>
		</table>
		<h4 py:if="len(loan.future()) != 0">Pagos a Efectuar</h4>
		<table class="pay small" py:if="len(loan.future()) != 0">
			<thead>
				<tr>
					<th colspan="5">Abono</th>
					<th>&nbsp;</th>
				</tr>
				<tr>
					<th>Mes</th>
					<th>Pago N&ordm;</th>
					<th>Intereses</th>
					<th>Cuota</th>
					<th>Capital</th>
					<th>Saldo</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td colspan="5">&nbsp;</td>
					<td><strong py:content="locale.currency(loan.debt)" /></td>
				</tr>
				<tr py:for="pay in loan.future()">
					<td py:content="pay['month']" />
					<td py:content="pay['number']" />
					<td py:content="locale.currency(pay['interest'])" />
					<td py:content="locale.currency(pay['payment'])" />
					<td py:content="locale.currency(pay['capital'])" />
					<td py:content="locale.currency(pay['amount'])" />
				</tr>
			</tbody>
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
					<th class="noprint">Borrar</th>
				</tr>
			</thead>
			<tbody>
				<?python
					i = 1
				?>
				<tr py:for="pay in loan.pays">
					<td py:content="pay.day.strftime('%d/%m/%y')" />
					<td py:content="i, '/', loan.months" />
					<?python
						i += 1
					?>
					<td py:content="locale.currency(pay.interest)" />
					<td py:content="locale.currency(pay.capital)" />
					<td py:content="locale.currency(pay.amount)" />
					<td py:content="pay.receipt" />
					<td><a href="${tg.url('/loan/pay/remove/%s' % pay.id)}">X</a></td>
				</tr>
			</tbody>
		</table>
	</body>
</html>
