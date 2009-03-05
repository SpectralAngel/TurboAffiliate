<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Afiliados</title>
	</head>
	<body>
		<form action="save">
			<fieldset>
				<legend>Datos de la Deducci&oacute;n</legend>
				<ul>
					<li>
						<label for="account">Cuenta:</label>
						<select name="account">
							<option py:for="account in accounts" py:content="account.code, ' - ', account.name" value="${account.id}" />
						</select>
						<input type="hidden" name="affiliate" value="${affiliate.id}" />
					</li>
					<li>
						<label for="amount">Monto:</label>
						<input name="amount" />
					</li>
					<li>
						<label for="month">Mes:</label>
						<input name="month" />
					</li>
					<li>
						<label for="year">A&ntilde;o:</label>
						<input name="year" />
					</li>
					<li>
                        <input type="submit" value="Agregar Deducci&oacute;n" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>

