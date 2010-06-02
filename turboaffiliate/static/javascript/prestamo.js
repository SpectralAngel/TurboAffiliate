$(document).ready(function(e)
{
    $('.ui-button').hover(
			function(){ $(this).addClass("ui-state-hover"); },
			function(){ $(this).removeClass("ui-state-hover"); }
		).mousedown(function(){ $(this).addClass("ui-state-active"); }
		).mouseup(function(){ $(this).removeClass("ui-state-active"); }
	);
    $('input.date-picker').datepicker({
        dateFormat: 'yy-mm-dd',
        changeMonth: true,
        changeYear: true,
        yearRange: 'c-70:c+5'
    });
    $('input.datepicker').datepicker({
        dateFormat: 'dd/mm/yy',
        changeMonth: true,
        changeYear: true,
        yearRange: 'c-70:c+5'
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
    $('#refinanciar').dialog(
    {
        title : "Crear un Refinanciamiento",
        modal:true,
        autoOpen:false,
        width:520,
        minWidth:520,
        buttons:{
                     'Refinanciar' : function() { $(this).submit() },
                     Cancelar :  function() { $(this).dialog('close'); }
                }
    });
    $('#calcular').click(function(e)
    {
    	var time = $('#tiempo').val();
    	var type = $('#interes').val() / (1200);
    	var capital = $('#capital').val();
    	$('#cuota').val(capital * type / (1 - Math.pow(type + 1, -time))); 
    });
});
