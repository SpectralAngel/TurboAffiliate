#!/usr/bin/python
# -*- coding: utf8 -*-
#
# model.py
# This file is part of TurboAffiliate
#
# Copyright (c) 2007 - 2010 Carlos Flores <cafg10@gmail.com>
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

from sqlobject import DateTimeCol, RelatedJoin, SQLObjectNotFound
from turbogears import identity
from turboaffiliate import release
from college import *

hub = PackageHub("turboaffiliate")
__connection__ = hub

class AppConfigError(Exception):
	pass

class Application(SQLObject):
	"""Application Specific Information

	It holds data important only to the aplication
	"""
	lastDrop = DateCol()
	version = StringCol(length=8, notNone=True)
	db_version = IntCol()

	@classmethod
	def createTable(cls, *args, **kw):
		super(Application, cls).createTable(*args, **kw)
		count = Application.select().count()
		if count == 0:
			Application(version=release.version, 
						db_version=9, 
						lastDrop=date.today())
		elif count > 1:
			raise AppConfigError
		elif count == 1:
			app = Application.get(1)
			app.version = release.version
			app.db_version = 9

# identity models.
class Visit(SQLObject):
	class sqlmeta:
		table = "visit"
	
	visit_key = StringCol(length=40, alternateID=True, 
						  alternateMethodName="by_visit_key")
	created = DateTimeCol(default=datetime.now)
	expiry = DateTimeCol()
	
	def lookup_visit(cls, visit_key):
		try:
			return cls.by_visit_key(visit_key)
		except SQLObjectNotFound:
			return None
	lookup_visit = classmethod(lookup_visit)

class VisitIdentity(SQLObject):
	visit_key = StringCol(length=40, alternateID=True, 
						  alternateMethodName="by_visit_key")
	user_id = IntCol()

class Group(SQLObject):
	"""
	An ultra-simple group definition.
	"""

	# names like "Group", "Order" and "User" are reserved words in SQL
	# so we set the name to something safe for SQL
	class sqlmeta:
		table = "tg_group"
	
	group_name = UnicodeCol(length=16, alternateID=True, 
							alternateMethodName="by_group_name")
	display_name = UnicodeCol(length=255)
	created = DateTimeCol(default=datetime.now)
	
	# collection of all users belonging to this group
	users = RelatedJoin("User", intermediateTable="user_group", 
						joinColumn="group_id", otherColumn="user_id")
	
	# collection of all permissions for this group
	permissions = RelatedJoin("Permission", joinColumn="group_id", 
							  intermediateTable="group_permission", 
							  otherColumn="permission_id")

class User(SQLObject):
	"""
	Reasonably basic User definition. Probably would want additional attributes.
	"""
	# names like "Group", "Order" and "User" are reserved words in SQL
	# so we set the name to something safe for SQL
	class sqlmeta:
		table = "tg_user"
	
	user_name = UnicodeCol(length=16, alternateID=True, 
						   alternateMethodName="by_user_name")
	email_address = UnicodeCol(length=255, alternateID=True, 
							   alternateMethodName="by_email_address")
	display_name = UnicodeCol(length=255)
	password = UnicodeCol(length=40)
	created = DateTimeCol(default=datetime.now)

	# groups this user belongs to
	groups = RelatedJoin("Group", intermediateTable="user_group", 
						 joinColumn="user_id", otherColumn="group_id")
	
	loans = MultipleJoin("Loan", joinColumn="aproval_id")
	logs = MultipleJoin("Logger", joinColumn="user_id")
	
	def _get_permissions(self):
		perms = set()
		for g in self.groups:
			perms = perms | set(g.permissions)
		return perms
	
	def has_permission(self, permission):
		
		perms = (p.permission_name for p in self._get_permissions())
		if permission in perms: return True
		else: return False
	
	def _set_password(self, cleartext_password):
		"Runs cleartext_password through the hash algorithm before saving."
		hash = identity.encrypt_password(cleartext_password)
		self._SO_set_password(hash)
	
	def set_password_raw(self, password):
		"Saves the password as-is to the database."
		self._SO_set_password(password)

class Permission(SQLObject):
	permission_name = UnicodeCol(length=16, alternateID=True, 
								 alternateMethodName="by_permission_name")
	description = UnicodeCol(length=255)
	
	groups = RelatedJoin("Group", 
						intermediateTable="group_permission", 
						 joinColumn="permission_id", 
						 otherColumn="group_id")

class Logger(SQLObject):
	
	user = ForeignKey("User")
	action = UnicodeCol(default="")
	day = DateTimeCol(default=datetime.now)

