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
	<meta content="text/html; charset=us-ascii" http-equiv="Content-Type" py:replace="''" />
	<title>Pr&eacute;stamos &bull; Recibo</title>
</head>
<body>
	<h1 style="text-align: center">Colegio de Profesores de
	Educaci&oacute;n Media de Honduras</h1>
	<h2 style="text-align: center">C&oacute;mite Administrativo Fondo
	AutoSeguro</h2>
	<h3 style="text-align: center">Recibo</h3>
	<p style="text-align: justify;">Recib&iacute; del Consejo Administrativo del
    Fondo del AutoSeguro, COPEMH, la cantidad de ${loan.letters}.
    (${locale.currency(loan.capital, True, True)}) por pr&eacute;stamo personal
    que me fue entregado el d&iacute;a ${loan.startDate.strftime('%d de %B de %Y')}
    Seg&uacute;n el detalle siguiente:</p>
	<table width="100%">
		<tr>
			<th>Monto del Prestamo</th>
			<td>${locale.currency(loan.capital, True, True)}</td>
		</tr>
		<tr>
			<td colspan="2">Deducciones</td>
		</tr>
		<tr py:for="d in loan.deductions">
			<td>${d.account.name}<br />${d.description}</td>
			<td>${locale.currency(d.amount, True, True)}</td>
		</tr>
		<tr>
			<td>Total deducciones</td>
			<th style="text-align: left;">${locale.currency(loan.total_deductions(), True, True)}</th>
		</tr>
		<tr>
			<td>Remanente o Monto Liquidado</td>
			<td>${locale.currency(loan.net(), True, True)}</td>
		</tr>
	</table>
	<p>Pr&eacute;stamo que me compromento a pagar en la forma convenida:<br />
	Cuota Mensual: <strong>${locale.currency(loan.payment, True, True)}</strong><br />
	Plazo en Meses: ${loan.months}</p>
	<ul>
		<li>Nombre del Afiliado: ${loan.affiliate.firstName} ${loan.affiliate.lastName}</li>
		<li>Identidad: ${loan.affiliate.cardID}</li>
		<li>Carnet: ${loan.affiliate.id}</li>
		<li>Instituto: ${loan.affiliate.school}</li>
		<li>Municipio: ${loan.affiliate.town}</li>
		<li>Departamento: ${loan.affiliate.state}</li>
		<li>Solicitud: ${loan.id}</li>
	</ul>
	<p class="center" style="text-align: center;"><strong>Recib&iacute; conforme:</strong></p>
	<p class="center" style="text-align: center">Vo. Bo. Secretario de Finanzas</p>
	<p style="text-align: center">Liquidado por:
        <span py:if="not loan.aproval is None">${loan.aproval.display_name}</span>
        Impreso por: ${tg.identity.user.display_name}
    </p>
</body>
</html>
