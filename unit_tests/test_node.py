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
Module for testing class VerseNode from module verse entities (vrsent)
"""

import sys
if sys.version >= '2.7':
    import unittest
else:
    import unittest2 as unittest
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
        cls.node = vrsent.session.test_node
        cls.tested = True

    def test_node_unlocked(self):
        """
        This method test if node is unlocked
        """
        self.assertEqual(self.node.locked, False)

    def test_node_locker(self):
        """
        This method tests if node was unlocked
        """
        self.assertEqual(self.node.locker, None)


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
        cls.node = vrsent.session.test_node
        cls.tested = True

    def test_node_locked(self):
        """
        This method test if node is locked
        """
        self.assertEqual(self.node.locked, True)

    def test_node_locker(self):
        """
        This method tests if node was locked by this client app
        """
        session = self.node.session
        avatar = session.avatars[session.avatar_id]
        self.assertEqual(self.node.locker, avatar)


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
        cls.node = vrsent.session.test_node
        cls.tested = True

    def test_node_owner_perm(self):
        """
        Testing permissions for owner of node
        """
        self.assertEqual(self.node.perm[vrsent.session.user_id], \
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

        cls.child_node = vrsent.session.test_link_node
        cls.parent_node = vrsent.session.test_scene_node
        cls.avatar_node = vrsent.session.avatar_node
        cls.tested = True

    def test_child_node_link(self):
        """
        Test of node with changed link to parent node
        """      
        self.assertEqual(self.child_node.parent, self.parent_node)

    def test_parent_node_link(self):
        """
        Test that new parent node includes child node in
        dictionary of child nodes
        """
        self.assertEqual(self.parent_node.child_nodes[self.child_node.id], self.child_node)

    def test_avatar_child_nodes(self):
        """
        Test that original parent node (avatar node) does not include
        reference at node anymore
        """
        try:
            node = self.avatar_node.child_nodes[self.child_node.id]
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
        cls.node = vrsent.session.test_destroy_node
        cls.tested = True

    def test_node_destroying(self):
        """
        Test of creating new node
        """      
        self.assertEqual(self.node.state, vrsent.verse_entity.ENTITY_DESTROYED)


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
        cls.node = vrsent.session.test_destroy_node
        cls.tested = True

    def test_node_destroying(self):
        """
        Test of creating new node
        """      
        self.assertEqual(self.node.state, vrsent.verse_entity.ENTITY_DESTROYING)


class TestCreatedNodeCase(unittest.TestCase):
    """
    Test case of created VerseNode
    """

    node = None
    avatar_node = None
    tested = False

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        cls.node = vrsent.session.test_node
        cls.avatar_node = vrsent.session.nodes[vrsent.session.avatar_id]
        cls.tested = True

    def test_node_created(self):
        """
        Test of creating new node
        """      
        self.assertEqual(self.node.state, vrsent.verse_entity.ENTITY_CREATED)

    def test_node_id(self):
        """
        Test of node ID
        """      
        self.assertIsNotNone(self.node.id)

    def test_node_subscribed(self):
        """
        Test of node subscribtion
        """      
        self.assertEqual(self.node.subscribed, True)

    def test_parent_node(self):
        """
        Test of parent node
        """
        self.assertEqual(self.node.parent, self.avatar_node)

    def test_node_is_child_node(self):
        """
        Test if new node is in child nodes of avatar node
        """
        self.assertEqual(self.avatar_node.child_nodes[self.node.id], self.node)

    def test_node_owner(self):
        """
        Test if owner of new node is current users
        """
        self.assertEqual(self.node.user_id, vrsent.session.user_id)


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
        cls.node = vrsent.session.test_node
        cls.tested = True

    def test_node_not_created(self):
        """
        Test of creating new node
        """      
        self.assertEqual(self.node.state, vrsent.verse_entity.ENTITY_CREATING)

    def test_node_not_subscribed(self):
        """
        Test of creating new node
        """      
        self.assertEqual(self.node.subscribed, False)
