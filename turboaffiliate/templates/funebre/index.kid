<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Obligaciones</title>
	</head>
	<body>
		<h1>Ayudas Funebres</h1>
		<form action="search" method="post">
			<fieldset>
				<legend>Buscar Ayuda Funebre</legend>
				<ul>
					<li>
						<label for="code">Carnet:</label>
						<input name="code" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="save" method="post">
			<fieldset>
				<legend>Agregar Ayuda Funebre</legend>
				<ul>
					<li>
						<label for="affiliate">Carnet:</label>
						<input name="affiliate" />
					</li>
					<li>
						<label for="amount">Cantidad:</label>
						<input name="amount" />
					</li>
					<li>
						<label for="cheque">Cheque:</label>
						<input name="cheque" />
					</li>
					<li>
						<label for="reason">Raz&oacute;n:</label>
						<textarea name="reason"></textarea>
					</li>
					<li>
						<input type="submit" value="Guardar" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
