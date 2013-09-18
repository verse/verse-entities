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
Module for testing class VerseNode from module versentities
"""


import unittest
import vrsent
import verse as vrs


TEST_NODE_CUSTOM_TYPE = 100


class TestNode(vrsent.VerseNode):
    """
    Subclass of VerseNode
    """
    custom_type = TEST_NODE_CUSTOM_TYPE

    rec_nd_crt_callbacks = {}

    @classmethod
    def _receive_node_create(cls, session, node_id, parent_id, user_id, custom_type):
        """
        Custom callback method called, when this custom_type of VerseNode is
        created by verse server and appropriate command is received.
        """
        cls.rec_nd_crt_callbacks[node_id] = True
        return super(TestNode, cls)._receive_node_create(session, node_id, parent_id, user_id, custom_type)


class SuperTestNode(TestNode):
    """
    Subclass of TestNode and VerseNode
    """
    @classmethod
    def _receive_node_create(cls, session, node_id, parent_id, user_id, custom_type):
        """
        Custom callback method called, when this custom_type of VerseNode is
        created by verse server and appropriate command is received.
        """
        cls.rec_nd_crt_callbacks[node_id] = False
        return super(TestNode, cls)._receive_node_create(session, node_id, parent_id, user_id, custom_type)


class TestSubclassNodeCase(unittest.TestCase):
    """
    Test case of new TestNode
    """

    node = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        __class__.node = vrsent.session.test_subclass_node
        __class__.tested = True

    def test_node_custom_type(self):
        """
        Test of creating new node
        """      
        self.assertEqual(__class__.node.custom_type, TEST_NODE_CUSTOM_TYPE)

    def test_node_instance(self):
        """
        Test of subclassing of node
        """
        self.assertTrue(isinstance(__class__.node, SuperTestNode))

    def test_node_custom_create_callback(self):
        """
        Test if custom callback method was called
        """
        self.assertFalse(__class__.node.rec_nd_crt_callbacks[__class__.node.id])
