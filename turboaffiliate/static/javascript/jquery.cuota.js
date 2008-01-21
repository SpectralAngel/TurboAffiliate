
function get_cuota(e)
{
	e.preventDefault();
	var time = $('#months').val();
	var type = $('#interest').val() / (1200);
	var capital = $('#amount').val();
	$('#payment').val(capital * type / (1 - Math.pow(type + 1, -time)));
}
