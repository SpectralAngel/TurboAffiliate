<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
    <title>TurboAffiliate &bull; Afiliados</title>
    <script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
    <script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
    <script src="${tg.url('/static/javascript/afiliado.js')}" type="text/javascript"></script>
  </head>
  <body>
    <h1>Afiliados</h1>
    <ul>
      <li><a href="${tg.url('all')}">Ver Todos los Afiliados</a></li>
      <li><a href="${tg.url('totalUrnas')}">Total de Urnas</a></li>
    </ul>
    <form action="${tg.url('stateSchool')}">
      <fieldset>
        <legend>Padr&oacute;n Electoral Departamental</legend>
        <ul>
          <li>
            <label for="state">Departamento:</label>
            <select name="state">
              <option>Atlantida</option>
              <option>Choluteca</option>
              <option>Colon</option>
              <option>Comayagua</option>
              <option>Copan</option>
              <option>Cortes</option>
              <option>El Paraiso</option>
              <option>Francisco Morazan</option>
              <option>Gracias a Dios</option>
              <option>Intibuca</option>
              <option>Islas de la Bahia</option>
              <option>La Paz</option>
              <option>Lempira</option>
              <option>Olancho</option>
              <option>Ocotepeque</option>
              <option>Santa Barbara</option>
              <option>Valle</option>
              <option>Yoro</option>
            </select>
          </li>
          <li>
            <input type="submit" value="Ver" />
          </li>
        </ul>
      </fieldset>
    </form>
    <form action="${tg.url('departamento')}">
      <fieldset>
        <legend>Padr&oacute;n Electoral Departamental sin Instituto</legend>
        <ul>
          <li>
            <label for="departamento">Departamento:</label>
            <select name="departamento">
              <option>Atlantida</option>
              <option>Choluteca</option>
              <option>Colon</option>
              <option>Comayagua</option>
              <option>Copan</option>
              <option>Cortes</option>
              <option>El Paraiso</option>
              <option>Francisco Morazan</option>
              <option>Gracias a Dios</option>
              <option>Intibuca</option>
              <option>Islas de la Bahia</option>
              <option>La Paz</option>
              <option>Lempira</option>
              <option>Olancho</option>
              <option>Ocotepeque</option>
              <option>Santa Barbara</option>
              <option>Valle</option>
              <option>Yoro</option>
            </select>
          </li>
          <li>
            <input type="submit" value="Ver" />
          </li>
        </ul>
      </fieldset>
    </form>
    <form action="${tg.url('urnasDepartamentales')}">
      <fieldset>
        <legend>Listado de Instituto para Urnas por Departamento</legend>
        <ul>
          <li>
            <label for="departamento">Departamento:</label>
            <select name="departamento">
              <option>Atlantida</option>
              <option>Choluteca</option>
              <option>Colon</option>
              <option>Comayagua</option>
              <option>Copan</option>
              <option>Cortes</option>
              <option>El Paraiso</option>
              <option>Francisco Morazan</option>
              <option>Gracias a Dios</option>
              <option>Intibuca</option>
              <option>Islas de la Bahia</option>
              <option>La Paz</option>
              <option>Lempira</option>
              <option>Olancho</option>
              <option>Ocotepeque</option>
              <option>Santa Barbara</option>
              <option>Valle</option>
              <option>Yoro</option>
            </select>
          </li>
          <li>
            <input type="submit" value="Ver" />
          </li>
        </ul>
      </fieldset>
    </form>
    <form action="${tg.url('urnasDepartamentalesCinco')}">
      <fieldset>
        <legend>Listado de Instituto con cinco Afiliados o m&aacute;s</legend>
        <ul>
          <li>
            <label for="departamento">Departamento:</label>
            <select name="departamento">
              <option>Atlantida</option>
              <option>Choluteca</option>
              <option>Colon</option>
              <option>Comayagua</option>
              <option>Copan</option>
              <option>Cortes</option>
              <option>El Paraiso</option>
              <option>Francisco Morazan</option>
              <option>Gracias a Dios</option>
              <option>Intibuca</option>
              <option>Islas de la Bahia</option>
              <option>La Paz</option>
              <option>Lempira</option>
              <option>Olancho</option>
              <option>Ocotepeque</option>
              <option>Santa Barbara</option>
              <option>Valle</option>
              <option>Yoro</option>
            </select>
          </li>
          <li>
            <input type="submit" value="Ver" />
          </li>
        </ul>
      </fieldset>
    </form>
    <form action="${tg.url('urnasMunicipio')}">
      <fieldset>
        <legend>Listado de Centros Por Municipio</legend>
        <ul>
          <li>
            <label for="departamento">Departamento:</label>
            <select name="departamento">
              <option>Atlantida</option>
              <option>Choluteca</option>
              <option>Colon</option>
              <option>Comayagua</option>
              <option>Copan</option>
              <option>Cortes</option>
              <option>El Paraiso</option>
              <option>Francisco Morazan</option>
              <option>Gracias a Dios</option>
              <option>Intibuca</option>
              <option>Islas de la Bahia</option>
              <option>La Paz</option>
              <option>Lempira</option>
              <option>Olancho</option>
              <option>Ocotepeque</option>
              <option>Santa Barbara</option>
              <option>Valle</option>
              <option>Yoro</option>
            </select>
          </li>
          <li>
            <input type="submit" value="Ver" />
          </li>
        </ul>
      </fieldset>
    </form>
    <form action="${tg.url('listaUrnasMunicipio')}">
      <fieldset>
        <legend>Listado de Urnas Por Municipio</legend>
        <ul>
          <li>
            <label for="departamento">Departamento:</label>
            <select name="departamento">
              <option>Atlantida</option>
              <option>Choluteca</option>
              <option>Colon</option>
              <option>Comayagua</option>
              <option>Copan</option>
              <option>Cortes</option>
              <option>El Paraiso</option>
              <option>Francisco Morazan</option>
              <option>Gracias a Dios</option>
              <option>Intibuca</option>
              <option>Islas de la Bahia</option>
              <option>La Paz</option>
              <option>Lempira</option>
              <option>Olancho</option>
              <option>Ocotepeque</option>
              <option>Santa Barbara</option>
              <option>Valle</option>
              <option>Yoro</option>
            </select>
          </li>
          <li>
            <input type="submit" value="Ver" />
          </li>
        </ul>
      </fieldset>
    </form>
    <form action="${tg.url('actas')}">
      <fieldset>
        <legend>Actas de Resultado Departamental</legend>
        <ul>
          <li>
            <label for="departamento">Departamento:</label>
            <select name="departamento">
              <option>Atlantida</option>
              <option>Choluteca</option>
              <option>Colon</option>
              <option>Comayagua</option>
              <option>Copan</option>
              <option>Cortes</option>
              <option>El Paraiso</option>
              <option>Francisco Morazan</option>
              <option>Gracias a Dios</option>
              <option>Intibuca</option>
              <option>Islas de la Bahia</option>
              <option>La Paz</option>
              <option>Lempira</option>
              <option>Olancho</option>
              <option>Ocotepeque</option>
              <option>Santa Barbara</option>
              <option>Valle</option>
              <option>Yoro</option>
            </select>
          </li>
          <li>
            <input type="submit" value="Ver" />
          </li>
        </ul>
      </fieldset>
    </form>
    <form action="${tg.url('cotizacion')}">
      <fieldset>
        <legend>Padr&oacute;n Electoral por Cotizaci&oacute;n</legend>
        <ul>
          <li>
            <label for="cotizacion">Cotiza por:</label>
            <select name="cotizacion">
              <option>Escalafon</option>
              <option>INPREMA</option>
              <option>UPN</option>
              <option>Ventanilla</option>
              <option>Ministerio</option>
              <option>Retirado</option>
            </select>
          </li>
          <li>
            <input type="submit" value="Buscar" />
          </li>
        </ul>
      </fieldset>
    </form>
  </body>
</html>

