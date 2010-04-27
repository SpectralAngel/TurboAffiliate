<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Afiliados</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/status.css')}" />
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" />
	</head>
	<body>
		<h1>Solicitudes para ${dia}</h1>
		<table>
            <caption>Solicitudes de Pr&eacute;stamo</caption>
            <thead>
                <tr>
                    <th>Afiliacion</th>
                    <th>Nombre</th>
                    <th>Monto</th>
                    <th>Periodo</th>
                    <th>Recibido</th>
                    <th>Entrega</th>
                    <th>Liquidar</th>
                    <th>Eliminar</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="solicitud in solicitudes">
                    <td><a class="show" href="${tg.url('/affiliate/%s' % solicitud.affiliate.id)}">${solicitud.affiliate.id}</a> </td>
                    <td>${solicitud.affiliate.firstName} ${solicitud.affiliate.lastName}</td>
                    <td>${locale.currency(solicitud.monto, True, True)}</td>
                    <td>${solicitud.periodo}</td>
                    <td>${solicitud.ingreso.strftime('%d de %B de %Y')}</td>
                    <td>${solicitud.entrega.strftime('%d de %B de %Y')}</td>
                    <td><a class="show" href="${tg.url('/solicitud/convertir/%s' % solicitud.id)}">Liquidar</a></td>
                    <td><a class="show" href="${tg.url('/solicitud/eliminar/%s' % solicitud.id)}">Eliminar</a></td>
                </tr>
            </tbody>
        </table>
	</body>
</html>
