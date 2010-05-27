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
    });
    
    $('.pagar').dialog(
    {
        title : "Agregar un Pago",
        modal:true,
        autoOpen:false,
        width:380,
        minWidth:380,
        buttons:{
                     'Agregar' : function() { $(this).submit() },
                     Cancelar :  function() { $(this).dialog('close'); }
                }
    });
    $('.deduccion').dialog(
    {
        title : "Agregar una Deducción",
        modal:true,
        autoOpen:false,
        width:520,
        minWidth:520,
        buttons:{
                     'Agregar' : function() { $(this).submit() },
                     Cancelar :  function() { $(this).dialog('close'); }
                }
    });
});
