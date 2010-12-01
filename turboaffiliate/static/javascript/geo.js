
var Geo = {
  departamento : function(url)
  {
    $.get(url+'/departamentos?tg_format=json', function(data)
    {
      $.each(data.departamentos, function(i, departamento)
      {
        var option = $('<option />');
        option.val(departamento.id);
        option.text(departamento.nombre);
        $('.departamento').append(option);
      });
    });
  },
  
  municipio : function(url, departamento, municipios)
  {
    $.get(url + '/municipios/' + departamento + '?tg_format=json', function(data)
    {
      $(municipios).empty();
      $.each(data.municipios, function(i, municipio)
      {
        var option = $('<option />');
        option.val(municipio.id);
        option.text(municipio.nombre);
        $(municipios).append(option);
      });
    });
  },
  
  municipioE : function(url, departamento, municipios)
  {
    $.get(url + '/municipios/' + departamento + '?tg_format=json', function(data)
    {
      $.each(data.municipios, function(i, municipio)
      {
        var option = $('<option />');
        option.val(municipio.id);
        option.text(municipio.nombre);
        $(municipios).append(option);
      });
    });
  }
}
