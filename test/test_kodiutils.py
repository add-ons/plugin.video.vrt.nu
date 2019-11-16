# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=invalid-name,missing-docstring

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from kodiutils import localize

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')


class KodiTests(unittest.TestCase):

    def test_localize(self):
        xbmc.settings['locale.language'] = 'resource.language.nl_nl'

        msg = localize(30958)
        #self.assertEqual(msg, "There is a problem with this VRT NU {protocol} stream. Try again with {component} {state} or try to play this program from the VRT NU website. Please report this problem at https://www.vrt.be/vrtnu/help/")  # noqa
        self.assertEqual(msg, "Er is een probleem met deze VRT NU {protocol}-stream. Probeer het opnieuw met {component} {state} of probeer dit programma af te spelen vanaf de VRT NU-website. Meld dit probleem op https://www.vrt.be/vrtnu/help/")  # noqa

        msg = localize(30958, component='Widevine DRM', state='enabled')
        #self.assertEqual(msg, "There is a problem with this VRT NU {protocol} stream. Try again with Widevine DRM enabled or try to play this program from the VRT NU website. Please report this problem at https://www.vrt.be/vrtnu/help/")  # noqa
        self.assertEqual(msg, "Er is een probleem met deze VRT NU {protocol}-stream. Probeer het opnieuw met Widevine DRM enabled of probeer dit programma af te spelen vanaf de VRT NU-website. Meld dit probleem op https://www.vrt.be/vrtnu/help/")  # noqa

        msg = localize(30958, protocol='MPEG-DASH', component='Widevine DRM', state='enabled')
        #self.assertEqual(msg, "There is a problem with this VRT NU MPEG-DASH stream. Try again with Widevine DRM enabled or try to play this program from the VRT NU website. Please report this problem at https://www.vrt.be/vrtnu/help/")  # noqa
        self.assertEqual(msg, "Er is een probleem met deze VRT NU MPEG-DASH-stream. Probeer het opnieuw met Widevine DRM enabled of probeer dit programma af te spelen vanaf de VRT NU-website. Meld dit probleem op https://www.vrt.be/vrtnu/help/")  # noqa


if __name__ == '__main__':
    unittest.main()
