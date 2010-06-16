<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" 
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../../master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Pagar Cuota</title>
        <script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/afiliado.js')}" type="text/javascript"></script>
    </head>
    <body>
        <h2>Pago de Cuota</h2>
        <form action="${tg.url('/affiliate/cuota/save')}" method="get">
            <fieldset>
                <input type="hidden" name="affiliate" value="${affiliate.id}" />
                <legend>Cuota</legend>
                <ul>
                    <li>
                        <label for="amount">Monto:</label>
                        <input name="amount" />
                    </li>
                    <li>
                        <label for="day">Fecha:</label>
                        <input name="day" class="date-picker" />
                    </li>
                    <li>
                        <label for="how">Tipo de Pago</label>
                        <select name="how">
                            <option value="1">M&aacute;s de un mes</option>
                            <option value="2" selected="selected">S&oacute;lo un mes</option>
                        </select>
                    </li>
                    <li>
                        <input type="submit" value="Grabar" />
                    </li>
                </ul>
            </fieldset>
        </form>
    </body>
</html>
