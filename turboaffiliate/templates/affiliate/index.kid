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
            <li><a href="${tg.url('add')}">A&ntilde;adir un Afiliado</a></li>
            <li><a href="${tg.url('last')">Ver el Ultimo Afiliado</a></li>
            <li><a href="${tg.url('extra')">A&ntilde;adir Deducciones Extra a Varios Afiliados</a></li>
            <li><a href="${tg.url('disabled')">Ver Afiliados Inactivos</a></li>
            <li><a href="${tg.url('all')">Ver Todos los Afiliados</a></li>
            <li><a href="${tg.url('solventYear')">Ver Solventes por A&ntilde;o</a></li>
            <li><a href="${tg.url('none')">Ver Afiliados sin a&ntilde;o de Afiliaci&oacute;n</a></li>
            <li><a href="${tg.url('noCard')">Ver Afiliados sin n&uacute;mero de Identidad</a></li>
        </ul>
        <form action="${tg.url('/affiliate/byCopemh')}">
            <fieldset>
                <legend>Buscar Afiliado</legend>
                <ul>
                    <li>
                        <label>Carnet:</label>
                        <input name="copemh" />
                    </li>
                    <li>
                        <input type="submit" value="Buscar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('search')}">
            <fieldset>
                <legend>Buscar Affiliado</legend>
                <ul>
                    <li>
                        <label>Nombre o Apellido:</label>
                        <input name="name" />
                    </li>
                    <li>
                        <input type="submit" value="Buscar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('card')}">
            <fieldset>
                <legend>Buscar Afiliado</legend>
                <ul>
                    <li>
                        <label>Identidad:</label>
                        <input name="cardID" />
                    </li>
                    <li>
                        <input type="submit" value="Buscar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('cobro')}">
            <fieldset>
                <legend>Buscar Afiliado Por N&uacute;mero de Cobro</legend>
                <ul>
                    <li>
                        <label>Cobro INPREMA:</label>
                        <input name="cobro" />
                    </li>
                    <li>
                        <input type="submit" value="Buscar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="byRange">
            <fieldset>
                <legend>Buscar Afiliados por C&oacute;digo de Departamento</legend>
                <ul>
                    <li>
                        <label>Identificador:</label>
                        <input name="code" />
                    </li>
                    <li>
                        <input type="submit" value="Buscar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('department')}">
            <fieldset>
                <legend>Reporte por Departamento</legend>
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
                        <input type="submit" value="Buscar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('cotization')}">
            <fieldset>
                <legend>Ver Deducci&oacute;n por Cotizaci&oacute;n</legend>
                <ul>
                    <li>
                        <label for="how">Cotiza por:</label>
                        <select name="how">
                            <option>Escalafon</option>
                            <option>INPREMA</option>
                            <option>UPN</option>
                            <option>Ventanilla</option>
                            <option>Ministerio</option>
                            <option>Retirado</option>
                        </select>
                    </li>
                    <li>
                        <label>A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li>
                        <label>Mes:</label>
                        <input name="month" />
                    </li>
                    <li>
                        <input type="submit" value="Buscar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('payment')}">
            <fieldset>
                <legend>Ver Afiliados por Cotizaci&oacute;n</legend>
                <ul>
                    <li>
                        <label for="how">Cotiza por:</label>
                        <select name="how">
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
        <form action="${tg.url('age')}">
            <fieldset>
                <legend>Ver Afiliados por Edad</legend>
                <ul>
                    <li>
                        <label for="how">Edad:</label>
                        <input name="age" />
                    </li>
                    <li>
                        <label>A&ntilde;o M&aacute;ximo de Afiliaci&oacute;n:</label>
                        <input name="joined" />
                    </li>
                    <li>
                        <input type="submit" value="Buscar" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('byDate')}">
            <fieldset>
                <legend>Mostrar seg&uacute;n fecha de afiliaci&oacute;n</legend>
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
        <form action="${tg.url('byTown')}">
            <fieldset>
                <legend>Mostrar por Municipio</legend>
                <ul>
                    <li>
                        <label>Municipio:</label>
                        <input name="town" />
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('bySchool')}">
            <fieldset>
                <legend>Mostrar por Instituto</legend>
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
                        <label>Instituto:</label>
                        <input name="school" />
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('manual')}">
            <fieldset>
                <legend>Posteo Manual de Afiliados, INPREMA, UPN</legend>
                <ul>
                    <li>
                        <label>Carnet:</label>
                        <input name="affiliate" />
                    </li>
                    <li>
                        <label>A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li>
                        <label>Mes:</label>
                        <input name="month" />
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('listmanual')}">
            <fieldset>
                <legend>Listado para Posteo Manual de Afiliados, INPREMA, UPN - Paso 1</legend>
                <ul>
                    <li>
                        <label for="payment">Cotiza por:</label>
                        <select name="payment">
                            <option>INPREMA</option>
                            <option>UPN</option>
                            <option>Ministerio</option>
                        </select>
                    </li>
                    <li>
                        <label>A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li>
                        <label>Mes:</label>
                        <input name="month" />
                    </li>
                    <li>
                        <label>D&iacute;a de Posteo:</label>
                        <input name="day" class="date-picker" />
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
        <form action="${tg.url('stateSchool')}">
            <fieldset>
                <legend>Mostrar por Instituto</legend>
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
        <form action="${tg.url('solvent')}">
            <fieldset>
                <legend>Afiliados Solventes por A&ntilde;o</legend>
                <ul>
                    <li>
                        <label>A&ntilde;o:</label>
                        <input name="year" />
                    </li>
                    <li>
                        <input type="submit" value="Ver" />
                    </li>
                </ul>
            </fieldset>
        </form>
    </body>
</html>
