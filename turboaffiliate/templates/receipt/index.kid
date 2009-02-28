<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Recibos</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/date.css')}" />
		<script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery.date.js')}" type="text/javascript"></script>
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
											 {p:'Anterior', n:'Siguiente',
											 c:'Cierre', b:'Elija la fecha'}
											);
			$('input.date-picker').datePicker({startDate:'01/01/2006'});
			$.datePicker.setDateFormat('ymd','-');
		});
		]]>
		</script>
	</head>
	<body>
		<h1>Caja</h1>
		<form action="${tg.url('/receipt/new')}" method="post">
			<fieldset>
				<legend>Crear Recibo</legend>
				<ul>
					<li>
						<label for="id">N&uacute;mero</label>
						<input name="id" />
					</li>
					<li>
						<label for="affiliate">C&oacute;digo Afiliado</label>
						<input name="affiliate" />
					</li>
					<li>
						<label for="name">Nombre:</label>
						<input name="name" />
					</li>
					<li>
						<label for="day">D&iacute;a</label>
						<input name="day" class="date-picker" />
					</li>
					<li>
						<label for="house">Casa:</label>
						<select name="house">
							<option py:for="house in houses" value="${house.id}" py:content="house.name" />
						</select>
					</li>
					<li>
						<input type="submit" value="Continuar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/receipt/cut')}" method="post">
			<fieldset>
				<legend>Corte de Caja General</legend>
				<ul>
					<li>
						<label for="house">Nombre:</label>
						<select name="house">
							<option py:for="house in houses" value="${house.id}" py:content="house.name" />
						</select>
					</li>
					<li>
						<label for="day">D&iacute;a</label>
						<input name="day" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/receipt/cut/company')}" method="post">
			<fieldset>
				<legend>Corte de Caja por Secci&oacute;n</legend>
				<ul>
					<li>
						<label for="house">Nombre:</label>
						<select name="house">
							<option py:for="house in houses" value="${house.id}" py:content="house.name" />
						</select>
					</li>
					<li>
						<label for="company">Nombre:</label>
						<select name="company">
							<option value="fas">Fondo AutoSeguro</option>
							<option value="jdc">Junta Directiva Central</option>
						</select>
					</li>
					<li>
						<label for="day">D&iacute;a</label>
						<input name="day" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/receipt/cuotas')}" method="post">
			<fieldset>
				<legend>Reporte de Cuotas</legend>
				<ul>
					<li>
						<label for="house">Nombre:</label>
						<select name="house">
							<option py:for="house in houses" value="${house.id}" py:content="house.name" />
						</select>
					</li>
					<li>
						<label for="day">D&iacute;a</label>
						<input name="day" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/receipt/cuotas/company')}" method="post">
			<fieldset>
				<legend>Reporte de Cuotas por Compa&ntilde;ia</legend>
				<ul>
					<li>
						<label for="house">Nombre:</label>
						<select name="house">
							<option py:for="house in houses" value="${house.id}" py:content="house.name" />
						</select>
					</li>
					<li>
						<label for="company">Nombre:</label>
						<select name="company">
							<option value="fas">Fondo AutoSeguro</option>
							<option value="jdc">Junta Directiva Central</option>
						</select>
					</li>
					<li>
						<label for="day">D&iacute;a</label>
						<input name="day" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/receipt/search')}" method="post">
			<fieldset>
				<legend>Ver Recibo</legend>
				<ul>
					<li>
						<label>N&uacute;mero</label>
						<input name="code" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/receipt/daily')}" method="post">
			<fieldset>
				<legend>Mostrar Recibos de un D&iacute;a</legend>
				<ul>
					<li>
						<label for="day">D&iacute;a</label>
						<input name="day" class="date-picker" />
					</li>
					<li>
						<label for="house">Nombre:</label>
						<select name="house">
							<option py:for="house in houses" value="${house.id}" py:content="house.name" />
						</select>
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/receipt/edit')}" method="post">
			<fieldset>
				<legend>Editar Recibo</legend>
				<ul>
					<li>
						<label>N&uacute;mero</label>
						<input name="receipt" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
