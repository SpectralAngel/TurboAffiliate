<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>Pr&eacute;stamos &bull; A&ntilde;adir</title>
		<script src="/static/javascript/jquery.js" type="text/javascript"></script>
		<script src="/static/javascript/jquery.date.js" type="text/javascript"></script>
		<script src="/static/javascript/jquery.cuota.js" type="text/javascript"></script>
		<script type="text/javascript">
		<![CDATA[
		$(document).ready(function(e)
		{
			$("#calc").click(get_cuota);
		});
		]]>
		</script>
	</head>
	<body>
		<h1>Crear un Pr&eacute;stamo</h1>
		<form action="${tg.url('/loan/ref')}" method="post">
			<fieldset>
				<legend>Informaci&oacute;n del Prestatario</legend>
				<ul>
					<li>
						<input type="hidden" name="cardID" value="${affiliate.cardID}" />
						<strong py:content="affiliate.firstName, affiliate.lastName" />
					</li>
				</ul>
			</fieldset>
			<fieldset>
				<legend>Informaci&oacute;n del Aval</legend>
				<ul>
					<li>
						<label for="avalFirst">Nombre:</label>
						<input name="avalFirst" />
					</li>
					<li>
						<label for="avalLast">Apellidos</label>
						<input name="avalLast" />
					</li>
					<li>
						<label for="avalCard">Identidad</label>
						<input name="avalCard" />
					</li>
				</ul>
			</fieldset>
			<fieldset>
				<legend>Datos del Prest&aacute;mo</legend>
				<ul>
					<li>
						<label for="amount">Monto:</label>
						<input name="amount" id="amount" />
						<p>Monto m&iacute;nimo: ${loan.amount}</p>
					</li>
					<li>
						<label for="months">Meses:</label>
						<input name="months" id="months" />
					</li>
					<li>
						<label for="interest">Interes:</label>
						<input name="interest" id="interest" />
					</li>
					<li>
						<label for="cuota">Cuota:</label>
						<input name="cuota" id="cuota" />
						<a href="#" id="calc" >Calcular</a>
					</li>
					<li>
						<input type="submit" value="Agregar Pr&eacute;stamo" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
