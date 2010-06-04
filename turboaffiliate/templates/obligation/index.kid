<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Obligaciones</title>
    </head>
    <body>
        <h1>Obligaciones</h1>
        <form action="${tg.url('/obligation/save')" method="post">
            <fieldset>
                <legend>A&ntilde;adir</legend>
                <ul>
                    <li>
                        <label for="month">Mes:</label>
                        <input name="month" />
                    </li>
                    <li>
                        <label for="year">A&ntilde;o:</label>
                        <input name= "year" />
                    </li>
                    <li>
                        <label for="name">Descripci&oacute;n:</label>
                        <input name="name" />
                    </li>
                    <li>
                        <label for="amount">Monto:</label>
                        <input name="amount" />
                    </li>
                    <li>
                        <label for="inprema">INPREMA:</label>
                        <input name="inprema" />
                    </li>
                    <li>
                        <label for="filiales">Filiales:</label>
                        <input name="filiales" />
                    </li>
                    <li>
                        <label for="account">Cuenta:</label>
                        <select name="account">
                            <option py:for="account in accounts" py:content="account.code, ' - ', account.name" value="${account.id}" />
                        </select>
                    </li>
                    <li><input type="submit" value="Guardar" /></li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('/obligation/view')}" method="post">
            <fieldset>
                <legend>Ver Obligaciones</legend>
                <ul>
                    <li>
                        <label for="year">A&ntilde;o</label>
                        <input name="year" />
                    </li>
                    <li><input type="submit" value="Buscar" /></li>
                </ul>
            </fieldset>
        </form>
    </body>
</html>
