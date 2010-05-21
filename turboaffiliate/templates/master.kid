<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<?python
	import sitetemplate
	from datetime import date
	from turboaffiliate import model
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
	<head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
	    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
	    <title py:replace="''">Your title goes here</title>
	    <meta py:replace="item[:]"/>
	    <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/smoothness/jquery-ui.css')}" media="screen" />
	    <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/style.css')}" media="screen" />
	    <link rel="stylesheet" type="text/css" href="${tg.url('/static/css/print.css')}" media="print" />
	</head>
	<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">
	    <div id="header">
	    	<div style="float: right;" py:if="tg.config('identity.on',False) and not 'logging_in' in locals()" id="pageLogin">
	    		<a href="https://bugs.launchpad.net/turboaffiliate/+filebug">Reportar un Fallo</a>&nbsp; 
				<span py:if="tg.identity.anonymous">
					<a href="${tg.url('/login')}">Iniciar Sesi&oacute;n</a>
				</span>
				<span py:if="not tg.identity.anonymous">
					Bienvenido ${tg.identity.user.display_name}.
					<a href="${tg.url('/logout')}">Cerrar Sesi&oacute;n</a>
				</span>
		    </div>
		    <h1 style="clear: both;">Sistema de Afiliados COPEMH</h1>
	    </div>
	    <div id="container">
	    	<div id="content" class="column">
				<div py:if="tg_flash" class="flash" py:content="tg_flash" />
	    		<div py:replace="[item.text]+item[:]"/>
	    	</div>
	    	<div id="sidebar-left" class="column">
	    		
    			<a class="menu" href="${tg.url('/affiliate')}">
    				<img src="${tg.url('/static/images/affiliate.png')}" alt="Afiliados" width="48" height="48" />
    				<span>Afiliados</span>
    			</a>
    			<a class="menu" href="${tg.url('/loan')}">
    				<img src="${tg.url('/static/images/loan.png')}" alt="Afiliados" width="48" height="48" />
    				<span>Pr&eacute;stamos</span>
    			</a>
    			<a class="menu" href="${tg.url('/company')}">
    				<img src="${tg.url('/static/images/company.png')}" alt="Afiliados" width="48" height="48" />
    				<span>Compa&ntilde;&iacute;as</span>
    			</a>
    			<a class="menu" href="${tg.url('/obligation')}">
    				<img src="${tg.url('/static/images/affiliate.png')}" alt="Afiliados" width="48" height="48" />
    				<span>Obligaciones</span>
    			</a>
	    		<a class="menu"  py:if="'admin' in tg.identity.groups" href="/catwalk">
					<img src="${tg.url('/static/images/admin.png')}" alt="Admin" width="48" height="48" />
					<span>Administrar</span>
				</a>
	    		<a class="menu"  py:if="'admin' in tg.identity.groups" href="/logger">
					<img src="${tg.url('/static/images/admin.png')}" alt="Admin" width="48" height="48" />
					<span>Ver Logs</span>
				</a>
				<a class="menu" href="http://172.16.10.68:8050">
					<img src="${tg.url('/static/images/admin.png')}" alt="Admin" width="48" height="48" />
					<span>Egresos</span>
				</a>
				<a class="menu" href="http://172.16.10.68:8040">
					<img src="${tg.url('/static/images/admin.png')}" alt="Admin" width="48" height="48" />
					<span>Caja SPS</span>
				</a>
                <a class="menu" href="http://172.16.10.68:8000">
					<img src="${tg.url('/static/images/admin.png')}" alt="Admin" width="48" height="48" />
					<span>Caja Ceiba</span>
				</a>
	    	</div>
	    	<div id="sidebar-right" class="column">
	    		<a class="menu" href="${tg.url('/')}">
			    	<img src="${tg.url('/static/images/home.png')}" alt="inicio" width="48" height="48" />
			    	<span>Inicio</span>
		    	</a>
				<a class="menu" href="${tg.url('/affiliate/add')}">
			    	<img src="${tg.url('/static/images/add48.png')}" alt="Partida" width="48" height="48" />
			    	<span>A&ntilde;adir Afiliado</span>
		    	</a>
	    		<a class="menu" href="${tg.url('/escalafon')}">
	    			<img src="${tg.url('/static/images/import.png')}" alt="Admin" width="48" height="48" />
	    			<span>Reportes y Deducciones</span>
	    		</a>
	    		<a class="menu" href="${tg.url('/affiliate/billing')}">
	    			<img src="${tg.url('/static/images/import.png')}" alt="Admin" width="48" height="48" />
	    			<span>Estados de Cuenta</span>
	    		</a>
	    		<a class="menu" href="javascript:back();">
	    			<img src="${tg.url('/static/images/back.png')}" width="48" height="48" />
	    			<span>Atr&aacute;s</span>
	    		</a>
	    	</div>
	    </div>
		<div id="footer-wrapper">
			<div id="footer">Copyright &copy; 2007 - 2009 COPEMH</div>
		</div>
	</body>
</html>
