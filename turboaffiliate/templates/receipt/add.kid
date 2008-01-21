<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>Recibos &bull; Nuevo</title>
	</head>
	<body>
		<h1>Crear un Recibo</h1>
		<form action="${tg.url('/receipt/new')}" method="post">
			<fieldset>
				<legend>Informaci&oacute;n del Recibo</legend>
				<ul>
					<li>
						<label for="id">N&uacute;mero</label>
						<input name="id" />
					</li>
					<li>
						<label for="affiliate">C&oacute;digo Afiliado</label>
						<input name="affiliate" />
					</li>
					<li>
						<label for="name">Nombre:</label>
						<input name="name" />
					</li>
					<li>
						<label for="house">Casa:</label>
						<select name="house">
							<option py:for="house in houses" value="${house.id}" py:content="house.name" />
						</select>
					</li>
					<li>
						<input type="submit" value="Continuar" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
