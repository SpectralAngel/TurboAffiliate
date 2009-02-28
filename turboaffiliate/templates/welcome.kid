<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Inicio</title>
	</head>
	<body>
		<h2>Bienvenido al Sistema de Afiliados del COPEMH</h2>
		<form action="${tg.url('affiliate/byCopemh')}">
			<fieldset>
				<legend>Buscar Afiliado</legend>
				<ul>
					<li>
						<label>Carnet:</label>
						<input name="copemh" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('affiliate/status')}">
			<fieldset>
				<legend>Ver Estado de Cuenta Aportaciones</legend>
				<ul>
					<li>
						<label>Carnet:</label>
						<input name="cardID" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="${tg.url('loan/add')}">
			<fieldset>
				<legend>A&ntilde;adir Pr&eacute;stamo a Afiliado</legend>
				<ul>
					<li>
						<label>Carnet:</label>
						<input name="cardID" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
