
function get_cuota(e)
{
	e.preventDefault();
	var time = $('#time').val();
	var type = $('#type').val() / (1200);
	var capital = $('#capital').val();
	$('#cuota').html('L. ' + Math.round(capital * type / (1 - Math.pow(type + 1, -time))));
}
