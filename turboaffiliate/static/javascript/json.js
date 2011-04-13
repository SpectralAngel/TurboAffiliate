
var JSON = {
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
  },
  
  cotizacion : function(url)
  {
    $.get(url + '/cotizacion?tg_format=json',function(data)
    {
      $.each(data.cotizaciones, function(i, cotizacion)
      {
        var option = $('<option />');
        option.val(cotizacion.id);
        option.text(cotizacion.nombre)
        $('.cotizaciones').append(option);
      });
    });
  },
  bancos : function(url)
  {
    $.get(url + '/bancos?tg_format=json', function(data)
    {
      $.each(data.bancos, function(i, banco)
      {
        var option = $('<option />');
        option.val(banco.id);
        option.text(banco.nombre)
        $('.bancos').append(option);
      });
    });
  },
  jubilados : function(url)
  {
    $.get(url + '/jubilados?tg_format=json', function(data)
    {
      $.each(data.cotizaciones, function(i, cotizacion)
      {
        var option = $('<option />');
        option.val(cotizacion.id);
        option.text(cotizacion.nombre)
        $('.jubilados').append(option);
      });
    });
  }
}
