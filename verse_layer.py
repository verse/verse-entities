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
from verse_entity import VerseEntity


# TODO: Finish implementation of this entity

class VerseLayer(VerseEntity):
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
        self.childs = {}
        self.values = {}

        # Set bindings
        if layer_id is not None:
            self.node.layers[layer_id] = self
        else:
            self.node.layer_queue[custom_type] = self
        if parent_layer is not None:
            self.parent_layer = parent_layer
            if layer_id is not None:
                self.parent_layer.childs[layer_id] = self

    def destroy(self):
        """
        Destructor of VerseLayer
        """
        # Clear bindings
        self.node.layers.pop(self.id)
        if self.parent_layer is not None:
            self.parent_layer.childs.pop(self.id)