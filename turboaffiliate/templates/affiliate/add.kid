<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; A&ntilde;adir Afiliado</title>
		<script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
		<script type="text/javascript">
		<![CDATA[
		$(document).ready(function(e)
		{
			$('input.date-picker').datepicker({
												dateFormat: 'yy-mm-dd',
												changeMonth: true,
												changeYear: true,
												yearRange: '1940:2010'
											  });
		});
		]]>
		</script>
	</head>
	<body>
		<h2>A&ntilde;adir un Afiliado</h2>
		<form action="save" method="post">
			<fieldset>
				<legend>Personal</legend>
				<ul>
					<li>
						<label>Identidad:</label>
						<input name="cardID" maxlength="15" />
					</li>
					<li>
						<label for="firstName">Nombres:</label>
						<input name="firstName" />
					</li>
					<li>
						<label for="lastName">Apellidos:</label>
						<input name="lastName" />
					</li>
					<li>
						<label for="birthPlace">Lugar de Nacimiento:</label>
						<input name="birthPlace" />
					</li>
					<li>
						<label for="phone">Tel&eacute;fono:</label>
						<input name="phone" />
					</li>
					<li>
						<label for="gender">Sexo:</label>
						<select name="gender">
							<option value="M">Masculino</option>
							<option value="F">Femenino</option>
						</select>
					</li>
					<li>
						<label for="birthday">Fecha de Nacimiento</label>
						<input name="birthday" class="date-picker" />
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
							<option>Escalafon</option>
							<option>UPN</option>
							<option>INPREMA</option>
							<option>Ventanilla</option>
							<option>Ministerio</option>
						</select>
					</li>
					<li>
						<label for="escalafon">Escalaf&oacute;n:</label>
						<input name="escalafon" />
					</li>
					<li>
						<label for="school">Instituto:</label>
						<input name="school" />
					</li>
					<li>
						<label for="school2">Instituto:</label>
						<input name="school2" />
					</li>
					<li>
						<label for="inprema">INPREMA:</label>
						<input name="inprema" />
					</li>
					<li>
						<label for="town">Municipio:</label>
						<input name="town" />
					</li>
					<li>
						<label for="state">Departamento:</label>
						<select name="state">
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
				</ul>
			</fieldset>
			<input type="submit" value="Guardar" />
		</form>
	</body>
</html>

