# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=missing-docstring

from __future__ import absolute_import, division, print_function, unicode_literals
import random
import unittest

from resources.lib import CATEGORIES, favorites, kodiwrapper, vrtapihelper, vrtplayer

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')


class TestVRTPlayer(unittest.TestCase):

    _kodi = kodiwrapper.KodiWrapper(None)
    _favorites = favorites.Favorites(_kodi)
    _apihelper = vrtapihelper.VRTApiHelper(_kodi, _favorites)
    _vrtplayer = vrtplayer.VRTPlayer(_kodi)

    def test_show_videos_single_episode_shows_videos(self):
        program = 'marathonradio'
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(program=program)
        self.assertTrue(episode_items, msg=program)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

        self._vrtplayer.show_episodes(program)
        # self.assertTrue(self._kodi.show_listing.called)

    def test_show_videos_single_season_shows_videos(self):
        program = 'het-weer'
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(program=program)
        self.assertTrue(episode_items, msg=program)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

        self._vrtplayer.show_episodes(program)
        # self.assertTrue(self._kodi.show_listing.called)

    def test_show_videos_multiple_seasons_shows_videos(self):
        program = 'pano'
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(program=program)
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)
        self.assertEqual(content, 'seasons')

        self._vrtplayer.show_episodes(program)
        # self.assertTrue(self._kodi.show_listing.called)

    def test_show_videos_specific_seasons_shows_videos(self):
        program = 'thuis'
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(program=program)
        self.assertTrue(episode_items, msg=program)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)
        self.assertEqual(content, 'seasons')

        self._vrtplayer.show_episodes(program)
        # self.assertTrue(self._kodi.show_listing.called)

    def test_categories_scraping(self):
        ''' Test to ensure our hardcoded categories conforms to scraped categories '''
        # Remove thumbnails from scraped categories first
        categories = [dict(id=c['id'], name=c['name']) for c in self._apihelper.get_categories()]
        self.assertEqual(categories, CATEGORIES)

    def test_random_tvshow_episodes(self):
        ''' Rest episode from a random tvshow in a random category '''
        categories = self._apihelper.get_categories()
        self.assertTrue(categories)

        category = random.choice(categories)
        tvshow_items = self._apihelper.get_tvshow_items(category['id'])
        self.assertTrue(tvshow_items, msg=category['id'])

        tvshow = random.choice(tvshow_items)
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(tvshow.path.split('/')[2])
        self.assertTrue(episode_items, msg=tvshow.path.split('/')[2])
        self.assertTrue(sort in ['dateadded', 'episode', 'label', 'unsorted'])
        self.assertTrue(ascending is True or ascending is False)
        self.assertTrue(content in ['episodes', 'seasons'], "Content for '%s' is '%s'" % (tvshow.title, content))

    def test_categories(self):
        ''' Test to ensure our hardcoded categories conforms to scraped categories '''
        category_items = self._apihelper.get_category_items()
        self.assertEqual(len(category_items), 17)


if __name__ == '__main__':
    unittest.main()
