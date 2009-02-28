<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; A&ntilde;adir Compa&ntilde;&iacute;a</title>
	</head>
	<body>
		<h2>A&ntilde;adir una Compa&ntilde;&iacute;a</h2>
		<form action="${tg.url('/company/save')}" method="post">
			<fieldset>
				<legend>Datos Generales</legend>
				<ul>
					<li>
						<label for="name">Nombre:</label>
						<input name="name" value="${company.name}" />
					</li>
					<li>
						<label for="rtn">N&uacute;mero RTN:</label>
						<input name="rtn" value="${company.rtn}" />
					</li>
					<li>
						<label for="description">Descripci&oacute;n:</label>
						<input name= "description" value="${company.description}" />
					</li>
				</ul>
			</fieldset>
			<input type="submit" value="Guardar" />
		</form>
	</body>
</html>
