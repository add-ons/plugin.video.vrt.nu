import unittest
from resources.lib.vrtplayer import urltolivestreamservice
from resources.lib.vrtplayer import vrtplayer
from tests import mockkodiwrapper

class UrlToStreamServiceTests(unittest.TestCase):

    def test_get_stream_from_url_does_not_crash(self):
        mock = mockkodiwrapper.MockKodiWrapper()
        service = urltolivestreamservice.UrlToLivestreamService(mock)
        stream = service.get_stream_from_url(vrtplayer.VRTPlayer._CANVAS_LIVESTREAM_)
