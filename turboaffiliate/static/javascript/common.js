$(document).ready(function(e)
{
  
  window.Meebo||function(c){function p(){return["<",i,' onload="var d=',g,";d.getElementsByTagName('head')[0].",
  j,"(d.",h,"('script')).",k,"='//cim.meebo.com/cim?iv=",a.v,"&",q,"=",c[q],c[l]?
  "&"+l+"="+c[l]:"",c[e]?"&"+e+"="+c[e]:"","'\"></",i,">"].join("")}var f=window,
  a=f.Meebo=f.Meebo||function(){(a._=a._||[]).push(arguments)},d=document,i="body",
  m=d[i],r;if(!m){r=arguments.callee;return setTimeout(function(){r(c)},100)}a.$=
  {0:+new Date};a.T=function(u){a.$[u]=new Date-a.$[0]};a.v=4;var j="appendChild",
  h="createElement",k="src",l="lang",q="network",e="domain",n=d[h]("div"),v=n[j](d[h]("m")),
  b=d[h]("iframe"),g="document",o,s=function(){a.T("load");a("load")};f.addEventListener?
  f.addEventListener("load",s,false):f.attachEvent("onload",s);n.style.display="none";
  m.insertBefore(n,m.firstChild).id="meebo";b.frameBorder="0";b.id="meebo-iframe";
  b.allowTransparency="true";v[j](b);try{b.contentWindow[g].open()}catch(w){c[e]=
  d[e];o="javascript:var d="+g+".open();d.domain='"+d.domain+"';";b[k]=o+"void(0);"}try{var t=
  b.contentWindow[g];t.write(p());t.close()}catch(x){b[k]=o+'d.write("'+p().replace(/"/g,
  '\\"')+'");d.close();'}a.T(1)}({network:"copemh_xo90ja"});
  Meebo("makeEverythingSharable");
  $('#meebo').children().addClass('noprint');
  
  $('#menu').ptMenu();
  $('.ui-button').hover(
      function(){ $(this).addClass("ui-state-hover"); },
      function(){ $(this).removeClass("ui-state-hover"); }
    ).mousedown(function(){ $(this).addClass("ui-state-active"); }
    ).mouseup(function(){ $(this).removeClass("ui-state-active"); }
  );
  
  $('input.datepicker').datepicker({
    dateFormat: 'dd/mm/yy',
    changeMonth: true,
    changeYear: true,
    yearRange: 'c-70:c+5'
  });
  
  $('input.date-picker').datepicker({
    dateFormat: 'yy-mm-dd',
    changeMonth: true,
    changeYear: true,
    yearRange: 'c-70:c+5'
  });
  
  $('#AgregarAfiliado').dialog(
  {
    title : "Agregar un Afiliado",
    modal:true,
    autoOpen:false,
    buttons :   {
            'Agregar Afiliado' : function() { $(this).submit() },
            'Cancelar' :  function() { $(this).dialog('close'); }
          }
  });
  
  $('#bID').dialog(
  {
    title : "Buscar Por Identidad",
    autoOpen:false,
    modal:true,
    buttons :   {
            'Buscar' : function() { $(this).submit() },
            'Cancelar' :  function() { $(this).dialog('close'); }
          }
  });
  
  $('#bAfiliacion').dialog(
  {
    title : "Buscar Por Carnet",
    autoOpen:false,
    modal:true,
    buttons :   {
            'Buscar' : function() { $(this).submit() },
            'Cancelar' :  function() { $(this).dialog('close'); }
          }
  });
  
  $('#bNombre').dialog(
  {
    title : "Buscar Por Nombre",
    autoOpen:false,
    modal:true,
    buttons :   {
            'Buscar' : function() { $(this).submit() },
            'Cancelar' :  function() { $(this).dialog('close'); }
          }
  });
  
  $(".striped tbody tr:odd").addClass("odd");
  $(".striped tbody tr:even").addClass("even");
  $(".deduced-674").addClass("ui-state-error").addClass("ui-corner-all");
  $('.button, button').button();
});
