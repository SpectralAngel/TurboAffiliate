<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import sitetemplate
    from datetime import date
    from turboaffiliate import model
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
<head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
  <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
  <title py:replace="''">Your title goes here</title>
  <meta py:replace="item[:]"/><script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
  <script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
  <script src="${tg.url('/static/javascript/common.js')}" type="text/javascript"></script>
  <script src="${tg.url('/static/javascript/calculadora.js')}" type="text/javascript"></script>
  <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/ui-lightness/jquery-ui.css')}" media="screen" />
  <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/menu.css')}" media="screen" />
  <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/tabla.css')}" media="screen" />
  <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/style.css')}" media="screen" />
  <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/form.css')}" media="screen" />
  <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/navegacion.css')}" media="screen" />
</head>
<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">
  <div id="navegacion">
    <ul id="menu">
      <li><a href="${tg.url('/')}">Inicio</a></li>
      <li><a href="${tg.url('/affiliate')}">Afiliados</a></li>
      <li><a href="${tg.url('/affiliate/add')}">Agregar Afiliado</a></li>
      <li><a href="${tg.url('/loan')}">Pr&eacute;stamos</a></li>
      <li><a href="${tg.url('/reintegro')}">Reintegros</a></li>
      <li><a href="${tg.url('/obligation')}">Obligaciones</a></li>
      <li><a href="${tg.url('/report')}">Reportes</a></li>
      <li><a href="${tg.url('/billing')}">Estados de Cuenta</a></li>
    </ul>
  </div>
  <div id="espaciador">
  </div>
  <div class="left-border">
    <div py:if="tg_flash" class="ui-widget">
      <div class="ui-state-highlight ui-corner-all flash" style="padding: 0.5em;">
        <span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span> 
        <strong>${tg_flash}</strong>
      </div>
    </div>
    <span class="ui-helper-clearfix" />
    <div py:replace="[item.text]+item[:]"/>
    <span class="ui-helper-clearfix" />
    <div id="pie">Copyright &copy; COPEMH 2007 - 2010</div>
  </div>
  <div id="utilerias">
    <button onclick="javascript:$('.calculadora').dialog('open');">Calculadora de Pr&eacute;stamos</button>
  </div>
  <form class="calculadora">
    <div>
      <ul>
        <li>
          <label>Capital:</label>
          <input id="capitalc" />
        </li>
        <li>
          <label>Meses:</label>
          <input id="tiempoc" />
        </li>
        <li>
          <label>Inter&eacute;s</label>
          <input id="interesc" />
        </li>
        <li>
          <label>Pago Mensual</label>
          <input id="cuotac" />
        </li>
      </ul>
    </div>
  </form>
</body>
</html>
