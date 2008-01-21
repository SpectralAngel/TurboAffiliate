<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>Pr&eacute;stamos &bull; A&ntilde;adir</title>
	</head>
	<body>
		<h1>Agregar Deducci&oacute;n</h1>
		<form action="${tg.url('/loan/deduction/save')}" method="post">
			<fieldset>
				<legend>Informaci&oacute;n del Prestatario</legend>
				<ul>
					<li>
						<input type="hidden" name="loan" value="${loan.id}" />
						<strong py:content="loan.affiliate.firstName,' ', loan.affiliate.lastName" />
					</li>
				</ul>
			</fieldset>
			<fieldset>
				<legend>Informaci&oacute;n de la Deducci&oacute;n</legend>
				<ul>
					<li>
						<label for="name">Concepto:</label>
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
						<label for="description">Descripci&oacute;n:</label>
						<textarea name="description" />
					</li>
					<li>
                        <input type="submit" value="Agregar Deducci&oacute;n" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
