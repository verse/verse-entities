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


ENTITY_RESERVED     = 0
ENTITY_CREATING     = 1
ENTITY_CREATED      = 2
ENTITY_ASSUMED      = 3
ENTITY_WANT_DESTROY = 4
ENTITY_DESTROYING   = 5
ENTITY_DESTROYED    = 6


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
        # When custom_type is not defined, then compute custom_type from
        # class name as modulo 65535 of original cutom_type hash
        custom_type = kwargs.get('custom_type', 0)
        if custom_type is None:
            # TODO: replace it with something more reliable
            self.custom_type = hash(self.__class__.__name__) % 65535
        else:
            if type(custom_type) == int:
                self.custom_type = custom_type
            else:
                self.custom_type = hash(custom_type) % 65535

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

    def _send_subscribe(self):
        """
        Dummy method
        """
        pass

    def _send_unsubscribe(self):
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
                self._send_subscribe()
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

    def _receive_create(self, *args, **kwargs):
        """
        This method is called when client receive callback function about
        it creating on Verse server
        """
        if self.state == ENTITY_RESERVED or self.state == ENTITY_CREATING:
            self.state = ENTITY_CREATED
            self._send_subscribe()
        elif self.state == ENTITY_ASSUMED:
            self.state = ENTITY_CREATED
        elif self.state == ENTITY_WANT_DESTROY:
            self._send_destroy()
            self.state = ENTITY_DESTROYING
        else:
            raise VerseStateError(self.state, "rcv_create")

    def _receive_destroy(self, *args, **kwargs):
        """
        This method is called when client receive callback function about
        it destroying on Verse server
        """
        if self.state == ENTITY_CREATED:
            self.state = ENTITY_DESTROYED
        elif self.state == ENTITY_DESTROYING:
            self.state = ENTITY_DESTROYED
            self._clean()
        else:
            raise VerseStateError(self.state, "rcv_destroy")

    def _clean(self):
        """
        This method is called, when entity is switched to destroy state
        and it is required to clean all data in this entity
        """
        pass