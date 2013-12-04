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
Module for testing explicit subscribing to custom subclasses of
VerseEntity subclasses (custom VerseNode, VerseTagGroup and VerseLayer)
"""

import sys
if sys.version >= '2.7':
    import unittest
else:
    import unittest2 as unittest
import vrsent
import verse as vrs


TEST_NODE_CUSTOM_TYPE = 220


class SubscribeNode(vrsent.VerseNode):
    """
    Subclass of VerseNode for testing explicit subscribing
    """

    custom_type = TEST_NODE_CUSTOM_TYPE

    def __init__(self, session, node_id=None, parent=None, user_id=None, custom_type=TEST_NODE_CUSTOM_TYPE):
        """
        Constructor of SubscribeNode
        """
        super(SubscribeNode, self).__init__(session=session, node_id=node_id, parent=parent, user_id=user_id, custom_type=custom_type)

    def _auto_subscribe(self):
    	"""
    	Automatic subscribing is disables. Client has to call node.subscribe() to
    	subscribe to node instanced from this class.
    	"""
    	return False

    @classmethod
    def _receive_node_create(cls, session, node_id, parent_id, user_id, custom_type):
        """
        Custom callback method called, when this custom_type of VerseNode is
        created by verse server and appropriate command is received.
        """
        return super(SubscribeNode, cls)._receive_node_create(session, node_id, parent_id, user_id, custom_type)


class TestSubscribeNodeCase(unittest.TestCase):
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
        cls.node = vrsent.session.test_subscribe_node
        cls.tested = True

    def test_node_unsubscribed(self):
        """
        Test that created node is unsubscribed
        """      
        self.assertEqual(self.node.subscribed, False)