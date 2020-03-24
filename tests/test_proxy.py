# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Integration tests for proxy-related functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import unittest
import addon

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcvfs = __import__('xbmcvfs')

plugin = addon.plugin


@unittest.skipIf(sys.version_info < (3, 6, 0), 'Skipping proxy tests on Python 3.5 and older')
class TestProxy(unittest.TestCase):
    """TestCase class"""

    def setUp(self):
        """Build up  function for TestCase class"""
        xbmc.settings['network.usehttpproxy'] = True
        xbmc.settings['network.httpproxytype'] = 0
        xbmc.settings['network.httpproxyserver'] = 'localhost'
        xbmc.settings['network.httpproxyport'] = '8899'

    def tearDown(self):
        """Clean up function for TestCase class"""
        xbmc.settings['network.usehttpproxy'] = False

    # Delete tokens method: '/tokens/delete'
    def test_clear_cookies_route(self):
        """Test clearing cookies"""
        plugin.run(['plugin://plugin.video.vrt.nu/tokens/delete', '0', ''])
        self.assertEqual(plugin.url_for(addon.delete_tokens), 'plugin://plugin.video.vrt.nu/tokens/delete')

    # Delete cache method: '/cache/delete'
    def test_invalidate_caches_route(self):
        """Test invalidate caches"""
        plugin.run(['plugin://plugin.video.vrt.nu/cache/delete', '0', ''])
        self.assertEqual(plugin.url_for(addon.delete_cache), 'plugin://plugin.video.vrt.nu/cache/delete')

    # A-Z menu: '/programs'
    def test_az_menu(self):
        """Test Programs menu"""
        plugin.run(['plugin://plugin.video.vrt.nu/programs', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs), 'plugin://plugin.video.vrt.nu/programs')

    # Categories menu: '/categories'
    def test_categories_menu(self):
        """Test Categories menu"""
        plugin.run(['plugin://plugin.video.vrt.nu/categories', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories), 'plugin://plugin.video.vrt.nu/categories')

    # Categories programs menu: '/categories/<category>'
    def test_categories_tvshow_menu(self):
        """Test Categories tvshow"""
        plugin.run(['plugin://plugin.video.vrt.nu/categories/docu', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories, category='docu'), 'plugin://plugin.video.vrt.nu/categories/docu')

    # Favorites menu: '/favorites'
    def test_favorites(self):
        """Test Favorites menu"""
        plugin.run(['plugin://plugin.video.vrt.nu/favorites/programs', '0', ''])
        self.assertEqual(plugin.url_for(addon.favorites_programs), 'plugin://plugin.video.vrt.nu/favorites/programs')
