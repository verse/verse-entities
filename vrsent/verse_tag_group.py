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
This module includes class VerseTagGroup representing verse tag group
at verse client. This class could not be used for sharing any data.
This class is used only for encapsulating verse tags.
"""

import verse as vrs
from . import verse_entity, verse_node


class VerseTagGroup(verse_entity.VerseEntity):
    """
    Class representing Verse tag group
    """

    def __init__(self, node, tg_id=None, custom_type=None):
        """
        Constructor of VerseTagGroup
        """
        super(VerseTagGroup, self).__init__(custom_type=custom_type)

        # Tag group can't exist without node
        if issubclass(node.__class__, verse_node.VerseNode) != True:
            raise TypeError("Node is not subclass of model.VerseNode")
        else:
            self.node = node

        self.id = tg_id

        self.tags = {}
        self.tag_queue = {}

        self._create()

        # Set bindings
        if tg_id is not None:
            self.node.taggroups[tg_id] = self
            self.node.tg_queue[self.custom_type] = self
        else:
            tg = None
            try:
                tg = self.node.tg_queue[self.custom_type]
            except KeyError:
                self.node.tg_queue[self.custom_type] = self
            if tg is not None:
                raise VerseCustomTypeError(self.custom_type)


    def _send_create(self):
        """
        Send tag group create command to Verse server
        """
        if self.node.id is not None:
            self.node.session.send_taggroup_create(self.node.id, self.custom_type)


    def _send_destroy(self):
        """
        Send tag group destroy command to Verse server
        """
        if self.id is not None:
            self.node.session.send_taggroup_destroy(self.node.prio, self.node.id, self.id)


    def _send_subscribe(self):
        """
        Send tag group subscribe command
        """
        if self.id is not None and self.subscribed == False:
            self.node.session.send_taggroup_subscribe(self.node.prio, self.node.id, self.id, self.version, self.crc32)
            self.subscribed = True


    def _clean(self):
        """
        This method clean all data from this tag group
        """
        # Remove references at all this taggroup
        if self.id is not None:
            self.node.taggroups.pop(self.id)
        self.node.tg_queue.pop(self.custom_type)
        # Clean all tags and queue of tags
        self.tags.clear()
        self.tag_queue.clear()


    def destroy(self):
        """
        Method for destroying tag group
        """
        # Change state and send destroy command to Verse server
        self._destroy()


    @staticmethod
    def _receive_tg_create(session, node_id, tg_id, custom_type):
        """
        Static method of class that add reference to the
        the dictionary of tag groups and send pending tag_create
        commands
        """
        node = None
        try:
            node = session.nodes[node_id]
        except KeyError:
            return
        # Is it tag group created by this client?
        try:
            tg = node.tg_queue[custom_type]
        except KeyError:
            tg = VerseTagGroup(node, tg_id, custom_type)
        else:
            tg.id = tg_id
            node.taggroups[tg_id] = tg
        # Update state and subscribe command
        tg._receive_create()
        # Send tag_create commands for pending tags
        for custom_type, tag in tg.tag_queue.items():
            session.send_tag_create(node.prio, node.id, tg.id, tag.data_type, tag.count, custom_type)
        # Return reference at tag group object
        return tg


    @staticmethod
    def _receive_tg_destroy(session, node_id, tg_id):
        """
        Static method of class that should be called when
        destroy callback session method is called
        """
        # Try to find node
        try:
            node = session.nodes[node_id]
        except KeyError:
            return
        # Try to find tag group
        try:
            tg = node.taggroups[tg_id]
        except KeyError:
            return
        # Destroy tag group
        tg._receive_destroy()
        # Return reference at this object
        return tg


    @staticmethod
    def _receive_tg_subscribe(session, node_id, tg_id, version, crc32):
        """
        Static method of class that should be called when tag group
        subscribe command is received from Verse server
        """
        # TODO
        pass


    @staticmethod
    def _receive_tg_unsubscribe(session, node_id, tg_id, version, crc32):
        """
        Static method of class that should be called when tag group
        unsubscribe command is received from Verse server
        """
        # TODO
        pass
