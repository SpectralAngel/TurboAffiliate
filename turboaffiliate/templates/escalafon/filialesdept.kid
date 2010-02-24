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
		<title>TurboAffiliate &bull; Filiales</title>
	</head>
	<body>
		<h1>Filiales Departamentales ${state}</h1>
		<table py:for="school in filiales">
		    <caption>${school}</caption>
		    <thead>
		        <tr>
		            <th>Afiliaci&oacute;n</th>
                    <th>Nombre</th>
		        </tr>
		    </thead>
            <tbody>
                <tr py:for="afiliado in filiales[school]">
                    <td>${afiliado.id}</td>
                    <td>${afiliado.firstName} ${afiliado.lastName}</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <th>Cantidad de Afiliados</th>
                    <th>${len(filiales[school])}</th>
                </tr>
            </tfoot>
		</table>
	</body>
</html>
