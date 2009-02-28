// jquery.json.js
// This file is part of TurboAffiliate
//
// Copyright © 2007 Carlos Flores <cafg10@gmail.com>
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
function get_account(e)
{
	e.preventDefault();
	var code = $('#account').val();
	var url = '/accounting/account/' + code + '?tg_format=json';
	$('#account_result').html('Buscando...');
	$.getJSON(url, function(json)
	{
		if(json.account == null)
		{
			$('#account_result').html('Cuenta no encontrada');
		}
		else
		{
			var result = 'Cuenta: ' + json.account.name;
			$('#account_result').html(result);
		}
	});
}
