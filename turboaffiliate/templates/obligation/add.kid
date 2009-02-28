<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; A&ntilde;adir Obligaci&oacute;n</title>
	</head>
	<body>
		<h2>A&ntilde;adir una Obligagic&oacute;n</h2>
		<form action="/obligation/save" method="post">
			<fieldset>
				<legend>Datos</legend>
				<ul>
					<li>
						<label for="company">Compa&ntilde;&iacute;a:</label>
						<select name="company">
							<option py:for="c in companies" value="${c.id}" py:content="c.name"/>
						</select>
					</li>
					<li>
						<label for="month">Mes:</label>
						<input name="month" />
					</li>
					<li>
						<label for="year">A&ntilde;o:</label>
						<input name= "year" />
					</li>
					<li>
						<label for="name">Descripci&oacute;n:</label>
						<input name="name" />
					</li>
					<li>
						<label for="amount">Monto:</label>
						<input name="amount" />
					</li>
					<li>
						<label for="account">Cuenta:</label>
						<select name="account">
							<option py:for="account in accounts" py:content="account.code, ' - ', account.name" value="${account.id}" />
						</select>
					</li>
					<li>
						<input type="submit" value="Guardar" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
