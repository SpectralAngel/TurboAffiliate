<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
<head>
  <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
  <title>TurboAffiliate &bull; B&uacute;squeda de Afiliados</title>
</head>
<body>
  <table class="striped">
    <caption>Resultados de la busqueda</caption>
    <thead>
      <tr>
        <th>Carnet</th>
        <th>Nombre</th>
        <th>Identidad</th>
        <th>Cotizaci&oacute;n</th>
      </tr>
    </thead>
    <tbody>
      <tr py:for="afiliado in result">
        <td><a href="${tg.url('/affiliate/%s' % afiliado.id)}"></a></td>
        <td>${afiliado.firstName} ${afiliado.lastName}</td>
        <td>${afiliado.cardID}</td>
        <td>${afiliado.payment}</td>
      </tr>
    </tbody>
  </table>
</body>
</html>
