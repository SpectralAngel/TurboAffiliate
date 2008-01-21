#!/usr/bin/python
# -*- coding: utf8 -*-
#
# utility.py
# This file is part of WebAc
#
# Copyright © 2007 Carlos Flores <cafg10@gmail.com>
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

class Cleaner(object):
	def __init__(self):
		pass
	
	def null(self, li):
		"""Removes Null values from strings to use them safely in SQL
		"""
		for string in li:
			if type(string) == str:
				string = string.replace('\x00', '')
	
	def identification(self, string):
		"""Cleans the passed string to be used in unique card-ID numbers.
		"""
		string = str(string)
		self.null([string])
		#string = string.replace('-', '')
		string = string.replace(' ', '')
		return string
