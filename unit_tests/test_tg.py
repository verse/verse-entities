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
Module for testing class VerseTagGroup from module versentities
"""

import unittest
import vrsent


class TestDestroyingTagGroupCase(unittest.TestCase):
    """
    Test case of destroying VerseTagGroup
    """

    node = None
    tg = None
    tag = None

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        __class__.node = vrsent.session.test_node
        __class__.tg = vrsent.session.test_node.test_destroy_tg

    def test_tg_destroying(self):
        """
        Test of state of destroying tag
        """      
        self.assertEqual(__class__.tg.state, vrsent.verse_entity.ENTITY_DESTROYING)


class TestDestroyedTagGroupCase(unittest.TestCase):
    """
    Test case of destroyed VerseTagGroup
    """

    node = None
    tg = None

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        __class__.node = vrsent.session.test_node
        __class__.tg = vrsent.session.test_node.test_destroy_tg

    def test_tgp_destroyed(self):
        """
        Test of state of destroyed tag group
        """      
        self.assertEqual(__class__.tg.state, vrsent.verse_entity.ENTITY_DESTROYED)


class TestCreatedTagGroupCase(unittest.TestCase):
    """
    Test case of VerseTagGroup
    """

    node = None
    tg = None

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        __class__.node = vrsent.session.test_node
        __class__.tg = vrsent.session.test_node.test_tg

    def test_tg_created(self):
        """
        Test of state of created tag group
        """      
        self.assertEqual(__class__.tg.state, vrsent.verse_entity.ENTITY_CREATED)

    def test_tg_id(self):
        """
        Test of tag group ID
        """      
        self.assertIsNotNone(__class__.tg.id)

    def test_tg_subscribed(self):
        """
        Test of subscription of created tag group
        """      
        self.assertEqual(__class__.tg.subscribed, True)


class TestNewTagGroupCase(unittest.TestCase):
    """
    Test case of VerseTagGroup
    """

    node = None
    tg = None

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        __class__.node = vrsent.session.test_node
        __class__.tg = vrsent.session.test_node.test_tg

    def test_tg_not_created(self):
        """
        Test of creating new tag group
        """      
        self.assertEqual(__class__.tg.state, vrsent.verse_entity.ENTITY_CREATING)

    def test_tg_not_subscribed(self):
        """
        Test of subscription of new tag group
        """      
        self.assertEqual(__class__.tg.subscribed, False)
