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
This module includes class VerseSession representing verse session
at verse client.
"""


import verse as vrs
from . import verse_node, verse_tag_group, verse_tag, verse_layer
import threading
import time


class CallbackUpdate(threading.Thread):
    """
    This class is used to run callback_update method in
    own thread
    """

    def __init__(self, session, *args, **kwargs):
        """
        This method initialize object of thread
        """
        super(CallbackUpdate, self).__init__(*args, **kwargs)
        self.session = session

    def run(self):
        """
        This method is executed, when thread is started.
        """
        # Never ending loop that executed callback functions,
        # when commands are received from Verse server
        while(self.session.state != 'DISCONNECTED'):
            self.session.callback_update()
            time.sleep(1.0 / self.session.fps)


class VerseSession(vrs.Session):
    """
    Class with session used in this client
    """

    # The list of session instances
    __sessions = {}

    # The dictionary of VerseNode subclasses (custom_type is used as key)
    node_custom_types = {}

    def __init__(self, hostname="localhost", service="12345", \
            flags=vrs.DGRAM_SEC_DTLS, callback_thread=False, \
            username=None, password=None):
        """
        Constructor of VerseSession
        """
        # Call method of parent class to connect to Verse server
        super(VerseSession, self).__init__(hostname, service, flags)
        self._fps = 60.0
        self.username = username
        self.password = password
        self.debug_print = False
        self.state = 'CONNECTING'
        # Add this session from list of sessions
        self.__class__.__sessions[hostname + ':' + service] = self
        # The dictionary of nodes that belongs to this session
        self.nodes = {}
        # The dictionary of users that belongs to this session
        self.users = {}
        # The dictionary of avatars/client that belongs to this session
        self.avatars = {}
        # The dictionary of avatar info nodes
        self._avatar_info_nodes = {}
        # The dictionary of nodes that were created by this client and Verse
        # server has not sent confirmation about creating of these nodes.
        # Each custom_type of node has its own queue
        self.my_node_queues = {}
        self.user_id = None
        self.avatar_id = None
        self.root_node = None
        # Start callback_update thread
        if callback_thread is True:
            self.cb_thread = CallbackUpdate(self)
            self.cb_thread.start()

    def __del__(self):
        """
        Destructor of VerseSession
        """
        pass

    def _receive_user_authenticate(self, username, methods):
        """
        Callback method for user authenticate
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_user_authenticate(username, self.password)
        # Default method to get username and password
        if username == "":
            if self.username is None:
                self.username = username = input('username: ')
            else:
                username = self.username
            self.send_user_authenticate(username, vrs.UA_METHOD_NONE, "")
        else:
            if methods.count(vrs.UA_METHOD_PASSWORD) >= 1:
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

    @property
    def avatar(self):
        """
        Getter of avatar object representing current avatar of the session
        """
        try:
            return self.avatars[self.avatar_id]
        except KeyError:
            return None

    # Connection
    def _receive_connect_accept(self, user_id, avatar_id):
        """
        Custom callback method for connect accept
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_connect_accept(user_id, avatar_id)
        # Save important informations
        self.user_id = user_id
        self.avatar_id = avatar_id
        self.state = 'CONNECTED'
        # "Subscribe" to root node
        self.root_node = verse_node.VerseNode(session=self, node_id=0, parent=None, user_id=100, custom_type=0)
        # Send pending node create commands
        for queue in self.my_node_queues.values():
            for node in queue:
                self.send_node_create(node._prio, node.custom_type)

    def _receive_connect_terminate(self, error):
        """
        Custom callback method for fake connect terminate command
        """
        # Call method of parent class
        if self.debug_print is True:
            super(VerseSession, self)._receive_connect_terminate(error)
        self.state = 'DISCONNECTED'
        # Remove this instance from the list of sessions
        self.__class__.__sessions.pop(self.hostname + ':' + self.service)

    def send_connect_terminate(self):
        """
        send_connect_terminate() -> None
        """
        self.state = 'DISCONNECTING'
        super(VerseSession, self).send_connect_terminate()

    # Nodes
    def _receive_node_create(self, node_id, parent_id, user_id, custom_type):
        """
        Custom callback method that is called, when client received
        command node_create
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_node_create(node_id, parent_id, user_id, custom_type)
        # Call calback method of model
        cls = verse_node.custom_type_subclass(custom_type)
        return cls._receive_node_create(self, node_id, parent_id, user_id, custom_type)

    def _receive_node_destroy(self, node_id):
        """
        Custom callback method for command node destroy
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_node_destroy(node_id)
        # Call callback method of model
        cls = verse_node.custom_type_subclass(self.nodes[node_id].custom_type)
        return cls._receive_node_destroy(self, node_id)

    def _receive_node_link(self, parent_node_id, child_node_id):
        """
        Custom callback method that is called, when client receive command
        changing link between nodes
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_node_link(parent_node_id, child_node_id)
        # Call calback method of model and return child node
        cls = verse_node.custom_type_subclass(self.nodes[child_node_id].custom_type)
        return cls._receive_node_link(self, parent_node_id, child_node_id)

    def _receive_node_lock(self, node_id, avatar_id):
        """
        Custom callback method for command node lock
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_node_lock(node_id, avatar_id)
        # Call callback method of coresponding class and return node
        cls = verse_node.custom_type_subclass(self.nodes[node_id].custom_type)
        return cls._receive_node_lock(self, node_id, avatar_id)

    def _receive_node_unlock(self, node_id, avatar_id):
        """
        Custom callback method for command node unlock
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_node_unlock(node_id, avatar_id)
        # Call callback method of coresponding class and return node
        cls = verse_node.custom_type_subclass(self.nodes[node_id].custom_type)
        return cls._receive_node_unlock(self, node_id, avatar_id)

    def _receive_node_perm(self, node_id, user_id, perm):
        """
        Custom callback method for command node perm
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_node_perm(node_id, user_id, perm)
        # Call callback method of model
        cls = verse_node.custom_type_subclass(self.nodes[node_id].custom_type)
        return cls._receive_node_perm(self, node_id, user_id, perm)

    def _receive_node_owner(self, node_id, user_id):
        """
        Custom callback method for command node owner
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_node_owner(node_id, user_id)
        # Call callback method of corresponding class and return node
        cls = verse_node.custom_type_subclass(self.nodes[node_id].custom_type)
        return cls._receive_node_owner(self, node_id, user_id)

    # TagGroups
    def _receive_taggroup_create(self, node_id, taggroup_id, custom_type):
        """
        Custom callback method that is called, when client received command
        tag group create
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_taggroup_create(node_id, taggroup_id, custom_type)
        try:
            node_custom_type = self.nodes[node_id].custom_type
        except KeyError:
            cls = verse_tag_group.VerseTagGroup
        else:
            cls = verse_tag_group.custom_type_subclass(node_custom_type, custom_type)
        # Call callback method of model
        return cls._receive_tg_create(self, node_id, taggroup_id, custom_type)

    def _receive_taggroup_destroy(self, node_id, taggroup_id):
        """
        Custom callback method that is called, when client received command
        tag group destroy
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_taggroup_destroy(node_id, taggroup_id)
        try:
            node_custom_type = self.nodes[node_id].custom_type
            custom_type = self.nodes[node_id].tag_groups[taggroup_id].custom_type
        except KeyError:
            cls = verse_tag_group.VerseTagGroup
        else:
            cls = verse_tag_group.custom_type_subclass(node_custom_type, custom_type)
        # Call calback method of model
        return cls._receive_tg_destroy(self, node_id, taggroup_id)

    # Tags
    def _receive_tag_create(self, node_id, taggroup_id, tag_id, data_type, count, custom_type):
        """
        Custom callback method that is called, when client received command tag create
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_tag_create(node_id, taggroup_id, tag_id, data_type, count, custom_type)
        try:
            node_custom_type = self.nodes[node_id].custom_type
            tg_custom_type = self.nodes[node_id].tag_groups[taggroup_id].custom_type
        except KeyError:
            cls = verse_tag.VerseTag
        else:
            cls = verse_tag.custom_type_subclass(node_custom_type, tg_custom_type, custom_type)
        # Call calback method of VerseTag or it's subclass
        return cls._receive_tag_create(self, node_id, taggroup_id, tag_id, data_type, count, custom_type)

    def _receive_tag_destroy(self, node_id, taggroup_id, tag_id):
        """
        Custom callback method that is called, when client received command tag destroy
        """
        # Call parent method to print debug information
        if self.debug_print is True:
            super(VerseSession, self)._receive_tag_destroy(node_id, taggroup_id, tag_id)
        # Call calback method of model
        try:
            node_custom_type = self.nodes[node_id].custom_type
            tg_custom_type = self.nodes[node_id].tag_groups[taggroup_id].custom_type
            tag_custom_type = self.nodes[node_id].tag_groups[taggroup_id].tags[tag_id].custom_type
        except KeyError:
            cls = verse_tag.VerseTag
        else:
            cls = verse_tag.custom_type_subclass(node_custom_type, tg_custom_type, tag_custom_type)
        # Call calback method of VerseTag or it's subclass
        return cls._receive_tag_destroy(self, node_id, taggroup_id, tag_id)

    def _receive_tag_set_values(self, node_id, taggroup_id, tag_id, value):
        """
        Custom callback method that is called, when client reveived command tag set value
        """
        # Call method of parent class
        if self.debug_print is True:
            super(VerseSession, self)._receive_tag_set_values(node_id, taggroup_id, tag_id, value)
        try:
            node_custom_type = self.nodes[node_id].custom_type
            tg_custom_type = self.nodes[node_id].tag_groups[taggroup_id].custom_type
            tag_custom_type = self.nodes[node_id].tag_groups[taggroup_id].tags[tag_id].custom_type
        except KeyError:
            cls = verse_tag.VerseTag
        else:
            cls = verse_tag.custom_type_subclass(node_custom_type, tg_custom_type, tag_custom_type)
        # Call calback method of VerseTag or it's subclass
        return cls._receive_tag_set_values(self, node_id, taggroup_id, tag_id, value)

    # Layer
    def _receive_layer_create(self, node_id, parent_layer_id, layer_id, data_type, count, custom_type):
        """
        Custom callback method that is called, when client received command layer create
        """
        # Call method of parent class
        if self.debug_print is True:
            super(VerseSession, self)._receive_layer_create(node_id, \
                parent_layer_id, \
                layer_id, \
                data_type, \
                count, \
                custom_type)
        try:
            node_custom_type = self.nodes[node_id].custom_type
        except KeyError:
            cls = verse_layer.VerseLayer
        else:
            cls = verse_layer.custom_type_subclass(node_custom_type, custom_type)
        # Call callback method of model
        return cls._receive_layer_create(self, \
            node_id, \
            parent_layer_id, \
            layer_id, \
            data_type, \
            count, \
            custom_type)

    def _receive_layer_destroy(self, node_id, layer_id):
        """
        Custom callback method that is called, when client received command layer destroy
        """
        # Call method of parent class
        if self.debug_print is True:
            super(VerseSession, self)._receive_layer_destroy(node_id, layer_id)
        try:
            node_custom_type = self.nodes[node_id].custom_type
            custom_type = self.nodes[node_id].layers[layer_id].custom_type
        except KeyError:
            cls = verse_layer.VerseLayer
        else:
            cls = verse_layer.custom_type_subclass(node_custom_type, custom_type)
        # Call callback method of model
        return cls._receive_layer_destroy(self, node_id, layer_id)

    def _receive_layer_set_value(self, node_id, layer_id, item_id, value):
        """
        Custom callback method that is called, when client received command layer set value
        """
        # Call method of parent class
        if self.debug_print is True:
            super(VerseSession, self)._receive_layer_set_value(node_id, layer_id, item_id, value)
        try:
            node_custom_type = self.nodes[node_id].custom_type
            custom_type = self.nodes[node_id].layers[layer_id].custom_type
        except KeyError:
            cls = verse_layer.VerseLayer
        else:
            cls = verse_layer.custom_type_subclass(node_custom_type, custom_type)
        # Call callback method of model
        return cls._receive_layer_set_value(self, node_id, layer_id, item_id, value)

    def _receive_layer_unset_value(self, node_id, layer_id, item_id):
        """
        Custom callback method that is called, when client received command layer unset value
        """
        # Call method of parent class
        if self.debug_print is True:
            super(VerseSession, self)._receive_layer_unset_value(node_id, layer_id, item_id)
        try:
            node_custom_type = self.nodes[node_id].custom_type
            custom_type = self.nodes[node_id].layers[layer_id].custom_type
        except KeyError:
            cls = verse_layer.VerseLayer
        else:
            cls = verse_layer.custom_type_subclass(node_custom_type, custom_type)
        # Call callback method of model
        return cls._receive_layer_unset_value(self, node_id, layer_id, item_id)
