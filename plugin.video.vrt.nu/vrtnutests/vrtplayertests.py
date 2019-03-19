# -*- coding: utf-8 -*-

# GNU General Public License v2.0 (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

import unittest
from resources.lib.vrtplayer import vrtplayer
from resources.lib.vrtplayer import vrtapihelper
from mock import MagicMock


class TestVRTPlayer(unittest.TestCase):

    def test_show_videos_single_episode_shows_videos(self):
        mock = MagicMock()
        mock.show_listing()
        player = vrtplayer.VRTPlayer(mock, None, vrtapihelper.VRTApiHelper(mock))
        player.show_episodes('/vrtnu/a-z/tussen-nu-en-morgen/2018/tussen-nu-en-morgen.relevant/')
        self.assertTrue(mock.show_listing.called)

    def test_show_videos_single_season_shows_videos(self):
        mock = MagicMock()
        mock.show_listing()
        player = vrtplayer.VRTPlayer(mock, None, vrtapihelper.VRTApiHelper(mock))
        player.show_episodes('/vrtnu/a-z/apocalyps--de-eerste-wereldoorlog/1/apocalyps--de-eerste-wereldoorlog-s1a3.relevant/')
        self.assertTrue(mock.show_listing.called)

    def test_show_videos_multiple_seasons_shows_videos(self):
        mock = MagicMock()
        mock.show_listing()
        player = vrtplayer.VRTPlayer(mock, None, vrtapihelper.VRTApiHelper(mock))
        player.show_episodes('vrtnu/a-z/animal-babies.relevant/')
        self.assertTrue(mock.show_listing.called)

    def test_show_videos_specific_seasons_shows_videos(self):
        mock = MagicMock()
        mock.show_listing()
        player = vrtplayer.VRTPlayer(mock, None, vrtapihelper.VRTApiHelper(mock))
        player.show_episodes('/vrtnu/a-z/thuis/24.lists.all-episodes.relevant/')
        self.assertTrue(mock.show_listing.called)


if __name__ == '__main__':
    unittest.main()
