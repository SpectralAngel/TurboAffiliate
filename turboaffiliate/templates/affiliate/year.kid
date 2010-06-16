<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
    locale.setlocale(locale.LC_ALL, """)
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
        <h1>Afiliados Solventes por A&ntilde;o</h1>
        <table width="100%">
            <thead>
                <tr>
                    <th>A&ntilde;0</th>
                    <th>Afiliados</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="year in years.keys()">
                    <td>${year}</td>
                    <td>${years[year]}</td>
                </tr>
            </tbody>
        </table>
    </body>
</html>
