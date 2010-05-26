$(document).ready(function(e)
{
    $('input.datepicker').datepicker({
        dateFormat: 'dd/mm/yy',
        changeMonth: true,
        changeYear: true,
    });
    
    $('.AgregarReintegro').dialog(
    {
        title : "Agregar Reintegro",
        modal:true,
        autoOpen:false,
        width:380,
        minWidth:380,
        buttons:{
                     'Agregar Reintegro' : function() { $(this).submit() },
                     Cancelar :  function() { $(this).dialog('close'); }
                }
    });
    $('.PagarReintegro').dialog(
    {
        title : "Pagar Reintegro",
        modal:true,
        autoOpen:false,
        width:380,
        minWidth:380,
        buttons:{
                     'Pagar Reintegro' : function() { $(this).submit() },
                     Cancelar :  function() { $(this).dialog('close'); }
                }
    });
});

function pagarReintegro(reintegro)
{
    $('.PagarReintegro').dialog('open');
    $('#reintegro').val(reintegro);
}
