<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; A&ntilde;adir Afiliado</title>
	</head>
	<body>
		<h2>Registrar Ayuda de Sobrevivencia</h2>
		<form action="save" method="post">
			<fieldset>
				<legend>Informaci&oacute;n de Ayuda Funebre</legend>
				<ul>
					<li>
						<label for="affiliate">Afiliado:</label>
						<span py:content="affiliate.firstName, ' ', affiliate.lastName" />
						<input type="hidden" value="${affiliate.id}" name="affiliate" />
					</li>
					<li>
						<label for="amount">Cantidad:</label>
						<input name="amount" />
					</li>
					<li>
						<input type="submit" value="Guardar" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
