# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Integration tests for changes to settings"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from addon import plugin
from kodiutils import open_settings

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

addon = xbmcaddon.Addon()


class TestSettings(unittest.TestCase):
    """TestCase class"""

    def tearDown(self):
        """Clean up function for TestCase class"""
        addon.settings['showfanart'] = True
        addon.settings['showoneoff'] = True
        addon.settings['showyoutube'] = True
        addon.settings['usefavorites'] = True
        addon.settings['usehttpcaching'] = True
        addon.settings['usemenucaching'] = True
        addon.settings['useresumepoints'] = True

    @staticmethod
    def test_menucaching_disabled():
        """Test without menu caching"""
        addon.settings['usehttpcaching'] = True
        addon.settings['usemenucaching'] = False
        plugin.run(['plugin://plugin.video.vrt.nu/recent', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/recent', '0', ''])

    @staticmethod
    def test_httpcaching_disabled():
        """Test without http caching"""
        addon.settings['usehttpcaching'] = False
        addon.settings['usemenucaching'] = True
        plugin.run(['plugin://plugin.video.vrt.nu/offline', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/offline', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/tvguide/date/today/canvas', '0', ''])

    @staticmethod
    def test_favorites_disabled():
        """Test without favorites"""
        plugin.run(['plugin://plugin.video.vrt.nu/', '0', ''])
        addon.settings['usefavorites'] = False
        addon.settings['useresumepoints'] = True
        plugin.run(['plugin://plugin.video.vrt.nu/', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/favorites', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/favorites/recent', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/favorites/offline', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/favorites/manage', '0', ''])

    @staticmethod
    def test_resumepoints_disabled():
        """Test without resumepoints"""
        plugin.run(['plugin://plugin.video.vrt.nu/favorites', '0', ''])
        addon.settings['usefavorites'] = True
        addon.settings['useresumepoints'] = False
        plugin.run(['plugin://plugin.video.vrt.nu/favorites', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/resumepoints/watchlater', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/resumepoints/continue', '0', ''])

    @staticmethod
    def test_opensettings():
        """Test open_settings"""
        open_settings()

    @staticmethod
    def test_youtube_disabled():
        """Test with showyoutube disabled"""
        addon.settings['showyoutube'] = False
        plugin.run(['plugin://plugin.video.vrt.nu/channels/radio1', '0', ''])

    @staticmethod
    def test_showfanart_disabled():
        """Test with showfanart disabled"""
        addon.settings['showfanart'] = False
        plugin.run(['plugin://plugin.video.vrt.nu/categories', '0', ''])

    @staticmethod
    def test_showoneoff_disabled():
        """Test with showoneofff disabled"""
        addon.settings['showoneoff'] = False
        plugin.run(['plugin://plugin.video.vrt.nu/programs', '0', ''])


if __name__ == '__main__':
    unittest.main()
