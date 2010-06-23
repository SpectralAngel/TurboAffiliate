<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Obligaciones</title>
    </head>
    <body>
        <div py:for="obligation in obligations">
            <h2>Obligaci&oacute;n N&uacute;mero  ${obligation.id}</h2>
            <ul>
                <li><strong>Mes:</strong> ${obligation.month}</li>
                <li><strong>A&ntilde;o:</strong> ${obligation.year}</li>
                <li><strong>Monto: </strong>${obligation.amount}</li>
                <li><strong>Monto Jubilados: </strong>${obligation.inprema}</li>
                <li><strong>Cuenta: </strong>${obligation.account.name}</li>
                <li><a href="${tg.url('/obligation/remove/%s' % obligation.id')}">Remover</a></li>
            </ul>
        </div>
    </body>
</html>
