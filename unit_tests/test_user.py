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
Module for testing class VerseUser from module versentities
"""


import sys
if sys.version >= '2.7':
    import unittest
else:
    import unittest2 as unittest
import vrsent


class TestUserCase(unittest.TestCase):
    """
    Test case of VerseUser
    """

    @classmethod
    def setUpClass(cls):
        """
        This method is called before any test is performed
        """
        print('Verse Users:')
        for user in vrsent.session.users.values():
            print(user)

    def test_user_count(self):
        """
        Test of users count. There should be at least three:
        Super users, Other users and current user
        """      
        self.assertGreaterEqual(len(vrsent.session.users), 3)

    def test_user_name(self):
        """
        Test non-zero length of current user
        """
        user_id = vrsent.session.user_id
        self.assertGreater(len(vrsent.session.users[user_id].name), 0)
