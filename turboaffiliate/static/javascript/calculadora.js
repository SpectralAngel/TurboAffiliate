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
                 'Reiniciar' : function()
                 {
                   $(':input','#calcular')
                    .not(':button, :submit, :reset, :hidden')
                    .val('').removeAttr('checked')
                    .removeAttr('selected');
                 },
                 'Calcular' : function() {
                   var time = $('#tiempoc').val();
                   var type = $('#interesc').val() / (1200);
                   var capital = $('#capitalc').val();
                   $('#cuotac').val(capital * type / (1 - Math.pow(type + 1, -time)));
                 },
                'Cerrar' : function(){ $(this).dialog('close'); }
              },
  });
  $('#paymentCalc').bind('click',function()
  {
   var time = $('#tiempo').val();
   var type = $('#interes').val() / (1200);
   var capital = $('#capital').val();
   $('#payment').val(capital * type / (1 - Math.pow(type + 1, -time)));
 });
});
