<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>Pr&eacute;stamos &bull; Pagar</title>
		<script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery.date.js')}" type="text/javascript"></script>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/date.css')}" />
	</head>
	<body>
		<h1>Pagar</h1>
		<form action="${tg.url('/payed/pay/new')}" method="post">
			<fieldset>
				<legend>Informaci&oacute;n del Prestatario</legend>
				<ul>
					<li>
						<input type="hidden" name="payedLoan" value="${loan.id}" />
						<strong py:content="loan.affiliate.firstName, ' ', loan.affiliate.lastName" />
					</li>
				</ul>
			</fieldset>
			<fieldset>
				<legend>Informaci&oacute;n del Pago</legend>
				<ul>
					<li>
						<label for="amount">Monto:</label>
						<input name="amount" />
						<span py:content="'Monto Sugerido: ', loan.payment" />
					</li>
					<li>
						<label for="day">Fecha:</label>
						<input name="day" class="date-picker" />
					</li>
					<li>
						<label for="interest">Intereses:</label>
						<input name="interest" />
					</li>
					<li>
						<label for="month">Mes:</label>
						<input name="month" />
					</li>
					<li>
						<label for="capital">Capital:</label>
						<input name="capital" />
					</li>
					<li>
						<label for="receipt">Recibo:</label>
						<input name="receipt" />
					</li>
					<li>	
						<input type="submit" value="Agregar Pago" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
