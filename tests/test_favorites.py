# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for Favorites functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from random import shuffle
from apihelper import ApiHelper
from favorites import Favorites
from resumepoints import ResumePoints

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
    _resumepoints = ResumePoints()
    _apihelper = ApiHelper(_favorites, _resumepoints)

    def test_get_recent_episodes(self):
        """Test items, sort and order"""
        episode_items, sort, ascending, content = self._apihelper.list_episodes(page=1, variety='recent')
        self.assertEqual(len(episode_items), itemsperpage)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_get_offline_episodes(self):
        """Test items, sort and order"""
        episode_items, sort, ascending, content = self._apihelper.list_episodes(page=1, variety='offline')
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    @unittest.SkipTest
    def test_unfollow_all(self):
        """Test unfollowing all programs"""
        programs = self._apihelper.get_tvshows()
        for program_item in programs:
            program_title = program_item.get('title')
            program = program_item.get('programName')
            if self._favorites.is_favorite(program):
                # Unfollow
                self._favorites.unfollow(program=program, title=program_title)
                self.assertFalse(self._favorites.is_favorite(program))

    @unittest.SkipTest
    def test_follow_number(self):
        """Test following X programs"""
        number = 118
        programs = self._apihelper.get_tvshows()
        shuffle(programs)
        print('VRT NU has %d programs available' % len(programs))
        for program_item in programs[:number]:
            program_title = program_item.get('title')
            program = program_item.get('programName')

            # Follow
            self._favorites.follow(program=program, title=program_title)
            self.assertTrue(self._favorites.is_favorite(program))

            # Unfollow
            # self._favorites.unfollow(program=program, title=program_title)
            # self.assertFalse(self._favorites.is_favorite(program))

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_follow_unfollow(self):
        """Test following and unfollowing programs"""
        programs = [
            {'program_title': 'Winteruur', 'program': 'winteruur'},
            {'program_title': 'De Campus Cup', 'program': 'de-campus-cup'},
            {'program_title': 'Terug naar Siberië', 'program': 'terug-naar-siberie'},
            {'program_title': 'Belle & Sebastian', 'program': 'belle---sebastian'},
        ]
        for program_item in programs:
            program_title = program_item.get('program_title')
            program = program_item.get('program')
            self._favorites.follow(program=program, title=program_title)
            self.assertTrue(self._favorites.is_favorite(program))

            self._favorites.unfollow(program=program, title=program_title)
            self.assertFalse(self._favorites.is_favorite(program))

            self._favorites.follow(program=program, title=program_title)
            self.assertTrue(self._favorites.is_favorite(program))

    def test_programs(self):
        """Test favorite programs list"""
        programs = self._favorites.programs()
        # NOTE: Getting favorites requires credentials
        if addon.settings.get('username') and addon.settings.get('password'):
            self.assertTrue(programs)
        print(programs)

    def test_titles(self):
        """Test favorite titles list"""
        titles = self._favorites.titles()
        # NOTE: Getting favorites requires credentials
        if addon.settings.get('username') and addon.settings.get('password'):
            self.assertTrue(titles)
        print(sorted(titles))


if __name__ == '__main__':
    unittest.main()
