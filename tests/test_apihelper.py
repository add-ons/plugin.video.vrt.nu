# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for ApiHelper functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from apihelper import ApiHelper
from data import CATEGORIES, CHANNELS
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
        self.assertTrue(70 <= len(title_items) <= 140, 'We got %s items instead.' % len(title_items))
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_get_api_data_multiple_seasons(self):
        """Test listing episodes for multiple seasons (winteruur)"""
        title_items, sort, ascending, content = self._apihelper.list_episodes(program='winteruur')
        self.assertTrue(5 < len(title_items) < 10)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)
        self.assertEqual(content, 'files')

    def test_get_api_data_specific_season(self):
        """Test listing episodes for a specific season (pano)"""
        title_items, sort, ascending, content = self._apihelper.list_episodes(program='pano', season='1582104246318')
        self.assertEqual(len(title_items), 15)
        self.assertEqual(sort, 'episode')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_get_api_data_specific_season_without_broadcastdate(self):
        """Test listing episodes without broadcastDate (wereldbeeld)"""
        title_items, sort, ascending, content = self._apihelper.list_episodes(program='wereldbeeld')
        self.assertEqual(len(title_items), 7)
        self.assertEqual(sort, 'episode')
        self.assertTrue(ascending)
        self.assertEqual(content, 'episodes')

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

    def test_predefined_episodes(self):
        """Test getting a predefined list of episodes by episodeId"""
        episode_items = self._apihelper.list_episodes(episode_id=['1649155986476', '1649161182026'], variety='featured.episodes')
        self.assertTrue(episode_items)

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

    def test_predefined_tvshows(self):
        """Test getting a predefined list of tvshows"""
        tvshow_items = self._apihelper.list_tvshows(programs=['thuis', 'terzake'])
        self.assertTrue(tvshow_items)

    def test_tvshows(self):
        """Test A-Z tvshow listing and CHANNELS list"""
        tvshow_items = self._apihelper.list_tvshows(category=None)

        # Test we get a non-empty A-Z listing back
        self.assertTrue(tvshow_items)

        # Test every brand is a known channel studio name
        bogus_brands = ['lang-zullen-we-lezen', 'VRT', 'mediafastforward', 'throwback']
        channel_studios = [c.get('studio') for c in CHANNELS] + bogus_brands
        for tvshow in tvshow_items:
            self.assertTrue(
                tvshow.info_dict['studio'] in channel_studios,
                "Program '%s' has brand '%s' missing from all brands: %s" % (tvshow.label, tvshow.info_dict['studio'], channel_studios)
            )

    def test_get_latest_episode(self):
        """Test getting the latest episode of a program (het-journaal)"""
        video = self._apihelper.get_latest_episode(program='het-journaal')
        self.assertTrue(video.get('listitem') is not None)
        self.assertTrue(video.get('video_id') is not None)
        self.assertTrue(video.get('publication_id') is not None)

    def test_episode_plot(self):
        """Test getting an episode plot (thuis)"""
        title_items, sort, ascending, content = self._apihelper.list_episodes(program='thuis', season='allseasons')
        self.assertEqual(sort, 'episode')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')
        plot = title_items[0].info_dict['plot']
        print(kodi_to_ansi(plot))

    def test_upnext(self):
        """Test getting next episode (winteruur)"""
        current_episode = dict(
            program_title='De Ideale Wereld',
            season_number=11,
            episode_number=28,
            path='plugin://plugin.video.vrtmax/play/id/vid-9ddc7c61-2bf4-4387-91d6-a8f07fbd6ea1/pbs-pub-778fddf2-1aa0-4184-832c-a2832dd77762',
            playcount='0',
            rating='0',
            runtime='600',
        )
        next_episode = self._apihelper.get_upnext(info=current_episode)
        self.assertTrue(next_episode)
        print(next_episode)

    def test_get_categories(self):
        """Test to ensure our local hardcoded categories conforms to online categories"""
        # Remove thumbnails from scraped categories first
        online_categories = [dict(id=c['id'], name=c['name']) for c in self._apihelper.get_online_categories()]
        local_categories = [dict(id=c['id'], name=c['name']) for c in CATEGORIES]
        print('Categories:')
        for category in online_categories:
            print('%s | %s' % (kodi_to_ansi(category.get('name')), kodi_to_ansi(category.get('id'))))

        self.assertTrue(self._apihelper.valid_categories(online_categories))
        self.assertTrue(self._apihelper.valid_categories(local_categories))
        self.assertEqual(online_categories, local_categories)


if __name__ == '__main__':
    unittest.main()
