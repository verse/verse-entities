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
This module implements object model of data shared at Verse server. it
provides classes for Node, TagGroup, Tag and Layer.
"""

from verse_session import VerseSession
from verse_node import VerseNode
from verse_tag_group import VerseTagGroup
from verse_tag import VerseTag
from verse_layer import VerseLayer

__all__ = ['VerseSession', 'VerseNode', 'VerseTagGroup', 'VerseTag', 'VerseLayer']