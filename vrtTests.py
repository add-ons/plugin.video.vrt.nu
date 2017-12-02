import unittest
from resources.lib.vrtplayer import vrtplayer
from mock import MagicMock

class TestVRTPlayer(unittest.TestCase):

    def test_show_videos(self):
        mock = MagicMock()
        mock.show_listing()
        player = vrtplayer.VRTPlayer(None, mock, None)
        player.show_videos('https://www.vrt.be/vrtnu/a-z/displaced/2017/displaced-s2017/')
        self.assertTrue(mock.show_listing.called)

if __name__ == '__main__':
    unittest.main()