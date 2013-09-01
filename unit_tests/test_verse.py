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
Module for testing verse module and versentities module
"""

import unittest
import vrsent
import verse as vrs
import time
import test_node, test_tg, test_tag, test_layer


class TestSession(vrsent.VerseSession):
    """
    Class with session used in this client
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor of TestSession
        """
        super(TestSession, self).__init__(*args, **kwargs)


    def _receive_connect_accept(self, user_id, avatar_id):
        """
        Custom callback method for connect accept
        """
        # Call parent method to change state of session
        super(TestSession, self)._receive_connect_accept(user_id, avatar_id)
        # Save important informations
        self.user_id = user_id
        self.avatar_id = avatar_id
        self.test_node = None
        self.test_tg = None
        self.test_tag = None
        self.test_layer = None
        self.test_scene_node = None
        self.test_destroy_node = None
        # Scene node
        self.scene_node = None
        self.state = 'CONNECTED'
        self.verbosity = 1
        self.debug_print = True


    # Node
    def _receive_node_create(self, node_id, parent_id, user_id, custom_type):
        """
        Custom callback method that is called, when client received
        command node_create
        """
        node = super(TestSession, self)._receive_node_create(node_id, parent_id, user_id, custom_type)

        # Start all unit tests, when avatar node is created
        if node_id == self.avatar_id:

            # Save reference at avatar node
            self.avatar_node = node

            # Try to find node that is parent node of all scene nodes
            try:
                self.scene_node = self.nodes[3]
            except KeyError:
                self.scene_node = vrsent.VerseNode(session=self, \
                    node_id=3, \
                    parent=self.root_node, \
                    user_id=100,
                    custom_type=0)

            # Create test scene node
            self.test_scene_node = vrsent.VerseNode(session=self, \
                node_id=None, \
                parent=self.scene_node, \
                user_id=None,
                custom_type=16)

            # Create new test node
            self.test_node = vrsent.VerseNode(session=self, \
                node_id=None, \
                parent=self.test_scene_node, \
                user_id=None, \
                custom_type=17)

            # Create new nodes for testing of destroying nodes
            self.test_destroy_node = vrsent.VerseNode(session=self, \
                node_id=None, \
                parent=None, \
                user_id=None,
                custom_type=18)
            # Destroy node immediately
            self.test_destroy_node.destroy()

            # Create new test tag group
            self.test_node.test_tg = vrsent.VerseTagGroup(node=self.test_node, \
                tg_id=None, \
                custom_type=32)

            # Create new test tag group for testing of tag group destroying 
            self.test_node.test_destroy_tg = vrsent.VerseTagGroup(node=self.test_node, \
                tg_id=None, \
                custom_type=33)
            self.test_node.test_destroy_tg.destroy()

            # Create new test tag and set it's value
            self.test_node.test_tg.test_tag = vrsent.VerseTag(tg=self.test_node.test_tg, \
                tag_id=None, \
                data_type=vrs.VALUE_TYPE_UINT8, \
                custom_type=64,
                value=(123,))

            # Create new tag for testing of tag destroying
            self.test_node.test_tg.test_destroy_tag = vrsent.VerseTag(tg=self.test_node.test_tg, \
                tag_id=None, \
                data_type=vrs.VALUE_TYPE_UINT8, \
                custom_type=65,
                value=(124,))
            # Destroy tag immediately
            self.test_node.test_tg.test_destroy_tag.destroy()

            # Create test layer
            self.test_node.test_layer = vrsent.VerseLayer(node=self.test_node, \
                parent_layer=None, \
                data_type=vrs.VALUE_TYPE_UINT8, \
                count=1,
                custom_type=128)
            # Fill layer with test values
            for item_id in range(10):
                self.test_node.test_layer.items[item_id] = (item_id,)
            # Create child layer of destroy layer
            self.test_node.test_child_layer = vrsent.VerseLayer(node=self.test_node, \
                parent_layer=self.test_node.test_layer, \
                data_type=vrs.VALUE_TYPE_UINT8, \
                count=1,
                custom_type=129)
            # Fill child layer with test values too
            for item_id in range(10):
                self.test_node.test_child_layer.items[item_id] = (item_id,)

            # Create test layer for testing of layer destroying
            self.test_node.test_destroy_layer = vrsent.VerseLayer(node=self.test_node, \
                parent_layer=None, \
                data_type=vrs.VALUE_TYPE_UINT8, \
                count=1,
                custom_type=130)
            # Create child layer of destroy layer
            self.test_node.test_destroy_child_layer = vrsent.VerseLayer(node=self.test_node, \
                parent_layer=self.test_node.test_destroy_layer, \
                data_type=vrs.VALUE_TYPE_UINT8, \
                count=1,
                custom_type=131)
            # Destroy layer immediately
            self.test_node.test_destroy_layer.destroy()

            # Test new Node
            suite = unittest.TestLoader().loadTestsFromTestCase(test_node.TestNewNodeCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)

            # Test new TagGroup
            suite = unittest.TestLoader().loadTestsFromTestCase(test_tg.TestNewTagGroupCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)

            # Test new Tag
            suite = unittest.TestLoader().loadTestsFromTestCase(test_tag.TestNewTagCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)

            # Test new Layer
            suite = unittest.TestLoader().loadTestsFromTestCase(test_layer.TestNewLayerCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)

        # Start unit testing of created node
        if node == self.test_node:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_node.TestCreatedNodeCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)

        # Start unit testing of destroying node
        if node == self.test_destroy_node:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_node.TestDestroyNodeCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)


    def _receive_node_destroy(self, node_id):
        """
        Custom callback method for command node destroy
        """
        node = super(TestSession, self)._receive_node_destroy(node_id)
        # Start unit testing of destroyed node
        if node == self.test_destroy_node:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_node.TestDestroyedNodeCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)


    def _receive_node_perm(self, node_id, user_id, perm):
        """
        Custom callback method for testing node permission
        """
        node = super(TestSession, self)._receive_node_perm(node_id, user_id, perm)
        # Start unit testing of node with permission
        if node == self.test_node and user_id == self.user_id:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_node.TestOwnerPermNodeCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)


    def _receive_node_link(self, parent_node_id, child_node_id):
        """
        Custom callback method that is called, when client receive command changing
        link between nodes
        """
        child_node = super(TestSession, self)._receive_node_link(parent_node_id, child_node_id)
        # Start unit testing of node with changed parent
        if child_node == self.test_node:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_node.TestLinkNodeCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)


    # TagGroups
    def _receive_taggroup_create(self, node_id, taggroup_id, custom_type):
        """
        Custom callback method that is called, when client received command
        tag group create
        """
        tg = super(TestSession, self)._receive_taggroup_create(node_id, taggroup_id, custom_type)
        # Start unit testing of created tag group
        if tg == self.test_node.test_tg:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_tg.TestCreatedTagGroupCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)
        elif tg == self.test_node.test_destroy_tg:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_tg.TestDestroyingTagGroupCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)


    def _receive_taggroup_destroy(self, node_id, taggroup_id):
        """
        Custom callback method that is called, when client received command
        tag group destroy
        """
        tg = super(TestSession, self)._receive_taggroup_destroy(node_id, taggroup_id)
        # Start unit testing of destroyed tag group
        if tg == self.test_node.test_destroy_tg:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_tg.TestDestroyedTagGroupCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)


    # Tags
    def _receive_tag_create(self, node_id, taggroup_id, tag_id, data_type, count, custom_type):
        """
        Custom callback method that is called, when client receive command tag create
        """
        tag = super(TestSession, self)._receive_tag_create(node_id, taggroup_id, tag_id, data_type, count, custom_type)
        try:
            test_new_tag = self.test_node.test_tg.test_tag
        except AttributeError:
            test_new_tag = None
        try:
            test_destroy_tag = self.test_node.test_tg.test_destroy_tag
        except AttributeError:
            test_destroy_tag = None
        # Start unit testing of created tag
        if tag == test_new_tag:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_tag.TestCreatedTagCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)
        # Start unit testing of tag in destroyed state
        elif tag == test_destroy_tag:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_tag.TestDestroyingTagCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)


    def _receive_tag_destroy(self, node_id, taggroup_id, tag_id):
        """
        Custom callback used for destroying of tag
        """
        tag = super(TestSession, self)._receive_tag_destroy(node_id, taggroup_id, tag_id)
        try:
            test_destroy_tag = self.test_node.test_tg.test_destroy_tag
        except AttributeError:
            test_destroy_tag = None
        # Start unit testing of destroyed tag
        if tag == test_destroy_tag:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_tag.TestDestroyedTagCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)


    def _receive_tag_set_values(self, node_id, taggroup_id, tag_id, value):
        """
        Custom callback method that is called, when client reveive command tag set value
        """
        tag = super(TestSession, self)._receive_tag_set_values(node_id, taggroup_id, tag_id, value)
        try:
            test_tag = self.test_node.test_tg.test_tag
        except AttributeError:
            test_tag = None
        # Start unit testing of tag with changed value
        if tag == test_tag:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_tag.TestChangedTagCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)


    # Layers
    def _receive_layer_create(self, node_id, parent_layer_id, layer_id, data_type, count, custom_type):
        """
        Custom callback method that is called, when client receive command layer create
        """
        layer = super(TestSession, self)._receive_layer_create(node_id, \
            parent_layer_id, \
            layer_id, \
            data_type, \
            count, \
            custom_type)
        if layer == self.test_node.test_layer:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_layer.TestCreatedLayerCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)
        elif layer == self.test_node.test_destroy_layer:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_layer.TestDestroyingLayerCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)


    def _receive_layer_destroy(self, node_id, layer_id):
        """
        Custom callback method that is called, when client receive command layer destroy
        """
        layer = super(TestSession, self)._receive_layer_destroy(node_id, layer_id)
        if layer == self.test_node.test_destroy_layer:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_layer.TestDestroyedLayerCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)


    def _receive_layer_set_value(self, node_id, layer_id, item_id, value):
        """
        Custom callback method that is called, when client receive command layer set value of item
        """
        layer = super(TestSession, self)._receive_layer_set_value(node_id, layer_id, item_id, value)
        if layer == self.test_node.test_layer:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_layer.TestLayerSetValueCase)
            unittest.TextTestRunner(verbosity=self.verbosity).run(suite)        


    def _receive_layer_unset_value(self, node_id, layer_id, item_id):
        """
        Custom callback method that is called, when client receive command layer unset value of item
        """
        layer = super(TestSession, self)._receive_layer_unset_value(node_id, layer_id, item_id)
        # TODO: add test


    def _receive_connect_terminate(self, error):
        """
        Custom callback method for fake connect terminate command
        """
        self.state = 'DISCONNECTED'


def main(hostname, username, password):
    """
    Function with main never ending verse loop
    """
    vrsent.session = TestSession(hostname, "12345", vrs.DGRAM_SEC_DTLS)
    vrsent.session.username = username
    vrsent.session.password = password

    DELAY = 0.05
    counter = 0

    while(vrsent.session.state != 'DISCONNECTED'):
        vrsent.session.callback_update()
        time.sleep(DELAY)
        counter += 1
        # Send connect termintate after 5 seconds
        if(counter == 100):
            vrsent.session.send_connect_terminate()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', nargs='?', default='localhost', help='Hostname of Verse server')
    parser.add_argument('--username', nargs='?', default=None, help='Username')
    parser.add_argument('--password', nargs='?', default=None, help='Password')
    args = parser.parse_args()
    #vrs.set_debug_level(vrs.PRINT_DEBUG_MSG)
    vrs.set_client_info("Python UnitTest Verse Client", "0.1")
    main(args.hostname, args.username, args.password)
