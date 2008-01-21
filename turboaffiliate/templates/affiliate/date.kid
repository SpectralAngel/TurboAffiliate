<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Afiliados</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print"/>
	</head>
	<body>
		<h3>COPEMH</h3>
		<h1>Afiliados entre <span py:content="start" /> y <span py:content="end" /></h1>
		<p>Al: </p>
		<table width="100%">
			<thead>
				<tr>
					<th>Carnet</th>
					<th>Nombre</th>
					<th>Fecha de Afiliaci&oacute;n</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="affiliate in affiliates">
					<td py:content="affiliate.escalafon" />
					<td py:content="affiliate.lastName, ' ', affiliate.firstName" />
					<td py:content="affiliate.joined" />
				</tr>
			</tbody>
		</table>
		<strong>Total de Afiliados: </strong><span py:content="count"/>
	</body>
</html>

