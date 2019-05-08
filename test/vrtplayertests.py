# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=unused-variable

from __future__ import absolute_import, division, unicode_literals
import mock
import random
import unittest

from resources.lib.vrtplayer import CATEGORIES, CHANNELS, vrtapihelper, vrtplayer


class TestVRTPlayer(unittest.TestCase):

    _kodi_wrapper = mock.MagicMock()
    _kodi_wrapper.get_proxies = mock.MagicMock(return_value=dict())
    _kodi_wrapper.get_localized_dateshort = mock.MagicMock(return_value='%d-%m-%Y')
    _api_helper = vrtapihelper.VRTApiHelper(_kodi_wrapper)

    def test_tvshows(self):
        ''' Test A-Z tvshow listing and CHANNELS list '''
        tvshow_items = self._api_helper.get_tvshow_items(category=None)

        # Test we get a non-empty A-Z listing back
        self.assertTrue(tvshow_items)

        # Test every brand is a known channel studio name
        bogus_brands = ['lang-zullen-we-lezen', 'VRT']
        channel_studios = [c.get('studio') for c in CHANNELS] + bogus_brands
        for tvshow in tvshow_items:
            self.assertTrue(tvshow.video_dict['studio'] in channel_studios, '%s | %s | %s' % (tvshow.title, tvshow.video_dict['studio'], channel_studios))

    def test_show_videos_single_episode_shows_videos(self):
        path = '/vrtnu/a-z/marathonradio.relevant/'
        episode_items, sort, ascending = self._api_helper.get_episode_items(path=path)
        self.assertTrue(episode_items, msg=path)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)

        player = vrtplayer.VRTPlayer(self._kodi_wrapper, self._api_helper)
        player.show_episodes(path)
        self.assertTrue(self._kodi_wrapper.show_listing.called)

    def test_show_videos_single_season_shows_videos(self):
        path = '/vrtnu/a-z/het-weer.relevant/'
        episode_items, sort, ascending = self._api_helper.get_episode_items(path=path)
        self.assertTrue(episode_items, msg=path)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)

        player = vrtplayer.VRTPlayer(self._kodi_wrapper, self._api_helper)
        player.show_episodes(path)
        self.assertTrue(self._kodi_wrapper.show_listing.called)

    def test_show_videos_multiple_seasons_shows_videos(self):
        path = '/vrtnu/a-z/pano.relevant/'
        episode_items, sort, ascending = self._api_helper.get_episode_items(path=path)
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)

        player = vrtplayer.VRTPlayer(self._kodi_wrapper, self._api_helper)
        player.show_episodes(path)
        self.assertTrue(self._kodi_wrapper.show_listing.called)

    def test_show_videos_specific_seasons_shows_videos(self):
        path = '/vrtnu/a-z/thuis.relevant/'
        episode_items, sort, ascending = self._api_helper.get_episode_items(path=path)
        self.assertTrue(episode_items, msg=path)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)

        player = vrtplayer.VRTPlayer(self._kodi_wrapper, self._api_helper)
        player.show_episodes(path)
        self.assertTrue(self._kodi_wrapper.show_listing.called)

    def test_get_recent_episodes(self):
        ''' Test items, sort and order '''
        episode_items, sort, ascending = self._api_helper.get_episode_items(page=1)
        self.assertEqual(len(episode_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)

    def test_get_program_episodes(self):
        ''' Test items, sort and order '''
        path = '/vrtnu/a-z/het-journaal.relevant/'
        episode_items, sort, ascending = self._api_helper.get_episode_items(path=path)
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)

    def test_get_tvshows(self):
        ''' Test items, sort and order '''
        path = 'nieuws-en-actua'
        tvshow_items = self._api_helper.get_tvshow_items(path)
        self.assertTrue(tvshow_items)

    def test_categories_scraping(self):
        ''' Test to ensure our hardcoded categories conforms to scraped categories '''
        # Remove thumbnails from scraped categories first
        vrt_player = vrtplayer.VRTPlayer(self._kodi_wrapper, self._api_helper)
        categories = [dict(id=c['id'], name=c['name']) for c in vrt_player.get_categories()]
        self.assertEqual(categories, CATEGORIES)

    def test_random_tvshow_episodes(self):
        ''' Rest episode from a random tvshow in a random category '''
        vrt_player = vrtplayer.VRTPlayer(self._kodi_wrapper, self._api_helper)
        categories = vrt_player.get_categories()
        self.assertTrue(categories)

        category = random.choice(categories)
        tvshow_items = self._api_helper.get_tvshow_items(category['id'])
        self.assertTrue(tvshow_items, msg=category['id'])

        tvshow = random.choice(tvshow_items)
        episode_items, sort, ascending = self._api_helper.get_episode_items(tvshow.url_dict['video_url'])
        self.assertTrue(episode_items, msg=tvshow.url_dict['video_url'])


if __name__ == '__main__':
    unittest.main()
