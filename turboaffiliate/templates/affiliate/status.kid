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
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/status.css')}" media="print"/>
	</head>
	<body>
		<center><h3>COPEMH</h3>
		<h4>Estado de Cuenta Aportaciones</h4>
		<div><strong>Al ${day.day}/${day.month}/${day.year}</strong></div>
		<h4>${affiliate.id} ${affiliate.firstName} ${affiliate.lastName}</h4>
		<div>Afiliado desde ${affiliate.joined.day}/${affiliate.joined.month}/${affiliate.joined.year}</div>
		<br />
		</center>
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
					<td class="deuda" py:content="locale.format('%s', sum(table.payed() for table in affiliate.cuotaTables), True)" />
					<td class="deuda" py:content="locale.format('%s', sum(table.debt() for table in affiliate.cuotaTables), True)" />
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
	</body>
</html>
