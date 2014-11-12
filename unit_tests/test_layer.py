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
Module for testing class VerseTagGroup from module vrsent (verse entities)
"""

import sys
if sys.version >= '2.7':
    import unittest
else:
    import unittest2 as unittest
import vrsent


class TestLayerSetValueCase(unittest.TestCase):
    """
    Test case of set value of layer
    """

    node = None
    layer = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        cls.node = vrsent.session.test_node
        cls.layer = vrsent.session.test_node.test_destroy_layer
        cls.tested = True

    def test_layer_set_value(self):
        """
        Test of destroyed layer
        """
        for key, value in self.layer.items.items():
            self.assertEqual(key, value)


class TestDestroyedLayerCase(unittest.TestCase):
    """
    Test case of destroyed VerseLayer
    """

    node = None
    layer = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        cls.node = vrsent.session.test_node
        cls.layer = vrsent.session.test_node.test_destroy_layer
        cls.tested = True

    def test_layer_destroyed(self):
        """
        Test of destroyed layer
        """      
        self.assertEqual(self.layer.state, vrsent.verse_entity.ENTITY_DESTROYED)


class TestDestroyingLayerCase(unittest.TestCase):
    """
    Test case of destroying VerseLayer
    """

    node = None
    layer = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        cls.node = vrsent.session.test_node
        cls.layer = vrsent.session.test_node.test_destroy_layer
        cls.tested = True

    def test_layer_destroying(self):
        """
        Test of destroying layer
        """      
        self.assertEqual(self.layer.state, vrsent.verse_entity.ENTITY_DESTROYING)


class TestNewLayerCase(unittest.TestCase):
    """
    Test case of VerseLayer
    """

    node = None
    layer = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        cls.node = vrsent.session.test_node
        cls.layer = vrsent.session.test_node.test_layer
        cls.tested = True

    def test_layer_not_created(self):
        """
        Test of creating new layer
        """      
        self.assertEqual(self.layer.state, vrsent.verse_entity.ENTITY_CREATING)

    def test_layer_not_subscribed(self):
        """
        Test of subscription of new layer
        """      
        self.assertEqual(self.layer.subscribed, False)


class TestCreatedLayerCase(unittest.TestCase):
    """
    Test case of created VerseLayer
    """

    node = None
    layer = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        cls.node = vrsent.session.test_node
        cls.layer = vrsent.session.test_node.test_layer
        cls.tested = True

    def test_layer_created(self):
        """
        Test of state of created layer
        """      
        self.assertEqual(self.layer.state, vrsent.verse_entity.ENTITY_CREATED)

    def test_layer_id(self):
        """
        Test of layer ID
        """      
        self.assertIsNotNone(self.layer.id)

    def test_layer_subscribed(self):
        """
        Test of subscription of created layer
        """      
        self.assertEqual(self.layer.subscribed, True)

    def test_layer_in_node(self):
        """
        Test of existence layer in dictionary of node
        """
        self.assertTrue(self.layer.id in self.node.layers)
