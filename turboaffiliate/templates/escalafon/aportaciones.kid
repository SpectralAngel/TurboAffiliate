<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
    import locale
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>TurboAffiliate &bull; Afiliados</title>
        <style type="text/css">
            h1
            {
                text-align: center;
            }
        </style>
    </head>
    <body>
        <h3>COPEMH</h3>
        <h1>Afiliados que aportaron ${month} de ${year}</h1>
        <table width="100%">
            <thead>
                <tr>
                    <th>Carnet</th>
                    <th>Apellido</th>
                    <th>Nombre</th>
                    <th>Identidad</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="d in deduced">
                    <td>${d.affiliate.id}</td>
                    <td>${d.affiliate.lastName}</td>
                    <td>${d.affiliate.firstName}</td>
                    <td>${d.affiliate.cardID}</td>
                </tr>
            </tbody>
        </table>
        <strong>Total de Afiliados: </strong>${deduced.count()}
    </body>
</html>
