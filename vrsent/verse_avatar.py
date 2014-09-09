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


class HostnameTag(verse_tag.VerseTag):
    """
    VerseTag subclass for storing hostname
    """

    custom_type = TAG_HOSTNAME_CT
    tg_custom_type = TG_INFO_CT
    node_custom_type = vrs.AVATAR_INFO_NODE_CT

    def __init__(self, tg, tag_id=None, data_type=vrs.VALUE_TYPE_STRING8, \
        count=1, custom_type=TAG_HOSTNAME_CT, value=None):
        """
        Constructor of HostnameTag
        """
        super(HostnameTag, self).__init__(tg=tg, \
            tag_id=tag_id, \
            data_type=data_type, \
            count=count, \
            custom_type=custom_type, \
            value=value)


class LoginTimeTag(verse_tag.VerseTag):
    """
    VerseTag subclass for storing login time
    """

    custom_type = TAG_LOGIN_TIME_CT
    tg_custom_type = TG_INFO_CT
    node_custom_type = vrs.AVATAR_INFO_NODE_CT

    def __init__(self, tg, tag_id=None, data_type=vrs.VALUE_TYPE_UINT64, \
        count=1, custom_type=TAG_LOGIN_TIME_CT, value=None):
        """
        Constructor of LoginTimeTag
        """
        super(LoginTimeTag, self).__init__(tg=tg, \
            tag_id=tag_id, \
            data_type=data_type, \
            count=count, \
            custom_type=custom_type, \
            value=value)


class ClientNameTag(verse_tag.VerseTag):
    """
    VerseTag subclass for storing client name
    """

    custom_type = TAG_CLIENT_NAME_CT
    tg_custom_type = TG_INFO_CT
    node_custom_type = vrs.AVATAR_INFO_NODE_CT

    def __init__(self, tg, tag_id=None, data_type=vrs.VALUE_TYPE_STRING8, \
        count=1, custom_type=TAG_CLIENT_NAME_CT, value=None):
        """
        Constructor of ClientNameTag
        """
        super(ClientNameTag, self).__init__(tg=tg, \
            tag_id=tag_id, \
            data_type=data_type, \
            count=count, \
            custom_type=custom_type, \
            value=value)


class ClientVersionTag(verse_tag.VerseTag):
    """
    VerseTag subclass for storing client version
    """

    custom_type = TAG_CLIENT_VERSION_CT
    tg_custom_type = TG_INFO_CT
    node_custom_type = vrs.AVATAR_INFO_NODE_CT

    def __init__(self, tg, tag_id=None, data_type=vrs.VALUE_TYPE_STRING8, \
        count=1, custom_type=TAG_CLIENT_VERSION_CT, value=None):
        """
        Constructor of ClientVersionTag
        """
        super(ClientVersionTag, self).__init__(tg=tg, \
            tag_id=tag_id, \
            data_type=data_type, \
            count=count, \
            custom_type=custom_type, \
            value=value)


class VerseAvatarInfo(verse_node.VerseNode):
    """
    Class storing information about Verse avatar/client
    """

    custom_type = vrs.AVATAR_INFO_NODE_CT

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
        self._tg_info._tag_hostname = HostnameTag(tg=self._tg_info)
        self._tg_info._tag_login_time = LoginTimeTag(tg=self._tg_info)
        self._tg_info._tag_client_name = ClientNameTag(tg=self._tg_info)
        self._tg_info._tag_client_version = ClientVersionTag(tg=self._tg_info)


class VerseAvatar(verse_node.VerseNode):
    """
    Class representing Verse avatar/client
    """

    custom_type = vrs.AVATAR_NODE_CT

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
            return 0
        else:
            try:
                return login_time[0]
            except TypeError:
                return 0

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
        This method is called, when server destroyed avatar node
        """
        # When this is avatar node, then remove avatar from dictionary of
        # avatars
        avatar = super(VerseAvatar, cls)._receive_node_destroy(session, node_id)
        if node_id in session.avatars:
            session.avatars.pop(node_id)
        return avatar

    @classmethod
    def _receive_node_perm(cls, session, node_id, user_id, perm):
        """
        This method is called, when client received command node_perm.
        This command specify user assigned to this avatar.
        """
        # When client received user permission for other user then super_user
        # or other_users, then this indicates user of this avatar/client
        if user_id != 100 and user_id != 65535:
            avatar = session.avatars[node_id]
            avatar._user_id = user_id
        return super(VerseAvatar, cls)._receive_node_perm(session, node_id, user_id, perm)
