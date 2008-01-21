<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Afiliados</title>
	</head>
	<body>
		<h1>Resultados de la B&uacute;squeda</h1>
		<ul>
			<li py:for="funebre in funebres">
				N&uacute;mero <a href="${tg.url('/funebre/%s' % funebre.id)}"><span py:content="funebre.id" /></a>
			</li>
		</ul>
	</body>
</html>
