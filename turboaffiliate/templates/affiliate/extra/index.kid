<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; A&ntilde;adir Afiliado</title>
	</head>
	<body>
		<form action="${tg.url('/affiliate/extra/many')}">
			<fieldset>
			    <legend>A&ntilde;adir una Deducci&oacute;n Extra a un Rango</legend>
				<ul>
					<li>
						<label for="amount">Cantidad:</label>
						<input name="amount" />
					</li>
					<li>
						<label for="account">Cuenta:</label>
						<select name="account">
							<option py:for="account in accounts" py:content="account.name" value="${account.id}" />
						</select>
					</li>
					<li>
						<label for="first">Primero</label>
						<input name="first" />
					</li>
					<li>
						<label for="last">Ultimo</label>
						<input name="last" />
					</li>
					<li>
						<label for="months">Meses</label>
						<input name="months" />
					</li>
				</ul>
			</fieldset>
			<input type="submit" value="Guardar" />
		</form>
        <form action="${tg.url('/affiliate/extra/payment')}">
			<fieldset>
			    <legend>Agregar por Tipo de Pago</legend>
				<ul>
					<li>
						<label for="amount">Cantidad:</label>
						<input name="amount" />
					</li>
					<li>
						<label for="account">Cuenta:</label>
						<select name="account">
							<option py:for="account in accounts" py:content="account.name" value="${account.id}" />
						</select>
					</li>
					<li>
						<label for="payment">Cotizaci&oacute;n:</label>
						<select name="payment">
							<option>Escalafon</option>
							<option>INPREMA</option>
							<option>UPN</option>
							<option>Ventanilla</option>
							<option>Ministerio</option>
							<option>Retirado</option>
						</select>
					</li>
					<li>
						<label for="months">Meses</label>
						<input name="months" />
					</li>
				</ul>
			</fieldset>
			<input type="submit" value="Agregar" />
		</form>
	</body>
</html>
