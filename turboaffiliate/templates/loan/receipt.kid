<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	from datetime import date
	import locale
	locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>Pr&eacute;stamos &bull; Recibo</title>
	</head>
	<body>
		<span style="text-align: center">Colegio de Profesores de Educaci&oacute;n Media de Honduras</span>
		<br />
		<span style="text-align: center">C&oacute;mite Administrativo Fondo AutoSeguro</span>
		<br />
		<span style="text-align: center">Recibo <span py:content="locale.currency(loan.capital)</span>
		<p>
			Recib&iacute; del Consejo Administrativo del Fondo del AutoSeguro, COPEMH,
			la cantidad de <strong py:content="loan.letters" />.
			(<span py:content="locale.currency(loan.capital)" />) por prestamo
			personal que me fue entregado el d&iacute;a
			<span py:content="loan.startDate.strftime('%A %d de %B de %Y')" />
			Seg&uacute;n el detalle siguiente:
		</p>
		<table width="100%">
			<tr>
				<th>Monto del Prestamo</th>
				<td py:content="locale.currency(loan.capital)" />
			</tr>
			<tr>
				<td colspan="2">Deducciones</td>
			</tr>
			<tr py:for="d in loan.deductions">
				<td><span py:content="d.name" /><br /><span py:content="d.description" /></td>
				<td py:content="'locale.currency(d.amount)" />
			</tr>
			<tr>
				<td>Total deducciones</td>
				<th py:content="locale.currency(sum(d.amount for d in loan.deductions))" />
			</tr>
			<tr>
				<td>Remanente o Monto Liquidado</td>
				<td py:content="locale.currency(loan.capital - sum(d.amount for d in loan.deductions))" />
			</tr>
		</table>
		<p>
			Pr&eacute;stamo que me compromento a pagar en la forma convenida:<br />
			Cuota Mensual: <span py:content="locale.currency(loan.payment)" />
			<br />
			Plazo en Meses: ${loan.months}
		</p>
		<ul>
			<li>Nombre del Afiliado: ${loan.affiliate.firstName} ${loan.affiliate.lastName}</li>
			<li>Identidad: ${loan.affiliate.cardID}</li>
			<li>Carnet: ${loan.affiliate.id}</li>
			<li>Instituto: ${loan.affiliate.school}</li>
			<li>Municipio: ${loan.affiliate.town}</li>
			<li>Departamento: ${loan.affiliate.cardID}</li>
			<li>Solicitud: ${loan.id}</li>
		</ul>
		<p class="center"><strong>Recib&iacute; conforme:</strong></p>
		<center><p class="center">Vo. Bo. Secretario de Finanzas</p></center>
		<p>Liquidado por: ${tg.identity.user.display_name}</p>
	</body>
</html>
