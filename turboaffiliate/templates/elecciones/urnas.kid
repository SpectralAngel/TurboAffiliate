<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
  import locale
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
    <title>TurboAffiliate &bull; ${departamento}</title>
    <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/form.css')}" media="screen" />
    <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print" />
    <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/billing.css')}" />
  </head>
  <body>
    <a href="javascript:print()">Imprimir</a>
    <h1>Listado de Urnas</h1>
    <table style="width: 100%">
      <caption py:content="departamento" />
      <thead>
        <tr>
          <th>Instituto</th>
          <th>Cantidad de Afiliados</th>
        </tr>
      </thead>
      <tbody>
        <tr py:for="instituto in urnas">
          <td py:content="instituto" />
          <td py:content="urnas[instituto]" />
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <th>Total de Afiliados</th>
          <th py:content="cantidad" />
        </tr>
        <tr>
          <th>Total de Centros</th>
          <th py:content="len(urnas)" />
        </tr>
      </tfoot>
    </table>
  </body>
</html>

