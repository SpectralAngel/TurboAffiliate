$(document).ready(function(e) {
$('.pagar').dialog(
{
    title: "Agregar un Pago",
    modal: true,
    autoOpen: false,
    width: 380,
    minWidth: 380,
    buttons: {
        'Agregar': function(){
            $(this).submit()
        },
        Cancelar: function(){
            $(this).dialog('close');
        }
    }
});
$('.deduccion').dialog(
{
    title: "Agregar una Deducción",
    modal: true,
    autoOpen: false,
    width: 520,
    minWidth: 520,
    buttons: {
        'Agregar': function(){
            $(this).submit()
        },
        Cancelar: function(){
            $(this).dialog('close');
        }
    }
});
$('#refinanciar').dialog(
{
    title: "Crear un Refinanciamiento",
    modal: true,
    autoOpen: false,
    width: 520,
    minWidth: 520,
    buttons: {
        'Refinanciar': function(){
            $(this).submit()
        },
        Cancelar: function(){
            $(this).dialog('close');
        }
    }
});
$('#cambiarTiempo').dialog(
{
    title: "Cambiar Periodo de Pago",
    autoOpen: false,
    width: 520,
    minWidth: 520,
    buttons: {
        'Guardar': function(){
            $(this).submit()
        },
        'Cancelar': function(){
            $(this).dialog('close');
        }
    }
});
$('#cambiarSaldo').dialog(
{
    title: "Cambiar Saldo",
    modal: true,
    autoOpen: false,
    width: 520,
    minWidth: 520,
    buttons: {
        'Guardar': function(){
            $(this).submit()
        },
        'Cancelar': function(){
            $(this).dialog('close');
        }
    }
});
$('#cambiarMonto').dialog(
{
    title: "Cambiar Monto",
    modal: true,
    autoOpen: false,
    width: 520,
    minWidth: 520,
    buttons: {
        'Guardar': function(){
            $(this).submit()
        },
        'Cancelar': function(){
            $(this).dialog('close');
        }
    }
});
$('#cambiarCuota').dialog(
{
    title: "Cambiar Cuota",
    modal: true,
    autoOpen: false,
    width: 520,
    minWidth: 520,
    buttons: {
        'Guardar': function(){
            $(this).submit()
        },
        'Cancelar': function(){
            $(this).dialog('close');
        }
    }
});
});
