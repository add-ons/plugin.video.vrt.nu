# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Integration tests for search functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from apihelper import ApiHelper
from favorites import Favorites
from search import Search
from resumepoints import ResumePoints

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

addon = xbmcaddon.Addon()
itemsperpage = int(addon.settings.get('itemsperpage'))


class TestSearch(unittest.TestCase):
    """TestClass class"""

    _favorites = Favorites()
    _resumepoints = ResumePoints()
    _apihelper = ApiHelper(_favorites, _resumepoints)

    def test_search_journaal(self):
        """Test search (journaal)"""
        search_items, sort, ascending, content = self._apihelper.list_search('journaal', page=1)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), itemsperpage)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_search_journaal_page2(self):
        """Test search page 2 (journaal)"""
        search_items, sort, ascending, content = self._apihelper.list_search('journaal', page=2)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), itemsperpage)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_search_weer(self):
        """Test search (weer)"""
        search_items, sort, ascending, content = self._apihelper.list_search('weer', page=1)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), itemsperpage)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_search_unicode(self):
        """Test unicode search (René)"""
        search_items, sort, ascending, content = self._apihelper.list_search('René', page=1)

        # Test we get a non-empty search result
        self.assertGreater(len(search_items), 0)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    @staticmethod
    def test_search_empty():
        """Test for empty search"""
        Search().search(keywords='')


if __name__ == '__main__':
    unittest.main()
