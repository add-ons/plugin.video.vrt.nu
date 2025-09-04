# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Integration tests for search functionality"""

import unittest
from api import get_programs
from search import Search

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

addon = xbmcaddon.Addon()


@unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
@unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
class TestSearch(unittest.TestCase):
    """TestClass class"""

    def test_search_journaal(self):
        """Test search (journaal)"""
        search_items = get_programs(keywords='journaal')

        # Test we get a non-empty search result
        self.assertGreater(len(search_items), 0)

    def test_search_weer(self):
        """Test search (weer)"""
        search_items = get_programs(keywords='weer')

        # Test we get a non-empty search result
        self.assertGreater(len(search_items), 0)

    def test_search_unicode(self):
        """Test unicode search (René)"""
        search_items = get_programs(keywords='René')

        # Test we get a non-empty search result
        self.assertGreater(len(search_items), 0)

    @staticmethod
    def test_search_empty():
        """Test for empty search"""
        Search().search(keywords='')


if __name__ == '__main__':
    unittest.main()
