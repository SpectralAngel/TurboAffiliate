<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Afiliados</title>
        <script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/prestamo.js')}" type="text/javascript"></script>
        <script type="text/javascript">
        <![CDATA[
        $(document).ready(function(e)
        {
            $('input.date-picker').datepicker({
                dateFormat: 'yy-mm-dd',
                changeMonth: true,
                changeYear: true,
                yearRange: '1940:2010'
            });
        });
        function showpay()
        {
        if(
            (document.calc.loan.value == null || document.calc.loan.value.length == 0) ||
            (document.calc.months.value == null || document.calc.months.value.length == 0) ||
            (document.calc.rate.value == null || document.calc.rate.value.length == 0))
        {
            document.calc.pay.value = "Incomplete data";
        }
        else
        {
            var princ = document.calc.loan.value;
            var term = document.calc.months.value;
            var intr = document.calc.rate.value / 1200;
            document.calc.pay.value = princ * intr / (1 - (Math.pow(1/(1 + intr), term)));
        }
        // payment = principle * monthly interest/(1 - (1/(1+MonthlyInterest)*Months))
        }
        ]]>
        </script>
    </head>
    <body>
        <h1>Pr&eacute;stamos</h1>
        <a href="dobles">Ver Afiliados con multiples pr&eacute;stamos</a>
        <form name="calc" method="post">
            <table>
                <caption>Calculadora de Pr&eacute;stamos</caption>
                <tr>
                    <th width="50%">Descripci&oacute;n</th>
                    <th width="50%">Entrada de Datos</th>
                </tr>
                <tr>
                    <td>Capital:</td>
                    <td><input  name="loan" size="10" /></td>
                </tr>
                <tr>
                    <td>Meses:</td>
                    <td><input name="months" size="10" /></td>
                </tr>
                <tr>
                    <td>Tasa de Inter&eacute;s</td>
                    <td ><input name="rate" size="10" /></td>
                </tr>
                <tr>
                    <td>Pago Mensual</td>
                    <td><em>Calculado</em><input name="pay" size="10" /></td>
                </tr>
                <tr>
                    <td align="center"><input type="button" onClick="javascript:showpay()" value="Calcular" /></td>
                    <td align="center"><input type="reset" value="Reiniciar" /></td>
                </tr>
            </table>
        </form>
        <form action="search" method="post">
            <fieldset>
                <legend>Buscar Pr&eacute;stamo</legend>
                <ul>
                    <li>
                        <label>N&uacute;mero de Pr&eacute;stamo</label>
                        <input name="loan" />
                    </li>
                    <li>
                        <input type="submit" value="Buscar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('/solicitud/dia')}">
            <fieldset>
                <legend>Solicitudes para una Fecha</legend>
                <ol>
                    <li>
                        <label>D&iacute;a</label>
                        <input name="dia" class="datepicker" />
                    </li>
                    <li>
                        <input type="submit" value="Mostrar" />
                    </li>
                </ol>
            </fieldset>
        </form>
        <form action="/payed">
            <fieldset>
                <legend>Ver Pr&eacute;stamo Pagado</legend>
                <ul>
                    <li>
                        <label>Solicitud:</label>
                        <input name="id" />
                    </li>
                    <li>
                        <input type="submit" value="Buscar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="period">
            <fieldset>
                <legend>Mostrar Pr&eacute;stamos de un Periodo</legend>
                <ul>
                    <li>
                        <label>Inicio:</label>
                        <input name="first" class="date-picker" />
                    </li>
                    <li>
                        <label>Final:</label>
                        <input name="last" class="date-picker" />
                    </li>
                    <li>
                        <input type="submit" value="Buscar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="cotizacion">
            <fieldset>
                <legend>Pr&eacute;stamos Otorgados por Periodo y Cotizacion</legend>
                <ul>
                    <li>
                        <label>Inicio:</label>
                        <input name="start" class="date-picker" />
                    </li>
                    <li>
                        <label>Final:</label>
                        <input name="end" class="date-picker" />
                    </li>
                    <li>
                        <label for="payment">Cotiza por:</label>
                        <select name="payment">
                            <option>Escalafon</option>
                            <option>INPREMA</option>
                            <option>UPN</option>
                            <option>Ministerio</option>
                            <option>Retirado</option>
                        </select>
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="/payed/payment">
            <fieldset>
                <legend>Pr&eacute;stamos por Periodo y Cotizacion - Pagados </legend>
                <ul>
                    <li>
                        <label>Inicio:</label>
                        <input name="start" class="date-picker" />
                    </li>
                    <li>
                        <label>Final:</label>
                        <input name="end" class="date-picker" />
                    </li>
                    <li>
                        <label for="payment">Cotiza por:</label>
                        <select name="payment">
                            <option>Escalafon</option>
                            <option>INPREMA</option>
                            <option>UPN</option>
                            <option>Ministerio</option>
                            <option>Retirado</option>
                        </select>
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="/payed/period">
            <fieldset>
                <legend>Pr&eacute;stamos por Periodo - Pagados</legend>
                <ul>
                    <li>
                        <label>Inicio:</label>
                        <input name="start" class="date-picker" />
                    </li>
                    <li>
                        <label>Final:</label>
                        <input name="end" class="date-picker" />
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="add">
            <fieldset>
                <legend>A&ntilde;adir Pr&eacute;stamo a Afiliado</legend>
                <ul>
                    <li>
                        <label>Carnet:</label>
                        <input name="affiliate" />
                    </li>
                    <li>
                        <input type="submit" value="Buscar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="day">
            <fieldset>
                <legend>Mostrar Pr&eacute;stamos de un D&iacute;a</legend>
                <ul>
                    <li>
                        <label>D&iacute;a:</label>
                        <input name="day" class="date-picker" />
                    </li>
                    <li>
                        <input type="submit" value="Buscar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="cartera">
            <fieldset>
                <legend>Mostrar Cartera Pr&eacute;stamos</legend>
                <ul>
                    <li>
                        <label>Inicio:</label>
                        <input name="first" class="date-picker" />
                    </li>
                    <li>
                        <label>Final:</label>
                        <input name="last" class="date-picker" />
                    </li>
                    <li>
                        <input type="submit" value="Buscar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="monthly">
            <fieldset>
                <legend>Reporte de Pr&eacute;stamos Otorgados</legend>
                <ul>
                    <li>
                        <label>Inicio:</label>
                        <input name="start" class="date-picker" />
                    </li>
                    <li>
                        <label>Final:</label>
                        <input name="end" class="date-picker" />
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="bypayment">
            <fieldset>
                <legend>Pr&eacute;stamos por Tipo de Cotizaci&oacute;n</legend>
                <ul>
                    <li>
                        <label for="payment">Cotiza por:</label>
                        <select name="payment">
                            <option>Escalafon</option>
                            <option>INPREMA</option>
                            <option>UPN</option>
                            <option>Ministerio</option>
                            <option>Retirado</option>
                        </select>
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="paymentDate">
            <fieldset>
                <legend>Pr&eacute;stamos por Tipo de Cotizaci&oacute;n y Fecha</legend>
                <ul>
                    <li>
                        <label for="payment">Cotiza por:</label>
                        <select name="payment">
                            <option>Escalafon</option>
                            <option>INPREMA</option>
                            <option>UPN</option>
                            <option>Ministerio</option>
                            <option>Retirado</option>
                        </select>
                    </li>
                    <li>
                        <label>Inicio:</label>
                        <input name="start" class="date-picker" />
                    </li>
                    <li>
                        <label>Final:</label>
                        <input name="end" class="date-picker" />
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="liquid">
            <fieldset>
                <legend>Reporte de Liquidaci&oacute;n de Pr&eacute;stamos</legend>
                <ul>
                    <li>
                        <label>Inicio:</label>
                        <input name="start" class="date-picker" />
                    </li>
                    <li>
                        <label>Final:</label>
                        <input name="end" class="date-picker" />
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="byCapital">
            <fieldset>
                <legend>Reporte de Capital e Intereses</legend>
                <ul>
                    <li>
                        <label>D&iacute;a:</label>
                        <input name="day" class="date-picker" />
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="resume">
            <fieldset>
                <legend>Resumen de Capital e Intereses por Periodo</legend>
                <ul>
                    <li>
                        <label>Inicio:</label>
                        <input name="start" class="date-picker" />
                    </li>
                    <li>
                        <label>Final:</label>
                        <input name="end" class="date-picker" />
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="pay/resume">
            <fieldset>
                <legend>Detalle de Pagos por Periodo</legend>
                <ul>
                    <li>
                        <label>Inicio:</label>
                        <input name="start" class="date-picker" />
                    </li>
                    <li>
                        <label>Final:</label>
                        <input name="end" class="date-picker" />
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="diverge">
            <fieldset>
                <legend>Divergencia de Pr&eacute;stamos</legend>
                <ul>
                    <li>
                        <label for="payment">Cotiza por:</label>
                        <select name="payment">
                            <option>Escalafon</option>
                            <option>INPREMA</option>
                            <option>UPN</option>
                            <option>Ministerio</option>
                            <option>Retirado</option>
                        </select>
                    </li>
                    <li>
                        <label>Inicio:</label>
                        <input name="start" />
                    </li>
                    <li>
                        <label>Final:</label>
                        <input name="end" />
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="cotizacionDepto">
            <fieldset>
                <legend>Pr&eacute;stamos por Tipo de Cotizaci&oacute;n y Departamento</legend>
                <ul>
                    <li>
                        <label for="cotizacion">Cotiza por:</label>
                        <select name="cotizacion">
                            <option>Escalafon</option>
                            <option>INPREMA</option>
                            <option>UPN</option>
                            <option>Ministerio</option>
                            <option>Retirado</option>
                        </select>
                    </li>
                    <li>
                        <label for="depto">Departamento:</label>
                        <select name="depto">
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
                        <input type="submit" value="Mostrar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="deducciones">
            <fieldset>
                <legend>Reporte de Deducciones de Pr&eacute;stamos</legend>
                <ul>
                    <li>
                        <label>Inicio:</label>
                        <input name="start" class="date-picker" />
                    </li>
                    <li>
                        <label>Final:</label>
                        <input name="end" class="date-picker" />
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="deduccionesDia">
            <fieldset>
                <legend>Reporte de Deducciones de Pr&eacute;stamos Diarios</legend>
                <ul>
                    <li>
                        <label>Inicio:</label>
                        <input name="start" class="date-picker" />
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
    </body>
</html>
