<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
  import locale
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
    <title>TurboAffiliate &bull; Afiliados</title>
    <style type="text/css">
      h1
      {
        text-align: center;
      }
    </style>
    <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print" />
  </head>
  <body>
    <h3>COPEMH</h3>
    <h1>Padr&oacute;n Electoral ${departamento}</h1>
    <table width="100%">
      <thead>
        <tr>
          <th>Carnet</th>
          <th>Apellido</th>
          <th>Nombre</th>
          <th>Identidad</th>
        </tr>
      </thead>
      <tbody>
        <tr py:for="afiliado in afiliados">
          <td><a href="${tg.url('/affiliate/%s') % afiliado.id}" py:content="afiliado.id" /></td>
          <td>${afiliado.lastName}</td>
          <td>${afiliado.firstName}</td>
          <td>${afiliado.cardID}</td>
        </tr>
      </tbody>
    </table>
    <strong>Total de Afiliados: </strong>${cantidad}
  </body>
</html>
