# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=invalid-name,missing-docstring

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import kodiutils

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

addon = xbmcaddon.Addon()


class TestKodiUtils(unittest.TestCase):
    def tearDown(self):
        xbmc.settings['debug.showloginfo'] = True
        addon.settings['max_log_level'] = '3'

    def test_localize(self):
        xbmc.settings['locale.language'] = 'resource.language.nl_nl'

        msg = kodiutils.localize(30958)
        #self.assertEqual(msg, "There is a problem with this VRT NU {protocol} stream. Try again with {component} {state} or try to play this program from the VRT NU website. Please report this problem at https://www.vrt.be/vrtnu/help/")  # noqa
        self.assertEqual(msg, "Er is een probleem met deze VRT NU {protocol}-stream. Probeer het opnieuw met {component} {state} of probeer dit programma af te spelen vanaf de VRT NU-website. Meld dit probleem op https://www.vrt.be/vrtnu/help/")  # noqa

        msg = kodiutils.localize(30958, component='Widevine DRM', state='enabled')
        #self.assertEqual(msg, "There is a problem with this VRT NU {protocol} stream. Try again with Widevine DRM enabled or try to play this program from the VRT NU website. Please report this problem at https://www.vrt.be/vrtnu/help/")  # noqa
        self.assertEqual(msg, "Er is een probleem met deze VRT NU {protocol}-stream. Probeer het opnieuw met Widevine DRM enabled of probeer dit programma af te spelen vanaf de VRT NU-website. Meld dit probleem op https://www.vrt.be/vrtnu/help/")  # noqa

        msg = kodiutils.localize(30958, protocol='MPEG-DASH', component='Widevine DRM', state='enabled')
        #self.assertEqual(msg, "There is a problem with this VRT NU MPEG-DASH stream. Try again with Widevine DRM enabled or try to play this program from the VRT NU website. Please report this problem at https://www.vrt.be/vrtnu/help/")  # noqa
        self.assertEqual(msg, "Er is een probleem met deze VRT NU MPEG-DASH-stream. Probeer het opnieuw met Widevine DRM enabled of probeer dit programma af te spelen vanaf de VRT NU-website. Meld dit probleem op https://www.vrt.be/vrtnu/help/")  # noqa

    @staticmethod
    def test_log_disabled():
        xbmc.settings['debug.showloginfo'] = False
        addon.settings['max_log_level'] = '0'
        kodiutils.log(3, 'No logging when quiet')

    @staticmethod
    def test_debug_logging():
        xbmc.settings['debug.showloginfo'] = True
        addon.settings['max_log_level'] = '3'
        kodiutils.log(0, 'Logging as quiet')
        kodiutils.log(1, 'Logging as info')
        kodiutils.log(2, 'Logging as verbose')
        kodiutils.log(3, 'Logging as debug')
        kodiutils.log_error('Logging as error')

    @staticmethod
    def test_input_down():
        kodiutils.input_down()

    @staticmethod
    def test_container_refresh():
        kodiutils.container_refresh()
        kodiutils.container_refresh('plugin://plugin.video.vrt.nu/')

    @staticmethod
    def test_container_update():
        kodiutils.container_update()
        kodiutils.container_update('plugin://plugin.video.vrt.nu/')

    def test_supports_drm(self):
        self.assertTrue(kodiutils.supports_drm())


if __name__ == '__main__':
    unittest.main()
