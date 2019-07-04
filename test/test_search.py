# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=missing-docstring

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

from resources.lib import favorites, vrtapihelper
import addon

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')


class TestSearch(unittest.TestCase):

    _favorites = favorites.Favorites(addon.kodi)
    _apihelper = vrtapihelper.VRTApiHelper(addon.kodi, _favorites)

    def test_search_journaal(self):
        ''' Test for journaal '''
        search_items, sort, ascending, content = self._apihelper.get_search_items('journaal', page=1)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_search_journaal_page2(self):
        ''' Test for journaal '''
        search_items, sort, ascending, content = self._apihelper.get_search_items('journaal', page=2)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_search_journaal_page3(self):
        ''' Test for journaal '''
        search_items, sort, ascending, content = self._apihelper.get_search_items('journaal', page=3)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_search_weer(self):
        ''' Test for journaal '''
        search_items, sort, ascending, content = self._apihelper.get_search_items('weer', page=1)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')


if __name__ == '__main__':
    unittest.main()
