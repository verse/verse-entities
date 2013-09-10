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

import verse as vrs
from . import verse_node, verse_tag_group, verse_tag


# TODO: this should be in verse module too
TG_INFO_CT = 0
TAG_HOSTNAME_CT = 0
TAG_LOGIN_TIME_CT = 1
TAG_CLIENT_NAME_CT = 2
TAG_CLIENT_VERSION_CT = 3


class VerseAvatarInfo(verse_node.VerseNode):
    """
    Class storing information about Verse avatar/client
    """

    custom_type = 5 # TODO: replace with constant from verse module

    def __init__(self, *args, **kwargs):
        """
        Constructor of class
        """
        # Call parent init method
        super(VerseAvatarInfo, self).__init__(*args, **kwargs)
        # Add reference to parent (avatar) node
        self.parent._info_node = self
        # Create tag group with info information due to specification
        self._tg_info = verse_tag_group.VerseTagGroup(node=self, custom_type=TG_INFO_CT)
        # Create tags due to specification
        self._tg_info._tag_hostname = verse_tag.VerseTag(tg=self._tg_info, \
            data_type=vrs.VALUE_TYPE_STRING8, \
            count=1, \
            custom_type=TAG_HOSTNAME_CT)
        self._tg_info._tag_login_time = verse_tag.VerseTag(tg=self._tg_info, \
            data_type=vrs.VALUE_TYPE_UINT64, \
            count=1, \
            custom_type=TAG_LOGIN_TIME_CT)
        self._tg_info._tag_client_name = verse_tag.VerseTag(tg=self._tg_info, \
            data_type=vrs.VALUE_TYPE_STRING8, \
            count=1, \
            custom_type=TAG_CLIENT_NAME_CT)
        self._tg_info._tag_client_version = verse_tag.VerseTag(tg=self._tg_info, \
            data_type=vrs.VALUE_TYPE_STRING8, \
            count=1, \
            custom_type=TAG_CLIENT_VERSION_CT)


class VerseAvatar(verse_node.VerseNode):
    """
    Class representing Verse avatar/client
    """

    custom_type = 4  # TODO: replace with constant from verse module

    def __init__(self, *args, **kwargs):
        """
        Constructor of class
        """
        # Call parent init method
        super(VerseAvatar, self).__init__(*args, **kwargs)
        # Info node and user_id could not be known yet
        self._info_node = None
        self._user_id = None
        # Add this avatar to the list of avatars
        self.session.avatars[self.id] = self

    def __str__(self):
        """
        Print method of this class
        """
        return 'Avatar (' + \
                str(self.id) + \
                '): ' + \
                self.username + \
                '@[' + \
                self.hostname + \
                '] (' + \
                self.client_name + \
                ' ' + \
                self.client_version + \
                ')'

    @property
    def hostname(self):
        """
        hostname property
        """
        try:
            hostname = self._info_node._tg_info._tag_hostname.value
        except AttributeError:
            return ""
        else:
            try:
                return hostname[0]
            except TypeError:
                return ""

    @property
    def login_time(self):
        """
        login time property
        """
        try:
            login_time = self._info_node._tg_info._tag_login_time.value
        except AttributeError:
            return ""
        else:
            try:
                return login_time[0]
            except TypeError:
                return ""

    @property
    def client_name(self):
        """
        client name property
        """
        try:
            client_name = self._info_node._tg_info._tag_client_name.value
        except AttributeError:
            return ""
        else:
            try:
                return client_name[0]
            except TypeError:
                return ""

    @property
    def client_version(self):
        """
        client name property
        """
        try:
            client_version = self._info_node._tg_info._tag_client_version.value
        except AttributeError:
            return ""
        else:
            try:
                return client_version[0]
            except TypeError:
                return ""

    @property
    def username(self):
        """
        user of this avatar
        """
        try:
            user = self.session.users[self._user_id]
        except KeyError:
            return ""
        else:
            return user.name

    @classmethod
    def _receive_node_destroy(cls, session, node_id):
        """
        """
        # When this is avatar node, then remove avatar from dictionary of
        # avatars
        if node_id in session.avatars:
            del session.avatars[node_id]
        return super(VerseAvatar, cls)._receive_node_destroy(cls, session, node_id)

    @classmethod
    def _receive_node_perm(cls, session, node_id, user_id, perm):
        """
        """
        # When client received user permission for other user then super_user
        # or other_users, then this indicates user of this avatar/client
        if user_id != 100 and user_id != 65535:
            avatar = session.avatars[node_id]
            avatar._user_id = user_id
        return super(VerseAvatar, cls)._receive_node_perm(cls, session, node_id, user_id, perm)
