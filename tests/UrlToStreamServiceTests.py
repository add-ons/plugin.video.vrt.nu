import unittest
from resources.lib.vrtplayer import urltostreamservice
from resources.lib.vrtplayer import vrtplayer
from tests import mockkodiwrapper

class UrlToStreamServiceTests(unittest.TestCase):

    def test_get_stream_from_url_gets_stream_does_not_crash(self):
        mock = mockkodiwrapper.MockKodiWrapper()
        service = urltostreamservice.UrlToStreamService(vrtplayer.VRTPlayer._VRT_BASE,
                                                           vrtplayer.VRTPlayer._VRTNU_BASE_URL,
                                                           mock)
        service.get_stream_from_url('/vrtnu/a-z/apocalyps--de-eerste-wereldoorlog/1/apocalyps--de-eerste-wereldoorlog-s1a5/')

