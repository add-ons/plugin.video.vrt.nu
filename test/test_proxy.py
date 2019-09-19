# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=duplicate-code,invalid-name,missing-docstring,protected-access

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import addon

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcvfs = __import__('xbmcvfs')

plugin = addon.plugin


class TestProxy(unittest.TestCase):
    def setUp(self):
        xbmc.GLOBAL_SETTINGS['network.usehttpproxy'] = True
        xbmc.GLOBAL_SETTINGS['network.httpproxytype'] = 0
        xbmc.GLOBAL_SETTINGS['network.httpproxyserver'] = '127.0.0.1'
        xbmc.GLOBAL_SETTINGS['network.httpproxyport'] = '8899'

    def tearDown(self):
        xbmc.GLOBAL_SETTINGS['network.usehttpproxy'] = False

    # Delete tokens method: '/tokens/delete'
    def test_clear_cookies_route(self):
        plugin.run(['plugin://plugin.video.vrt.nu/tokens/delete', '0', ''])
        self.assertEqual(plugin.url_for(addon.delete_tokens), 'plugin://plugin.video.vrt.nu/tokens/delete')

    # Delete cache method: '/cache/delete'
    def test_invalidate_caches_route(self):
        plugin.run(['plugin://plugin.video.vrt.nu/cache/delete', '0', ''])
        self.assertEqual(plugin.url_for(addon.delete_cache), 'plugin://plugin.video.vrt.nu/cache/delete')

    # A-Z menu: '/programs'
    def test_az_menu(self):
        plugin.run(['plugin://plugin.video.vrt.nu/programs', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs), 'plugin://plugin.video.vrt.nu/programs')

    # Categories menu: '/categories'
    def test_categories_menu(self):
        plugin.run(['plugin://plugin.video.vrt.nu/categories', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories), 'plugin://plugin.video.vrt.nu/categories')

    # Categories programs menu: '/categories/<category>'
    def test_categories_tvshow_menu(self):
        plugin.run(['plugin://plugin.video.vrt.nu/categories/docu', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories, category='docu'), 'plugin://plugin.video.vrt.nu/categories/docu')

    # Favorites menu: '/favorites'
    def test_favorites(self):
        plugin.run(['plugin://plugin.video.vrt.nu/favorites/programs', '0', ''])
        self.assertEqual(plugin.url_for(addon.favorites_programs), 'plugin://plugin.video.vrt.nu/favorites/programs')
