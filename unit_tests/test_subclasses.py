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


TEST_NODE_CUSTOM_TYPE = 19
TEST_TG_CUSTOM_TYPE = 34
TEST_TAG_CUSTOM_TYPE = 66


class TestTag(vrsent.VerseTag):
    """
    Subclass of VerseTag
    """
    custom_type = TEST_TAG_CUSTOM_TYPE
    tg_custom_type = TEST_TG_CUSTOM_TYPE
    node_custom_type = TEST_NODE_CUSTOM_TYPE

    rec_nt_crt_callbacks = {}

    def __init__(self, tg, tag_id=None, data_type=vrs.VALUE_TYPE_UINT8, count=1, custom_type=None, value=(0,)):
        """
        Construcor of class
        """
        super(TestTag, self).__init__(tg=tg, tag_id=tag_id, data_type=data_type, count=count, custom_type=custom_type, value=value)


    @classmethod
    def _receive_tag_create(cls, session, node_id, tg_id, tag_id, data_type, count, custom_type):
        """
        Custom callback method of subclass
        """
        cls.rec_nt_crt_callbacks[(node_id, tg_id, tag_id)] = cls.__name__
        return super(TestTag, cls)._receive_tag_create(session, node_id, tg_id, tag_id, data_type, count, custom_type)


class SuperTestTag(TestTag):
    """
    Subclass of TestTag
    """

    @classmethod
    def _receive_tag_create(cls, session, node_id, tg_id, tag_id, data_type, count, custom_type):
        """
        Custom callback method of subclass
        """
        cls.rec_nt_crt_callbacks[(node_id, tg_id, tag_id)] = cls.__name__
        return super(SuperTestTag, cls)._receive_tag_create(session, node_id, tg_id, tag_id, data_type, count, custom_type)


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
        cls.rec_nd_crt_callbacks[node_id] = cls.__name__
        return super(TestNode, cls)._receive_node_create(session, node_id, parent_id, user_id, custom_type)


class SuperTestNode(TestNode):
    """
    Subclass of TestNode
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor of this subclass
        """
        super(SuperTestNode, self).__init__(*args, **kwargs)
        self.test_tg = vrsent.VerseTagGroup(node=self, custom_type=TEST_TG_CUSTOM_TYPE)
        self.test_tg.test_tag = TestTag(tg=self.test_tg)

    @classmethod
    def _receive_node_create(cls, session, node_id, parent_id, user_id, custom_type):
        """
        Custom callback method called, when this custom_type of VerseNode is
        created by verse server and appropriate command is received.
        """
        cls.rec_nd_crt_callbacks[node_id] = cls.__name__
        return super(SuperTestNode, cls)._receive_node_create(session, node_id, parent_id, user_id, custom_type)


class TestSubclassNodeCase(unittest.TestCase):
    """
    Test case of new TestNode and SuperTestNode
    """

    node = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        cls.node = vrsent.session.test_subclass_node
        cls.tested = True

    def test_node_custom_type(self):
        """
        Test of creating new node
        """      
        self.assertEqual(self.node.custom_type, TEST_NODE_CUSTOM_TYPE)

    def test_node_instance(self):
        """
        Test of subclassing of node
        """
        self.assertTrue(isinstance(self.node, SuperTestNode))

    def test_node_custom_create_callback(self):
        """
        Test if custom callback method was called
        """
        self.assertEqual(self.node.rec_nd_crt_callbacks[self.node.id], 'SuperTestNode')


class TestSubclassTagCase(unittest.TestCase):
    """
    Test case of new TestTag
    """

    node = None
    tg = None
    tag = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        cls.node = vrsent.session.test_subclass_node
        cls.tg   = vrsent.session.test_subclass_node.test_tg
        cls.tag  = vrsent.session.test_subclass_node.test_tg.test_tag
        cls.tested = True

    def test_node_custom_type(self):
        """
        Test of creating new node
        """      
        self.assertEqual(self.tag.custom_type, TEST_TAG_CUSTOM_TYPE)

    def test_node_instance(self):
        """
        Test of subclassing of node
        """
        self.assertTrue(isinstance(self.tag, TestTag))

    def test_node_custom_create_callback(self):
        """
        Test if custom callback method was called
        """
        self.assertEqual(self.tag.rec_nt_crt_callbacks[(self.node.id, self.tg.id, self.tag.id)], \
            'SuperTestTag')
