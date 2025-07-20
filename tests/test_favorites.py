# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for Favorites functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from api import get_recent_episodes, get_program_id, get_favorite_programs, is_favorite, get_offline_programs, set_favorite

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

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_get_recent_episodes(self):
        """Test items, sort and order"""
        episode_items, sort, ascending, content = get_recent_episodes(use_favorites=True)
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_get_offline_programs(self):
        """Test items, sort and order"""
        programs = get_offline_programs(use_favorites=True)
        self.assertTrue(programs)

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
            program_id = get_program_id(program_item.get('program_name'))

            set_favorite(program_id=program_id, program_title=program_title)
            self.assertTrue(is_favorite(program_item.get('program_name')))

            set_favorite(program_id=program_id, program_title=program_title, favorited=False)
            self.assertFalse(is_favorite(program_item.get('program_name')))

            set_favorite(program_id=program_id, program_title=program_title)
            self.assertTrue(is_favorite(program_item.get('program_name')))

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_programs(self):
        """Test favorite programs list"""
        programs = get_favorite_programs()
        print([program.info_dict.get('tvshowtitle') for program in programs])


if __name__ == '__main__':
    unittest.main()
