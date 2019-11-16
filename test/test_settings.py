# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=invalid-name,missing-docstring

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
    def tearDown(self):
        addon.settings['usemenucaching'] = True
        addon.settings['usehttpcaching'] = True
        addon.settings['usefavorites'] = True
        addon.settings['useresumepoints'] = True

    @staticmethod
    def test_menucaching_disabled():
        ''' Test without menu caching '''
        addon.settings['usemenucaching'] = False
        addon.settings['usehttpcaching'] = True
        plugin.run(['plugin://plugin.video.vrt.nu/recent', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/recent', '0', ''])

    @staticmethod
    def test_httpcaching_disabled():
        ''' Test without http caching '''
        addon.settings['usehttpcaching'] = False
        addon.settings['usemenucaching'] = True
        plugin.run(['plugin://plugin.video.vrt.nu/offline', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/offline', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/tvguide/date/today/canvas', '0', ''])

    @staticmethod
    def test_favorites_disabled():
        ''' Test without favorites '''
        plugin.run(['plugin://plugin.video.vrt.nu/', '0', ''])
        addon.settings['usefavorites'] = False
        addon.settings['useresumepoints'] = True
        plugin.run(['plugin://plugin.video.vrt.nu/', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/favorites', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/favorites/recent', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/favorites/offline', '0', ''])

    @staticmethod
    def test_resumepoints_disabled():
        ''' Test without resumepoints '''
        plugin.run(['plugin://plugin.video.vrt.nu/favorites', '0', ''])
        addon.settings['useresumepoints'] = False
        addon.settings['usefavorites'] = True
        plugin.run(['plugin://plugin.video.vrt.nu/favorites', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/resumepoints/watchlater', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/resumepoints/continue', '0', ''])

    @staticmethod
    def test_opensettings():
        ''' Test open_settings '''
        open_settings()


if __name__ == '__main__':
    unittest.main()
