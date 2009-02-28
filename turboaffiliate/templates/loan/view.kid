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
		<script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery.date.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery.cuota.js')}" type="text/javascript"></script>
		<script type="text/javascript">
		<![CDATA[
		$(document).ready(function(e)
		{
			$("#calc").click(get_cuota);
		});
		]]>
		</script>
	</head>
	<body>
		<div style="text-align: center;">
			<h1>COPEMH</h1>
			<h2>Estado de Cuenta P&eacute;stamos</h2>
			<h3 py:content="'Pr&eacute;stamo N&uacute;mero ', loan.id" />
		</div>
		<ul>
			<li>
				<strong>Prestatario:</strong>
				<a href="${tg.url('/affiliate/%s' % loan.affiliate.id)}">
					<span py:content="loan.affiliate.id" />
				</a>
				<span py:content="loan.affiliate.firstName, ' ', loan.affiliate.lastName" />
			</li>
			<li>
				<strong>Fecha de Inicio:</strong>
				<span py:content="loan.startDate.strftime('%d/%m/%Y')" />
			</li>
			<li>
				<strong>Pago Mensual:</strong>
				<span py:content="locale.currency(loan.payment, True, True)" />
			</li>
			<li>
				<strong>Monto Original:</strong>
				<span py:content="locale.currency(loan.capital, True, True)" />
			</li>
			<li>
				<strong>Monto Debido</strong>
				<span py:content="locale.currency(loan.debt, True, True)" />
			</li>
		</ul>
		<ul>
			<li class="add">
				<a href="${tg.url('/loan/pay/add/%s' % loan.id)}">Agregar un Pago</a>
			</li>
			<li class="delete">
				<a href="${'/loan/remove/%s' % loan.id}">Eliminar</a>
			</li>
			<li class="add">
				<a href="${tg.url('/loan/deduction/add/%s' % loan.id)}">A&ntilde;adir Deducci&oacute;n</a>
			</li>
			<li>
				<a href="${tg.url('/loan/increase/%s' % loan.id)}">Corregir Mes +1</a>
			</li>
			<li>
				<a href="${tg.url('/loan/decrease/%s' % loan.id)}">Corregir Mes -1</a>
			</li>
		</ul>
		<form action="${tg.url('/loan/modify')}">
			<fieldset>
				<legend>Cambiar Cuota</legend>
				<ul>
					<li>
						<label for="payment">Cuota:</label>
						<input name="payment" />
						<input type="hidden" name="loan" value="${loan.id}" />
					</li>
					<li>
						<input value="Modificar"  type="submit" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/loan/debt')}">
			<fieldset>
				<legend>Cambiar Saldo</legend>
				<ul>
					<li>
						<label for="debt">Cuota:</label>
						<input name="debt" />
						<input type="hidden" name="loan" value="${loan.id}" />
					</li>
					<li>
						<input value="Modificar"  type="submit" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/loan/month')}">
			<fieldset>
				<legend>Cambiar Periodo de Pago</legend>
				<ul>
					<li>
						<label for="months">Meses:</label>
						<input name="months" id="months" />
						<input type="hidden" name="loan" value="${loan.id}" />
						<input name="capital" id="amount" value="${loan.capital}" type="hidden" />
						<input name="interest" id="interest" value="${loan.interest}" type="hidden" />
					</li>
					<li>
						<label for="payment">Cuota:</label>
						<input name="payment" id="payment" />
						<a href="javascript:void()" id="calc" >Calcular</a>
					</li>
					<li>
						<input value="Modificar"  type="submit" />
					</li>
				</ul>
			</fieldset>
		</form>
		<h4>Deducciones Aplicadas</h4>
		<table>
			<thead>
				<tr>
					<th>Concepto</th>
					<th>Cantidad</th>
					<th py:if="'admin' in tg.identity.groups">Borrar</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="deduction in loan.deductions">
					<td py:content="deduction.name" />
					<td py:content="locale.currency(deduction.amount, True, True)" />
					<td py:if="'admin' in tg.identity.groups">
						<a href="${tg.url('/loan/deduction/remove/%s' % deduction.id)}">Borrar</a>
					</td>
				</tr>
			</tbody>
		</table>
		<h4>Pagos Efectuados</h4>
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
					<td py:content="pay.day.strftime('%d/%m/%Y')" />
					<td py:content="locale.currency(pay.interest, True, True)" />
					<td py:content="locale.currency(pay.capital, True, True)" />
					<td py:content="locale.currency(pay.amount, True, True)" />
					<td><a href="${tg.url('/loan/pay/remove/%s' % pay.id)}">X</a></td>
				</tr>
			</tbody>
		</table>
	</body>
</html>

