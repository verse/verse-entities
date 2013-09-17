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
Module for testing class VerseAvatar from module versentities
"""


import unittest
import vrsent
import verse as vrs

class TestAvatarCase(unittest.TestCase):
    """
    Test case of VerseAvatar
    """

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        print('Verse Avatars:')
        for avatar in vrsent.session.avatars.values():
            print(avatar)
        

    def test_avatar_count(self):
        """
        Test of avatars count. There should be at least one
        """      
        self.assertGreaterEqual(len(vrsent.session.avatars), 1)


    def test_avatar_name(self):
        """
        Test non-zero length of current avatar name
        """
        avatar_id = vrsent.session.avatar_id
        self.assertGreater(len(vrsent.session.avatars[avatar_id].username), 0)


    def test_avatar_hostname(self):
        """
        Test non-zero length of current avatar hostname
        """
        avatar_id = vrsent.session.avatar_id
        self.assertGreater(len(vrsent.session.avatars[avatar_id].hostname), 0)


    def test_avatar_client_name(self):
        """
        Test non-zero length of current avatar client name
        """
        avatar_id = vrsent.session.avatar_id
        self.assertGreater(len(vrsent.session.avatars[avatar_id].client_name), 0)


    def test_avatar_client_version(self):
        """
        Test non-zero length of current avatar client version
        """
        avatar_id = vrsent.session.avatar_id
        self.assertGreater(len(vrsent.session.avatars[avatar_id].client_version), 0)


    def test_avatar_login_time(self):
        """
        Test non-zero value of current avatar login time
        """
        avatar_id = vrsent.session.avatar_id
        self.assertGreater(vrsent.session.avatars[avatar_id].login_time, 0)
