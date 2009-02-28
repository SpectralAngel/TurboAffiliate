
function get_account(e)
{
	e.preventDefault();
	var code = $('#account').val();
	var url = '/account/' + code// + '?tg_format=json';
	$('#target').html('Buscando...');
	$.getJSON(url, function(json)
	{
		if(json.account == null)
		{
			$('#target').html('La Cuenta no ha sido encontrada');
		}
		else
		{
			$('#target').html(json.account.name);
			// $('#detail').val(json.account.name);
			$('#unit').val(json.account.amount);
		}
	});
}
