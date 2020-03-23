# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for Kodi utilities"""

# pylint: disable=invalid-name

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
    """TestCase class"""

    def tearDown(self):
        """Clean up function for TestCase class"""
        xbmc.settings['debug.showloginfo'] = True
        addon.settings['max_log_level'] = '3'

    def test_localize(self):
        """Test localizing strings"""
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
        """Test with logging disabled"""
        xbmc.settings['debug.showloginfo'] = False
        addon.settings['max_log_level'] = '0'
        kodiutils.log(3, 'No logging when quiet')

    @staticmethod
    def test_debug_logging():
        """Test with debug logging enabled"""
        xbmc.settings['debug.showloginfo'] = True
        addon.settings['max_log_level'] = '3'
        kodiutils.log(0, 'Logging as quiet')
        kodiutils.log(1, 'Logging as info')
        kodiutils.log(2, 'Logging as verbose')
        kodiutils.log(3, 'Logging as debug')
        kodiutils.log_error('Logging as error')

    @staticmethod
    def test_input_down():
        """Test pressing down key"""
        kodiutils.input_down()

    @staticmethod
    def test_container_refresh():
        """Test refreshing the current container"""
        kodiutils.container_refresh()
        kodiutils.container_refresh(None)
        kodiutils.container_refresh('plugin://plugin.video.vrt.nu/')

    @staticmethod
    def test_container_update():
        """Test updating the current container"""
        kodiutils.container_update(None)
        kodiutils.container_update('plugin://plugin.video.vrt.nu/')

    def test_supports_drm(self):
        """Test if Kodi supports DRM"""
        self.assertTrue(kodiutils.supports_drm())

    def test_jsonrpc(self):
        """Test jsonrpc functionality"""
        ret = kodiutils.jsonrpc(method='Input.Down')
        self.assertTrue(isinstance(ret, dict))

        ret = kodiutils.jsonrpc(dict(method='Input.Down'))
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 1)

        ret = kodiutils.jsonrpc(dict(method='Input.Down'), dict(method='Player.Open'))
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 2)


if __name__ == '__main__':
    unittest.main()
