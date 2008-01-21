<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Afiliados</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/status.css')}" />
	</head>
	<body>
		<center><h3>COPEMH</h3>
		<h4>Estado de Cuenta Aportaciones</h4>
		<div><strong>Al ${day.day}/${day.month}/${day.year}</strong></div>
		<h4>${affiliate.id} ${affiliate.firstName} ${affiliate.lastName}</h4>
		<div>Afiliado desde ${affiliate.joined.day}/${affiliate.joined.month}/${affiliate.joined.year}</div>
		</center>
		<table class="small">
			<thead>
				<tr>
					<td>A&ntilde;o</td>
					<td>Enero</td>
					<td>Febrero</td>
					<td>Marzo</td>
					<td>Abril</td>
					<td>Mayo</td>
					<td>Junio</td>
					<td>Julio</td>
					<td>Agosto</td>
					<td>Sept</td>
					<td>Oct</td>
					<td>Nov</td>
					<td>Dic</td>
					<td class="deuda">Total</td>
					<td class="deuda">Deuda</td>
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
				</tr>
			</tbody>
		</table>
	</body>
</html>
