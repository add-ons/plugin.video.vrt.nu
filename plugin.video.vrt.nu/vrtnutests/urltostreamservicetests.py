import unittest
from resources.lib.vrtplayer import vrtplayer, urltostreamservice, tokenresolver
from mock import MagicMock

class UrlToStreamServiceTests(unittest.TestCase):

    def _side_effect(self, arg):
        vals = {'username': '***@gmail.com', 'password': '**', 'showsubtitles': 'true' , 'usedrm':False}
        return vals[arg]

    def test_get_ondemand_stream_from_url_gets_stream_does_not_crash(self):
        mock = MagicMock()
        token_resolver = tokenresolver.TokenResolver(mock)
        mock.get_setting = MagicMock(side_effect=self._side_effect)
        mock.get_userdata_path.return_value = "vrttest"
        mock.check_if_path_exists.return_value = False
        mock.make_dir.return_value = None
        mock.open_path.return_value = False
        mock.check_inputstream_adaptive.return_value = False
        service = urltostreamservice.UrlToStreamService(vrtplayer.VRTPlayer._VRT_BASE, vrtplayer.VRTPlayer._VRTNU_BASE_URL, mock, token_resolver)
        stream = service.get_stream_from_url('/vrtnu/a-z/22-3-1-jaar-later---het-onderzoek/2017/22-3-1-jaar-later---het-onderzoek-s2017/')
        self.assertTrue(stream != None)

    def test_get_live_stream_from_url_does_not_crash(self):
        mock = MagicMock()
        token_resolver = tokenresolver.TokenResolver(mock)
        mock.get_setting = MagicMock(side_effect=self._side_effect)
        mock.get_userdata_path.return_value = "vrttest"
        mock.check_if_path_exists.return_value = False
        mock.make_dir.return_value = None
        mock.open_path.return_value = False
        mock.check_inputstream_adaptive.return_value = False
        service = urltostreamservice.UrlToStreamService(vrtplayer.VRTPlayer._VRT_BASE, vrtplayer.VRTPlayer._VRTNU_BASE_URL, mock, token_resolver)
        stream = service.get_stream_from_url(vrtplayer.VRTPlayer._CANVAS_LIVESTREAM_)
        self.assertTrue(stream != None)

