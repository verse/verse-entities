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
from . import verse_entity, verse_tag_group


class VerseTag(verse_entity.VerseEntity):
    """
    Class representing Verse tag
    """
    
    def __init__(self, tg, tag_id=None, data_type=None, custom_type=None, value=(0,)):
        """
        Constructor of VerseTag
        """

        # Call method of parent to initialize basic values
        super(VerseTag, self).__init__(custom_type=custom_type)

        # Tag can't exist without tag group
        if issubclass(tg.__class__, verse_tag_group.VerseTagGroup) != True:
            raise TypeError("Tag group is not subclass of model.VerseTagGroup")
        else:
            self.tg = tg

        # Delete useless things
        del self.version
        del self.crc32

        # Remember own ID
        self.id = tag_id

        # If data type is not set, then try to estimate it. Only three
        # Python data types are supported for Verse tags
        if data_type is None:
            if type(value[0]) == int:
                self.data_type = vrs.VALUE_TYPE_UINT64
            elif type(value[0]) == float:
                self.data_type = vrs.VALUE_TYPE_REAL64
            elif type(value[0]) == str:
                self.data_type = vrs.VALUE_TYPE_STRING
            else:
                raise TypeError("Unsupported data_type: ", type(value[0]))
        else:
            # No need to do check of data_type, because Verse module do this
            self.data_type = data_type

        # No need to do check of values and count of tuple items, because Verse module do this
        self._value = value
        self.count = len(value)

        # Change state and send command, when it is possible
        self._create()

        # Set bindings between tag group and this tag
        if tag_id is not None:
            self.tg.tags[tag_id] = self
            self.tg.tag_queue[custom_type] = self
        else:
            tag = None
            try:
                tag = self.tg.tag_queue[custom_type]
            except KeyError:
                self.tg.tag_queue[custom_type] = self
            # Check uniqueness of custom_type inside the tag group
            if tag is not None:
                raise VerseCustomTypeError(custom_type)


    def destroy(self):
        """
        Send destroy command of VerseTag
        """
        # Change state and send destroy command to Verse server
        self._destroy()

    @property
    def value(self):
        """
        The value is property of VerseTag
        """
        return self._value

    @value.setter
    def value(self, val):
        """
        The setter of value
        """
        self._value = val
        # Send value to Verse server
        if self.tg.node.session is not None and self.id is not None:
            self.tg.node.session.send_tag_set_value(self.tg.node.prio, \
                self.tg.node.id, \
                self.tg.id, \
                self.id, \
                self.data_type, \
                self._value)

    @value.deleter
    def value(self):
        """
        The deleter of value
        """
        # Send destroy command to Verse server
        self._send_destroy()

    def _send_create(self):
        """
        Send tag create command to Verse server
        """
        if self.tg.node.session is not None and self.tg.id is not None:
            self.tg.node.session.send_tag_create(self.tg.node.prio, \
                self.tg.node.id, \
                self.tg.id, \
                self.data_type, \
                self.count, \
                self.custom_type)

    def _send_destroy(self):
        """
        Send tag destroy command to Verse server
        """
        if self.tg.node.session is not None and self.id is not None:
            self.tg.node.session.send_tag_destroy(self.node.prio, \
                self.tg.node.id, \
                self.tg.id, \
                self.id)

    def _clean(self):
        """
        This method try to clean content (value) of this tag
        """
        # Remove references on this tag from tag group
        if self.id is not None:
            self.tg.tags.pop(self.id)
        self.tg.tag_queue.pop(self.custom_type)
        # Remove value
        del self._value

    @staticmethod
    def _receive_tag_create(session, node_id, tg_id, tag_id, data_type, count, custom_type):
        """
        Static method of class that should be called when
        coresponding callback function is called
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
        # Was this tag created by this client?
        try:
            tag = tg.tag_queue[custom_type]
            # Add reference to dictionary of tags to tag group
            tg.tags[tag_id] = tag
            tag.id = tag_id
        except KeyError:
            tag = VerseTag(node, tg, tag_id, data_type, count, custom_type)
        # Update state
        tag._receive_create()
        # Send tag value
        tag.value = tag._value
        # Return reference at tag object
        return tag

    @staticmethod
    def _receive_tag_set_value(session, node_id, tg_id, tag_id, value):
        """
        Static method of class that should be called when
        coresponding callback function is called
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
        # Try to find tag
        try:
            tag = tg.tags[tag_id]
        except KeyError:
            return
        # Set value, but don't send set_value command
        tag._value = value
        # Return reference at this tag
        return tag

    @staticmethod
    def _receive_tag_destroy(session, node_id, tg_id, tag_id):
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
        # Try to find tag
        try:
            tag = tg.tag_queue[custom_type]
        except KeyError:
            return
        # Change state and call clen method
        tag._receive_destroy()
        # Return reference at this destroyed tag
        return tag
