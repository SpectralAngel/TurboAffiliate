<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python
    from datetime import date
    import locale
    locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml"
	xmlns:py="http://purl.org/kid/ns#">
<head>
	<meta content="text/html; charset=us-ascii" http-equiv="Content-Type"
		py:replace="''" />
	<title>Pr&eacute;stamos &bull; Recibo</title>
</head>
<body>
	<h1 style="text-align: center">Colegio de Profesores de
	Educaci&oacute;n Media de Honduras</h1>
	<h2 style="text-align: center">C&oacute;mite Administrativo Fondo
	AutoSeguro</h2>
	<h3 style="text-align: center">Recibo</h3>
	<p><span style="text-align: center">Recib&iacute; del Consejo
	Administrativo del Fondo del AutoSeguro, COPEMH, la cantidad de <strong
		py:content="loan.letters" />. (<span
		py:content="locale.currency(loan.capital, True, True)" />) por prestamo personal
	que me fue entregado el d&iacute;a <span py:content="date.today().strftime('%d de %B de %Y')" /> Seg&uacute;n el detalle siguiente:</span></p>
	<table width="100%">
		<tr>
			<th>Monto del Prestamo</th>
			<td py:content="locale.currency(loan.capital, True, True)"></td>
		</tr>
		<tr>
			<td colspan="2">Deducciones</td>
		</tr>
		<tr py:for="d in loan.deductions">
			<td>
				<span py:content="d.account.name" /><br />
				<span py:content="d.description" />
			</td>
			<td py:content="locale.currency(d.amount, True, True)"></td>
		</tr>
		<tr>
			<td>Total deducciones</td>
			<th style="text-align: left;"
				py:content="locale.currency(sum(d.amount for d in loan.deductions), True, True)" />
		</tr>
		<tr>
			<td>Remanente o Monto Liquidado</td>
			<td
				py:content="locale.currency(loan.capital - sum(d.amount for d in loan.deductions), True, True)">
			</td>
		</tr>
	</table>
	<p>Pr&eacute;stamo que me
	compromento a pagar en la forma convenida:<br />
	Cuota Mensual: <strong py:content="locale.currency(loan.payment, True, True)" /><br />
	Plazo en Meses: ${loan.months}</p>
	<ul>
		<li>Nombre del Afiliado:
		${loan.affiliate.firstName} ${loan.affiliate.lastName}</li>
		<li>Identidad:
		${loan.affiliate.cardID}</li>
		<li>Carnet:
		${loan.affiliate.id}</li>
		<li>Instituto:
		${loan.affiliate.school}</li>
		<li>Municipio:
		${loan.affiliate.town}</li>
		<li>Departamento:
		${loan.affiliate.cardID}</li>
		<li>Solicitud: ${loan.id}</li>
	</ul>
	<p class="center"><span style="text-align: center"><strong>Recib&iacute;
	conforme:</strong></span></p>
	<center>
	<p class="center"><span style="text-align: center">Vo. Bo.
	Secretario de Finanzas</span></p>
	</center>
	<p><span style="text-align: center">Liquidado por:
	${tg.identity.user.display_name}</span></p>
</body>
</html>
