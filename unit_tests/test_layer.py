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
import versentities as vrsent


class TestNewLayerCase(unittest.TestCase):
    """
    Test case of VerseLayer
    """

    node = None
    layer = None

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        __class__.node = vrsent.session.test_node
        __class__.layer = vrsent.session.test_node.test_layer

    def test_layer_not_created(self):
        """
        Test of creating new tag group
        """      
        self.assertEqual(__class__.layer.state, vrsent.verse_entity.ENTITY_CREATING)

    def test_layer_not_subscribed(self):
        """
        Test of subscription of new tag group
        """      
        self.assertEqual(__class__.layer.subscribed, False)


class TestCreatedLayerCase(unittest.TestCase):
    """
    Test case of created VerseLayer
    """

    node = None
    layer = None

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        __class__.node = vrsent.session.test_node
        __class__.layer = vrsent.session.test_node.test_layer

    def test_layer_created(self):
        """
        Test of state of created layer
        """      
        self.assertEqual(__class__.layer.state, vrsent.verse_entity.ENTITY_CREATED)

    def test_layer_id(self):
        """
        Test of layer ID
        """      
        self.assertIsNotNone(__class__.layer.id)

    def test_layer_subscribed(self):
        """
        Test of subscription of created layer
        """      
        self.assertEqual(__class__.layer.subscribed, True)