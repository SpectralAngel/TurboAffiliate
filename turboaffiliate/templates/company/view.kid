<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Compa&ntilde;&iacute;as</title>
	</head>
	<body>
		<div py:for="company in companies">
		<h1>Informaci&oacute;n de la Compa&ntilde;&iacute;a</h1>
		<h2 py:content="company.name" />
		<ul>
			<li>
				<a href="${tg.url('/company/edit/%s' % company.id)}">Editar</a>
			</li>
			<li>
				<a class="delete" href="${tg.url('/company/delete/%s' % company.id)}">Eliminar</a>
			</li>
		</ul>
		<ul>
			<li>
				<strong>RTN: </strong><span py:content="company.rtn" />
			</li>
			<li>
				<strong>Descipci&oacute;n: </strong>
				<span py:content="company.description" />
			</li>
			<li>
				<a href="${tg.url('/obligation/add/')}">
					A&ntilde;adir Obligaci&oacute;n
				</a>
			</li>
		</ul>
		</div>
	</body>
</html>

