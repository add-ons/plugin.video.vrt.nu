# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for Favorites functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from random import shuffle
from api import get_recent_episodes, get_programs, get_offline_programs
from favorites import Favorites

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

addon = xbmcaddon.Addon()
addon.settings['usefavorites'] = True
itemsperpage = int(addon.settings.get('itemsperpage'))


class TestFavorites(unittest.TestCase):
    """TestCase class"""

    _favorites = Favorites()

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_get_recent_episodes(self):
        """Test items, sort and order"""
        episode_items, sort, ascending, content = get_recent_episodes(use_favorites=True)
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    @staticmethod
    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_get_offline_programs():
        """Test items, sort and order"""
        get_offline_programs(use_favorites=True)

    @unittest.SkipTest
    def test_unfollow_all(self):
        """Test unfollowing all programs"""
        programs = get_programs(channel='een')
        for program_item in programs:
            program_title = program_item.get('title')
            program_name = program_item.get('programName')
            if self._favorites.is_favorite(program_name):
                # Unfollow
                self._favorites.unfollow(program_name=program_name, title=program_title)
                self.assertFalse(self._favorites.is_favorite(program_name))

    @unittest.SkipTest
    def test_follow_number(self):
        """Test following X programs"""
        number = 118
        programs = get_programs(channel='een')
        shuffle(programs)
        print('VRT MAX has %d programs available' % len(programs))
        for program_item in programs[:number]:
            program_title = program_item.get('title')
            program_name = program_item.get('programName')

            # Follow
            self._favorites.follow(program_name=program_name, title=program_title)
            self.assertTrue(self._favorites.is_favorite(program_name))

            # Unfollow
            # self._favorites.unfollow(program_name=program_name, title=program_title)
            # self.assertFalse(self._favorites.is_favorite(program_name))

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_follow_unfollow(self):
        """Test following and unfollowing programs"""
        programs = [
            {'program_title': 'Winteruur', 'program_name': 'winteruur'},
            {'program_title': 'Thuis', 'program_name': 'thuis'},
            {'program_title': '#LikeMe', 'program_name': '-likeme'},
        ]
        for program_item in programs:
            program_title = program_item.get('program_title')
            program_name = program_item.get('program_name')
            self._favorites.follow(program_name=program_name, title=program_title)
            self.assertTrue(self._favorites.is_favorite(program_name))

            self._favorites.unfollow(program_name=program_name, title=program_title)
            self.assertFalse(self._favorites.is_favorite(program_name))

            self._favorites.follow(program_name=program_name, title=program_title)
            self.assertTrue(self._favorites.is_favorite(program_name))

    def test_programs(self):
        """Test favorite programs list"""
        programs = self._favorites.programs()
        # NOTE: Getting favorites requires credentials
        if addon.settings.get('username') and addon.settings.get('password'):
            self.assertTrue(programs)
        print(programs)


if __name__ == '__main__':
    unittest.main()
