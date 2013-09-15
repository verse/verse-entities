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


class TestUnLockNodeCase(unittest.TestCase):
    """
    Test case of VerseNode unlocking
    """

    node = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        __class__.node = vrsent.session.test_node
        __class__.tested = True

    def test_node_unlocked(self):
        """
        This method test if node is unlocked
        """
        self.assertEqual(__class__.node.locked, False)

    def test_node_locker(self):
        """
        This method tests if node was unlocked
        """
        self.assertEqual(__class__.node.locker, None)


class TestLockNodeCase(unittest.TestCase):
    """
    Test case of VerseNode locking
    """

    node = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        __class__.node = vrsent.session.test_node
        __class__.tested = True

    def test_node_locked(self):
        """
        This method test if node is locked
        """
        self.assertEqual(__class__.node.locked, True)

    def test_node_locker(self):
        """
        This method tests if node was locked by this client app
        """
        session = __class__.node.session
        avatar = session[session.avatar_id]
        self.assertEqual(__class__.node.locker, avatar)


class TestOwnerPermNodeCase(unittest.TestCase):
    """
    Test case of VerseNode with access permissions
    """

    node = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        __class__.node = vrsent.session.test_node
        __class__.tested = True

    def test_node_owner_perm(self):
        """
        Testing permissions for owner of node
        """
        self.assertEqual(__class__.node.perm[vrsent.session.user_id], \
            vrs.PERM_NODE_READ | vrs.PERM_NODE_WRITE)


class TestLinkNodeCase(unittest.TestCase):
    """
    Test case of VerseNode with changed link to parent node
    """

    child_node = None
    parent_node = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        __class__.child_node = vrsent.session.test_node
        __class__.parent_node = vrsent.session.test_scene_node
        __class__.avatar_node = vrsent.session.avatar_node
        __class__.tested = True

    def test_child_node_link(self):
        """
        Test of node with changed link to parent node
        """      
        self.assertEqual(__class__.child_node.parent, __class__.parent_node)

    def test_parent_node_link(self):
        """
        Test that new parent node includes child node in
        dictionary of child nodes
        """
        self.assertEqual(__class__.parent_node.child_nodes[__class__.child_node.id], __class__.child_node)

    def test_avatar_child_nodes(self):
        """
        Test that original parent node (avatar node) does not include
        reference at node anymore
        """
        try:
            node = __class__.avatar_node.child_nodes[__class__.child_node.id]
        except KeyError:
            node = None
        self.assertIsNone(node)


class TestDestroyedNodeCase(unittest.TestCase):
    """
    Test case of destroying of VerseNode
    """

    node = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        __class__.node = vrsent.session.test_destroy_node
        __class__.tested = True

    def test_node_destroying(self):
        """
        Test of creating new node
        """      
        self.assertEqual(__class__.node.state, vrsent.verse_entity.ENTITY_DESTROYED)


class TestDestroyNodeCase(unittest.TestCase):
    """
    Test case of destroying of VerseNode
    """

    node = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        __class__.node = vrsent.session.test_destroy_node
        __class__.tested = True

    def test_node_destroying(self):
        """
        Test of creating new node
        """      
        self.assertEqual(__class__.node.state, vrsent.verse_entity.ENTITY_DESTROYING)


class TestCreatedNodeCase(unittest.TestCase):
    """
    Test case of created VerseNode
    """

    node = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        __class__.node = vrsent.session.test_node
        __class__.tested = True

    def test_node_created(self):
        """
        Test of creating new node
        """      
        self.assertEqual(__class__.node.state, vrsent.verse_entity.ENTITY_CREATED)

    def test_node_id(self):
        """
        Test of node ID
        """      
        self.assertIsNotNone(__class__.node.id)

    def test_node_subscribed(self):
        """
        Test of node subscribtion
        """      
        self.assertEqual(__class__.node.subscribed, True)


class TestNewNodeCase(unittest.TestCase):
    """
    Test case of new VerseNode
    """

    node = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        __class__.node = vrsent.session.test_node
        __class__.tested = True

    def test_node_not_created(self):
        """
        Test of creating new node
        """      
        self.assertEqual(__class__.node.state, vrsent.verse_entity.ENTITY_CREATING)

    def test_node_not_subscribed(self):
        """
        Test of creating new node
        """      
        self.assertEqual(__class__.node.subscribed, False)
