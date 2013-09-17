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

import verse as vrs
from . import verse_node, verse_tag_group, verse_tag


# TODO: this should be in verse module too
TG_INFO_CT = 0
TAG_USERNAME_CT = 0


class VerseUser(verse_node.VerseNode):
    """
    A VerseUser is class representing user
    """

    custom_type = 6 # TODO: replace with constant

    def __init__(self, *args, **kwargs):
        """
        Constructor of VerseUser
        """

        # Call parent init method
        super(VerseUser, self).__init__(*args, **kwargs)

        # Create tag group and tag due to specification
        self._tg_info = verse_tag_group.VerseTagGroup(node=self, custom_type=TG_INFO_CT)
        self._tg_info._tag_name = verse_tag.VerseTag(tg=self._tg_info, \
            data_type=vrs.VALUE_TYPE_STRING8, \
            count=1, \
            custom_type=TAG_USERNAME_CT)

        # Add this verse user to the dictionary of users
        self.session.users[self.id] = self

    def __str__(self):
        """
        Print method of this class
        """
        return 'User (' + \
                str(self.id) + \
                '): ' + \
                self.name

    @property
    def name(self):
        """
        The name is property of VerseUser
        """
        try:
            name = self._tg_info._tag_name.value
        except AttributeError:
            return ""
        else:
            try:
                return name[0]
            except TypeError:
                return ""

    @classmethod
    def _receive_node_destroy(cls, session, node_id):
        """
        Static method that is called, when node with user is destroyed and
        this user is no longer valid user.
        """
        # Remove verse user from the dictionary of users
        if node_id in session.users:
            del session.users[node_id]
        return super(VerseUser, cls)._receive_node_destroy(session, node_id)