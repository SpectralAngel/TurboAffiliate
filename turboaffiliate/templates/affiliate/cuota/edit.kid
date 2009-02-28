<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" 
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Editar Cuota</title>
	</head>
	<body>
		<h2>Editar Cuota de <span py:replace="table.affiliate.firstName, ' ', table.affiliate.lastName" /> A&ntilde;o <span py:replace="table.year" /></h2>
		<form action="${tg.url('/affiliate/cuota/change')}" method="post">
			<fieldset>
				<input type="hidden" name="id" value="${table.id}" />
				<legend>Cuota</legend>
				<ul>
					<li py:for="n in range(1, 13)">
						<label>Mes <span py:replace="n" />:</label>
						<input py:if="getattr(table, 'month%s' % n)" type="checkbox" name="${'month%s' % n}" checked="" />
						<input py:if="not getattr(table, 'month%s' % n)" type="checkbox" name="${'month%s' % n}" />
					</li>
					<li>
						<input type="submit" value="Grabar" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
