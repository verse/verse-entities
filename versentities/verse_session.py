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


import verse as vrs
from . import verse_node, verse_tag_group, verse_tag, verse_layer


class VerseSession(vrs.Session):
    """
    Class with session used in this client
    """

    # The list of session instances
    __sessions = {}

    # The dictionary of nodes that belongs to this session
    nodes = {}

    # The dictionary of nodes that were created by this client and Verse
    # server has not sent confirmation about creating of these nodes.
    # Each custom_type of node has its own queue
    my_node_queues = {}

    def __init__(self, hostname="localhost", service="12345", flags=vrs.DGRAM_SEC_DTLS):
        """
        Constructor of VerseSession
        """
        # Call method of parent class to connect to Verse server
        super(VerseSession, self).__init__(hostname, service, flags)
        self._fps = 60.0
        self.username = None
        self.password = None
        self.debug_print = False
        self.state = 'CONNECTING'
        self.__class__.__sessions[hostname+':'+service] = self


    def _receive_user_authenticate(self, username, methods):
        """
        Callback method for user authenticate
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_user_authenticate(self, username, password)
        # Default method to get username and password
        if username=="":
            if self.username is None:
                self.username = username = input('username: ')
            else:
                username = self.username
            self.send_user_authenticate(username, vrs.UA_METHOD_NONE, "")
        else:
            if methods.count(vrs.UA_METHOD_PASSWORD)>=1:
                if self.password is None:
                    self.password = password = input('password: ')
                else:
                    password = self.password
                self.send_user_authenticate(username, vrs.UA_METHOD_PASSWORD, password)
            else:
                print("Unsuported authenticate method")


    @property
    def fps(self):
        """
        Getter of session FPS
        """
        return self._fps


    @fps.setter
    def fps(self, val):
        """
        Setter of session FPS
        """
        self._fps = val
        self.send_fps(val)


    def _receive_connect_accept(self, user_id, avatar_id):
        """
        Custom callback method for connect accept
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_connect_accept(self, user_id, avatar_id)
        # Save important informations
        self.user_id = user_id
        self.avatar_id = avatar_id
        # "Subscribe" to root node
        self.root_node = verse_node.VerseNode(session=self, node_id=0, parent=None, user_id=100, custom_type=0)
        self.state = 'CONNECTED'


    def _receive_node_create(self, node_id, parent_id, user_id, custom_type):
        """
        Custom callback method that is called, when client received
        command node_create
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_node_create(node_id, parent_id, user_id, custom_type)
        # Call calback method of model
        node = verse_node.VerseNode._receive_node_create(self, node_id, parent_id, user_id, custom_type)

        return node


    def _receive_node_destroy(self, node_id):
        """
        Custom callback method for command node destroy
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_node_destroy(node_id)
        # Call callback method of model
        node = verse_node.VerseNode._receive_node_destroy(self, node_id)

        return node


    def _receive_node_link(self, parent_node_id, child_node_id):
        """
        Custom callback method that is called, when client receive command changing
        link between nodes
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_node_link(parent_node_id, child_node_id)
        # Call calback method of model
        child_node = verse_node.VerseNode._receive_node_link(self, parent_node_id, child_node_id)

        return child_node


    def _receive_taggroup_create(self, node_id, taggroup_id, custom_type):
        """
        Custom callback method that is called, when client received command
        tag group create
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_taggroup_create(node_id, taggroup_id, custom_type)
        # Call calback method of model
        tg = verse_tag_group.VerseTagGroup._receive_tg_create(self, node_id, taggroup_id, custom_type)
        return tg


    def _receive_tag_create(self, node_id, taggroup_id, tag_id, data_type, count, custom_type):
        """
        Custom callback method that is called, when client receive command tag create
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_tag_create(node_id, taggroup_id, tag_id, data_type, count, custom_type)
        # Call calback method of model
        tag = verse_tag.VerseTag._receive_tag_create(self, node_id, taggroup_id, tag_id, data_type, count, custom_type)

        return tag

    def _receive_tag_set_value(self, node_id, taggroup_id, tag_id, value):
        """
        Custom callback method that is called, when client reveive command tag set value
        """
        # Call method of parent class
        if self.debug_print is True:
            super(VerseSession, self)._receive_tag_set_value(node_id, taggroup_id, tag_id, value)
        # Call callback method of model
        tag = verse_tag.VerseTag._receive_tag_set_value(self, node_id, taggroup_id, tag_id, value)

        return tag


    def _receive_connect_terminate(self, error):
        """
        Custom callback method for fake connect terminate command
        """
        # Call method of parent class
        if self.debug_print is True:
            super(VerseSession, self)._receive_connect_terminate(error)
        self.state = 'DISCONNECTED'
