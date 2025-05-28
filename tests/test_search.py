# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Integration tests for search functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from api import get_programs
from search import Search

import xbmcaddon

ADDON = xbmcaddon.Addon()


@unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
@unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
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
