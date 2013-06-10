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
This module includes class VerseLayer representing verse layer at verse
client. This class could be used for sharing list or dictionaries.
"""

import verse as vrs
from . import verse_entity


class VerseLayer(verse_entity.VerseEntity):
    """
    Class representing Verse layer
    """

    def __init__(self, node, parent_layer=None, layer_id=None, data_type=None, count=1, custom_type=None):
        """
        Constructor of VerseLayer
        """
        super(VerseLayer, self).__init__(custom_type=custom_type)
        self.node = node
        self.id = layer_id
        self.data_type = data_type
        self.count = count
        self.child_layers = {}
        self.values = {}

        # Set bindings
        if layer_id is not None:
            self.node.layers[layer_id] = self
        else:
            self.node.layer_queue[custom_type] = self
        if parent_layer is not None:
            self.parent_layer = parent_layer
            if layer_id is not None:
                self.parent_layer.child_layers[layer_id] = self

    def destroy(self):
        """
        Destructor of VerseLayer
        """
        # Clear bindings
        self.node.layers.pop(self.id)
        if self.parent_layer is not None:
            self.parent_layer.childs.pop(self.id)

    def _send_create(self):
        """
        Send layer create to Verse server
        """
        if self.node.session is not None and self.id is not None:
            if self.parent_layer is not None:
                self.node.session.send_layer_create(self.node.prio, self.node.id, self.parent_layer.id, self.data_type, self.count, self.custom_type)
            else:
                self.node.session.send_layer_create(self.node.prio, self.node.id, -1, self.data_type, self.count, self.custom_type)

    def _send_destroy(self):
        """
        Send layer destroy command to Verse server
        """
        if self.node.session is not None and self.id is not None:
            self.node.session.send_layer_destroy(self.node.prio, self.node.id, self.id)

    def _send_subscribe(self):
        """
        Send layer subscribe command to Verse server
        """
        if self.node.session is not None and self.id is not None:
            self.node.session.send_layer_subscribe(self.node.prio. self.node.id, self.id, self.version, self.crc32)

    def _send_unsubscribe(self):
        """
        Send layer unsubscribe to Verse server
        """
        if self.node.session is not None and self.id is not None:
            self.node.session.send_layer_unsubscribe(self.node.prio, self.node.id, self.id, self.version, self.crc22)

    def _clean(self):
        """
        This method clean all data from this object
        """
        # Clean all child nodes, but do not send destroy commands
        # for them, because Verse server do this automaticaly too
        for layer in self.child_layers.values():
            layer.parent_layer = None
            layer._clean()
        self.child_layers.clear()

    def destroy(self):
        """
        Change state of entity and send destroy command to Verse server
        """
        self._destroy()
        