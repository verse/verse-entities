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


import sys
if sys.version >= '2.7':
    import unittest
else:
    import unittest2 as unittest
import vrsent
import verse as vrs


TEST_NODE_CUSTOM_TYPE = 219
TEST_TG_CUSTOM_TYPE = 34
TEST_LAYER_CUSTOM_TYPE = 132
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
        Constructor of class
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


class TestTagGroup(vrsent.VerseTagGroup):
    """
    Custom subclass of VerseTagGroup
    """

    custom_type = TEST_TG_CUSTOM_TYPE
    node_custom_type = TEST_NODE_CUSTOM_TYPE

    rec_tg_crt_callbacks = {}

    def __init__(self, node, tg_id=None, custom_type=TEST_TG_CUSTOM_TYPE):
        """
        Constructor of custom TestTagGroup
        """
        super(TestTagGroup, self).__init__(node=node, tg_id=tg_id, custom_type=custom_type)
        self.test_tag = TestTag(tg=self)

    @classmethod
    def _receive_tg_create(cls, session, node_id, tg_id, custom_type):
        """
        Custom callback method called, when this custom_type of VerseTagGroup is
        created by verse server and appropriate command is received.
        """
        cls.rec_tg_crt_callbacks[(node_id, tg_id)] = cls.__name__
        return super(TestTagGroup, cls)._receive_tg_create(session, node_id, tg_id, custom_type)


class SuperTestTagGroup(TestTagGroup):
    """
    Subclass of VerseTagGroup
    """

    @classmethod
    def _receive_tg_create(cls, session, node_id, tg_id, custom_type):
        """
        Custom callback method called, when this custom_type of VerseTagGroup is
        created by verse server and appropriate command is received.
        """
        cls.rec_tg_crt_callbacks[(node_id, tg_id)] = cls.__name__
        return super(SuperTestTagGroup, cls)._receive_tg_create(session, node_id, tg_id, custom_type)


class TestLayer(vrsent.VerseLayer):
    """
    Custom subclass of VerseLayer
    """

    custom_type = TEST_LAYER_CUSTOM_TYPE
    node_custom_type = TEST_NODE_CUSTOM_TYPE

    rec_layer_crt_callbacks = {}

    def __init__(self,
                 node,
                 parent_layer=None,
                 layer_id=None,
                 data_type=vrs.VALUE_TYPE_UINT8, 
                 count=1,
                 custom_type=TEST_LAYER_CUSTOM_TYPE):
        """
        Constructor of custom TestLayer
        """
        super(TestLayer, self).__init__(node=node,
                                        parent_layer=parent_layer,
                                        layer_id=layer_id,
                                        data_type=data_type,
                                        count=count,
                                        custom_type=custom_type)
        for item_id in range(10):
            self.items[item_id] = (item_id,)

    @classmethod
    def _receive_layer_create(cls, session, node_id, parent_layer_id, layer_id, data_type, count, custom_type):
        """
        Custom callback method called, when this custom_type of VerseLaer is
        created by verse server and appropriate command is received.
        """
        cls.rec_layer_crt_callbacks[(node_id, layer_id)] = cls.__name__
        return super(TestLayer, cls)._receive_layer_create(session, node_id, parent_layer_id, layer_id, data_type, count, custom_type)


class SuperTestLayer(TestLayer):
    """
    Subclass of VerseTagGroup
    """

    @classmethod
    def _receive_layer_create(cls, session, node_id, parent_layer_id, layer_id, data_type, count, custom_type):
        """
        Custom callback method called, when this custom_type of VerseLaer is
        created by verse server and appropriate command is received.
        """
        cls.rec_layer_crt_callbacks[(node_id, layer_id)] = cls.__name__
        return super(TestLayer, cls)._receive_layer_create(session, node_id, parent_layer_id, layer_id, data_type, count, custom_type)


class CustomTag(vrsent.VerseTag):
    """
    Another subclass of VerseTag
    """

    def __init__(self, tg, tag_id=None, data_type=vrs.VALUE_TYPE_UINT8, count=1, custom_type=None, value=(0,)):
        """
        Constructor of CustomTag
        """
        super(CustomTag, self).__init__(tg=tg, tag_id=tag_id, data_type=data_type, count=count, custom_type=custom_type, value=value)


class CustomTagGroup(vrsent.VerseTagGroup):
    """
    Another subclass of VerseTagGroup
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
        super(CustomTagGroup, self).__init__(*args, **kwargs)


class CustomNode(vrsent.VerseNode):
    """
    Another subclass of VerseNode
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor of CustomNode
        """
        super(CustomNode, self).__init__(*args, **kwargs)
        self.custom_tg = CustomTagGroup(node=self)


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
        self.test_tg = TestTagGroup(node=self)
        self.test_layer = TestLayer(node=self)

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


class TestSubclassLayerCase(unittest.TestCase):
    """
    Test case of custom VerseTagGroup subclass
    """

    node = None
    layer = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        cls.node = vrsent.session.test_subclass_node
        cls.layer   = vrsent.session.test_subclass_node.test_layer
        cls.tested = True

    def test_layer_custom_type(self):
        """
        Test of creating new layer
        """
        self.assertEqual(self.layer.custom_type, TEST_LAYER_CUSTOM_TYPE)

    def test_layer_instance(self):
        """
        Test of subclassing of layer
        """
        self.assertTrue(isinstance(self.layer, TestLayer))

    def test_layer_custom_create_callback(self):
        """
        Test if custom callback method was called
        """
        self.assertEqual(self.layer.rec_layer_crt_callbacks[(self.node.id, self.layer.id)], \
            'SuperTestLayer')


class TestSubclassTagGroupCase(unittest.TestCase):
    """
    Test case of custom VerseTagGroup subclass
    """

    node = None
    tg = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        cls.node = vrsent.session.test_subclass_node
        cls.tg   = vrsent.session.test_subclass_node.test_tg
        cls.tested = True

    def test_tg_custom_type(self):
        """
        Test of creating new tag group
        """
        self.assertEqual(self.tg.custom_type, TEST_TG_CUSTOM_TYPE)

    def test_tg_instance(self):
        """
        Test of subclassing of tag group
        """
        self.assertTrue(isinstance(self.tg, TestTagGroup))

    def test_tg_custom_create_callback(self):
        """
        Test if custom callback method was called
        """
        self.assertEqual(self.tg.rec_tg_crt_callbacks[(self.node.id, self.tg.id)], \
            'SuperTestTagGroup')


class TestSubclassTagCase(unittest.TestCase):
    """
    Test case of custom VerseTag subclass
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

    def test_tag_custom_type(self):
        """
        Test of creating new tag
        """      
        self.assertEqual(self.tag.custom_type, TEST_TAG_CUSTOM_TYPE)

    def test_tag_instance(self):
        """
        Test of subclassing of tag
        """
        self.assertTrue(isinstance(self.tag, TestTag))

    def test_tag_custom_create_callback(self):
        """
        Test if custom callback method was called
        """
        self.assertEqual(self.tag.rec_nt_crt_callbacks[(self.node.id, self.tg.id, self.tag.id)], \
            'SuperTestTag')
