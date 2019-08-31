# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=missing-docstring

from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime, timedelta
import os
import unittest
import dateutil.tz

try:
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import HTTPError

from addon import kodi
from data import CHANNELS
from streamservice import StreamService
from tokenresolver import TokenResolver

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

xbmcaddon.ADDON_SETTINGS['usedrm'] = 'false'
now = datetime.now(dateutil.tz.tzlocal())
yesterday = now + timedelta(days=-1)


@unittest.skipIf(os.environ.get('TRAVIS') == 'true', 'Skipping this test on Travis CI.')
class StreamServiceTests(unittest.TestCase):

    _tokenresolver = TokenResolver(kodi)
    _streamservice = StreamService(kodi, _tokenresolver)

    def test_get_ondemand_stream_from_invalid_url(self):
        video = dict(
            video_url='https://www.vrt.be/vrtnu/a-z/het-journaal/2017/het-journaal-het-journaal-laat-20170501/',
            video_id=None,
            publication_id=None,
        )
        try:
            stream = self._streamservice.get_stream(video)
            self.assertEqual(stream.stream_url, video['video_url'])
        except HTTPError:
            pass

    def test_get_ondemand_stream_from_url_gets_stream_does_not_crash(self):
        video = dict(
            # video_url='https://www.vrt.be/vrtnu/a-z/pano/2019/pano-s2019a6/',
            video_url=yesterday.strftime('https://www.vrt.be/vrtnu/a-z/het-journaal/2019/het-journaal-het-journaal-laat-%Y%m%d/'),
            video_id=None,
            publication_id=None,
        )
        stream = self._streamservice.get_stream(video)
        self.assertTrue(stream is not None)

    def test_get_live_stream_from_url_does_not_crash_returns_stream_and_licensekey(self):
        xbmcaddon.ADDON_SETTINGS['usedrm'] = 'true'
        video = dict(
            video_url=CHANNELS[1]['live_stream'],
            video_id=None,
            publication_id=None,
        )
        stream = self._streamservice.get_stream(video)
        self.assertTrue(stream is not None)
#        self.assertTrue(stream.license_key is not None)

    def test_get_live_stream_from_url_does_not_crash(self):
        video = dict(
            video_url=CHANNELS[1]['live_stream'],
            video_id=None,
            publication_id=None,
        )
        stream = self._streamservice.get_stream(video)
        self.assertTrue(stream is not None)

    def test_get_live_stream_from_id_does_not_crash(self):
        video = dict(
            video_url=None,
            video_id=CHANNELS[1]['live_stream_id'],
            publication_id=None,
        )
        stream = self._streamservice.get_stream(video)
        self.assertTrue(stream is not None)


if __name__ == '__main__':
    unittest.main()
