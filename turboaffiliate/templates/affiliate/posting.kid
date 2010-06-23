<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Afiliados</title>
        <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print"/>
        <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/style.css')}" media="screen"/>
        <style type="text/css">
            h1
            {
                text-align: center;
            }
        </style>
    </head>
    <body>
        <h3>COPEMH</h3>
        <h1>Afiliados que Cotizan por ${how}</h1>
        <table width="100%">
            <thead>
                <tr>
                    <th>Carnet</th>
                    <th>Apellido</th>
                    <th>Nombre</th>
                    <th>Aportaci&oacute;n</th>
                    <th>Deducciones</th>
                    <th>Prestamos</th>
                    <th>Total</th>
                    <th>Posteo Autom&aacute;tico</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="affiliate in affiliates">
                    <td><a href="${tg.url('/affiliate/%s' % affiliate.id)}">${affiliate.id}</a></td>
                    <td py:content="affiliate.lastName" />
                    <td py:content="affiliate.firstName" />
                    <td py:content="obligation" />
                    <td>
                        <ul>
                            <li py:for="extra in affiliate.extras">
                                <span py:content="extra.account.name" />
                                <span py:content="locale.currency(extra.amount, True, True)" />
                            </li>
                        </ul>
                    </td>
                    <td>
                        <ul>
                            <li py:for="loan in affiliate.loans">
                                <span py:content="locale.currency(loan.get_payment(), True, True)" />
                            </li>
                        </ul>
                    </td>
                    <td py:content="locale.currency(sum(loan.get_payment() for loan in affiliate.loans) + sum(extra.amount for extra in affiliate.extras) + obligation, True, True)" />
                    <td><a href="${tg.url('/affiliate/transfer?affiliate=%s&amp;obligation=%s' % (affiliate.id, obligation))}">X</a></td>
                </tr>
            </tbody>
        </table>
        <strong>Total de Afiliados: </strong><span py:content="count"/>
    </body>
</html>

