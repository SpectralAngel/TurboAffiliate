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
		<title>TurboAffiliate &bull; Afiliado ${affiliate.id}</title>
	</head>
	<body>
		<div id="breadcrum">
			<a class="previous" href="${tg.url('/affiliate/%s' % (affiliate.id - 1))}">Anterior</a>
			<a class="next" href="${tg.url('/affiliate/%s' % (affiliate.id + 1))}">Siguiente</a>
		</div>
        <ul class="toolbox">
			<li>
				<a class="edit" href="${tg.url('/affiliate/edit/%s' % affiliate.id)}">Editar</a>
			</li>
			<li py:if="'admin' in tg.identity.groups">
				<a class="delete" href="${tg.url('/affiliate/remove/%s' % affiliate.id)}">Borrar</a>
			</li>
			<li>
				<a class="add" href="${tg.url('/affiliate/extra/add/%s' % affiliate.id)}">A&ntilde;adir Deducci&oacute;n Extra</a>
			</li>
			<li>
				<a class="add" href="${tg.url('/affiliate/jubilate/%s' % affiliate.id)}">Editar Fecha de Jubilaci&oacute;n</a>
			</li>
			<li>
				<a py:if="affiliate.active" class="delete" href="${tg.url('/affiliate/deactivate/%s' % affiliate.id)}">Desactivar Afiliado</a>
				<a py:if="not affiliate.active" class="delete" href="${tg.url('/affiliate/activate/%s' % affiliate.id)}">Activar Afiliado</a>
			</li>
			<li>
				<a class="view" href="${tg.url('/affiliate/deduced/%s' % affiliate.id)}">Ver detalle de Deducciones</a>
			</li>
		</ul>
        <h1 class="afiliado">${affiliate.id} - ${affiliate.firstName} ${affiliate.lastName}</h1>
        <h2><span class="pago">${affiliate.payment}</span> ${affiliate.cardID}
        <span class="pago" py:if="affiliate.payment == 'INPREMA'">N&uacute;mero de Cobro:
        ${affiliate.escalafon}</span>
        </h2>
        
        <h3>Afiliado desde <span py:if="not affiliate.joined is None">${affiliate.joined.strftime('%d de %B de %Y')}</span>
            <a href="${tg.url('/affiliate/status/%s' % affiliate.id)}">Estado de Cuenta</a>
        </h3>
		
        <span class="flash" py:if="affiliate.payment == 'INPREMA' and affiliate.jubilated == None">
		Este Afiliado requiere Actualizar sus datos de Jubilaci&oacute;n haga
		<a href="${tg.url('/affiliate/jubilate/%s' % affiliate.id)}">click aqu&iacute;</a>
		actualizarlos</span>
		<span class="flash" py:if="affiliate.cardID == None">Este afiliado no
		tiene tarjeta de identidad ingresada haga
		<a href="${tg.url('/affiliate/edit/%s' % affiliate.id)}">click aqu&iacute;</a>
		para ingresarla</span>
		<span class="flash" py:if="affiliate.state == None or affiliate.state ==''">Este afiliado no
		tiene Departamento
		<a href="${tg.url('/affiliate/edit/%s' % affiliate.id)}">Ingresar</a></span>
		<span class="flash" py:if="affiliate.town == None or affiliate.town ==''">Este afiliado no
		tiene Ciudad
		<a href="${tg.url('/affiliate/edit/%s' % affiliate.id)}">Ingresar</a></span>
		<h3 class="flash" py:if="not affiliate.active">Afiliado desactivado, razon:<strong><span class="flash" py:if="not affiliate.active" py:content="affiliate.reason" /></strong></h3>
		<h3>Informaci&oacute;n Personal</h3>
		<ul>
			<li>
				<strong>Lugar de Nacimiento: </strong>
				<span py:content="affiliate.birthPlace" />
			</li>
			<li>
				<strong>Fecha de Nacimiento: </strong>
				<span py:if="not affiliate.birthday is None" py:content="affiliate.birthday.strftime('%d de %B de %Y')" />
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
				<a href="${tg.url('/affiliate/status/%s' % affiliate.id)}">Estado de Cuenta</a>
			</li>
		</ul>
        
        <table>
            <caption>Cobros a Efectuar</caption>
            <thead>
                <th>Concepto</th>
                <th>Retrasada</th>
                <th>Mes</th>
                <th>Anio</th>
                <th>Cantidad</th>
            </thead>
            <tbody>
                <tr>
                    <td>Aportaci&oacute;n Ordinaria</td>
                    <td>No</td>
                    <td></td>
                    <td></td>
                    <td>${locale.currency(affiliate.get_cuota(), True, True)}</td>
                </tr>
                <tr py:for="loan in affiliate.loans">
                    <td>Cuota de Pr&eacute;stamo</td>
                    <td>No</td>
                    <td></td>
                    <td></td>
                    <td>${locale.currency(loan.get_payment(), True, True)}</td>
                </tr>
                <tr py:for="extra in affiliate.extras">
                    <td>${extra.account.name}</td>
                    <td>${extra.retrasada}</td>
                    <td>${extra.mes}</td>
                    <td>${extra.anio}</td>
                    <td>${locale.currency(extra.amount, True, True)}</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="4">Total de Deducciones</td>
                    <td>${locale.currency(affiliate.get_monthly(), True, True)}</td>
                </tr>
            </tfoot>
        </table>
        <table>
            <caption>Pr&eacute;stamos Personales</caption>
            <thead>
                <tr>
                    <th>Solicitud</th>
                    <th>Monto</th>
                    <th>Deuda</th>
                    <th>Cuota</th>
                    <th>Ultimo Pago</th>
                    <th>Ver</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="loan in affiliate.loans">
                    <td>${loan.id}</td>
                    <td>${locale.currency(loan.capital, True, True)}</td>
                    <td>${locale.currency(loan.debt, True, True)}</td>
                    <td>${locale.currency(loan.payment, True, True)}</td>
                    <td>${loan.last.strftime('%d de %B de %Y')}</td>
                    <td><a href="${tg.url('/loan/%s' % loan.id)}" >Ver</a></td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <th colspan="6"><a href="${tg.url('/loan/add/%s' % affiliate.id)}">Agregar Pr&eacute;stamo</a></th>
                </tr>
            </tfoot>
        </table>
        <table>
            <caption>Historial de Pr&eacute;stamos</caption>
            <thead>
                <tr>
                    <th>Solicitud</th>
                    <th>Monto</th>
                    <th>Deuda</th>
                    <th>Cuota</th>
                    <th>Ultimo Pago</th>
                    <th>Ver</th>
                </tr>
            </thead>
            <tbody>
                <tr py:for="loan in affiliate.refinancedLoans">
                    <td>${loan.id}</td>
                    <td>${locale.currency(loan.capital, True, True)}</td>
                    <td>${locale.currency(loan.debt, True, True)}</td>
                    <td>${locale.currency(loan.payment, True, True)}</td>
                    <td>${loan.last.strftime('%d de %B de %Y')}</td>
                    <td><a href="${tg.url('/refinanced/%s' % loan.id)}" >Ver</a></td>
                </tr>
                <tr py:for="loan in affiliate.payedLoans">
                    <td>${loan.id}</td>
                    <td>${locale.currency(loan.capital, True, True)}</td>
                    <td>${locale.currency(0)}</td>
                    <td>${locale.currency(loan.payment, True, True)}</td>
                    <td>${loan.last.strftime('%d de %B de %Y')}</td>
                    <td><a href="${tg.url('/payed/%s' % loan.id)}" >Ver</a></td>
                </tr>
            </tbody>
        </table>
        <form action="${tg.url('/affiliate/deduced/mostrar')}" method="get">
            <fieldset>
                <legend>Ver Deducciones Realizadas</legend>
                <ul>
                    <input type="hidden" value="${affiliate.id}" name="afiliado" />
                    <li>
                        <label>Mes:</label>
                        <input name="mes" />
                    </li>
                    <li>
                        <label>A&ntilde;o:</label>
                        <input name="anio" />
                    </li>
                    <li><input value="Mostrar" type="submit" /></li>
                </ul>
            </fieldset>
        </form>
		<div id="observaciones">
			<h2>Observaciones</h2>
			<p py:for="observacion in affiliate.observaciones" py:content="observacion.texto" />
			<form action="${tg.url('/affiliate/observacion/add')}">
				<fieldset>
					<legend>Agregar Observaci&oacute;n</legend>
					<ol>
						<li>
							<input name="affiliate" value="${affiliate.id}" type="hidden" />
							<label>Observaci&oacute;n</label>
							<textarea name="texto"></textarea>
						</li>
						<li>
							<input type="submit" value="Agregar" />
						</li>
					</ol>
				</fieldset>
			</form>
		</div>
	</body>
</html>
