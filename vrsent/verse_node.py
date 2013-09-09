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
This module includes class VerseNode representing verse node
"""


import verse as vrs
from . import verse_entity


def custom_type_subclass(custom_type):
    """
    This method tries to return VerseNode subclass with specified custom type.
    Otherwise it returns VerseNode class.
    """
    try:
        cls = VerseNode._subclasses[custom_type]
    except KeyError:
        cls = VerseNode
    else:
        cls = last_subclass(cls)
    return cls


def last_subclass(cls):
    """
    This method returns last subclass of VerseNode subclass
    """
    if len(cls.__subclasses__()) > 0 and cls.__subclasses__()[0].custom_type == cls.custom_type:
        return last_subclass(cls.__subclasses__()[0])
    else:
        return cls


class VerseNode(verse_entity.VerseEntity):
    """
    Class representing Verse node
    """

    # The dictionary of subclasses
    _subclasses = {}

    def __new__(cls, *args, **kwargs):
        """
        Pre-constructor of VerseNode. It can 
        """
        if len(cls.__subclasses__()) > 0:
            try:
                custom_type = kwargs['custom_type']
            except KeyError:
                return super(VerseNode, cls).__new__(cls)
            else:
                sub_cls = None
                if custom_type in cls._subclasses:
                    sub_cls = cls._subclasses[custom_type]
                else:
                    for sub_cls_it in cls.__subclasses__():
                        sub_cls_type = getattr(sub_cls_it, 'custom_type', None)
                        if sub_cls_type is not None and sub_cls_type == custom_type:
                            sub_cls = cls._subclasses[custom_type] = last_subclass(sub_cls_it)
                if sub_cls is not None:
                    return super(VerseNode, sub_cls).__new__(sub_cls)
                else:
                    return super(VerseNode, cls).__new__(cls)
        else:
            return super(VerseNode, cls).__new__(cls)

    
    def __init__(self, session, node_id=None, parent=None, user_id=None, custom_type=None):
        """
        Constructor of VerseNode
        """

        # Check if this object is created with right custom_type
        # and when custom_type is not specified, then set it
        # according class definition
        if hasattr(self.__class__, 'custom_type'):
            if custom_type is not None:
                assert self.__class__.custom_type == custom_type
            else:
                custom_type = self.__class__.custom_type

        super(VerseNode, self).__init__(custom_type=custom_type)

        self.session = session

        self.id = node_id

        # When parent node is set, then it has to be subclass of VerseNode
        if parent is not None:
            if issubclass(parent.__class__, VerseNode) != True:
                raise TypeError("Node is not subclass of model.VerseNode")
        self.parent = parent
        
        self.user_id = user_id
        self.child_nodes = {}
        self.taggroups = {}
        self.tg_queue = {}
        self.layers = {}
        self.layer_queue = {}
        self.prio = vrs.DEFAULT_PRIORITY
        self.perms = {}

        # Change state and send commands
        self._create()

        # When node_id is not set, then:
        if node_id is None:
            # Try to find queue of custom_type of node or create new one
            try:
                node_queue = self.session.my_node_queues[custom_type]
            except KeyError:
                node_queue = []
                self.session.my_node_queues[self.custom_type] = node_queue
            # Add this object to the queue
            node_queue.insert(0, self)
        else:
            self.session.nodes[node_id] = self
            if self.parent is not None:
                self.parent.child_nodes[node_id] = self


    def destroy(self, send_destroy_cmd=True):
        """
        This method try to send destroy command
        """
        # Change state and send commands
        self._destroy()


    def _clean(self):
        """
        This method try to destroy all data in this object
        """
        # Delete all child nodes, but do not send destroy command
        # for these nodes
        for child_node in self.child_nodes.values():
            child_node.parent = None
            child_node._clean()
        self.child_nodes.clear()
        # Remove reference on this node
        if self.id is not None:
            # Remove this node from dictionary of nodes
            self.session.nodes.pop(self.id)
            # Remove this node from dictionar of child nodes
            if self.parent is not None:
                try:
                    self.parent.child_nodes.pop(self.id)
                except KeyError:
                    pass
                self.parent = None
        # Clear tag groups
        self.taggroups.clear()
        self.tg_queue.clear()
        # Clear layers
        self.layers.clear()
        self.layer_queue.clear()


    def _send_create(self):
        """
        This method send node create command to Verse server
        """
        if self.session.state == 'CONNECTED' and self.id is None:
            self.session.send_node_create(self.prio, self.custom_type)


    def _send_destroy(self):
        """
        This method send destroy command to Verse server
        """
        if self.session.state == 'CONNECTED' and self.id is not None:
            self.session.send_node_destroy(self.prio, self.id)


    def _send_subscribe(self):
        """
        This method send subscribe command to Verse server
        """
        if self.session.state == 'CONNECTED' and self.id is not None:
            self.session.send_node_subscribe(self.prio, self.id, self.version, self.crc32)
            self.subscribed = True


    @classmethod
    def _receive_node_create(cls, session, node_id, parent_id, user_id, custom_type):
        """
        Static method of class that should be called, when coresponding callback
        method of class is called. This method moves node from queue to
        the dictionary of nodes and send pending commands.
        """
        send_pending_data = False

        # Try to find parent node
        try:
            parent_node = session.nodes[parent_id]
        except KeyError:
            parent_node = None

        # Is it node created by this client?
        if parent_id == session.avatar_id and user_id == session.user_id:
            node_queue = session.my_node_queues[custom_type]
            # If this is node created by this client, then add it to
            # dictionary of nodes
            node = node_queue.pop()
            node.id = node_id
            session.nodes[node_id] = node
            if node.parent is None:
                node.parent = parent_node
            send_pending_data = True
        else:
            # Was this node already created?
            # e.g.: avatar node, user node, parent of scene node, etc.
            try:
                node = session.nodes[node_id]
            except KeyError:
                node = VerseNode(session=session, node_id=node_id, parent=parent_node, user_id=user_id, custom_type=custom_type)
            else:
                send_pending_data = True

        # Change state of node
        node._receive_create()

        # When this node was created by this client, then it is neccessary to send
        # create/set command for node priority, tag_groups and layers
        if send_pending_data == True:

            # When node priority is different from default node priority
            if node.prio != vrs.DEFAULT_PRIORITY:
                session.send_node_prio(node.prio, node.id, node.prio)

            # When parent node is different then current parent, then send node_link
            # command to Verse server
            if node.parent is not None and parent_id != node.parent.id:
                session.send_node_link(node.prio, node.parent.id, node.id)
                # Add reference to list of child nodes to parent node now,
                # because it is possible to do now (node id is known)
                node.parent.child_nodes[node.id] = node

            # Send tag_group_create command for pending tag groups
            for custom_type in node.tg_queue.keys():
                session.send_taggroup_create(node.prio, node.id, custom_type)

            # Send layer_create command for pending layers without parent layer
            # This module will send automaticaly layer_create command for layers
            # with parent layers, when layer_create command of their parent layers
            # will be received
            for layer in node.layer_queue.values():
                if layer.parent_layer is None:
                    session.send_layer_create(node.prio, \
                        node.id, \
                        -1, \
                        layer.data_type, \
                        layer.count, \
                        layer.custom_type)

        # Return reference at node
        return node

    @classmethod
    def _receive_node_destroy(cls, session, node_id):
        """
        Static method of class that should be called, when destroy_node
        callback method of Session class is called. This method removes
        node from dictionary and node will be destroyed.
        """
        # Try to find node
        try:
            node = session.nodes[node_id]
        except KeyError:
            return
        # Set entity state and clean data in this node
        node._receive_destroy()
        # Return reference at this node
        return node


    @classmethod
    def _receive_node_perm(cls, session, node_id, user_id, perm):
        """
        Static method of class that is called, when client received infomration
        about permission for specific user
        """
        try:
            node = session.nodes[node_id]
        except KeyError:
            return
        # Store information about this permissions
        node.perms[user_id] = perm
        # Return reference at this node
        return node


    @classmethod
    def _receive_node_link(cls, session, parent_node_id, child_node_id):
        """
        """
        # Try to find parent node
        try:
            parent_node = session.nodes[parent_node_id]
        except KeyError:
            return
        # Try to find child node
        try:
            child_node = session.nodes[child_node_id]
        except KeyError:
            return
        # When current link between nodes is different, then
        # set new link between nodes
        if child_node.parent.id != parent_node.id:
            # First remove child node from list of child nodes
            # of current parent node
            child.parent.child_nodes.pop(child_node_id)
            # Set new parent of child node
            child.parent = parent_node
            # Add child node to the list of child node of new
            # parent node
            parent_node.child_nodes[child_node_id] = child_node

        # Return reference at child node
        return child_node

    @classmethod
    def _receive_node_subscribe(cls, session, node_id, version, crc32):
        """
        Static method of class that should be called when
        node subscribe command is received from Verse server
        """
        # TODO
        pass


    @classmethod
    def _receive_node_unsubscribe(cls, session, node_id, version, crc32):
        """
        Static method of class that should be called when
        node unsubscribe command is received from Verse server
        """
        # TODO
        pass