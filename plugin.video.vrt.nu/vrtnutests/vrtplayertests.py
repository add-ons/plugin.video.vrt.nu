# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import mock
import unittest

from resources.lib.vrtplayer import vrtapihelper, vrtplayer


class TestVRTPlayer(unittest.TestCase):

    _kodi_wrapper = mock.MagicMock()
    _kodi_wrapper.get_proxies = mock.MagicMock(return_value=dict())

    def test_show_videos_single_episode_shows_videos(self):
        player = vrtplayer.VRTPlayer(None, self._kodi_wrapper, None, vrtapihelper.VRTApiHelper(self._kodi_wrapper))
        self._kodi_wrapper.show_listing()
        player.show_episodes('/vrtnu/a-z/tussen-nu-en-morgen/2018/tussen-nu-en-morgen.relevant/')
        self.assertTrue(self._kodi_wrapper.show_listing.called)

    def test_show_videos_single_season_shows_videos(self):
        player = vrtplayer.VRTPlayer(None, self._kodi_wrapper, None, vrtapihelper.VRTApiHelper(self._kodi_wrapper))
        player.show_episodes('/vrtnu/a-z/apocalyps--de-eerste-wereldoorlog/1/apocalyps--de-eerste-wereldoorlog-s1a3.relevant/')
        self.assertTrue(self._kodi_wrapper.show_listing.called)

    def test_show_videos_multiple_seasons_shows_videos(self):
        player = vrtplayer.VRTPlayer(None, self._kodi_wrapper, None, vrtapihelper.VRTApiHelper(self._kodi_wrapper))
        player.show_episodes('vrtnu/a-z/animal-babies.relevant/')
        self.assertTrue(self._kodi_wrapper.show_listing.called)

    def test_show_videos_specific_seasons_shows_videos(self):
        player = vrtplayer.VRTPlayer(None, self._kodi_wrapper, None, vrtapihelper.VRTApiHelper(self._kodi_wrapper))
        player.show_episodes('/vrtnu/a-z/thuis/24.lists.all-episodes.relevant/')
        self.assertTrue(self._kodi_wrapper.show_listing.called)


if __name__ == '__main__':
    unittest.main()
