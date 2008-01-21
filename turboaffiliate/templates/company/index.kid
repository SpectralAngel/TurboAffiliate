<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Compa&ntilde;&iacute;as</title>
	</head>
	<body>
		<h1>Compa&ntilde;&iacute;as</h1>
		<ul>
			<li>
				<a href="add">A&ntilde;adir Compa&ntilde;&iacute;a</a>
			</li>
			<li>
				<a href="view">Ver Compa&ntilde;&iacute;as</a>
			</li>
		</ul>
		<form action="${tg.url('/company/search')}">
			<fieldset>
				<legend>Buscar Compa&ntilde;&iacute;a</legend>
				<ul>
					<li>
						<label for="rtn">RTN</label>
						<input name="rtn" />
					</li>
					<li>
						<input type="submit" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
