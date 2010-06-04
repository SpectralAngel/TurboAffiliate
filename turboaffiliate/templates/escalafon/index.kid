<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Volantes y Deducciones</title>
    </head>
    <body>
        <h2>Volantes y Deducciones</h2>
        <form action="${tg.url('postReport')}">
            <fieldset>
                <legend>Ver Reporte de Ingresos</legend>
                <ul>
                    <li>
                        <label for="year">A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li>
                        <label for="month">Mes</label>
                        <input name="month" />
                    </li>
                    <li><input type="submit" value="Mostrar Reporte" /></li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('report')}">
            <fieldset>
                <legend>Ver Reporte de Ingresos Previos</legend>
                <ul>
                    <li>
                        <label for="payment">Cotizaci&oacute;n:</label>
                        <select name="payment">
                            <option>Escalafon</option>
                            <option>INPREMA</option>
                            <option>UPN</option>
                        </select>
                    </li>
                    <li>
                        <label for="year">A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li>
                        <label for="month">Mes</label>
                        <input name="month" />
                    </li>
                    <li><input type="submit" value="Mostrar Reporte" /></li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('extra')}">
            <fieldset>
                <legend>Mostrar Cuentas por Cobrar</legend>
                <ul>
                    <li>
                        <label for="account">Cuenta:</label>
                        <select name="account">
                            <option py:for="account in accounts" value="${account.id}" py:content="account.name" />
                        </select>
                    </li>
                    <li><input type="submit" value="Mostrar Reporte" /></li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('deduced')}">
            <fieldset>
                <legend>Mostrar Cobros Efecutados</legend>
                <ul>
                    <li>
                        <label for="account">Cuenta:</label>
                        <select name="account">
                            <option py:for="account in accounts" value="${account.id}" py:content="account.name" />
                        </select>
                    </li>
                    <li>
                        <label for="month">Mes:</label>
                        <input name="month" />
                    </li>
                    <li>
                        <label for="year">A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li><input type="submit" value="Mostrar Reporte" /></li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('OtherReport')}" method="post">
            <fieldset>
                <legend>Actualizar Otras Cotizaciones - Paso 2</legend>
                <ul>
                    <li>
                        <label for="payment">Cotizaci&oacute;n:</label>
                        <select name="payment">
                            <option>INPREMA</option>
                            <option>UPN</option>
                            <option>Ministerio</option>
                        </select>
                    </li>
                    <li>
                        <label for="year">A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li>
                        <label for="month">Mes</label>
                        <input name="month" />
                    </li>
                    <li><input type="submit" value="Actualizar Reporte" /></li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('showReport')}">
            <fieldset>
                <legend>Mostrar Otros Reportes - Paso 3</legend>
                <ul>
                    <li>
                        <label for="payment">Cotizaci&oacute;n:</label>
                        <select name="payment">
                            <option>INPREMA</option>
                            <option>UPN</option>
                            <option>Ministerio</option>
                        </select>
                    </li>
                    <li>
                        <label for="year">A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li>
                        <label for="month">Mes</label>
                        <input name="month" />
                    </li>
                    <li><input type="submit" value="Mostrar Reporte" /></li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('deduced')}">
            <fieldset>
                <legend>Mostrar Reporte Por Cuenta</legend>
                <ul>
                    <li>
                        <label for="account">Cuenta:</label>
                        <select name="account">
                            <option py:for="account in accounts" value="${account.id}" py:content="account.name" />
                        </select>
                    </li>
                    <li>
                        <label for="month">Mes:</label>
                        <input name="month" />
                    </li>
                    <li>
                        <label for="year">A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li><input type="submit" value="Mostrar Reporte" /></li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('deducedPayment')}">
            <fieldset>
                <legend>Mostrar Reporte Por Cuenta y Cotizaci&oacute;n</legend>
                <ul>
                    <li>
                        <label for="payment">Cotizaci&oacute;n:</label>
                        <select name="payment">
                            <option>INPREMA</option>
                            <option>UPN</option>
                        </select>
                    </li>
                    <li>
                        <label for="account">Cuenta:</label>
                        <select name="account">
                            <option py:for="account in accounts" value="${account.id}" py:content="account.name" />
                        </select>
                    </li>
                    <li>
                        <label for="month">Mes:</label>
                        <input name="month" />
                    </li>
                    <li>
                        <label for="year">A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li>
                        <input type="submit" value="Mostrar Reporte" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('filialesDept')}">
            <fieldset>
                <legend>Mostrar Reporte de Filiales</legend>
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
                        <label for="month">Mes:</label>
                        <input name="month" />
                    </li>
                    <li>
                        <label for="year">A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li>
                        <input type="submit" value="Mostrar Reporte" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('aportaciones')}">
            <fieldset>
                <legend>Mostrar Afiliados que Aportaron</legend>
                <ul>
                    <li>
                        <label for="month">Mes:</label>
                        <input name="month" />
                    </li>
                    <li>
                        <label for="year">A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li>
                        <input type="submit" value="Mostrar Reporte" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="empty">
            <fieldset>
                <legend>Afiliados que cotizaron al menos una vez</legend>
                <ul>
                    <li>
                        <label for="payment">Cotiza por:</label>
                        <select name="payment">
                            <option>Escalafon</option>
                            <option>INPREMA</option>
                            <option>UPN</option>
                            <option>Ventanilla</option>
                        </select>
                    </li>
                    <li>
                        <label>A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li>
                        <input type="submit" value="Buscar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('aportaron')}">
            <fieldset>
                <legend>Mostrar Afiliados que Aportaron</legend>
                <ul>
                    <li>
                        <label for="month">Mes:</label>
                        <input name="month" />
                    </li>
                    <li>
                        <label for="year">A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li><input type="submit" value="Mostrar Reporte" /></li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('noAportaron')}">
            <fieldset>
                <legend>Mostrar Afiliados que no Aportaron</legend>
                <ul>
                    <li>
                        <label for="month">Mes:</label>
                        <input name="month" />
                    </li>
                    <li>
                        <label for="year">A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li><input type="submit" value="Mostrar Reporte" /></li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('conTabla')}">
            <fieldset>
                <legend>Reporte Aseguradora</legend>
                <ul>
                    <li>
                        <label for="month">Mes:</label>
                        <input name="month" />
                    </li>
                    <li>
                        <label for="year">A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li><input type="submit" value="Mostrar Reporte" /></li>
                </ul>
            </fieldset>
        </form>
    </body>
</html>
