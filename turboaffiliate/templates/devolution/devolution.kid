<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; A&ntilde;adir Afiliado</title>
	</head>
	<body>
		<h1>Ayuda de Sobrevivencia N&uacute;mero <span py:content="survival.id" /></h1>
		<ul>
			<li>
				<a href="${tg.url('delete/%s' % survival.id)}">Borrar</a>
			</li>
		</ul>
		<ul>
			<li>
				<a href="${tg.url('/affiliate/%s' % survival.affiliate.id)}">
					<span py:content="survival.affiliate" />
				</a>
			</li>
			<li>
				<span py:content="survival.amount" />
			</li>
			<li>
				<span py:content="survival.reason" />
			</li>
		</ul>
	</body>
</html>
