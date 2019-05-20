# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

from resources.lib.kodiwrappers import kodiwrapper
from resources.lib.vrtplayer import favorites, vrtapihelper

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')


class TestSearch(unittest.TestCase):

    _kodi = kodiwrapper.KodiWrapper(None, 'plugin.video.vrt.nu', xbmcaddon.Addon)
    _favorites = favorites.Favorites(_kodi)
    _apihelper = vrtapihelper.VRTApiHelper(_kodi, _favorites)

    def test_search_journaal(self):
        ''' Test for journaal '''
        search_items, sort, ascending, content = self._apihelper.search('journaal', page=1)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_search_journaal_page2(self):
        ''' Test for journaal '''
        search_items, sort, ascending, content = self._apihelper.search('journaal', page=2)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_search_journaal_page3(self):
        ''' Test for journaal '''
        search_items, sort, ascending, content = self._apihelper.search('journaal', page=3)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_search_weer(self):
        ''' Test for journaal '''
        search_items, sort, ascending, content = self._apihelper.search('weer', page=1)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')


if __name__ == '__main__':
    unittest.main()
