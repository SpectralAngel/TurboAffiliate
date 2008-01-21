<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Editar Afiliado</title>
		<script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery.date.js')}" type="text/javascript"></script>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/date.css')}" />
		<script type="text/javascript">
		<![CDATA[
		$(document).ready(function(e)
		{
			$.datePicker.setLanguageStrings(['Domingo', 'Lunes', 'Martes',
											 'Miércoles', 'Jueves', 'Viernes',
											 'Sábado'],	['Enero', 'Febrero',
											 'Marzo', 'Abril', 'Mayo', 'Junio',
											 'Julio', 'Agosto', 'Septiembre',
											 'Octubre', 'Noviembre', 'Diciembre'],
											 {p:'Atras', n:'Siguiente',
											 c:'Cierre', b:'Elija la fecha'}
											);
			$('input.date-picker').datePicker({startDate:'01/01/1950'});
			$.datePicker.setDateFormat('ymd','-');
		});
		]]>
		</script>
	</head>
	<body>
		<h2>Editar un Afiliado</h2>
		<form action="${tg.url('/affiliate/save')}" method="post">
			<fieldset>
				<legend>Personal</legend>
				<input type="hidden" value="${affiliate.id}" name="affiliate" />
				<ul>
					<li>
						<label for="firstName">Nombre:</label>
						<input name="firstName" value="${affiliate.firstName}" />
					</li>
					<li>
						<label for="lastName">Apellido:</label>
						<input name="lastName" value="${affiliate.lastName}" />
					</li>
					<li>
						<label for="birthPlace">Lugar de Nacimiento:</label>
						<input name= "birthPlace" value="${affiliate.birthPlace}" />
					</li>
					<li>
						<label for="phone">Tel&eacute;fono:</label>
						<input name="phone" value="${affiliate.phone}"/>
					</li>
					<li>
						<label>Identidad:</label>
						<input name="cardID" value="${affiliate.cardID}" maxlength="15"/>
					</li>
					<li>
						<label for="birthday">Fecha de Nacimiento</label>
						<input name="birthday" value="${affiliate.birthday}" class="date-picker" />
						<span class="help">formato: a&ntilde;o-mes-d&iacute;a</span>
					</li>
					<li>
						<label for="joined">Fecha de Afiliaci&oacute;n</label>
						<input name="joined" value="${affiliate.joined}" class="date-picker" />
						<span class="help">formato: a&ntilde;o-mes-d&iacute;a</span>
					</li>
				</ul>
			</fieldset>
			<fieldset>
				<legend>Colegiaci&oacute;n</legend>
				<ul>
					<li>
						<label for="payment">Cotiza por:</label>
						<select name="payment">
							<option py:if="affiliate.payment == 'Escalafon'" selected="">Escalafon</option>
							<option py:if="not affiliate.payment == 'Escalafon'">Escalafon</option>
							<option py:if="affiliate.payment == 'UPN'" selected="">UPN</option>
							<option py:if="not affiliate.payment == 'UPN'">UPN</option>
							<option py:if="affiliate.payment == 'INPREMA'" selected="">INPREMA</option>
							<option py:if="not affiliate.payment == 'INPREMA'">INPREMA</option>
							<option py:if="affiliate.payment == 'Ventanilla'" selected="">Ventanilla</option>
							<option py:if="not affiliate.payment == 'Ventanilla'">Ventanilla</option>
						</select>
					</li>
					<li>
						<label for="escalafon">Escalaf&oacute;n:</label>
						<input name="escalafon" value="${affiliate.escalafon}" />
					</li>
					<li>
						<label for="school">Instituto:</label>
						<input name="school" value="${affiliate.school}" />
					</li>
					<li>
						<label for="town">Municipio:</label>
						<input name="town" value="${affiliate.town}" />
					</li>
					<li>
						<label for="state">Departamento:</label>
						<input name="state" value="${affiliate.state}" />
					</li>
					<li>
						<input type="submit" value="Guardar" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
