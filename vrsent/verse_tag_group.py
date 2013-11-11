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


from . import verse_entity


def find_tg_subclass(cls, node_custom_type, custom_type):
    """
    This method tries to find subclass with specific custom_types
    """
    sub_cls = cls
    for sub_cls_it in cls.__subclasses__():
        # Try to get attribute custom_type from subclass
        sub_cls_custom_type = getattr(sub_cls_it, 'custom_type', -1)
        # Try to get attribute node_custom_type from subclass
        sub_cls_node_custom_type = getattr(sub_cls_it, 'node_custom_type', -1)
        # All custom types have to match
        if sub_cls_custom_type == custom_type and \
                sub_cls_node_custom_type == node_custom_type:
            # When subclass with corresponding custom_types is found,
            # then store it in dictionary of subclasses
            sub_cls = cls._subclasses[(node_custom_type, custom_type)] = verse_entity.last_subclass(sub_cls_it)
            break
    return sub_cls


def custom_type_subclass(node_custom_type, custom_type):
    """
    This method tries to return VerseTagGroup subclass with specified custom type.
    Otherwise it returns VerseTag class.
    """
    sub_cls = VerseTagGroup
    try:
        sub_cls = VerseTagGroup._subclasses[(node_custom_type, custom_type)]
    except KeyError:
        sub_cls = find_tg_subclass(VerseTagGroup, node_custom_type, custom_type)
    else:
        sub_cls = verse_entity.last_subclass(sub_cls)
    return sub_cls


class VerseTagGroup(verse_entity.VerseEntity):
    """
    Class representing Verse tag group
    """
    
    _subclasses = {}

    custom_type = None
    node_custom_type = None

    def __new__(cls, *args, **kwargs):
        """
        Pre-constructor of VerseTagGroup. It can return class defined
        by custom_type of received command or corresponding tag group.
        """
        if len(cls.__subclasses__()) > 0:
            try:
                node = kwargs['node']
                custom_type = kwargs['custom_type']
            except KeyError:
                # TODO: try to find node and custom_type in args
                return super(VerseTagGroup, cls).__new__(cls)
            else:
                sub_cls = cls
                node_custom_type = node.custom_type
                try:
                    sub_cls = cls._subclasses[(node_custom_type, custom_type)]
                except KeyError:
                    # When instance of this class has never been created, then try
                    # to find corresponding subclass.
                    sub_cls = find_tg_subclass(cls, node_custom_type, custom_type)
                return super(VerseTagGroup, sub_cls).__new__(sub_cls)
        else:
            return super(VerseTagGroup, cls).__new__(cls)

    def __init__(self, node, tg_id=None, custom_type=None):
        """
        Constructor of VerseTagGroup
        """
        super(VerseTagGroup, self).__init__(custom_type=custom_type)

        self.node = node
        self.id = tg_id
        self.tags = {}
        self.tag_queue = {}

        self._create()

        # Set bindings
        if tg_id is not None:
            self.node.tag_groups[tg_id] = self
            self.node.tg_queue[self.custom_type] = self
        else:
            tg = None
            try:
                tg = self.node.tg_queue[self.custom_type]
            except KeyError:
                self.node.tg_queue[self.custom_type] = self
            if tg is not None:
                raise TypeError('VerseTagGroup with: ' +
                                str(self.custom_type) +
                                ' already exists in VerseNode: ' +
                                str(node.id))

    def __str__(self):
        """
        String representation of VerseTagGroup
        """
        return 'VerseTagGroup, id:' + \
            str(self.id) + \
            ', custom_type: ' + \
            str(self.custom_type)

    def _send_create(self):
        """
        Send tag group create command to Verse server
        """
        if self.node.id is not None:
            self.node.session.send_taggroup_create(self.node.prio,
                                                   self.node.id,
                                                   self.custom_type)

    def _send_destroy(self):
        """
        Send tag group destroy command to Verse server
        """
        if self.id is not None:
            self.node.session.send_taggroup_destroy(self.node.prio,
                                                    self.node.id, self.id)

    def subscribe(self):
        """
        This method tries to send tag group subscribe command
        """
        if self.id is not None and self.subscribed is False:
            self.node.session.send_taggroup_subscribe(self.node.prio,
                                                      self.node.id,
                                                      self.id,
                                                      self.version,
                                                      self.crc32)
            self.subscribed = True

    def unsubscribe(self):
        """
        This method tries to send tag group unsubscribe command
        """
        if self.id is not None and self.subscribed is False:
            self.node.session.send_taggroup_unsubscribe(self.node.prio,
                                                        self.node.id,
                                                        self.id,
                                                        self.version,
                                                        self.crc32)
            self.subscribed = True

    def _clean(self):
        """
        This method clean all data from this tag group
        """
        # Remove references at all this taggroup
        if self.id is not None:
            self.node.tag_groups.pop(self.id)
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

    @classmethod
    def _receive_tg_create(cls, session, node_id, tg_id, custom_type):
        """
        Static method of class that add reference to the
        the dictionary of tag groups and send pending tag_create
        commands
        """

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
            node.tag_groups[tg_id] = tg

        # Update state and subscribe command
        tg._receive_create()

        # Send tag_create commands for pending tags
        for custom_type, tag in tg.tag_queue.items():
            session.send_tag_create(node.prio, node.id, tg.id, tag.data_type,
                                    tag.count, custom_type)
        # Return reference at tag group object
        return tg

    @classmethod
    def _receive_tg_destroy(cls, session, node_id, tg_id):
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
        # Destroy tag group
        tg._receive_destroy()
        # Return reference at this object
        return tg

    @classmethod
    def _receive_tg_subscribe(cls, session, node_id, tg_id, version, crc32):
        """
        Static method of class that should be called when tag group
        subscribe command is received from Verse server
        """
        # TODO
        pass

    @classmethod
    def _receive_tg_unsubscribe(cls, session, node_id, tg_id, version, crc32):
        """
        Static method of class that should be called when tag group
        unsubscribe command is received from Verse server
        """
        # TODO
        pass
