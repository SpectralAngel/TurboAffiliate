<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Pr&eacute;stamos</title>
	</head>
	<body>
		<h1>Reporte de Pr&eacute;stamos Otorgados entre ${start.strftime('%d de %B de %Y')}
        y ${end.strftime('%d de %B de %Y')}</h1>
		<table>
			<thead>
				<tr>
					<th>Mes</th>
					<th>Cantidad</th>
					<th>Capital</th>
                    <th>Neto</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="month in months">
					<td>${month['month']}</td>
					<td>${month['number']}</td>
					<td>${locale.currency(month['amount'], True, True)}</td>
                    <td>${locale.currency(month['net'], True, True)}</td>
				</tr>
			</tbody>
			<tfoot>
				<tr>
					<th colspan="2">Total:</th>
					<th>${locale.currency(total, True, True)}</th>
                    <th>${locale.currency(total, True, True)}</th>
				</tr>
			</tfoot>
		</table>
	</body>
</html>
