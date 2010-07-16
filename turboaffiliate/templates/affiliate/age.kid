<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
<head>
  <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''" />
  <title>TurboAffiliate &bull; Afiliados</title>
  <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/status.css')}" media="print" />
  <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print" />
</head>
<body>
  <h1>Reporte de Afiliados</h1>
  <table>
    <thead>
      <tr>
        <th>Carnet</th>
        <th>Nombre</th>
        <th>Ingreso</th>
      </tr>
    </thead>
    <tbody>
      <tr py:for="affiliate in affiliates">
        <td><a href="${tg.url('/affiliate/%s' % affiliate.id)}">${affiliate.id}</a></td>
        <td>${affiliate.firstName} ${affiliate.lastName}</td>
        <td>${affiliate.joined}</td>
        <!-- <td py:content="affiliate.get_age()" /> -->
      </tr>
    </tbody>
  </table>
</body>
</html>
