# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for StreamService functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime, timedelta
import os
import unittest
import dateutil.tz

try:
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import HTTPError

from data import CHANNELS
from streamservice import StreamService
from tokenresolver import TokenResolver

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

addon = xbmcaddon.Addon()

now = datetime.now(dateutil.tz.tzlocal())
yesterday = now + timedelta(days=-1)


class TestStreamService(unittest.TestCase):
    """TestCase class"""

    _tokenresolver = TokenResolver()
    _streamservice = StreamService(_tokenresolver)

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_get_ondemand_stream_from_invalid_url(self):
        """Test getting stream from invalid URL"""
        video = {
            'video_url': 'https://www.vrt.be/vrtmax/a-z/vrt-nws-laat/2017/vrt-nws-laat-d20170501/',
            'video_id': None,
            'publication_id': None,
        }
        try:
            stream = self._streamservice.get_stream(video)
        except HTTPError:
            pass
        else:
            self.assertEqual(None, stream)

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_get_ondemand_stream_from_invalid_videoid(self):
        """Test getting stream from invalid video_id"""
        video = {
            'video_url': None,
            'video_id': 'invalid_vid-4662107f-fc26-4f66-9076-984ee4bb80ee',
            'publication_id': 'pbs-pub-be74b2e3-5054-4e4c-b8aa-42e9cd4877b6',
        }
        try:
            stream = self._streamservice.get_stream(video)
        except HTTPError:
            pass
        else:
            self.assertEqual(None, stream)

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_get_ondemand_stream_from_url_gets_stream_does_not_crash(self):
        """Test getting stream from URL does not crash"""
        video = {
            'video_url': yesterday.strftime('https://www.vrt.be/vrtmax/a-z/vrt-nws-journaal/%Y/vrt-nws-journaal-vrt-nws-journaal-19u-%Y%m%d/'),
            'video_id': None,
            'publication_id': None,
        }
        stream = self._streamservice.get_stream(video)
        # NOTE: Testing live streams only works within Europe
        if os.environ.get('GITHUB_ACTIONS') != 'true':
            self.assertTrue(stream is not None)

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_get_ondemand_stream_from_from_videoid_geoblocked(self):
        """Test getting stream from geoblocked video_id"""
        # Undercover S01E01
        video = {
            'video_id': 'vid-b77b58cb-eebf-4b00-b772-0d6b4caad6a5',
            'publication_id': 'pbs-pub-8a1068a5-cffc-4b25-96cc-2b15b3c513dc',
        }
        stream = self._streamservice.get_stream(video)
        # NOTE: Testing geoblocked streams only works within Europe
        if os.environ.get('GITHUB_ACTIONS') != 'true':
            self.assertTrue(stream is not None)

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_get_mpd_live_stream_from_url_does_not_crash_returns_stream(self):
        """Test getting MPEG-DASH stream from URL"""
        addon.settings['usedrm'] = True
        addon.settings['useinputstreamadaptive'] = True
        video = {
            'video_url': CHANNELS[1]['live_stream'],
            'video_id': None,
            'publication_id': None,
        }
        stream = self._streamservice.get_stream(video)
        # NOTE: Testing live streams only works within Europe
        if os.environ.get('GITHUB_ACTIONS') != 'true':
            self.assertTrue(stream is not None)
            self.assertTrue(stream.license_headers is not None)

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_get_mpd_live_stream_from_url_does_not_crash(self):
        """Test getting MPEG-DASH stream from URL"""
        addon.settings['usedrm'] = True
        addon.settings['useinputstreamadaptive'] = True
        video = {
            'video_url': CHANNELS[0]['live_stream'],
            'video_id': None,
            'publication_id': None,
        }
        stream = self._streamservice.get_stream(video)
        # NOTE: Testing live streams only works within Europe
        if os.environ.get('GITHUB_ACTIONS') != 'true':
            self.assertTrue(stream is not None)

    def test_get_mpd_live_stream_from_id_does_not_crash(self):
        """Test getting MPEG-DASH stream from URL"""
        addon.settings['usedrm'] = True
        addon.settings['useinputstreamadaptive'] = True
        video = {
            'video_url': None,
            'video_id': CHANNELS[1]['live_stream_id'],
            'publication_id': None
        }
        stream = self._streamservice.get_stream(video)
        # NOTE: Testing live streams only works within Europe
        if os.environ.get('GITHUB_ACTIONS') != 'true':
            self.assertTrue(stream is not None)
        video = {
            'video_url': None,
            'video_id': CHANNELS[3]['live_stream_id'],
            'publication_id': None,
        }
        stream = self._streamservice.get_stream(video)
        # NOTE: Testing live streams only works within Europe
        if os.environ.get('GITHUB_ACTIONS') != 'true':
            self.assertTrue(stream is not None)


if __name__ == '__main__':
    unittest.main()
