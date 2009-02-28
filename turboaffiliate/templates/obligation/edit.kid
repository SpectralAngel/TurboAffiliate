<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
from datetime import date
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Editar Afiliado</title>
		<script src="/static/javascript/jquery.js" type="text/javascript"></script>
		<script src="/static/javascript/jquery.date.js" type="text/javascript"></script>
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
		<form action="/affiliate/save" method="post">
			<fieldset>
				<legend>Personal</legend>
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
						<label>Identidad:</label>
						<input name="cardID" value="${affiliate.cardID}" />
					</li>
					<li>
						<label for="birthday">Fecha de Nacimiento</label>
						<input name="birthday" value="${affiliate.birthday}" class="date-picker"/>
					</li>
				</ul>
			</fieldset>
			<fieldset>
				<legend>Colegiaci&oacute;n</legend>
				<ul>
					<li>
						<label for="escalafon">Escalaf&oacute;n:</label>
						<input name="escalafon" value="${affiliate.escalafon}" />
					</li>
				</ul>
			</fieldset>
			<input type="submit" value="Guardar" />
		</form>
	</body>
</html>
