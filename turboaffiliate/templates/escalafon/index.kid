<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Volantes y Deducciones</title>
	</head>
	<body>
		<h2>Volantes y Deducciones</h2>
		<ul>
			<li><a href="${tg.url('filialesAll')}">Ver Filiales</a></li>
			<li><a href="${tg.url('filialesFive')}">Ver Filiales con 5 afiliados o m&aacute;s</a></li>
		</ul>
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
		<form action="${tg.url('/escalafon/postReport')}" method="post">
			<fieldset>
				<legend>Ver Reporte de Ingresos</legend>
				<ul>
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
		<form action="${tg.url('/escalafon/report')}" method="post">
			<fieldset>
				<legend>Ver Reporte de Ingresos Previos</legend>
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
		<form action="${tg.url('/escalafon/deduced')}" method="post">
			<fieldset>
				<legend>Mostrar Cobros Efecutados</legend>
				<ul>
					<li>
						<label for="account">Cuenta:</label>
						<select name="account">
							<option py:for="account in accounts" value="${account.id}" py:content="account.name" />
						</select>
					</li>
					<li>
						<label for="month">Mes:</label>
						<input name="month" />
					</li>
					<li>
						<label for="year">A&ntilde;o:</label>
						<input name="year" />
					</li>
					<li>
						<input type="submit" value="Mostrar Reporte" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/escalafon/OtherReport')}" method="post">
			<fieldset>
				<legend>Actualizar Otras Cotizaciones</legend>
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
						<input type="submit" value="Actualizar Reporte" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/escalafon/showReport')}" method="post">
			<fieldset>
				<legend>Mostrar Otros Reportes</legend>
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
						<input type="submit" value="Mostrar Reporte" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/escalafon/deduced')}" method="post">
			<fieldset>
				<legend>Mostrar Reporte Por Cuenta</legend>
				<ul>
					<li>
						<label for="account">Cuenta:</label>
						<select name="account">
							<option py:for="account in accounts" value="${account.id}" py:content="account.name" />
						</select>
					</li>
					<li>
						<label for="month">Mes:</label>
						<input name="month" />
					</li>
					<li>
						<label for="year">A&ntilde;o:</label>
						<input name="year" />
					</li>
					<li>
						<input type="submit" value="Mostrar Reporte" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/escalafon/deducedPayment')}" method="post">
			<fieldset>
				<legend>Mostrar Reporte Por Cuenta y Cotizaci&oacute;n</legend>
				<ul>
					<li>
						<label for="payment">Cotizaci&oacute;n:</label>
						<select name="payment">
							<option>INPREMA</option>
							<option>UPN</option>
						</select>
					</li>
					<li>
						<label for="account">Cuenta:</label>
						<select name="account">
							<option py:for="account in accounts" value="${account.id}" py:content="account.name" />
						</select>
					</li>
					<li>
						<label for="month">Mes:</label>
						<input name="month" />
					</li>
					<li>
						<label for="year">A&ntilde;o:</label>
						<input name="year" />
					</li>
					<li>
						<input type="submit" value="Mostrar Reporte" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/escalafon/filiales')}" method="post">
			<fieldset>
				<legend>Mostrar Reporte de Filiales</legend>
				<ul>
					<li>
						<label for="month">Mes:</label>
						<input name="month" />
					</li>
					<li>
						<label for="year">A&ntilde;o:</label>
						<input name="year" />
					</li>
					<li>
						<input type="submit" value="Mostrar Reporte" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('/escalafon/cuotas')}" method="post">
			<fieldset>
				<legend>Mostrar Reporte de Cuotas Retrasadas</legend>
				<ul>
					<li>
						<label for="month">Mes:</label>
						<input name="month" />
					</li>
					<li>
						<label for="year">A&ntilde;o:</label>
						<input name="year" />
					</li>
					<li>
						<input type="submit" value="Mostrar Reporte" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
