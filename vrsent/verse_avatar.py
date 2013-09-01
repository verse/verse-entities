# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

"""
This module include class VerseAvatar representing verse avatar/client
"""

class VerseAvatar(object):
	"""
	Class representing Verse avatar/client
	"""

	def __init__(self, avatar_node):
		"""
		Constructor of class
		"""
		self._node = avatar_node
		self._info_node = None
		self._tg_info = None
		self._tag_hostname = None
		self._tag_login_time = None
		self._tag_client_name = None
		self._tag_client_version = None
		self._user_id = None

	def __str__(self):
		"""
		Print method of this class
		"""
		return 'Avatar (' + \
				str(self._node.id) + \
				'): ' + \
				self.username + \
				'@' + \
				self.hostname + \
				' (' + \
				self.client_name + \
				':' + \
				self.client_version + \
				')'

	@property
	def hostname(self):
		"""
		hostname property
		"""
		try:
			hostname = self._tag_hostname.value
		except AttributeError:
			return ""
		else:
			return hostname[0]

	@property
	def login_time(self):
		"""
		login time property
		"""
		try:
			login_time = self._tag_login_time.value
		except AttributeError:
			return ""
		else:
			return login_time[0]

	@property
	def client_name(self):
		"""
		client name property
		"""
		try:
			client_name = self._tag_client_name.value
		except AttributeError:
			return ""
		else:
			return client_name[0]

	@property
	def client_version(self):
		"""
		client name property
		"""
		try:
			client_version = self._tag_client_version.value
		except AttributeError:
			return ""
		else:
			return client_version[0]

	@property
	def username(self):
		"""
		user of this avatar
		"""
		try:
			user = self._node.session.users[self._user_id]
		except KeyError:
			return ""
		else:
			return user.name