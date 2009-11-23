<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Afiliados</title>
		<script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery-ui.js')}" type="text/javascript"></script>
		<script type="text/javascript">
		<![CDATA[
		$(document).ready(function(e)
		{
			$('input.date-picker').datepicker({
												dateFormat: 'yy-mm-dd',
												changeMonth: true,
												changeYear: true,
												yearRange: '1940:2010'
											  });
		});
		]]>
		</script>
	</head>
	<body>
		<h1>Pr&eacute;stamos</h1>
		<a href="dobles">Ver Afiliados con multiples pr&eacute;stamos</a>
		<form action="search" method="post">
			<fieldset>
				<legend>Buscar Pr&eacute;stamo</legend>
				<ul>
					<li>
						<label>N&uacute;mero de Pr&eacute;stamo</label>
						<input name="loan" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="/payed">
			<fieldset>
				<legend>Ver Pr&eacute;stamo Pagado</legend>
				<ul>
					<li>
						<label>Solicitud:</label>
						<input name="id" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="period">
			<fieldset>
				<legend>Mostrar Pr&eacute;stamos de un Periodo</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="first" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="last" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="cotizacion">
			<fieldset>
				<legend>Pr&eacute;stamos Otorgados por Periodo y Cotizacion</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="start" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="end" class="date-picker" />
					</li>
					<li>
						<label for="payment">Cotiza por:</label>
						<select name="payment">
							<option>Escalafon</option>
							<option>INPREMA</option>
							<option>UPN</option>
							<option>Ministerio</option>
							<option>Retirado</option>
						</select>
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="/payed/payment">
			<fieldset>
				<legend>Pr&eacute;stamos por Periodo y Cotizacion - Pagados </legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="start" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="end" class="date-picker" />
					</li>
					<li>
						<label for="payment">Cotiza por:</label>
						<select name="payment">
							<option>Escalafon</option>
							<option>INPREMA</option>
							<option>UPN</option>
							<option>Ministerio</option>
							<option>Retirado</option>
						</select>
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="/payed/period">
			<fieldset>
				<legend>Pr&eacute;stamos por Periodo - Pagados</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="start" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="end" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="add">
			<fieldset>
				<legend>A&ntilde;adir Pr&eacute;stamo a Afiliado</legend>
				<ul>
					<li>
						<label>Carnet:</label>
						<input name="cardID" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="day">
			<fieldset>
				<legend>Mostrar Pr&eacute;stamos de un D&iacute;a</legend>
				<ul>
					<li>
						<label>D&iacute;a:</label>
						<input name="day" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="cartera">
			<fieldset>
				<legend>Mostrar Cartera Pr&eacute;stamos</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="first" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="last" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="monthly">
			<fieldset>
				<legend>Reporte de Pr&eacute;stamos Otorgados</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="start" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="end" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="bypayment">
			<fieldset>
				<legend>Pr&eacute;stamos por Tipo de Cotizaci&oacute;n</legend>
				<ul>
					<li>
						<label for="payment">Cotiza por:</label>
						<select name="payment">
							<option>Escalafon</option>
							<option>INPREMA</option>
							<option>UPN</option>
							<option>Ministerio</option>
							<option>Retirado</option>
						</select>
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="paymentDate">
			<fieldset>
				<legend>Pr&eacute;stamos por Tipo de Cotizaci&oacute;n y Fecha</legend>
				<ul>
					<li>
						<label for="payment">Cotiza por:</label>
						<select name="payment">
							<option>Escalafon</option>
							<option>INPREMA</option>
							<option>UPN</option>
							<option>Ministerio</option>
							<option>Retirado</option>
						</select>
					</li>
					<li>
						<label>Inicio:</label>
						<input name="start" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="end" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="liquid">
			<fieldset>
				<legend>Reporte de Liquidaci&oacute;n de Pr&eacute;stamos</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="start" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="end" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="byCapital">
			<fieldset>
				<legend>Reporte de Capital e Intereses</legend>
				<ul>
					<li>
						<label>D&iacute;a:</label>
						<input name="day" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="resume">
			<fieldset>
				<legend>Resumen de Capital e Intereses por Periodo</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="start" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="end" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="pay/resume">
			<fieldset>
				<legend>Detalle de Pagos por Periodo</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="start" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="end" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="diverge">
			<fieldset>
				<legend>Divergencia de Pr&eacute;stamos</legend>
				<ul>
					<li>
						<label for="payment">Cotiza por:</label>
						<select name="payment">
							<option>Escalafon</option>
							<option>INPREMA</option>
							<option>UPN</option>
							<option>Ministerio</option>
							<option>Retirado</option>
						</select>
					</li>
					<li>
						<label>Inicio:</label>
						<input name="start" />
					</li>
					<li>
						<label>Final:</label>
						<input name="end" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="cotizacionDepto">
			<fieldset>
				<legend>Pr&eacute;stamos por Tipo de Cotizaci&oacute;n y Departamento</legend>
				<ul>
					<li>
						<label for="cotizacion">Cotiza por:</label>
						<select name="cotizacion">
							<option>Escalafon</option>
							<option>INPREMA</option>
							<option>UPN</option>
							<option>Ministerio</option>
							<option>Retirado</option>
						</select>
					</li>
					<li>
						<label for="depto">Departamento:</label>
						<select name="depto">
							<option>Atlantida</option>
							<option>Choluteca</option>
							<option>Colon</option>
							<option>Comayagua</option>
							<option>Copan</option>
							<option>Cortes</option>
							<option>El Paraiso</option>
							<option>Francisco Morazan</option>
							<option>Gracias a Dios</option>
							<option>Intibuca</option>
							<option>Islas de la Bahia</option>
							<option>La Paz</option>
							<option>Lempira</option>
							<option>Olancho</option>
							<option>Ocotepeque</option>
							<option>Santa Barbara</option>
							<option>Valle</option>
							<option>Yoro</option>
						</select>
					</li>
					<li>
						<input type="submit" value="Mostrar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="deducciones">
			<fieldset>
				<legend>Reporte de Deducciones de Pr&eacute;stamos</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="start" class="date-picker" />
					</li>
					<li>
						<label>Final:</label>
						<input name="end" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="deduccionesDia">
			<fieldset>
				<legend>Reporte de Deducciones de Pr&eacute;stamos Diarios</legend>
				<ul>
					<li>
						<label>Inicio:</label>
						<input name="start" class="date-picker" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>

