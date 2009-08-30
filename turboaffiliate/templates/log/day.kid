<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Compa&ntilde;&iacute;as</title>
		<script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
		
	</head>
	<body>
		<h1>Logs del ${start.strftime('%d/%m/%y')} al ${end.strftime('%d/%m/%y')}</h1>
		<table>
			<thead>
				<tr>
					<th>Fecha</th>
					<th>Acci&oacute;n</th>
					<th>Usuario</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="log in logs">				
					<td py:content="log.day" />
					<td py:content="log.action" />
					<td py:content="log.user.display_name" />
				</tr>
			</tbody>
		</table>
	</body>
</html>
