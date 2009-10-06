<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; ${departamento}</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/form.css')}" media="screen" />

		 <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" />

		 <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/billing.css')}" />
	</head>
	<body>
		<a href="javascript:print()">Imprimir</a>
		<h1>Listado de Urnas <span py:content="departamento" /></h1>
		<div py:for="municipio in urnas">
			<h2 py:content="municipio" />
			<table py:for="instituto in urnas[municipio]" style="width: 100%" class="page">
				<caption py:content="instituto, ' Municipio de ', municipio" />
				<thead>
					<tr>
						<th class="numero">N&uacute;mero</th>
						<th class="nombre">Nombre</th>
						<th class="nombre">Apellido</th>
						<th>Firma</th>
					</tr>
				</thead>
				<tbody>
					<tr py:for="afiliado in urnas[municipio][instituto]">
						<td class="numero" py:content="afiliado.id" />
						<td class="nombre" py:content="afiliado.firstName" />
						<td class="nombre" py:content="afiliado.lastName" />
						<td></td>
					</tr>
				</tbody>
				<tfoot>
					<tr>
						<th colspan="3">Total de Afiliados</th>
						<th py:content="len(urnas[municipio][instituto])" />
					</tr>
				</tfoot>
			</table>
		</div>
	</body>
</html>

