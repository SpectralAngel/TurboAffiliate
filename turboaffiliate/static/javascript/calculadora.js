$(document).ready(function(e)
{
  $('.calculadora').dialog(
  {
      title : "Calculadora de Préstamos",
      modal:false,
      autoOpen:false,
      width:380,
      minWidth:380,
            
      buttons:{
                 'Reiniciar' : function() { $(this).reset(); },
                 'Calcular' : function() {
                   var time = $('#tiempoc').val();
                   var type = $('#interesc').val() / (1200);
                   var capital = $('#capitalc').val();
                   $('#cuotac').val(capital * type / (1 - Math.pow(type + 1, -time)));
                 },
                'Cerrar' : function(){ $(this).dialog('close'); }
              },
  });
});