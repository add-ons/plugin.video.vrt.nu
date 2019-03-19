# -*- coding: utf-8 -*-

# GNU General Public License v2.0 (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

import unittest
from resources.lib.vrtplayer import vrtplayer, streamservice, tokenresolver
from mock import MagicMock

use_drm = False


class StreamServiceTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._use_drm = 'false'

    def _side_effect(self, arg):
        vals = {'username': 'qsdfdsq', 'password': 'qsdfqsdfds', 'showsubtitles': 'true', 'usedrm': self._use_drm}
        return vals[arg]

    def test_get_ondemand_stream_from_url_gets_stream_does_not_crash(self):
        mock = MagicMock()
        token_resolver = tokenresolver.TokenResolver(mock)
        mock.get_setting = MagicMock(side_effect=self._side_effect)
        mock.get_userdata_path.return_value = "vrttest"
        mock.check_if_path_exists.return_value = False
        mock.make_dir.return_value = None
        mock.open_path.return_value = False
        mock.check_inputstream_adaptive.return_value = True
        service = streamservice.StreamService(vrtplayer.VRTPlayer.VRT_BASE, vrtplayer.VRTPlayer.VRTNU_BASE_URL, mock, token_resolver)
        video = {'video_url' : 'vrtnu/a-z/pano/2019/pano-s2019a6/', 'video_id' : None, 'publication_id' : None,}
        stream = service.get_stream(video)
        self.assertTrue(stream is not None)

    def test_get_live_stream_from_url_does_not_crash_returns_stream_and_licensekey(self):
        self._use_drm = 'true'
        mock = MagicMock()
        token_resolver = tokenresolver.TokenResolver(mock)
        mock.get_setting = MagicMock(side_effect=self._side_effect)
        mock.get_userdata_path.return_value = "vrttest"
        mock.check_if_path_exists.return_value = False
        mock.make_dir.return_value = None
        mock.open_path.return_value = False
        mock.check_inputstream_adaptive.return_value = True
        service = streamservice.StreamService(vrtplayer.VRTPlayer.VRT_BASE, vrtplayer.VRTPlayer.VRTNU_BASE_URL, mock, token_resolver)
        video = {'video_url' : vrtplayer.VRTPlayer._CANVAS_LIVESTREAM_, 'video_id' : None, 'publication_id' : None}
        stream = service.get_stream(video)
        self.assertTrue(stream is not None)
        self.assertTrue(stream.license_key is not None)

    def test_get_live_stream_from_url_does_not_crash(self):
        mock = MagicMock()
        token_resolver = tokenresolver.TokenResolver(mock)
        mock.get_setting = MagicMock(side_effect=self._side_effect)
        mock.get_userdata_path.return_value = "vrttest"
        mock.check_if_path_exists.return_value = False
        mock.make_dir.return_value = None
        mock.open_path.return_value = False
        mock.check_inputstream_adaptive.return_value = True
        service = streamservice.StreamService(vrtplayer.VRTPlayer.VRT_BASE, vrtplayer.VRTPlayer.VRTNU_BASE_URL, mock, token_resolver)
        video = {'video_url' : vrtplayer.VRTPlayer._CANVAS_LIVESTREAM_, 'video_id' : None, 'publication_id' : None}
        stream = service.get_stream(video)
        self.assertTrue(stream is not None)


if __name__ == '__main__':
    unittest.main()
