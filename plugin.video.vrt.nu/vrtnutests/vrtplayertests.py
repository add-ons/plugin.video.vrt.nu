# -*- coding: UTF-8 -*-

# GNU General Public License v2.0 (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

''' This is the actual VRT Nu video plugin entry point '''

from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
from resources.lib.vrtplayer import vrtplayer
from resources.lib.vrtplayer import vrtapihelper
from mock import MagicMock


class TestVRTPlayer(unittest.TestCase):

    def test_show_videos_single_episode_shows_videos(self):
        mock = MagicMock()
        mock.show_listing()
        player = vrtplayer.VRTPlayer(None, mock, None, vrtapihelper.VRTApiHelper())
        player.show_videos('/vrtnu/a-z/tussen-nu-en-morgen/2018/tussen-nu-en-morgen.relevant/', None)
        self.assertTrue(mock.show_listing.called)

    def test_show_videos_single_season_shows_videos(self):
        mock = MagicMock()
        mock.show_listing()
        player = vrtplayer.VRTPlayer(None, mock, None, vrtapihelper.VRTApiHelper())
        player.show_videos('/vrtnu/a-z/apocalyps--de-eerste-wereldoorlog/1/apocalyps--de-eerste-wereldoorlog-s1a3.relevant/', None)
        self.assertTrue(mock.show_listing.called)

    def test_show_videos_multiple_seasons_shows_videos(self):
        mock = MagicMock()
        mock.show_listing()
        player = vrtplayer.VRTPlayer(None, mock, None, vrtapihelper.VRTApiHelper())
        player.show_videos('%2fvrtnu%2fa-z%2fanimal-babies.relevant%2f', None)
        self.assertTrue(mock.show_listing.called)

    def test_show_videos_specific_seasons_shows_videos(self):
        mock = MagicMock()
        mock.show_listing()
        player = vrtplayer.VRTPlayer(None, mock, None, vrtapihelper.VRTApiHelper())
        player.show_videos('/vrtnu/a-z/thuis/24.lists.all-episodes.relevant/', None)
        self.assertTrue(mock.show_listing.called)


if __name__ == '__main__':
    unittest.main()
