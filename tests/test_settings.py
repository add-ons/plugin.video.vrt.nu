# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Integration tests for changes to settings"""

import os
import unittest
from addon import plugin
from kodiutils import open_settings
from streamservice import StreamService
from tokenresolver import TokenResolver

import xbmcaddon

ADDON = xbmcaddon.Addon()


class TestSettings(unittest.TestCase):
    """TestCase class"""

    _tokenresolver = TokenResolver()
    _streamservice = StreamService(_tokenresolver)

    def tearDown(self):
        """Clean up function for TestCase class"""
        ADDON.setSetting('showfanart', 'true')
        ADDON.setSetting('showoneoff', 'true')
        ADDON.setSetting('showyoutube', 'true')
        ADDON.setSetting('usedrm', 'true')
        ADDON.setSetting('usefavorites', 'true')
        ADDON.setSetting('usehttpcaching', 'true')
        ADDON.setSetting('useinputstreamadaptive', 'true')
        ADDON.setSetting('usemenucaching', 'true')
        ADDON.setSetting('useresumepoints', 'true')

    @staticmethod
    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_menucaching_disabled():
        """Test without menu caching"""
        ADDON.setSetting('usehttpcaching', 'true')
        ADDON.setSetting('usemenucaching', 'false')
        plugin.run(['plugin://plugin.video.vrt.nu/recent', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/recent', '0', ''])

    @staticmethod
    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_httpcaching_disabled():
        """Test without http caching"""
        ADDON.setSetting('usehttpcaching', 'false')
        ADDON.setSetting('usemenucaching', 'true')
        plugin.run(['plugin://plugin.video.vrt.nu/offline', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/offline', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/tvguide/date/today/canvas', '0', ''])

    @staticmethod
    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_favorites_disabled():
        """Test without favorites"""
        plugin.run(['plugin://plugin.video.vrt.nu/', '0', ''])
        ADDON.setSetting('usefavorites', 'false')
        ADDON.setSetting('useresumepoints', 'true')
        plugin.run(['plugin://plugin.video.vrt.nu/', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/favorites', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/favorites/recent', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/favorites/offline', '0', ''])

    @staticmethod
    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_resumepoints_disabled():
        """Test without resumepoints"""
        plugin.run(['plugin://plugin.video.vrt.nu/favorites', '0', ''])
        ADDON.setSetting('usefavorites', 'true')
        ADDON.setSetting('useresumepoints', 'false')
        plugin.run(['plugin://plugin.video.vrt.nu/favorites', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/resumepoints/continue', '0', ''])

    @staticmethod
    def test_opensettings():
        """Test open_settings"""
        open_settings()

    @staticmethod
    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_youtube_disabled():
        """Test with showyoutube disabled"""
        ADDON.setSetting('showyoutube', 'false')
        plugin.run(['plugin://plugin.video.vrt.nu/channels/radio1', '0', ''])

    @staticmethod
    def test_showfanart_disabled():
        """Test with showfanart disabled"""
        ADDON.setSetting('showfanart', 'false')
        plugin.run(['plugin://plugin.video.vrt.nu/categories', '0', ''])

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_ondemand_stream(self):
        """Test ondemand stream"""
        ADDON.setSetting('usedrm', 'false')
        ADDON.setSetting('useinputstreamadaptive', 'false')
        video = {'video_url': 'https://www.vrt.be/vrtmax/a-z/winteruur/1/winteruur-s1a1/'}
        stream = self._streamservice.get_stream(video)
        # NOTE: Testing live streams only works within Europe
        if os.environ.get('GITHUB_ACTIONS') != 'true':
            self.assertTrue(stream is not None)

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_ondemand_stream_ia(self):
        """Test with usedrm disabled"""
        ADDON.setSetting('usedrm', 'false')
        ADDON.setSetting('useinputstreamadaptive', 'true')
        video = {'video_url': 'https://www.vrt.be/vrtmax/a-z/winteruur/1/winteruur-s1a1/'}
        stream = self._streamservice.get_stream(video)
        # NOTE: Testing live streams only works within Europe
        if os.environ.get('GITHUB_ACTIONS') != 'true':
            self.assertTrue(stream is not None)

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_ondemand_stream_drm(self):
        """Test with useinputstreamadaptive disabled"""
        ADDON.setSetting('usedrm', 'true')
        ADDON.setSetting('useinputstreamadaptive', 'false')
        video = {'video_url': 'https://www.vrt.be/vrtmax/a-z/winteruur/1/winteruur-s1a1/'}
        stream = self._streamservice.get_stream(video)
        # NOTE: Testing live streams only works within Europe
        if os.environ.get('GITHUB_ACTIONS') != 'true':
            self.assertTrue(stream is not None)

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_ondemand_stream_drm_ia(self):
        """Test with usedrm and useinputstreamadaptive disabled"""
        ADDON.setSetting('usedrm', 'true')
        ADDON.setSetting('useinputstreamadaptive', 'true')
        video = {'video_url': 'https://www.vrt.be/vrtmax/a-z/winteruur/1/winteruur-s1a1/'}
        stream = self._streamservice.get_stream(video)
        # NOTE: Testing live streams only works within Europe
        if os.environ.get('GITHUB_ACTIONS') != 'true':
            self.assertTrue(stream is not None)


if __name__ == '__main__':
    unittest.main()
