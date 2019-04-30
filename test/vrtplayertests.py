# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, unicode_literals
import mock
import unittest

from resources.lib.vrtplayer import vrtapihelper, vrtplayer


class TestVRTPlayer(unittest.TestCase):

    _kodi_wrapper = mock.MagicMock()
    _kodi_wrapper.get_proxies = mock.MagicMock(return_value=dict())
    _kodi_wrapper.get_localized_dateshort = mock.MagicMock(return_value='%d-%m-%Y')
    _api_helper = vrtapihelper.VRTApiHelper(_kodi_wrapper)

    def test_show_videos_single_episode_shows_videos(self):
        path = '/vrtnu/a-z/marathonradio.relevant/'
        episode_items, sort, ascending = self._api_helper.get_episode_items(path)
        self.assertTrue(episode_items, msg=path)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)

        player = vrtplayer.VRTPlayer(None, self._kodi_wrapper, None, self._api_helper)
        player.show_episodes(path)
        self.assertTrue(self._kodi_wrapper.show_listing.called)

    def test_show_videos_single_season_shows_videos(self):
        path = '/vrtnu/a-z/het-weer.relevant/'
        episode_items, sort, ascending = self._api_helper.get_episode_items(path)
        self.assertTrue(episode_items, msg=path)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)

        player = vrtplayer.VRTPlayer(None, self._kodi_wrapper, None, self._api_helper)
        player.show_episodes(path)
        self.assertTrue(self._kodi_wrapper.show_listing.called)

    def test_show_videos_multiple_seasons_shows_videos(self):
        path = '/vrtnu/a-z/pano.relevant/'
        episode_items, sort, ascending = self._api_helper.get_episode_items(path)
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)

        player = vrtplayer.VRTPlayer(None, self._kodi_wrapper, None, self._api_helper)
        player.show_episodes(path)
        self.assertTrue(self._kodi_wrapper.show_listing.called)

    def test_show_videos_specific_seasons_shows_videos(self):
        path = '/vrtnu/a-z/thuis.relevant/'
        episode_items, sort, ascending = self._api_helper.get_episode_items(path)
        self.assertTrue(episode_items, msg=path)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)

        player = vrtplayer.VRTPlayer(None, self._kodi_wrapper, None, self._api_helper)
        player.show_episodes(path)
        self.assertTrue(self._kodi_wrapper.show_listing.called)

    def test_get_recent_episodes(self):
        ''' Test items, sort and order '''
        path = 'recent'
        episode_items, sort, ascending = self._api_helper.get_episode_items(path)
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)

    def test_get_program_episodes(self):
        ''' Test items, sort and order '''
        path = '/vrtnu/a-z/het-journaal.relevant/'
        episode_items, sort, ascending = self._api_helper.get_episode_items(path)
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)

    def test_get_tvshows(self):
        ''' Test items, sort and order '''
        path = 'nieuws-en-actua'
        tvshow_items = self._api_helper.get_tvshow_items(path)
        self.assertTrue(tvshow_items)


if __name__ == '__main__':
    unittest.main()
