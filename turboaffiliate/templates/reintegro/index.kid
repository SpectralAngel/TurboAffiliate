<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Compa&ntilde;&iacute;as</title>
        <script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/reintegro.js')}" type="text/javascript"></script>
    </head>
    <body>
        <a href="${tg.url('/reintegro/cobros')}">Mostrar Reintegros por Efectuar</a>
        <form action="${tg.url('/reintegro/emision')}">
            <fieldset>
                <legend>Mostrar Reintegros por Fecha de Emisi&oacute;n</legend>
                <ul>
                    <li>
                        <label>Inicio:</label>
                        <input name="inicio" class="datepicker" />
                    </li>
                    <li>
                        <label>Final:</label>
                        <input name="fin" class="datepicker" />
                    </li>
                    <li>
                        <input type="submit" value="Mostrar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('/reintegro/pagados')}">
            <fieldset>
                <legend>Mostrar Reintegros Pagados en un periodo</legend>
                <ul>
                    <li>
                        <label>Inicio:</label>
                        <input name="inicio" class="datepicker" />
                    </li>
                    <li>
                        <label>Final:</label>
                        <input name="fin" class="datepicker" />
                    </li>
                    <li>
                        <input type="submit" value="Mostrar" />
                    </li>
                </ul>
            </fieldset>
        </form>
    </body>
</html>
