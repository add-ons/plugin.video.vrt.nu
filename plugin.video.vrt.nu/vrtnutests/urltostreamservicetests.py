import unittest
from resources.lib.vrtplayer import vrtplayer, urltostreamservice
from vrtnutests import mockkodiwrapper



class UrlToStreamServiceTests(unittest.TestCase):

    def test_get_stream_from_url_gets_stream_does_not_crash(self):
        mock = mockkodiwrapper.MockKodiWrapper()
        service = urltostreamservice.UrlToStreamService(vrtplayer.VRTPlayer._VRT_BASE,
                                                           vrtplayer.VRTPlayer._VRTNU_BASE_URL,
                                                           mock)
        stream = service.get_stream_from_url('/vrtnu/a-z/22-3-1-jaar-later---het-onderzoek/2017/22-3-1-jaar-later---het-onderzoek-s2017/')
        print stream


    def test_get_stream_from_url_does_not_crash(self):
        mock = mockkodiwrapper.MockKodiWrapper()
        service = urltostreamservice.UrlToStreamService(vrtplayer.VRTPlayer._VRT_BASE,
                                                           vrtplayer.VRTPlayer._VRTNU_BASE_URL, mock)
        stream = service.get_stream_from_url(vrtplayer.VRTPlayer._CANVAS_LIVESTREAM_)
        print stream

