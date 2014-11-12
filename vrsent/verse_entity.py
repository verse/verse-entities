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
This module includes class VerseEntitty that is used as parent class
of other verse entities (node, tag group, tag and layer). This module
also includes class VerseStateError that is raised, when verse entity
wants to do unauthorized state switch.
"""


import verse as vrs


ENTITY_RESERVED = 0
ENTITY_CREATING = 1
ENTITY_CREATED = 2
ENTITY_ASSUMED = 3
ENTITY_WANT_DESTROY = 4
ENTITY_DESTROYING = 5
ENTITY_DESTROYED = 6


# Set of supported Verse value types
SUPPORTED_VALUE_TYPES = set((
    vrs.VALUE_TYPE_UINT8,
    vrs.VALUE_TYPE_UINT16,
    vrs.VALUE_TYPE_UINT32,
    vrs.VALUE_TYPE_UINT64,
    vrs.VALUE_TYPE_REAL16,
    vrs.VALUE_TYPE_REAL32,
    vrs.VALUE_TYPE_REAL64,
    vrs.VALUE_TYPE_STRING8
))


# Set of supported data types
SUPPORTED_DATA_TYPES = set((int, float, str))


# Dictionary used for estimation of VerseTag VerseLayer data_type
DATA_TYPE_DICT = {
    int: vrs.VALUE_TYPE_UINT64,
    float: vrs.VALUE_TYPE_REAL64,
    str: vrs.VALUE_TYPE_STRING8
}


def last_subclass(cls):
    """
    This method is used to return last subclass of VerseNode,
    VerseTag, VerseTagGroup or VerseLayer subclass
    """
    if len(cls.__subclasses__()) > 0:
        return last_subclass(cls.__subclasses__()[0])
    else:
        return cls


def name_to_custom_type(cls_name):
    """
    This method should be used for generating 'unique' custom_type
    from name of custom subclasses
    """
    str_hash = 1
    max_val = (1 << 64) - 1
    for ch in cls_name:
        num = ord(ch) 
        str_hash += num + (str_hash << 6) + (str_hash << 16) - str_hash
        str_hash &= max_val
    return str_hash % 65535


class VerseStateError(Exception):
    """
    Exception for invalid state changes
    """

    def __init__(self, state, transition):
        """
        Constructor of exception
        """
        self.state = state
        self.transition = transition

    def __str__(self):
        """
        Method for printing content of exception
        """
        return str(self.state) + '!' + str(self.transition)


class VerseEntity(object):
    """
    Parent class for VerseNode, Verse, VerseTagGroup and VerseLayer
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor of VerseEntity
        """
        self.id = None
        self.version = 0
        self.crc32 = 0
        self.state = ENTITY_RESERVED
        self.subscribed = False
        # Try to get custom_type argument
        custom_type = kwargs.get('custom_type', None)
        if custom_type is None:
            try:
                custom_type = args[-1]
            except IndexError:
                pass
        # When custom_type is not specified, then raise error
        if custom_type is None:
            raise TypeError('No custom_type specified')
        else:
            if type(custom_type) == int:
                self.custom_type = custom_type
            else:
                raise TypeError('Specified custom_type is not int')

    def _send_create(self):
        """
        Dummy method
        """
        pass

    def _send_destroy(self):
        """
        Dummy method
        """
        pass

    def _auto_subscribe(self):
        """
        Default behavior is to automatically subscribe to everything.
        This could be changed in subclass.
        """
        return True

    def subscribe(self):
        """
        Dummy method
        """
        pass

    def unsubscribe(self):
        """
        Dummy method
        """
        pass

    def _create(self):
        """
        This method switch state, when client wants to create new entity
        """
        if self.state == ENTITY_RESERVED:
            if self.id is None:
                self._send_create()
                self.state = ENTITY_CREATING
            else:
                # Skip _send_create(), when ID is known and jump to assumed state
                self.state = ENTITY_ASSUMED
                if self._auto_subscribe() is True:
                    self.subscribe()
        else:
            raise VerseStateError(self.state, "create")

    def _destroy(self):
        """
        This method switch entity state, when client wants to destroy entity
        """
        if self.state == ENTITY_CREATED or self.state == ENTITY_ASSUMED:
            self._send_destroy()
            self.state = ENTITY_DESTROYING
        elif self.state == ENTITY_CREATING:
            self.state = ENTITY_WANT_DESTROY
        else:
            raise VerseStateError(self.state, "destroy")

    def cb_receive_create(self, *args, **kwargs):
        """
        This method is called when client receive callback function about
        it creating on Verse server
        """
        if self.state == ENTITY_RESERVED or self.state == ENTITY_CREATING:
            self.state = ENTITY_CREATED
            if self._auto_subscribe() is True:
                self.subscribe()
        elif self.state == ENTITY_ASSUMED:
            self.state = ENTITY_CREATED
        elif self.state == ENTITY_WANT_DESTROY:
            self._send_destroy()
            self.state = ENTITY_DESTROYING
        else:
            raise VerseStateError(self.state, "rcv_create")

    def cb_receive_destroy(self, *args, **kwargs):
        """
        This method is called when client receive callback function about
        it destroying on Verse server
        """
        if self.state == ENTITY_CREATED:
            self.state = ENTITY_DESTROYED
        elif self.state == ENTITY_DESTROYING:
            self.state = ENTITY_DESTROYED
            self.clean()
        else:
            raise VerseStateError(self.state, "rcv_destroy")

    def clean(self):
        """
        This method is called, when entity is switched to destroy state
        and it is required to clean all data in this entity
        """
        pass
