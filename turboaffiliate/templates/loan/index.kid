<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Afiliados</title>
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
		<h1>Pr&eacute;stamos</h1>
		<form action="search" method="post">
			<fieldset>
				<legend>Buscar Pr&eacute;stamo</legend>
				<ul>
					<li>
						<label>N&uacute;mero de Pr&eacute;stamo</label>
						<input name="code" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="/payed">
			<fieldset>
				<legend>Ver Pr&eacute;stamo Pagado</legend>
				<ul>
					<li>
						<label>Solicitud:</label>
						<input name="id" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="add">
			<fieldset>
				<legend>A&ntilde;adir Pr&eacute;stamo a Afiliado</legend>
				<ul>
					<li>
						<label>Carnet:</label>
						<input name="cardID" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="day">
			<fieldset>
				<legend>Mostrar Pr&eacute;stamos de un D&iacute;a</legend>
				<ul>
					<li>
						<label>D&iacute;a:</label>
						<input name="day" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="period">
			<fieldset>
				<legend>Mostrar Pr&eacute;stamos de un Periodo</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="first" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="last" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="cartera">
			<fieldset>
				<legend>Mostrar Cartera Pr&eacute;stamos</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="first" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="last" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="monthly">
			<fieldset>
				<legend>Reporte de Pr&eacute;stamos Otorgados</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="start" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="end" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="bypayment">
			<fieldset>
				<legend>Pr&eacute;stamos por Tipo de Cotizaci&oacute;n</legend>
				<ul>
					<li>
						<label for="payment">Cotiza por:</label>
						<select name="payment">
							<option>Escalafon</option>
							<option>INPREMA</option>
							<option>UPN</option>
						</select>
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="liquid">
			<fieldset>
				<legend>Reporte de Liquidaci&oacute;n de Pr&eacute;stamos</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="start" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="end" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="byCapital">
			<fieldset>
				<legend>Reporte de Capital e Intereses</legend>
				<ul>
					<li>
						<label>D&iacute;a:</label>
						<input name="day" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="resume">
			<fieldset>
				<legend>Resumen de Capital e Intereses por Periodo</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="start" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="end" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="pay/resume">
			<fieldset>
				<legend>Detalle de Pagos por Periodo</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="start" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="end" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
