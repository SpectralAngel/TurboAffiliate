<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	from datetime import date
	import locale
	locale.setlocale(locale.LC_ALL, "en-US")
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
	<head>
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
		<title>Pr&eacute;stamos &bull; Paga&eacute;</title>
		<link rel="stylesheet" type="text/css" href="${tg.url('/static/css/pagare.css')}" />
	</head>
	<body>
		<h1 style="text-align: center">Pagar&eacute; por L. <span py:content="locale.currency(loan.capital)" /></h1>
		<p>
			Yo, <strong py:content="loan.affiliate.firstName, loan.affiliate.lastName" />,
			pagar&eacute; al Colegio de Profesores de Educaci&oacute;n de
			Honduras. (COPEMH). La cantidad de <strong py:content="loan.letters, 'Lempiras'" />
			(<span py:content="locale.currency(loan.capital)" />) que en esta
			fecha recibo a mi entera satisfacci&oacute;n y en calidad de
			pr&eacute;stamo. Esta obligaci&oacute;n devengar&aacute; intereses a la tasa de
			${loan.interest}% anual. El pago se har&aacute; en las
			oficinas del COPEMH en esta ciudad, en Lempiras exclusivamente o en
			moneda de curso legal en la Rep&uacute;blica de Honduras.
		</p>
		<p>
			En fe de lo cual firmo este pagar&eacute; en la ciudad de Tegucigalpa
			el d&iacute;a <span py:content="loan.startDate.strftime('%d de %B de %Y')" />
		</p>
		<p class="center">Firma del Suscriptor</p>
		<p>
			Nombre del Afiliado: <strong py:content="loan.affiliate.firstName, loan.affiliate.lastName" />
			<br />
			Tarjeta de <strong>Identidad: <span py:content="loan.affiliate.cardID" />
		</p>
		<!-- <div py:if="loan.aval != None">
		<h2>Por Aval</h2>
		<p>
			Por virtud de este Aval y como Fiador(es), garantizo(mos)
			incondicionalmente el pago inmediato del principal, intereses y
			costes de la obligaci&oacute;n descrita en este documento, de acuerdo
			con las condiciones pactadas. Autorizo(mos) cualquier extensi&oacute;n
			o renovaci&oacute;n del plazo. En f&eacute; de lo cual firmo(mos) por
			Aval en la fecha arriba indicada.
		</p>
		<p class="center">Firma del Aval</p>
		<p>
			Nombre del aval: ${loan.aval.firstName} ${loan.aval.lastName}
			<br />
			Identidad: ${loan.aval.cardID}
		</p>
		</div> -->
	</body>
</html>
