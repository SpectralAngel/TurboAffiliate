<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Obligaciones</title>
	</head>
	<body>
		<div py:for="obligation in obligations">
			<h2 py:content="'Obligaci&oacute;n N&uacute;mero ', obligation.id" />
			<ul>
				<li>
					<strong>Compa&ntilde;&iacute;a:</strong>
					<span py:content="obligation.company.name" />
				</li>
				<li>
					<strong>Mes:</strong>
					<span py:content="obligation.month" />
				</li>
				<li>
					<strong>A&ntilde;o:</strong>
					<span py:content="obligation.year" />
				</li>
				<li>
					<strong>Monto:</strong>
					<span py:content="obligation.amount" />
				</li>
				<li>
					<strong>Cuenta:</strong>
					<span py:content="obligation.account.name" />
				</li>
				<li>
					<a href="${'/obligation/remove/%s' % obligation.id}">
						Remover
					</a>
				</li>
			</ul>
		</div>
	</body>
</html>
