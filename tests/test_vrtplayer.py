# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for VRTPlayer functionality"""

from datetime import datetime
import random
import unittest
import dateutil.tz
from api import get_categories, get_categories_data, get_episodes, get_featured, get_programs
from vrtplayer import VRTPlayer

import xbmcaddon

ADDON = xbmcaddon.Addon()
now = datetime.now(dateutil.tz.tzlocal())


class TestVRTPlayer(unittest.TestCase):
    """TestCase class"""

    _vrtplayer = VRTPlayer()

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_show_videos_single_episode_shows_videos(self):
        """Test listing single episode for a given program (wij--roger-raveel)"""
        program_name = 'wij--roger-raveel'
        season_name = '2021'
        episode_items, sort, ascending, content = get_episodes(program_name=program_name, season_name=season_name)
        self.assertTrue(episode_items, msg=program_name)
        self.assertEqual(sort, 'label')
        self.assertTrue(ascending)
        self.assertEqual(content, 'episodes')

        self._vrtplayer.show_episodes_menu(program_name)

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_show_videos_single_season_shows_videos(self):
        """Test listing single season for a given program (het-weer)"""
        program_name = 'het-weer'
        season_name = now.strftime('%Y')
        episode_items, sort, ascending, content = get_episodes(program_name=program_name, season_name=season_name)
        self.assertTrue(episode_items, msg=program_name)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

        self._vrtplayer.show_episodes_menu(program_name)

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_show_videos_multiple_seasons_shows_videos(self):
        """Test listing multiple season for a given program (pano)"""
        program_name = 'pano'
        episode_items, sort, ascending, content = get_episodes(program_name=program_name)
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'unsorted')
        self.assertTrue(ascending)
        self.assertEqual(content, 'files')

        self._vrtplayer.show_episodes_menu(program_name)

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_show_videos_specific_seasons_shows_videos(self):
        """Test listing specific seasons for a given program (thuis)"""
        program_name = 'thuis'
        episode_items, sort, ascending, content = get_episodes(program_name=program_name)
        self.assertTrue(episode_items, msg=program_name)
        self.assertEqual(sort, 'unsorted')
        self.assertTrue(ascending)
        self.assertEqual(content, 'files')

        self._vrtplayer.show_episodes_menu(program_name)

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_random_tvshow_episodes(self):
        """Test episode from a random tvshow in a random category"""
        categories = get_categories_data()
        self.assertTrue(categories)

        category = random.choice(categories)
        program_items = get_programs(category=category['id'])
        self.assertTrue(program_items, msg=category['id'])

        program = random.choice(program_items)
        print('Random tvshow {}'.format(program.path))
        if program.path.startswith('plugin://plugin.video.vrt.nu/programs/'):
            # When random program has episodes
            episode_items, sort, ascending, content = get_episodes(program.path.split('/')[4].replace('.relevant', ''))
            self.assertTrue(episode_items, msg=program.path.split('/')[4])
            self.assertTrue(sort in ['dateadded', 'episode', 'label', 'unsorted'])
            self.assertTrue(ascending is True or ascending is False)
            self.assertTrue(content in ['episodes', 'files'], "Content for '%s' is '%s'" % (program.label, content))
        elif program.path.startswith('plugin://plugin.video.vrt.nu/play/id/'):
            # When random program is playable item
            pass
        else:
            self.fail('We did not expect this, either we find episodes or it is a playable item')

    def test_categories(self):
        """Test to ensure our hardcoded categories conforms to scraped categories"""
        category_items = get_categories()
        self.assertEqual(len(category_items), 19)

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_featured(self):
        """Test featured menu"""
        featured_items, _, _, _ = get_featured()
        self.assertTrue(5 < len(featured_items) < 25)

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_play_unknown_program(self):
        """Test playing latest episode of an unknown program"""
        self._vrtplayer.play_latest_episode(program_name='foobar')

    def test_play_unknown_airdate(self):
        """Test playing unknown airdate"""
        self._vrtplayer.play_episode_by_air_date(channel='een', start_date='2100-01-01T23:59:58', end_date='2100-01-01T23:59:59')
        self._vrtplayer.play_episode_by_air_date(channel='foo', start_date='2100-01-01T23:59:58', end_date='2100-01-01T23:59:59')

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_play_unknown_episode_id(self):
        """Test playing unknown Up Next episode_id"""
        self._vrtplayer.play_upnext(episode_id='1234567890')


if __name__ == '__main__':
    unittest.main()
