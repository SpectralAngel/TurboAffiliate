<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>Pr&eacute;stamos &bull; A&ntilde;adir</title>
	</head>
	<body>
		<h1>A&ntilde;adir una cuenta</h1>
		<form action="${tg.url('/account/agregarRetrasada')}" method="post">
			<fieldset>
				<legend>Informaci&oacute;n de la Cuenta</legend>
				<ul>
					<li>
						<label>cuenta:</label>
						<select name="account" >
						    <option py:for="a in accounts" value="${a.id}">${a.name}</option>
						</select>
					</li>
					<li>
						<label for="month">Mes</label>
						<input name="month" />
					</li>
					<li>
						<label for="year">A&ntilde;o</label>
						<input name="year" />
					</li>
					<li>
						<input type="submit" value="Guardar" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
