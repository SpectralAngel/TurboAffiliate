<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	from datetime import date
	import locale
	locale.setlocale(locale.LC_ALL, "en-US")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>Pr&eacute;stamos &bull; Recibo</title>
	</head>
	<body>
		<center>Colegio de Profesores de Educaci&oacute;n Media de Honduras</center>
		<br />
		<center>C&oacute;mite Administrativo Fondo AutoSeguro</center>
		<br />
		<center>Recibo L. ${locale.format('%s', loan.capital, True)}</center>
		<p>
			Recib&iacute; del Consejo Administrativo del Fondo del AutoSeguro, COPEMH,
			la cantidad de <strong>${loan.letters}</strong>. (L. ${locale.format('%s', loan.capital, True)})
			por prestamo personal que me fue entregado el d&iacute;a ${loan.startDate.day, '/', loan.startDate.month, '/',  loan.startDate.year}.
			Seg&uacute;n el detalle siguiente:
		</p>
		<table width="100%">
			<tr>
				<td><strong>Monto del Prestamo</strong></td>
				<td><strong>L. ${locale.format('%s', loan.capital, True)}</strong></td>
			</tr>
			<tr>
				<td colspan="2">Deducciones</td>
			</tr>
			<tr py:for="d in loan.deductions">
				<td>${d.name}<br /><span py:content="d.description" /></td>
				<td py:content="'L. ', locale.format('%s', d.amount, True)" />
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
		<p>
			Pr&eacute;stamo que me compromento a pagar en la forma convenida:<br />
			Cuota Mensual: ${locale.format('%s', loan.payment, True)}
			<br />
			Plazo en Meses: ${loan.months}
		</p>
		<p>
			Nombre del Afiliado: ${loan.affiliate.firstName} ${loan.affiliate.lastName}
			<br />
			Identidad: ${loan.affiliate.cardID}
			<br />
			Carnet: ${loan.affiliate.id}
			<br />
			Instituto: ${loan.affiliate.school}
			<br />
			Municipio: ${loan.affiliate.town}
			<br />
			Departamento: ${loan.affiliate.cardID}
			<br />
			Solicitud: ${loan.id}
		</p>
		<p class="center"><strong>Recib&iacute; conforme:</strong></p>
		<center><p class="center">Vo. Bo. Secretario de Finanzas</p></center>
		<p>Liquidado por: ${tg.identity.user.display_name}</p>
	</body>
</html>
