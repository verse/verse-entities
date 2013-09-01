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
This module includes class VerseUser representing verse user
"""

class VerseUser(object):
    """
    A VerseUser is class representing user
    """

    def __init__(self, user_node):
        """
        Constructor of VerseUser
        """
        self._node = user_node
        self._tg_info = None
        self._tag_name = None
        # Add this user to the dictionary of users
        self._node.session.users[self._node.id] = self

    def __str__(self):
        """
        Print method of this class
        """
        return 'User (' + \
                str(self._node.id) + \
                '): ' + \
                self.name

    @property
    def name(self):
        """
        The name is property of VerseUser
        """
        try:
            name = self._tag_name.value
        except AttributeError:
            return ""
        else:
            return name[0]
