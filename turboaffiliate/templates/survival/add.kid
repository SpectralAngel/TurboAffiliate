<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; A&ntilde;adir Afiliado</title>
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
			$('input.date-picker').datePicker();
			$.datePicker.setDateFormat('ymd','-');
		});
		]]>
		</script>
	</head>
	<body>
		<h2>Registrar Ayuda de Sobrevivencia</h2>
		<form action="save" method="post">
			<fieldset>
				<legend>Informaci&oacute;n de Ayuda Funebre</legend>
				<ul>
					<li>
						<label for="affiliate">Afiliado:</label>
						<span py:content="affiliate.firstName, ' ', affiliate.lastName" />
						<input type="hidden" value="${affiliate.id}" name="affiliate" />
					</li>
					<li>
						<label for="cheque">Cheque:</label>
						<input name="cheque" />
					</li>
					<li>
						<label for="day">Fecha:</label>
						<input name="day" class="date-picker" />
					</li>
					<li>
						<label for="reason">Raz&oacute;n</label>
						<textarea name="reason">
						</textarea>
					</li>
					<li>
						<label for="amount">Cantidad:</label>
						<input name="amount" />
					</li>
					<li>
						<input type="submit" value="Guardar" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
