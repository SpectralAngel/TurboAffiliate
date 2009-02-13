<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Estados de Cuenta</title>
	</head>
	<body>
		<h1>Estados de Cuenta</h1>
		<form action="state">
			<fieldset>
				<legend>Por Departamento</legend>
				<ul>
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
					<li>
						<input type="submit" value="Mostrar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="payment">
			<fieldset>
				<legend>Cotizaci&oacute;n</legend>
				<ul>
					<li>
						<label for="how">Cotiza por:</label>
						<select name="how">
							<option>Escalafon</option>
							<option>INPREMA</option>
							<option>UPN</option>
							<option>Ventanilla</option>
						</select>
					</li>
					<li>
						<input type="submit" value="Mostrar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="rango">
			<fieldset>
				<legend>Rango</legend>
				<ul>
					<li>
						<label for="start">Inicio:</label>
						<input name="start" />
					</li>
					<li>
						<label for="end">Fin:</label>
						<input name="end" />
					</li>
					<li>
						<input type="submit" value="Mostrar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="school">
			<fieldset>
				<legend>Instituto</legend>
				<ul>
					<li>
						<label for="school">Instituto:</label>
						<input name="school" />
					</li>
					<li>
						<input type="submit" value="Mostrar" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
