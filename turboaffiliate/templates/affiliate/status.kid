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
		 <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/form.css')}" media="screen" />
		 <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print" />
	</head>
	<body>
		<div style="text-align: center">
			<h3>COPEMH</h3>
			<h4>Estado de Cuenta Aportaciones</h4>
			<div><strong py:content="'Al ', day.strftime('%d de %B de %Y')" /></div>
			<h4 py:content="affiliate.id, ' ', affiliate.firstName, ' ', affiliate.lastName " />
			<span>Afiliado desde </span><span py:content="affiliate.joined.strftime('%d de %B de %Y')" />
			<p style="color: red;" py:if="affiliate.jubilated is None and affiliate.payment == 'INPREMA'">Advertencia, el afiliado esta jubilado y no tiene Fecha de Jubilacion, los calculos son erroneos</p>
		</div>
		<table class="small" width="100%">
			<thead>
				<tr>
					<th>A&ntilde;o</th>
					<th>Enero</th>
					<th>Febrero</th>
					<th>Marzo</th>
					<th>Abril</th>
					<th>Mayo</th>
					<th>Junio</th>
					<th>Julio</th>
					<th>Agosto</th>
					<th>Sept</th>
					<th>Oct</th>
					<th>Nov</th>
					<th>Dic</th>
					<th class="deuda">Total</th>
					<th class="deuda">Deuda</th>
					<th class="noprint">E</th>
					<th class="noprint">B</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="table in affiliate.cuotaTables">
					<td py:content="table.year" />
					<td py:content="table.amount(1)" />
					<td py:content="table.amount(2)" />
					<td py:content="table.amount(3)" />
					<td py:content="table.amount(4)" />
					<td py:content="table.amount(5)" />
					<td py:content="table.amount(6)" />
					<td py:content="table.amount(7)" />
					<td py:content="table.amount(8)" />
					<td py:content="table.amount(9)" />
					<td py:content="table.amount(10)" />
					<td py:content="table.amount(11)" />
					<td py:content="table.amount(12)" />
					<td class="deuda" py:content="table.payed()" />
					<td class="deuda" py:content="table.debt()" />
					<td class="noprint"><a class="delete" href="${tg.url('/affiliate/cuota/edit/%s' % table.id)}">X</a></td>
					<td class="noprint"><a class="delete" href="${tg.url('/affiliate/cuota/remove/%s' % table.id)}">X</a></td>
				</tr>
			</tbody>
			<tfoot>
				<tr class="total">
					<td colspan="13">&nbsp;</td>
					<td class="deuda" py:content="locale.currency(sum(table.payed() for table in affiliate.cuotaTables), True, True)" />
					<td class="deuda" py:content="locale.currency(sum(table.debt() for table in affiliate.cuotaTables), True, True)" />
				</tr>
			</tfoot>
		</table>
        <table style="width: 100%; text-align: center;">
            <caption>Cobros a Efectuar</caption>
            <thead>
                <th>Concepto</th>
                <th>Retrasada</th>
                <th>Mes</th>
                <th>Anio</th>
                <th>Cantidad</th>
            </thead>
            <tbody>
                <tr>
                    <td>Aportaci&oacute;n Ordinaria</td>
                    <td>No</td>
                    <td></td>
                    <td></td>
                    <td>${locale.currency(affiliate.get_cuota(), True, True)}</td>
                </tr>
                <tr py:for="loan in affiliate.loans">
                    <td>Cuota de Pr&eacute;stamo</td>
                    <td>No</td>
                    <td></td>
                    <td></td>
                    <td>${locale.currency(loan.get_payment(), True, True)}</td>
                </tr>
                <tr py:for="extra in affiliate.extras">
                    <td>${extra.account.name}</td>
                    <td py:if="extra.retrasada">S&iacute;</td>
                    <td py:if="not extra.retrasada">No</td>
                    <td>${extra.mes}</td>
                    <td>${extra.anio}</td>
                    <td>${locale.currency(extra.amount, True, True)}</td>
                </tr>
                <tr py:for="reintegro in affiliate.reintegros" py:if="not reintegro.pagado">
                    <td>Reintegro</td>
                    <td>No</td>
                    <td>${reintegro.motivo}</td>
                    <td>${extra.fecha.strftime('%d/%m/%Y')}</td>
                    <td>${locale.currency(reintegro.monto, True, True)}</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <th colspan="4">Total de Deducciones</th>
                    <th>${locale.currency(affiliate.get_monthly(), True, True)}</th>
                </tr>
            </tfoot>
        </table>
		<form action="${tg.url('/affiliate/populate')}" method="post" class="noprint">
			<fieldset>
				<legend>A&ntilde;adir A&ntilde;o</legend>
				<input type="hidden" value="${affiliate.id}" name="affiliate" />
				<ul>
					<li>
						<label for="year">A&ntilde;o</label>
						<input name="year" />
					</li>
					<li>
						<input type="submit" value="A&ntilde;adir" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/affiliate/fill')}" method="post" class="noprint">
			<fieldset>
				<legend>Postear A&ntilde;os</legend>
				<input type="hidden" value="${affiliate.id}" name="affiliate" />
				<ul>
					<li>
						<label for="start">A&ntilde;o Inicial</label>
						<input name="start" />
					</li>
					<li>
						<label for="end">A&ntilde;o Final</label>
						<input name="end" />
					</li>
					<li>
						<input type="submit" value="A&ntilde;adir" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
