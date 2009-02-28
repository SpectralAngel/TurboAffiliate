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
			<li py:for="affiliate in result">
				<h2><a href="${tg.url('/affiliate/%s' % affiliate.id)}" py:content="affiliate.firstName,' ', affiliate.lastName" /></h2>
				<span py:content="'Afiliado N&uacute;mero: ', affiliate.id" />
				<span py:content="'Identidad: ', affiliate.cardID" />
				<span py:content="'Escalaf&oacute;n: ', affiliate.escalafon" />
				<span py:for="loan in affiliate.loans" py:content="'Pr&eacute;stamo: ', loan.capital" />
			</li>
		</ul>
	</body>
</html>
