<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''" />
        <title>TurboAffiliate &bull; Afiliados</title>
        <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/solvencia.css')}" />
    </head>
    <body>
        <h1>Constancia de Solvencia</h1>
        <p>El Suscrito Presidente del Colegio de Profesores de Educaci&oacute;n
        Media de Honduras <span class="enfasis">COPEMH</span>, por este medio
        <span class="enfasis">HACE CONSTAR QUE: <span class="subrayado">
        ${afiliado.firstName} ${afiliado.lastName} con n&uacute;mero de
        afiliaci&oacute;n ${afiliado.id} SE ENCUENTRA SOLVENTE EN APORTACIONES
        HASTA EL MES DE ${mes.upper()} DE ${anio}</span></span>.</p>
        <p>Y para los fines legales se extiende la constancia el d&iacute;a 
        ${dia.strftime('%A, %d de %B de %Y')}.</p>
        <br />
        <br />
        <div class="firma enfasis">PROF. JAIME RODRIGUEZ</div>
        <div class="firma enfasis">PRESIDENTE</div>
        <div class="firma enfasis">COPEMH</div>
    </body>
</html>
