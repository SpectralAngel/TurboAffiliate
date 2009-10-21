s<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Compa&ntilde;&iacute;as</title>
		<script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
		<script type="text/javascript">
		<![CDATA[
		$(document).ready(function(e)
		{
			$('input.date-picker').datepicker({ dateFormat: 'yy-mm-dd' });
		});
		]]>
		</script>
	</head>
	<body>
		<form action="${tg.url('/asamblea/agregar')}">
			<fieldset>
				<legend>Agregar Asamblea</legend>
				<ul>
					<li>
						<label>A&ntilde;o:</label>
						<input name="anio" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/asamblea/asistente')}">
			<fieldset>
				<legend>Agregar Asistente</legend>
				<ul>
					<li>
						<label>Asamblea</label>
						<select name="asamblea">
							<option py:for="asamblea in asambleas" py:content="asamblea.id" />
						</select>
					</li>
					<li>
						<label>Afiliado</label>
						<input name="afiliado" />
					</li>
					<li>
						<label for="departamento">Departamento:</label>
						<select name="departamento">
							<option>Atlantida</option>
							<option>Choluteca</option>
							<option>Colon</option>
							<option>Comayagua</option>
							<option>Copan</option>
							<option>Cortes</option>
							<option>El Paraiso</option>
							<option>Francisco Morazan</option>
							<option>Gracias a Dios</option>
							<option>Intibuca</option>
							<option>Islas de la Bahia</option>
							<option>La Paz</option>
							<option>Lempira</option>
							<option>Olancho</option>
							<option>Ocotepeque</option>
							<option>Santa Barbara</option>
							<option>Valle</option>
							<option>Yoro</option>
						</select>
					</li>
					<li>
						<label>Muncipio</label>
						<input name="municipio" />
					</li>
					<li>
						<label>Cuenta</label>
						<input name="cuenta" />
					</li>
					<li>
						<label>Banco</label>
						<select name="banco">
							<option py:for="banco in bancos" py:content="banco.nombre" value="${banco.codigo}" />
						</select>
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
