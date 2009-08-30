<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>Pr&eacute;stamos &bull; A&ntilde;adir</title>
		<script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery.cuota.js')}" type="text/javascript"></script>
		<script type="text/javascript">
		$(document).ready(function(e)
		{
			$("#calc").click(get_cuota);
			$('#startDate').datepicker({ dateFormat: 'yy-mm-dd' });
		});
		</script>
	</head>
	<body>
		<h1>Crear un Pr&eacute;stamo</h1>
		<form action="${tg.url('/loan/new')}" method="post">
			<fieldset>
				<legend>Datos del Prest&aacute;mo</legend>
				<ul>
					<li>
						<label for="affiliate">Afiliado:</label>
						<input readonly="readonly" name="affiliate" value="${affiliate.id}" />
						<a href="${tg.url('/affiliate/%s' % affiliate.id)}" py:content="affiliate.firstName, ' ', affiliate.lastName" />
					</li>
					<li>
						<label for="id">Solicitud:</label>
						<input name="id" />
					</li>
					<li>
						<label for="capital">Monto:</label>
						<input name="capital" id="amount" />
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
						<label for="startDate">Fecha de Inicio:</label>
						<input name="startDate" id="startDate" type="text" />
					</li>
					<li>
						<label for="cuota">Cuota:</label>
						<input name="payment" id="payment" />
						<a href="javascript:void()" id="calc" >Calcular</a>
					</li>
					<li>
						<input type="submit" value="Agregar Pr&eacute;stamo" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>

