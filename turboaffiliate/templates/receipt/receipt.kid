<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>TurboAffiliate &bull; Afiliados</title>
		<script src="/static/javascript/jquery.js" type="text/javascript"></script>
		<script src="/static/javascript/jquery.account.js" type="text/javascript"></script>
		<script type="text/javascript">
		<![CDATA[
		$(document).ready(function(e)
		{
			$('#account1').click(get_account);
		});
		]]>
		</script>
	</head>
	<body>
		<h1>Recibo ${receipt.id} </h1>
		<h2>${receipt.affiliate} &nbsp;  &nbsp; ${receipt.name}</h2>
		<table>
			<thead>
				<tr>
					<th>Cantidad</th>
					<th>Concepto</th>
					<th>Detalle</th>
					<th>Precio Unitario</th>
					<th>Valor</th>
					<th py:if="receipt.closed == False">Borrar</th>
				</tr>
			</thead>
			<tbody>
				<tr py:for="line in receipt.lines">
					<td py:content="line.qty" />
					<td py:content="line.account.name" />
					<td py:content="line.detail" />
					<td py:content="line.unit" />
					<td py:content="line.value()" />
					<td py:if="receipt.closed == False"><a class="delete" href="${tg.url('line/remove/%s' % line.id)}">X</a></td>
				</tr>
			</tbody>
		</table>
		<form>
			<fieldset>
				<legend>Cat&aacute;logo de Cuentas</legend>
				<label for="account">Cuenta:</label>
				<select name="account">
					<option py:for="account in accounts" py:content="account.code, ' - ', account.name" value="${account.id}" />
				</select>
			</fieldset>
		</form>
		<form py:if="receipt.closed == False" action="${tg.url('/receipt/line/save')}" method="post">
			<fieldset>
                <input name="receipt" type="hidden" value="${receipt.id}" />
				<legend>A&ntilde;adir L&iacute;nea</legend>
				<table>
					<thead>
						<tr>
							<th>C&oacute;digo</th>
							<th>Concepto</th>
							<th>Detalle</th>
							<th>Cantidad</th>
							<th>Precio Unitario</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td><input name="account" id="account" /><a href="#" id="account1">Buscar</a></td>
							<td id="target"></td>
							<td><input name="detail" id="detail" /></td>
							<td><input name="qty" id="qty" /></td>
							<td><input name="unit" id="unit" /></td>
						</tr>
					</tbody>
				</table>
				<input type="submit" value="Agregar Linea" />
			</fieldset>
		</form>
		<a href="${tg.url('/receipt/printer/%s' % receipt.id)}">Cerrar y preparar impresi&oacute;n</a>
	</body>
</html>
