<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; A&ntilde;adir Afiliado</title>
	</head>
	<body>
		<h2>A&ntilde;adir un Afiliado</h2>
		<form action="/affiliate/deactivateTrue" method="post">
			<fieldset>
				<legend>Desactivar Afiliado</legend>
				<ul>
					<li>
						<label>Afiliado:</label>
						<input value="${affiliate.firstName + ' ' + affiliate.firstName}" readonly="readonly" />
						<input value="${affiliate.id}" name="affiliate" readonly="readonly" />
					</li>
					<li>
						<label>Raz&oacute;n</label>
						<select name="reason">
							<option>Retiro</option>
							<option>Fallecimiento</option>
							<option>Renuncia</option>
							<option>No es Afiliado</option>
							<option>Suspendido</option>
						</select>
					</li>
					<li><input type="submit" value="Desactivar" /> </li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
