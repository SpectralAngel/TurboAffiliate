<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>Pr&eacute;stamos &bull; Pagar</title>
		<script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery.cuota.js')}" type="text/javascript"></script>
		<script type="text/javascript">
		<![CDATA[
		$(document).ready(function(e)
		{
			$('input.date-picker').datepicker({
												dateFormat: 'yy-mm-dd',
												changeMonth: true,
												changeYear: true,
												yearRange: '1940:2010'
											  });
		});
		]]>
		</script>
	</head>
	<body>
		<h1>Pagar</h1>
		<form action="${tg.url('/loan/pay/new')}" method="post">
			<fieldset>
				<legend>Informaci&oacute;n del Prestatario</legend>
				<ul>
					<li>
						<input type="hidden" name="code" value="${loan.id}" />
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
