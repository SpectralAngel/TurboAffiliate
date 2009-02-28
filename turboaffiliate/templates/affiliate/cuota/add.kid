<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" 
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Pagar Cuota</title>
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
		<h2>Pago de Cuota</h2>
		<form action="${tg.url('/affiliate/cuota/save')}" method="get">
			<fieldset>
				<input type="hidden" name="affiliate" value="${affiliate.id}" />
				<legend>Cuota</legend>
				<ul>
					<li>
						<label for="amount">Monto:</label>
						<input name="amount" />
					</li>
					<li>
						<label for="day">Fecha:</label>
						<input name="day" class="date-picker" />
					</li>
					<li>
						<label for="how">Tipo de Pago</label>
						<select name="how">
							<option value="1">M&aacute;s de un mes</option>
							<option value="2" selected="selected">S&oacute;lo un mes</option>
						</select>
					</li>
					<li>
						<input type="submit" value="Grabar" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
