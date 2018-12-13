import unittest
from resources.lib.vrtplayer import vrtplayer
from mock import MagicMock

class TestVRTPlayer(unittest.TestCase):


    def test_show_videos_single_episode_shows_videos(self):
        mock = MagicMock()
        mock.show_listing()
        player = vrtplayer.VRTPlayer(None,mock,None)
        player.show_videos('https://www.vrt.be/vrtnu/a-z/tussen-nu-en-morgen/2018/tussen-nu-en-morgen/')
        self.assertTrue(mock.show_listing.called)

    def test_show_videos_single_season_shows_videos(self):
        mock = MagicMock()
        mock.show_listing()
        player = vrtplayer.VRTPlayer(None,mock,None)
        player.show_videos('https://www.vrt.be/vrtnu/a-z/apocalyps--de-eerste-wereldoorlog/1/apocalyps--de-eerste-wereldoorlog-s1a3/')
        self.assertTrue(mock.show_listing.called)

    def test_show_videos_multiple_seasons_shows_videos(self):
        mock = MagicMock()
        mock.show_listing()
        player = vrtplayer.VRTPlayer(None,mock,None)
        player.show_videos('https://www.vrt.be/vrtnu/a-z/thuis/24/thuis-s24a4478/')
        self.assertTrue(mock.show_listing.called)

    def test_show_videos_specific_seasons_shows_videos(self):
        mock = MagicMock()
        mock.show_listing()
        player = vrtplayer.VRTPlayer(None,mock,None)
        player.show_videos('/vrtnu/a-z/thuis/24.lists.all-episodes/')
        self.assertTrue(mock.show_listing.called)
        

if __name__ == '__main__':
    unittest.main()
