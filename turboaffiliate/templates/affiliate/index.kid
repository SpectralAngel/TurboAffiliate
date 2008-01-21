<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master.kid'">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Afiliados</title>
		<script src="${tg.url('/static/javascript/jquery.js')}" type="text/javascript"></script>
		<script src="${tg.url('/static/javascript/jquery.date.js')}" type="text/javascript"></script>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/date.css')}" />
		<script type="text/javascript">
		<![CDATA[
		$(document).ready(function(e)
		{
			$.datePicker.setLanguageStrings(['Domingo', 'Lunes', 'Martes',
											 'Miércoles', 'Jueves', 'Viernes',
											 'Sábado'],	['Enero', 'Febrero',
											 'Marzo', 'Abril', 'Mayo', 'Junio',
											 'Julio', 'Agosto', 'Septiembre',
											 'Octubre', 'Noviembre', 'Diciembre'],
											 {p:'Atras', n:'Siguiente',
											 c:'Cierre', b:'Elija la fecha'}
											);
			$('input.date-picker').datePicker({startDate:'01/01/1950'});
			$.datePicker.setDateFormat('ymd','-');
		});
		]]>
		</script>
	</head>
	<body>
		<h1>Afiliados</h1>
		<ul>
			<li><a href="add">A&ntilde;adir un Afiliado</a></li>
			<li><a href="last">Ver el Ultimo Afiliado</a></li>
			<li><a href="extra">A&ntilde;adir Deducciones Extra a Varios Afiliados</a></li>
			<li><a href="disabled">Ver Afiliados Inactivos</a></li>
			<li><a href="all">Ver Todos los Afiliados</a></li>
			<li><a href="solventYear">Ver Solventes por A&ntilde;o</a></li>
			<li><a href="none">Ver Afiliados sin a&ntilde;o de Afiliaci&oacute;n</a></li>
		</ul>
		<form action="${tg.url('/affiliate/byCopemh')}">
			<fieldset>
				<legend>Buscar Afiliado</legend>
				<ul>
					<li>
						<label>Carnet:</label>
						<input name="copemh" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="search">
			<fieldset>
				<legend>Buscar Affiliado</legend>
				<ul>
					<li>
						<label>Nombre o Apellido:</label>
						<input name="name" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="card" method="post">
			<fieldset>
				<legend>Buscar Affiliado</legend>
				<ul>
					<li>
						<label>Identidad:</label>
						<input name="cardID" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="byRange">
			<fieldset>
				<legend>Buscar Afiliados por C&oacute;digo de Departamento</legend>
				<ul>
					<li>
						<label>Identificador:</label>
						<input name="code" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="department" method="post">
			<fieldset>
				<legend>Reporte por Departamento</legend>
				<ul>
					<li>
						<label for="state">Departamento:</label>
						<select name="state">
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
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="cotization">
			<fieldset>
				<legend>Ver Deducci&oacute;n por Cotizaci&oacute;n</legend>
				<ul>
					<li>
						<label for="how">Cotiza por:</label>
						<select name="how">
							<option>Escalafon</option>
							<option>INPREMA</option>
							<option>UPN</option>
						</select>
					</li>
					<li>
						<label>A&ntilde;o:</label>
						<input name="year" />
					</li>
					<li>
						<label>Mes:</label>
						<input name="month" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="payment">
			<fieldset>
				<legend>Ver Afiliados por Cotizaci&oacute;n</legend>
				<ul>
					<li>
						<label for="how">Cotiza por:</label>
						<select name="how">
							<option>Escalafon</option>
							<option>INPREMA</option>
							<option>UPN</option>
						</select>
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="age">
			<fieldset>
				<legend>Ver Afiliados por Edad</legend>
				<ul>
					<li>
						<label for="how">Edad:</label>
						<input name="age" />
					</li>
					<li>
						<label>A&ntilde;o M&aacute;ximo de Afiliaci&oacute;n:</label>
						<input name="joined" />
					</li>
					<li>
						<input type="submit" value="Buscar" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="byDate">
			<fieldset>
				<legend>Mostrar seg&uacute;n fecha de afiliaci&oacute;n</legend>
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
		<form action="byTown">
			<fieldset>
				<legend>Mostrar por Municipio</legend>
				<ul>
					<li>
						<label>Municipio:</label>
						<input name="town" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="bySchool">
			<fieldset>
				<legend>Mostrar por Instituto</legend>
				<ul>
					<li>
						<label>Instituto:</label>
						<input name="school" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="manual">
			<fieldset>
				<legend>Posteo Manual de Afiliados, INPREMA, UPN</legend>
				<ul>
					<li>
						<label>Carnet:</label>
						<input name="affiliate" />
					</li>
					<li>
						<label>A&ntilde;o:</label>
						<input name="year" />
					</li>
					<li>
						<label>Mes:</label>
						<input name="month" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		<form action="listmanual">
			<fieldset>
				<legend>Listado para Posteo Manual de Afiliados, INPREMA, UPN</legend>
				<ul>
					<li>
						<label for="payment">Cotiza por:</label>
						<select name="payment">
							<option>INPREMA</option>
							<option>UPN</option>
						</select>
					</li>
					<li>
						<label>A&ntilde;o:</label>
						<input name="year" />
					</li>
					<li>
						<label>Mes:</label>
						<input name="month" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
		
		<form action="solvent">
			<fieldset>
				<legend>Afiliados Solventes por A&ntilde;o</legend>
				<ul>
					<li>
						<label>A&ntilde;o:</label>
						<input name="year" />
					</li>
					<li>
						<input type="submit" value="Ver" />
					</li>
				</ul>
			</fieldset>
		</form>
	</body>
</html>
