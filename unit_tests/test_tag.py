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
Module for testing class VerseTag from module versentities
"""


import unittest
import versentities as vrsent


class TestChangedTagCase(unittest.TestCase):
    """
    Test case of VerseTag values
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
        __class__.tg = vrsent.session.test_node.test_tg
        __class__.tag = vrsent.session.test_node.test_tg.test_tag

    def test_tag_value(self):
        """
        Test of tag value
        """      
        self.assertEqual(__class__.tag.value, (123,))

    @classmethod
    def tearDownClass(cls):
        """
        This method is called, when all method has been performed
        """
        vrsent.session.send_connect_terminate()


class TestDestroyingTagCase(unittest.TestCase):
    """
    Test case of destroying VerseTag
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
        __class__.tg = vrsent.session.test_node.test_tg
        __class__.tag = vrsent.session.test_node.test_tg.test_destroy_tag

    def test_tag_destroying(self):
        """
        Test of state of destroying tag
        """      
        self.assertEqual(__class__.tag.state, vrsent.verse_entity.ENTITY_DESTROYING)


class TestDestroyedTagCase(unittest.TestCase):
    """
    Test case of destroyed VerseTag
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
        __class__.tg = vrsent.session.test_node.test_tg
        __class__.tag = vrsent.session.test_node.test_tg.test_destroy_tag

    def test_tag_destroyed(self):
        """
        Test of state of destroyed tag
        """      
        self.assertEqual(__class__.tag.state, vrsent.verse_entity.ENTITY_DESTROYED)


class TestCreatedTagCase(unittest.TestCase):
    """
    Test case of created VerseTag
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
        __class__.tg = vrsent.session.test_node.test_tg
        __class__.tag = vrsent.session.test_node.test_tg.test_tag

    def test_tag_created(self):
        """
        Test of state of created tag
        """      
        self.assertEqual(__class__.tag.state, vrsent.verse_entity.ENTITY_CREATED)


class TestNewTagCase(unittest.TestCase):
    """
    Test case of new VerseTag
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
        __class__.tg = vrsent.session.test_node.test_tg
        __class__.tag = vrsent.session.test_node.test_tg.test_tag

    def test_tag_not_created(self):
        """
        Test of state of created tag
        """      
        self.assertEqual(__class__.tag.state, vrsent.verse_entity.ENTITY_CREATING)
