#!/usr/bin/python
# -*- coding: utf8 -*-
#
# num2stres.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2007 Carlos Flores <cafg10@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from decimal import Decimal
from plugin import num2word_ES

def parse(number):
	string = str(int(number))
	cents = Decimal(str(int(number) - int(number)))  * Decimal(100)
	if cents != 0:
		cents = " con " + num2word_ES.to_card(int(cents))
	else:
		cents = " exactos"
	return (num2word_ES.to_card(int(number)) + cents).capitalize()
