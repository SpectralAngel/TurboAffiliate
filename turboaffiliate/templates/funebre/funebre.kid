<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; A&ntilde;adir Afiliado</title>
	</head>
	<body>
		<h1>Ayuda Funebre N&uacute;mero <span py:content="funebre.id" /></h1>
		<ul>
			<li>
				<a href="${tg.url('delete/%s' % funebre.id)}">Borrar</a>
			</li>
		</ul>
		<ul>
			<li>
				<a href="${tg.url('/affiliate/%s' % funebre.affiliate.id)}">
					<span py:content="funebre.affiliate.id, ' ', funebre.affiliate.firstName, ' ', funebre.affiliate.lastName" />
				</a>
			</li>
			<li>
				Cantidad: <span py:content="locale.currency(funebre.amount, True, True)" />
			</li>
			<li>
				Raz&oacute;n<span py:content="funebre.reason" />
			</li>
			<li>
				Fecha: <span py:content="funebre.day" />
			</li>
		</ul>
	</body>
</html>
