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
This module includes class VerseTag representing verse tag at verse
client. This class could be used for sharing of scalar values or
vector of values (2D, 3D or Quaternions).
"""


from . import verse_entity


def find_tag_subclass(cls, node_custom_type, tg_custom_type, custom_type):
    """
    This method tries to find subclass with specific custom_types
    """
    sub_cls = cls
    for sub_cls_it in cls.__subclasses__():
        # Try to get attribute custom_type from subclass
        sub_cls_custom_type = getattr(sub_cls_it, 'custom_type', None)
        # Raise error, when developer created subclass without custom_type
        if sub_cls_custom_type is None:
            raise AttributeError('Subclass of VerseTag: ' + 
                                 str(sub_cls_it) + 
                                 ' does not have attribute custom_type')
        # Try to get attribute tg_custom_type from subclass
        sub_cls_tg_custom_type = getattr(sub_cls_it, 'tg_custom_type', None)
        # Raise error, when developer created subclass without tg_custom_type
        if sub_cls_tg_custom_type is None:
            raise AttributeError('Subclass of VerseTag: ' +
                                 str(sub_cls_it) +
                                 ' does not have attribute tg_custom_type')
        # Try to get attribute node_custom_type from subclass
        sub_cls_node_custom_type = getattr(sub_cls_it, 'node_custom_type', None)
        # Raise error, when developer created subclass without node_custom_type
        if sub_cls_node_custom_type is None:
            raise AttributeError('Subclass of VerseTag: ' +
                                 str(sub_cls_it) +
                                 ' does not have attribute node_custom_type')
        if sub_cls_custom_type == custom_type and \
                sub_cls_tg_custom_type == tg_custom_type and \
                sub_cls_node_custom_type == node_custom_type:
            # When subclass with corresponding custom_types is found,
            # then store it in dictionary of subclasses
            sub_cls = \
                cls.subclasses[(node_custom_type, tg_custom_type, custom_type)] = \
                verse_entity.last_subclass(sub_cls_it)
            break
    return sub_cls


def custom_type_subclass(node_custom_type, tg_custom_type, custom_type):
    """
    This method tries to return VerseTag subclass with specified custom type.
    Otherwise it returns VerseTag class.
    """
    try:
        sub_cls = VerseTag.subclasses[(node_custom_type, tg_custom_type, custom_type)]
    except KeyError:
        sub_cls = find_tag_subclass(VerseTag, node_custom_type, tg_custom_type, custom_type)
    else:
        sub_cls = verse_entity.last_subclass(sub_cls)
    return sub_cls


class VerseTag(verse_entity.VerseEntity):
    """
    Class representing Verse tag
    """

    # The dictionary of subclasees of VerseTag. The key of this dictionary is tuple of:
    # (node.custom_type, tg.custom_type, tag.custom_type)
    # When subclass of VerseTag is created, then it has to include class attributes
    # custom_type, tg_custom_type and node_custom_type
    subclasses = {}

    def __new__(cls, *args, **kwargs):
        """
        Pre-constructor of new VerseTag. It can return subclass VerseTag
        according custom_type of tag, tag group and node.
        """
        if len(cls.__subclasses__()) > 0:
            try:
                tag_group = kwargs['tg']
                custom_type = kwargs['custom_type']
            except KeyError:
                return super(VerseTag, cls).__new__(cls)
            else:
                node_custom_type = tag_group.node.custom_type
                tg_custom_type = tag_group.custom_type
                try:
                    sub_cls = cls.subclasses[(node_custom_type, tg_custom_type, custom_type)]
                except KeyError:
                    # When instance of this class has never been created, then try
                    # to find corresponding subclass.
                    sub_cls = find_tag_subclass(cls, node_custom_type, tg_custom_type, custom_type)
                return super(VerseTag, sub_cls).__new__(sub_cls)
        else:
            return super(VerseTag, cls).__new__(cls)

    def __init__(self, tg, tag_id=None, data_type=None, count=None, custom_type=None, value=None):
        """
        Constructor of VerseTag
        """
        # Check if this object is created with right custom_type
        # and when custom_type is not specified, then set it
        # according class definition
        if hasattr(self.__class__, 'custom_type'):
            if custom_type is not None:
                assert self.__class__.custom_type == custom_type
            else:
                custom_type = self.__class__.custom_type

        # Call method of parent to initialize basic values
        super(VerseTag, self).__init__(custom_type=custom_type)

        self.tg = tg

        # Delete useless things
        del self.version
        del self.crc32

        # Remember own ID
        self.id = tag_id

        # If data type is not set, then try to estimate it. Only three
        # Python data types are supported for Verse tags
        if data_type is None and value is None:
            raise TypeError("VerseTag value and VerseTag data_type are None")
        elif data_type is None:
            if issubclass(value.__class__, tuple):
                # Set data_type with max possible precision
                try:
                    self.data_type = verse_entity.DATA_TYPE_DICT[type(value[0])]
                except KeyError:
                    raise TypeError("Unsupported data_type of VerseTag value: ", type(value[0]))
            else:
                raise TypeError("VerseTag value is not tuple: ", type(value))
        else:
            # No need to do check of data_type, because Verse module do this
            self.data_type = data_type

        # No need to do check of values and count of tuple items, because Verse module do this
        self._value = value
        if count is not None:
            self.count = count
        elif value is not None:
            self.count = len(value)

        # Change state and send command, when it is possible
        self._create()

        # Set bindings between tag group and this tag
        if tag_id is not None:
            self.tg.tags[tag_id] = self
            self.tg.tag_queue[self.custom_type] = self
        else:
            tag = None
            try:
                tag = self.tg.tag_queue[self.custom_type]
            except KeyError:
                self.tg.tag_queue[self.custom_type] = self
            # Check uniqueness of custom_type inside the tag group
            if tag is not None:
                raise TypeError('VerseTag with: ' +
                                str(self.custom_type) +
                                ' already exists in VerseTagGroup: ' +
                                str(tg.id))

    def __str__(self):
        """
        String representation of VerseTag
        """
        return 'VerseTag, id: ' + \
            str(self.id) + \
            ', data_type: ' + \
            str(self.data_type) + \
            ', count: ' + \
            str(self.count) + \
            ', custom_type: ' + \
            str(self.custom_type) + \
            ', values: ' + \
            str(self.value)

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
        if self.id is not None:
            self.tg.node.session.send_tag_set_values(
                self.tg.node.prio,
                self.tg.node.id,
                self.tg.id,
                self.id,
                self.data_type,
                self._value
            )

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
        if self.tg.id is not None:
            self.tg.node.session.send_tag_create(
                self.tg.node.prio,
                self.tg.node.id,
                self.tg.id,
                self.data_type,
                self.count,
                self.custom_type
            )

    def _send_destroy(self):
        """
        Send tag destroy command to Verse server
        """
        if self.id is not None:
            self.tg.node.session.send_tag_destroy(
                self.tg.node.prio,
                self.tg.node.id,
                self.tg.id,
                self.id
            )

    def clean(self):
        """
        This method try to clean content (value) of this tag
        """
        # Remove references on this tag from tag group
        if self.id is not None:
            self.tg.tags.pop(self.id)
        self.tg.tag_queue.pop(self.custom_type)
        # Remove value
        del self._value

    @classmethod
    def cb_receive_tag_create(cls, session, node_id, tg_id, tag_id, data_type, count, custom_type):
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
            tg = node.tag_groups[tg_id]
        except KeyError:
            return
        # Was this tag created by this client?
        try:
            tag = tg.tag_queue[custom_type]
        except KeyError:
            # When this tag was created by other client, then create new tag object for this tag
            tag = VerseTag(tg=tg, tag_id=tag_id, data_type=data_type, count=count, custom_type=custom_type)
        else:
            # Add reference to dictionary of tags to tag group
            tg.tags[tag_id] = tag
            tag.id = tag_id
        # Update state
        tag.cb_receive_create()
        # Send tag value, when it is tag created by this client
        # When this tag was created by some other Verse client,
        # then Verse server will send value, when received command
        # is acked to Verse server
        if tag._value is not None:
            tag.value = tag._value
        # Return reference at tag object
        return tag

    @classmethod
    def cb_receive_tag_set_values(cls, session, node_id, tg_id, tag_id, value):
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
            tg = node.tag_groups[tg_id]
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

    @classmethod
    def cb_receive_tag_destroy(cls, session, node_id, tg_id, tag_id):
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
            tg = node.tag_groups[tg_id]
        except KeyError:
            return
        # Try to find tag
        try:
            tag = tg.tags[tag_id]
        except KeyError:
            return
        # Change state and call clean method
        tag.cb_receive_destroy()
        # Return reference at this destroyed tag
        return tag
