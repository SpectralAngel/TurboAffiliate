<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import locale
	locale.setlocale(locale.LC_ALL, "en-US")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Afiliados</title>
	</head>
	<body>
		<div id="breadcrum">
			<a class="previous" href="${tg.url('/affiliate/%s' % (affiliate.id - 1))}">Anterior</a>
			<a class="next" href="${tg.url('/affiliate/%s' % (affiliate.id + 1))}">Siguiente</a>
		</div>
		<h1 py:content="affiliate.id, ' ', affiliate.firstName, ' ', affiliate.lastName" />
		<span class="flash" py:if="affiliate.payment == 'INPREMA' and affiliate.jubilated == None">
		Este Afiliado requiere Actualizar sus datos de Jubilaci&oacute;n haga
		<a href="${tg.url('/affiliate/jubilate/%s' % affiliate.id)}">click aqu&iacute;</a>
		actualizarlos</span>
		<ul class="toolbox">
			<li>
				<a class="edit" href="${tg.url('/affiliate/edit/%s' % affiliate.id)}">Editar</a>
			</li>
			<li py:if="'admin' in tg.identity.groups">
				<a class="delete" href="${tg.url('/affiliate/remove/%s' % affiliate.id)}">Borrar</a>
			</li>
			<li>
				<a href="${tg.url('/funebre/add/%s' % affiliate.id)}">A&ntilde;adir Ayuda Funebre</a>
			</li>
			<li>
				<a class="add" href="${tg.url('/affiliate/extra/add/%s' % affiliate.id)}">A&ntilde;adir Deducci&oacute;n Extra</a>
			</li>
			<li>
				<a py:if="affiliate.active" class="delete" href="${tg.url('/affiliate/off/%s' % affiliate.id)}">Desactivar Afiliado</a>
				<a py:if="not affiliate.active" class="delete" href="${tg.url('/affiliate/on/%s' % affiliate.id)}">Activar Afiliado</a>
			</li>
			<li>
				<a class="view" href="${tg.url('/affiliate/deduced/%s' % affiliate.id)}">Ver detalle de Deducciones</a>
			</li>
		</ul>
		<h3>Informaci&oacute;n Personal</h3>
		<ul>
			<li>
				<strong>Lugar de Nacimiento: </strong>
				<span py:content="affiliate.birthPlace" />
			</li>
			<li>
				<strong>Identidad: </strong>
				<span py:content="affiliate.cardID" />
			</li>
			<li>
				<strong>Fecha de Nacimiento: </strong>
				<span py:content="affiliate.birthday" />
			</li>
			<li>
				<strong>G&eacute;nero:</strong>
				<span py:if="affiliate.gender == 'M'">Masculino</span>
				<span py:if="affiliate.gender == 'F'">Femenino</span>
			</li>
			<li>
				<strong>Tel&eacute;fono: </strong>
				<span py:content="affiliate.phone" />
			</li>
		</ul>
		<h3>Informaci&oacute;n Colegiaci&oacute;n</h3>
		<ul>
			<li>
				<strong>Cotiza por: </strong>
				<span py:content="affiliate.payment" />
			</li>
			<li py:if="affiliate.payment == 'INPREMA'">
				<strong>Jubilado: </strong>
				<span py:content="affiliate.jubilated" />
			</li>
			<li>
				<strong>Instituto: </strong>
				<span py:content="affiliate.school" />
			</li>
			<li>
				<strong>Instituto: </strong>
				<span py:content="affiliate.school2" />
			</li>
			<li>
				<strong>Municipio: </strong>
				<span py:content="affiliate.town" />
			</li>
			<li>
				<strong>Departamento: </strong>
				<span py:content="affiliate.state" />
			</li>
			<li>
				<strong>Escalaf&oacute;n: </strong>
				<span py:content="affiliate.escalafon" />
			</li>
			<li>
				<strong>Fecha de Afiliaci&oacute;n: </strong>
				<span py:content="affiliate.joined" />
			</li>
			<li>
				<a href="${tg.url('/affiliate/status/%s' % affiliate.id)}">Estado de Cuenta</a>
			</li>
			<li>
				<a href="${tg.url('/affiliate/cuota/pay/%s' % affiliate.id)}">Pagar Cuota</a>
			</li>
		</ul>
		<h3 py:if="len(affiliate.extras) != 0">Deducciones Extra</h3>
		<ul py:if="len(affiliate.extras) != 0">
			<li py:for="extra in affiliate.extras">
				<span py:content="extra.account.name" /> <span py:content="locale.currency(extra.amount)" />
				<a href="${tg.url('/affiliate/extra/delete/%s' % extra.id)}">Eliminar</a>
			</li>
		</ul>
		<div id="loan" py:for="loan in affiliate.loans">
			<h3>Pr&eacute;stamo</h3>
			<span py:content="'Monto Total: ', locale.currency(loan.capital)" />
			<span py:content="'Monto Adeudado: ', locale.currency(loan.debt)" />
			<a href="${tg.url('/loan/%s' % loan.id)}" >Ver Pr&eacute;stamo</a>
		</div>
		<div id="loan" py:for="loan in affiliate.refinancedLoans">
			<h3>Pr&eacute;stamo Refinanciado</h3>
			<span py:content="'Monto Total: ', locale.currency(loan.capital)" />
			<span py:content="'Monto Adeudado: ', locale.currency(loan.debt)" />
			<a href="${tg.url('/refinanced/%s' % loan.id)}" >Ver Pr&eacute;stamo</a>
		</div>
		<div id="loan" py:for="loan in affiliate.payedLoans">
			<h3>Pr&eacute;stamo Pagado</h3>
			<span py:content="'Monto Total: ', locale.currency(loan.capital)" />
			<span py:content="'Ultimo Pago: ', loan.last" />
			<a href="${tg.url('/payed/%s' % loan.id)}" >Ver Pr&eacute;stamo</a>
		</div>
		<a href="${tg.url('/loan/add/%s' % affiliate.id)}">Agregar Pr&eacute;stamo</a>
	</body>
</html>
