$(document).ready(function(e)
{
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
    width: 350,
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
    buttons :   {
            'Buscar' : function() { $(this).submit() },
            'Cancelar' :  function() { $(this).dialog('close'); }
          }
  });
  
  $('#bAfiliacion').dialog(
  {
    title : "Buscar Por Carnet",
    autoOpen:false,
    buttons :   {
            'Buscar' : function() { $(this).submit() },
            'Cancelar' :  function() { $(this).dialog('close'); }
          }
  });
  
  $('#bNombre').dialog(
  {
    title : "Buscar Por Nombre",
    autoOpen:false,
    buttons :   {
            'Buscar' : function() { $(this).submit() },
            'Cancelar' :  function() { $(this).dialog('close'); }
          }
  });
  
  $(".striped tbody tr:odd").addClass("odd");
  $(".striped tbody tr:even").addClass("even");
  $(".deduced-674").addClass("bg-danger");
  //$('.button, button').button();
  // Workaround a bug found added in JQuery 1.5 + JQuery UI 1.8.x
  // $('#ui-datepicker-div').hide();
});
