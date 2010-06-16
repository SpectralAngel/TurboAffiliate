<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
    locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Pr&eacute;stamos</title>
    </head>
    <body>
        <h1 py:content="'Prestamos Otorgados'" />
        <div py:for="loan in loans">
        <h3>Pr&eacute;stamo N&uacute;mero ${loan.id}</h3>
            <ul>
                <li>
                    <strong>Prestatario:</strong> ${loan.affiliate.firstName} ${loan.affiliate.lastName}
                    ${loan.affiliate.cardID}
                    <a href="${tg.url('/affiliate/%s' % loan.affiliate.id)}">${loan.affiliate.id}</a>
                </li>
                <li>
                    <strong>Monto Original:</strong>${locale.currency(loan.capital, True, True)}
                </li>
                <li>
                    <strong>Saldo Actual:</strong>
                    <span py:content="locale.currency(loan.totaldebt(), True, True)" />
                </li>
                <li>
                    <strong>Fecha de Otorgamiento:</strong>
                    <span py:content="loan.startDate.strftime('%d de %B de %Y')" />
                </li>
            </ul>
        </div>
        <strong>Monto Total:</strong>
        <span py:content="locale.currency(amount, True, True)" />
        <br />
        <strong>Prestamos Otorgados:</strong>
        <span py:content="count" />
    </body>
</html>
