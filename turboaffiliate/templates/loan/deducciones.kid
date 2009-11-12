<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Pr&acute;stamos</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print" />
	</head>
	<body>
		<h1>Reporte de Deducciones de Pr&eacute;stamos</h1>
		<strong py:content="'del ', start.strftime('%d de %B de %Y')" />
		<strong py:content="'Al ', end.strftime('%d de %B de %Y')" />
		<table width="100%">
			<thead>
				<tr>
					<th>Pr&eacute;stamo</th>
					<th>Nombre</th>
					<th>Monto</th>
					<th>Intereses</th>
					<th>Papeleo</th>
					<th>Aportaciones</th>
					<th>Prestamo</th>
					<th>Neto</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="loan in loans">
					<td py:content="loan.id" />
					<td><a href="${tg.url('/affiliate/%s' % loan.afiliado.id)}" py:content="loan.afiliado.firstName, ' ', loan.afiliado.lastName" /></td>
					<td py:content="locale.currency(loan.monto, True, True)" />
					<td py:content="locale.currency(loan.intereses, True, True)" />
					<td py:content="locale.currency(loan.papeleo, True, True)" />
					<td py:content="locale.currency(loan.aportaciones, True, True)" />
					<td py:content="locale.currency(loan.retencion, True, True)" />
					<td py:content="locale.currency(loan.neto, True, True)" />
				</tr>
			</tbody>
			<tfoot>
				<tr>
					<th colspan="2">Total:</th>
					<th py:content="locale.currency(monto, True, True)" />
					<th py:content="locale.currency(intereses, True, True)" />
					<th py:content="locale.currency(papeleo, True, True)" />
					<th py:content="locale.currency(aportaciones, True, True)" />
					<th py:content="locale.currency(retencion, True, True)" />
					<th py:content="locale.currency(neto, True, True)" />
				</tr>
			</tfoot>
		</table>
	</body>
</html>