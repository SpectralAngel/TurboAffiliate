<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Compa&ntilde;&iacute;as</title>
		<script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
		<script type="text/javascript">
		<![CDATA[
		$(document).ready(function(e)
		{
			$('input.date-picker').datepicker({ dateFormat: 'yy-mm-dd' });
		});
		]]>
		</script>
	</head>
	<body>
		<form action="${tg.url('/logger/day')}">
			<fieldset>
				<legend>Mostrar Logs</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="start" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="end" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
