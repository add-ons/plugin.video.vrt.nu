# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for ApiHelper functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from apihelper import ApiHelper
from data import CHANNELS
from favorites import Favorites
from resumepoints import ResumePoints
from xbmcextra import kodi_to_ansi

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

addon = xbmcaddon.Addon()
itemsperpage = int(addon.settings.get('itemsperpage'))


class TestApiHelper(unittest.TestCase):
    """TestCase class"""

    _favorites = Favorites()
    _resumepoints = ResumePoints()
    _apihelper = ApiHelper(_favorites, _resumepoints)

    def test_get_api_data_single_season(self):
        """Test listing episodes for a single season (het-journaal)"""
        title_items, sort, ascending, content = self._apihelper.list_episodes(program='het-journaal', season='allseasons')
        self.assertTrue(110 <= len(title_items) <= 140, 'We got %s items instead.' % len(title_items))
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_get_api_data_multiple_seasons(self):
        """Test listing episodes for multiple seasons (thuis)"""
        title_items, sort, ascending, content = self._apihelper.list_episodes(program='thuis')
        self.assertTrue(len(title_items) < 5)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)
        self.assertEqual(content, 'seasons')

    def test_get_api_data_specific_season(self):
        """Test listing episodes for a specific season (pano)"""
        title_items, sort, ascending, content = self._apihelper.list_episodes(program='pano')
        self.assertEqual(len(title_items), 6)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)
        self.assertEqual(content, 'seasons')

    def test_get_api_data_specific_season_without_broadcastdate(self):
        """Test listing episodes without broadcast date (postbus-x)"""
        title_items, sort, ascending, content = self._apihelper.list_episodes(program='postbus-x')
        self.assertEqual(len(title_items), 4)
        self.assertEqual(sort, 'label')
        self.assertTrue(ascending)
        self.assertEqual(content, 'seasons')

    def test_get_recent_episodes(self):
        """Test items, sort and order"""
        episode_items, sort, ascending, content = self._apihelper.list_episodes(page=1, variety='recent')
        self.assertEqual(len(episode_items), itemsperpage)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_get_recent_episodes_page1(self):
        """Test items, sort and order"""
        episode_items, sort, ascending, content = self._apihelper.list_episodes(page=2, variety='recent')
        self.assertEqual(len(episode_items), itemsperpage)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_get_recent_episodes_page2(self):
        """Test items, sort and order"""
        episode_items, sort, ascending, content = self._apihelper.list_episodes(page=3, variety='recent')
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

    def test_get_tvshows(self):
        """Test get tvshows (humor)"""
        category = 'humor'
        tvshow_items = self._apihelper.get_tvshows(category=category)
        self.assertTrue(tvshow_items)

    def test_list_tvshows(self):
        """Test items, sort and order (nieuws-en-actua)"""
        category = 'nieuws-en-actua'
        tvshow_items = self._apihelper.list_tvshows(category=category)
        self.assertTrue(tvshow_items)

    def test_tvshows(self):
        """Test A-Z tvshow listing and CHANNELS list"""
        tvshow_items = self._apihelper.list_tvshows(category=None)

        # Test we get a non-empty A-Z listing back
        self.assertTrue(tvshow_items)

        # Test every brand is a known channel studio name
        bogus_brands = ['lang-zullen-we-lezen', 'VRT']
        channel_studios = [c.get('studio') for c in CHANNELS] + bogus_brands
        for tvshow in tvshow_items:
            self.assertTrue(tvshow.info_dict['studio'] in channel_studios, '%s | %s | %s' % (tvshow.label, tvshow.info_dict['studio'], channel_studios))

    def test_get_latest_episode(self):
        """Test getting the latest episode of a program (het-journaal)"""
        video = self._apihelper.get_latest_episode(program='het-journaal')
        self.assertTrue(video.get('listitem') is not None)
        self.assertTrue(video.get('video_id') is not None)
        self.assertTrue(video.get('publication_id') is not None)

    def test_episode_plot(self):
        """Test getting an episode plot (thuis)"""
        title_items, sort, ascending, content = self._apihelper.list_episodes(program='thuis', season='allseasons')
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')
        plot = title_items[0].info_dict['plot']
        print(kodi_to_ansi(plot))

    def test_upnext(self):
        """Test getting next episode (winteruur)"""
        current_episode = dict(
            program='winteruur',
            path='plugin://plugin.video.vrt.nu/play/whatson/705308178527',
            playcount='0',
            rating='0',
            runtime='600',
        )
        next_episode = self._apihelper.get_upnext(info=current_episode)
        print(next_episode)


if __name__ == '__main__':
    unittest.main()
