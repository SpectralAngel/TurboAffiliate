$(document).ready(function(e)
{
  $('.agregarSolicitud').dialog(
  {
    title : "Agregar Solicitud",
    modal:true,
    autoOpen:false,
    width:380,
    minWidth:380,
    buttons:{
             'Agregar' : function() { $(this).submit() },
             Cancelar :  function() { $(this).dialog('close'); }
            }
  });
  
  $('.verDeducciones').dialog(
  {
    title : "Mostrar Deducciones",
    modal:true,
    autoOpen:false,
    width:380,
    minWidth:380,
    buttons:{
             'Mostrar' : function() { $(this).submit() },
             Cancelar :  function() { $(this).dialog('close'); }
            }
  });
  
  
  $('#deduccionAnual').dialog(
  {
    title : "Mostrar Deducciones",
    modal:true,
    autoOpen:false,
    width:380,
    minWidth:380,
    buttons:{
             'Mostrar' : function() { $(this).submit() },
             'Cancelar' :  function() { $(this).dialog('close'); }
            }
  });
  $('.agregarObservacion').dialog(
  {
    title : "Agregar Observación",
    modal:true,
    autoOpen:false,
    width:380,
    minWidth:380,
    buttons:{
               'Agregar' : function() { $(this).submit() },
               Cancelar :  function() { $(this).dialog('close'); }
            }
  })
  ;$('.desactivar').dialog(
  {
    title : "Desactivar Afiliado",
    modal:true,
    autoOpen:false,
    width:380,
    minWidth:380,
    buttons:{
               'Desactivar' : function() { $(this).submit() },
               Cancelar :  function() { $(this).dialog('close'); }
            }
  });
  $('.editar').dialog(
  {
    title : "Editar Afiliado",
    modal:true,
    autoOpen:false,
    width:380,
    minWidth:380,
    buttons:{
             'Guardar' : function() { $(this).submit() },
             Cancelar :  function() { $(this).dialog('close'); }
            }
  });
  $('.extra').dialog(
  {
    title : "Añadir Deducción Extra",
    modal:true,
    autoOpen:false,
    width:480,
    minWidth:480,
    buttons:{
             'Agregar' : function() { $(this).submit() },
             Cancelar :  function() { $(this).dialog('close'); }
            }
  });
  $('.jubilar').dialog(
  {
    title : "Jubilar o Cambiar Fecha de Jubilación",
    modal:true,
    autoOpen:false,
    width:480,
    minWidth:480,
    buttons:{
               'Efectuar Cambio' : function() { $(this).submit() },
               Cancelar :  function() { $(this).dialog('close'); }
            }
  })
  ;$('.muerte').dialog(
  {
    title : "Reportar Fallecimiento",
    modal:true,
    autoOpen:false,
    width:480,
    minWidth:480,
    buttons:{
               'Efectuar Cambio' : function() { $(this).submit() },
               Cancelar :  function() { $(this).dialog('close'); }
            }
  });
  ;$('#Prestamo').dialog(
  {
    title : "Agregar Préstamo",
    modal:true,
    autoOpen:false,
    width:480,
    minWidth:480,
    buttons:{
               'Agregar' : function() { $(this).submit() },
               Cancelar :  function() { $(this).dialog('close'); }
            }
  });
});
