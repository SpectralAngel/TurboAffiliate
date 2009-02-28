<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>Pr&eacute;stamos &bull; A&ntilde;adir</title>
		<script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery.date.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery.cuota.js')}" type="text/javascript"></script>
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
		<h1>Editar un Pr&eacute;stamo</h1>
		<form action="${tg.url('/loan/save')}" method="post">
			<fieldset>
				<legend>Datos del Prest&aacute;mo</legend>
				<input type="hidden" name="id" value="${loan.id}" />
				<ul>
					<li>
						<label for="capital">Monto:</label>
						<input name="capital" id="amount" value="${loan.capital}" />
					</li>
					<li>
						<label for="months">Meses:</label>
						<input name="months" id="months" value="${loan.months}" />
					</li>
					<li>
						<label for="interest">Interes:</label>
						<input name="interest" id="interest" value="${loan.interest}" />
					</li>
					<li>
						<label for="cuota">Cuota:</label>
						<input name="payment" id="payment" value="${loan.payment}" />
						<a href="javascript:void()" id="calc" >Calcular</a>
					</li>
					<li>
						<input type="submit" value="Guardar Cambios" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
