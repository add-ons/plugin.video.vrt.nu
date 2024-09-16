# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for Api functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from api import (get_episodes, get_favorite_programs, get_latest_episode, get_next_info, get_online_categories,
                 get_offline_programs, get_programs, get_recent_episodes, get_search, get_single_episode, valid_categories)
from data import CATEGORIES
from xbmcextra import kodi_to_ansi

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

addon = xbmcaddon.Addon()
itemsperpage = int(addon.settings.get('itemsperpage'))


@unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
@unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
class TestApi(unittest.TestCase):
    """TestCase class"""

    def test_get_api_data_single_season(self):
        """Test listing episodes for a single season (zomerhit)"""
        title_items, sort, ascending, content = get_episodes(program_name='brussel-nieuwsstraat', season_name='2')
        self.assertEqual(len(title_items), 13)
        self.assertEqual(sort, 'episode')
        self.assertTrue(ascending)
        self.assertEqual(content, 'episodes')

    def test_get_api_data_multiple_seasons(self):
        """Test listing episodes for multiple seasons (winteruur)"""
        title_items, sort, ascending, content = get_episodes(program_name='winteruur')
        self.assertTrue(5 < len(title_items) < 15)
        self.assertEqual(sort, 'unsorted')
        self.assertTrue(ascending)
        self.assertEqual(content, 'files')

    def test_get_api_data_specific_season(self):
        """Test listing episodes for a specific season (pano)"""
        title_items, sort, ascending, content = get_episodes(program_name='pano', season_name='2020')
        self.assertEqual(len(title_items), 15)
        self.assertEqual(sort, 'dateadded')  # Pano has 'daily' programType
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_get_api_data_specific_season_without_broadcastdate(self):
        """Test listing episodes without broadcastDate (wereldbeeld)"""
        title_items, sort, ascending, content = get_episodes(program_name='wereldbeeld', season_name='1')
        self.assertEqual(len(title_items), 7)
        self.assertEqual(sort, 'episode')
        self.assertTrue(ascending)
        self.assertEqual(content, 'episodes')

    def test_get_recent_episodes(self):
        """Test items, sort and order"""
        episode_items, sort, ascending, content = get_recent_episodes()
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_get_offline_programs(self):
        """Test items"""
        program_items = get_offline_programs()
        self.assertTrue(program_items)

    def test_get_single_episode(self):
        """Test getting a single episode by episodeId"""
        episode_items = get_single_episode(episode_id='1649155986476')
        self.assertTrue(episode_items)

    def test_get_programs_category(self):
        """Test get programs (humor)"""
        category = 'humor'
        program_items = get_programs(category=category)
        self.assertTrue(program_items)

    def test_get_programs_channel(self):
        """Test get programs (canvas)"""
        channel = 'canvas'
        program_items = get_programs(channel=channel)
        self.assertTrue(program_items)

    def test_get_programs_keywords(self):
        """Test get programs using keywords"""
        keywords = 'kaas'
        program_items = get_search(keywords=keywords)
        print(len(program_items))
        self.assertTrue(program_items)

    def test_get_favorite_programs(self):
        """Test getting favorite programs"""
        programs = get_favorite_programs()
        self.assertTrue(programs)

    def test_get_latest_episode(self):
        """Test getting the latest episode of a program (vrt-nws-journaal)"""
        video = get_latest_episode(program_name='vrt-nws-journaal')
        self.assertTrue(video.get('listitem') is not None)
        self.assertTrue(video.get('video_id') is not None)
        self.assertTrue(video.get('publication_id') is not None)

    def test_episode_plot(self):
        """Test getting an episode plot (thuis)"""
        title_items, sort, ascending, content = get_episodes(program_name='thuis', season_name='28')
        self.assertEqual(sort, 'dateadded')  # Thuis has 'daily' programType
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')
        plot = title_items[0].info_dict['plot']
        print(kodi_to_ansi(plot))

    def test_upnext(self):
        """Test getting next episode (de-ideale-wereld)"""
        episode_id = '1700435154519'
        next_episode = get_next_info(episode_id).get('next_episode')
        self.assertTrue(next_episode)
        print(next_episode)

    def test_get_categories(self):
        """Test to ensure our local hardcoded categories conforms to online categories"""
        # Remove thumbnails from scraped categories first
        online_categories = [{'id': c['id'], 'name': c['name']} for c in get_online_categories()]
        local_categories = [{'id': c['id'], 'name': c['name']} for c in CATEGORIES]
        print('Categories:')
        for category in online_categories:
            print('%s | %s' % (kodi_to_ansi(category.get('name')), kodi_to_ansi(category.get('id'))))

        self.assertTrue(valid_categories(online_categories))
        self.assertTrue(valid_categories(local_categories))
        self.assertEqual(online_categories, local_categories)


if __name__ == '__main__':
    unittest.main()
