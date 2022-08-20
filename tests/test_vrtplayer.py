# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for VRTPlayer functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime
import random
import unittest
import dateutil.tz
from apihelper import ApiHelper
from favorites import Favorites
from resumepoints import ResumePoints
from vrtplayer import VRTPlayer

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

now = datetime.now(dateutil.tz.tzlocal())


class TestVRTPlayer(unittest.TestCase):
    """TestCase class"""

    _favorites = Favorites()
    _resumepoints = ResumePoints()
    _apihelper = ApiHelper(_favorites, _resumepoints)
    _vrtplayer = VRTPlayer()

    def test_show_videos_single_episode_shows_videos(self):
        """Test listing single episode for a given program (wij--roger-raveel)"""
        program = 'wij--roger-raveel'
        episode_items, sort, ascending, content = self._apihelper.list_episodes(program=program)
        self.assertTrue(episode_items, msg=program)
        self.assertEqual(sort, 'label')
        self.assertTrue(ascending)
        self.assertEqual(content, 'episodes')

        self._vrtplayer.show_episodes_menu(program)

    def test_show_videos_single_season_shows_videos(self):
        """Test listing single season for a given program (het-weer)"""
        program = 'het-weer'
        season = '1640081117563'
        episode_items, sort, ascending, content = self._apihelper.list_episodes(program=program, season=season)
        self.assertTrue(episode_items, msg=program)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

        self._vrtplayer.show_episodes_menu(program)

    def test_show_videos_multiple_seasons_shows_videos(self):
        """Test listing multiple season for a given program (pano)"""
        program = 'pano'
        episode_items, sort, ascending, content = self._apihelper.list_episodes(program=program)
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)
        self.assertEqual(content, 'files')

        self._vrtplayer.show_episodes_menu(program)

    def test_show_videos_specific_seasons_shows_videos(self):
        """Test listing specific seasons for a given program (thuis)"""
        program = 'thuis'
        episode_items, sort, ascending, content = self._apihelper.list_episodes(program=program)
        self.assertTrue(episode_items, msg=program)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)
        self.assertEqual(content, 'files')

        self._vrtplayer.show_episodes_menu(program)

    def test_random_tvshow_episodes(self):
        """Test episode from a random tvshow in a random category"""
        categories = self._apihelper.get_categories()
        self.assertTrue(categories)

        category = random.choice(categories)
        tvshow_items = self._apihelper.list_tvshows(category['id'])
        self.assertTrue(tvshow_items, msg=category['id'])

        tvshow = random.choice(tvshow_items)
        if tvshow.path.startswith('plugin://plugin.video.vrtmax/programs/'):
            # When random program has episodes
            episode_items, sort, ascending, content = self._apihelper.list_episodes(tvshow.path.split('/')[4].replace('.relevant', ''))
            self.assertTrue(episode_items, msg=tvshow.path.split('/')[4])
            self.assertTrue(sort in ['dateadded', 'episode', 'label', 'unsorted'])
            self.assertTrue(ascending is True or ascending is False)
            self.assertTrue(content in ['episodes', 'files'], "Content for '%s' is '%s'" % (tvshow.label, content))
        elif tvshow.path.startswith('plugin://plugin.video.vrtmax/play/id/'):
            # When random program is playable item
            pass
        else:
            self.fail('We did not expect this, either we find episodes or it is a playable item')

    def test_categories(self):
        """Test to ensure our hardcoded categories conforms to scraped categories"""
        category_items = self._apihelper.list_categories()
        self.assertEqual(len(category_items), 19)

    def test_featured(self):
        """Test to ensure our hardcoded featured conforms to scraped featured"""
        featured_items = self._apihelper.list_featured(online=True)
        from data import FEATURED
        for feature in featured_items:
            self.assertTrue(feature.label in [item.get('name') for item in FEATURED], msg='%s is missing' % feature.label)
        for feature in FEATURED:
            print(feature.get('name'))
            self.assertTrue(feature.get('name') in [item.label for item in featured_items], msg='%s doesn\'t exist online' % feature.get('name'))
        self.assertEqual(len(featured_items), 7)

    def test_play_unknown_program(self):
        """Test playing latest episode of an unknown program"""
        self._vrtplayer.play_latest_episode(program='foobar')

    def test_play_unknown_airdate(self):
        """Test playing unknown airdate"""
        self._vrtplayer.play_episode_by_air_date(channel='een', start_date='2100-01-01T23:59:58', end_date='2100-01-01T23:59:59')
        self._vrtplayer.play_episode_by_air_date(channel='foo', start_date='2100-01-01T23:59:58', end_date='2100-01-01T23:59:59')

    def test_play_unknown_episode_id(self):
        """Test playing unknown Up Next episode_id"""
        self._vrtplayer.play_upnext(episode_id='1234567890')


if __name__ == '__main__':
    unittest.main()
