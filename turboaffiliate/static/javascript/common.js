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
  
  $(".striped tbody tr:odd").addClass("odd");
  $(".striped tbody tr:even").addClass("even");
  
  $('#calcular').click(function(e)
  {
    var time = $('#tiempo').val();
    var type = $('#interes').val() / (1200);
    var capital = $('#capital').val();
    $('#cuota').val(capital * type / (1 - Math.pow(type + 1, -time))); 
  });
});
