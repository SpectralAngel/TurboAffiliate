<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Importar Escalaf&oacute;n</title>
	</head>
	<body>
		<h2>Escalaf&oacute;n</h2>
		<!--<form action="${tg.url('/escalafon/upload')}" method="post" enctype="multipart/form-data">
			<fieldset>
				<legend>Archivo a Importar</legend>
				<ul>
					<li>
						<label for="upload">Mes:</label>
						<input type="file" name="upload" />
					</li>
					<li>
						<input type="submit" value="Guardar" />
					</li>
				</ul>
			</fieldset>
		</form>
		-->
		<form action="${tg.url('/escalafon/export')}">
			<fieldset>
				<legend>Generar Volante</legend>
				<ul>
					<li>
						<label for="month">Mes:</label>
						<input name="month" maxlength="2" />
					</li>
					<li>
						<label for="year">A&ntilde;o:</label>
						<input name="year" maxlength="4" />
					</li>
					<li>
						<input type="submit" value="Exportar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/affiliate/extra/upload')}" method="post" enctype="multipart/form-data">
			<fieldset>
				<legend>Importar Otros Volantes</legend>
				<ul>
					<li>
						<label for="upload">Archivo:</label>
						<input type="file" name="upload" />
					</li>
					<li>
						<label for="account">Cuenta:</label>
						<select name="account">
							<option py:for="account in accounts" py:content="account.name" value="${account.id}" />
						</select>
					</li>
					<li>
						<label for="months">Meses</label>
						<input name="months" />
					</li>
					<li>
						<input type="submit" value="Guardar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/escalafon/report')}" method="post">
			<fieldset>
				<legend>Ver Reporte de Ingresos</legend>
				<ul>
					<li>
						<label for="payment">Cotizaci&oacute;n:</label>
						<select name="payment">
							<option>Escalafon</option>
							<option>INPREMA</option>
							<option>UPN</option>
						</select>
					</li>
					<li>
						<label for="year">A&ntilde;o:</label>
						<input name="year" />
					</li>
					<li>
						<label for="month">Mes</label>
						<input name="month" />
					</li>
					<li>
						<input type="submit" value="Mostrar Reporte" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/escalafon/extra')}" method="post">
			<fieldset>
				<legend>Mostrar Cuentas por Cobrar</legend>
				<ul>
					<li>
						<label for="account">Cuenta:</label>
						<select name="account">
							<option py:for="account in accounts" value="${account.id}" py:content="account.name" />
						</select>
					</li>
					<li>
						<input type="submit" value="Mostrar Reporte" />
					</li>
				</ul>
			</fieldset>
		</form>
		<!--
		<form action="${tg.url('/escalafon/others')}" method="post">
			<fieldset>
				<legend>Actuaalizar Otras Cotizaciones</legend>
				<ul>
					<li>
						<label for="payment">Cotizaci&oacute;n:</label>
						<select name="payment">
							<option>INPREMA</option>
							<option>UPN</option>
						</select>
					</li>
					<li>
						<label for="year">A&ntilde;o:</label>
						<input name="year" />
					</li>
					<li>
						<label for="month">Mes</label>
						<input name="month" />
					</li>
					<li>
						<input type="submit" value="Actualizar y Mostrar Reporte" />
					</li>
				</ul>
			</fieldset>
		</form>
		-->
	</body>
</html>
