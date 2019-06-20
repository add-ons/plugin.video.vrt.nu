# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=missing-docstring

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import addon

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

plugin = addon.plugin


class TestRouter(unittest.TestCase):

    def test_main_menu(self):
        plugin.run(['plugin://plugin.video.vrt.nu/', '0', ''])
        self.assertEqual(plugin.url_for(addon.main_menu), 'plugin://plugin.video.vrt.nu/')

    # Favorites menu: '/favorites'
    def test_favorites(self):
        plugin.run(['plugin://plugin.video.vrt.nu/favorites', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/favorites/programs', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/favorites/recent', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/favorites/recent/2', '0', ''])
        self.assertEqual(plugin.url_for(addon.favorites_recent, page=2), 'plugin://plugin.video.vrt.nu/favorites/recent/2')
        plugin.run(['plugin://plugin.video.vrt.nu/favorites/offline', '0', ''])

    # A-Z menu: '/programs'
    def test_az_menu(self):
        plugin.run(['plugin://plugin.video.vrt.nu/programs', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs), 'plugin://plugin.video.vrt.nu/programs')

    # Episodes menu: '/programs/<program>'
    def test_episodes_menu(self):
        plugin.run(['plugin://plugin.video.vrt.nu/programs/thuis', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs, program='thuis'), 'plugin://plugin.video.vrt.nu/programs/thuis')
        plugin.run(['plugin://plugin.video.vrt.nu/programs/de-campus-cup', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs, program='de-campus-cup'), 'plugin://plugin.video.vrt.nu/programs/de-campus-cup')

    # Categories menu: '/categories'
    def test_categories_menu(self):
        plugin.run(['plugin://plugin.video.vrt.nu/categories', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories), 'plugin://plugin.video.vrt.nu/categories')

    # Categories programs menu: '/categories/<category>'
    def test_categories_tvshow_menu(self):
        plugin.run(['plugin://plugin.video.vrt.nu/categories/docu', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories, category='docu'), 'plugin://plugin.video.vrt.nu/categories/docu')
        plugin.run(['plugin://plugin.video.vrt.nu/categories/kinderen', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories, category='kinderen'), 'plugin://plugin.video.vrt.nu/categories/kinderen')

    # Featured menu: '/featured'
    def test_featured_menu(self):
        plugin.run(['plugin://plugin.video.vrt.nu/featured', '0', ''])
        self.assertEqual(plugin.url_for(addon.featured), 'plugin://plugin.video.vrt.nu/featured')

    # Featured programs menu: '/featured/<cfeatured>'
    def test_featured_tvshow_menu(self):
        plugin.run(['plugin://plugin.video.vrt.nu/featured/kortfilm', '0', ''])
        self.assertEqual(plugin.url_for(addon.featured, feature='kortfilm'), 'plugin://plugin.video.vrt.nu/featured/kortfilm')

    # Channels menu = '/channels/<channel>'
    def test_channels_menu(self):
        plugin.run(['plugin://plugin.video.vrt.nu/channels', '0', ''])
        self.assertEqual(plugin.url_for(addon.channels), 'plugin://plugin.video.vrt.nu/channels')
        plugin.run(['plugin://plugin.video.vrt.nu/channels/ketnet', '0', ''])
        self.assertEqual(plugin.url_for(addon.channels, channel='ketnet'), 'plugin://plugin.video.vrt.nu/channels/ketnet')

    # Live TV menu: '/livetv'
    def test_livetv_menu(self):
        plugin.run(['plugin://plugin.video.vrt.nu/livetv', '0', ''])
        self.assertEqual(plugin.url_for(addon.livetv), 'plugin://plugin.video.vrt.nu/livetv')

    # Most recent menu: '/recent/<page>'
    def test_recent_menu(self):
        plugin.run(['plugin://plugin.video.vrt.nu/recent', '0', ''])
        self.assertEqual(plugin.url_for(addon.recent), 'plugin://plugin.video.vrt.nu/recent')
        plugin.run(['plugin://plugin.video.vrt.nu/recent/2', '0', ''])
        self.assertEqual(plugin.url_for(addon.recent, page=2), 'plugin://plugin.video.vrt.nu/recent/2')

    # Soon offline menu: '/offline/<page>'
    def test_offline_menu(self):
        plugin.run(['plugin://plugin.video.vrt.nu/offline', '0', ''])
        self.assertEqual(plugin.url_for(addon.offline), 'plugin://plugin.video.vrt.nu/offline')

    # TV guide menu: '/tvguide/<date>/<channel>'
    def test_tvguide_date_menu(self):
        plugin.run(['plugin://plugin.video.vrt.nu/tvguide', '0', ''])
        self.assertEqual(plugin.url_for(addon.tv_guide), 'plugin://plugin.video.vrt.nu/tvguide')
        plugin.run(['plugin://plugin.video.vrt.nu/tvguide/today', '0', ''])
        self.assertEqual(plugin.url_for(addon.tv_guide, date='today'), 'plugin://plugin.video.vrt.nu/tvguide/today')
        plugin.run(['plugin://plugin.video.vrt.nu/tvguide/today/canvas', '0', ''])
        self.assertEqual(plugin.url_for(addon.tv_guide, date='today', channel='canvas'), 'plugin://plugin.video.vrt.nu/tvguide/today/canvas')

    # Search VRT NU menu: '/search/<search_string>/<page>'
    def test_search_menu(self):
        plugin.run(['plugin://plugin.video.vrt.nu/search', '0', ''])
        self.assertEqual(plugin.url_for(addon.search), 'plugin://plugin.video.vrt.nu/search')
        plugin.run(['plugin://plugin.video.vrt.nu/search/dag', '0', ''])
        self.assertEqual(plugin.url_for(addon.search, search_string='dag'), 'plugin://plugin.video.vrt.nu/search/dag')
        plugin.run(['plugin://plugin.video.vrt.nu/search/dag/2', '0', ''])
        self.assertEqual(plugin.url_for(addon.search, search_string='dag', page=2), 'plugin://plugin.video.vrt.nu/search/dag/2')

    # Follow method: '/follow/<program>/<title>'
    def test_follow_route(self):
        plugin.run(['plugin://plugin.video.vrt.nu/follow/thuis/Thuis', '0', ''])
        self.assertEqual(plugin.url_for(addon.follow, program='thuis', title='Thuis'), 'plugin://plugin.video.vrt.nu/follow/thuis/Thuis')

    # Unfollow method: '/unfollow/<program>/<title>'
    def test_unfollow_route(self):
        plugin.run(['plugin://plugin.video.vrt.nu/unfollow/thuis/Thuis', '0', ''])
        self.assertEqual(plugin.url_for(addon.unfollow, program='thuis', title='Thuis'), 'plugin://plugin.video.vrt.nu/unfollow/thuis/Thuis')

    # Delete tokens method: '/tokens/delete'
    def test_clear_cookies_route(self):
        plugin.run(['plugin://plugin.video.vrt.nu/tokens/delete', '0', ''])
        self.assertEqual(plugin.url_for(addon.delete_tokens), 'plugin://plugin.video.vrt.nu/tokens/delete')

    # Delete cache method: '/cache/delete'
    def test_invalidate_caches_route(self):
        plugin.run(['plugin://plugin.video.vrt.nu/cache/delete', '0', ''])
        self.assertEqual(plugin.url_for(addon.delete_cache), 'plugin://plugin.video.vrt.nu/cache/delete')

    # Refresh favorites method: '/favorites/refresh'
    def test_refresh_favorites_route(self):
        plugin.run(['plugin://plugin.video.vrt.nu/favorites/refresh', '0', ''])
        self.assertEqual(plugin.url_for(addon.favorites_refresh), 'plugin://plugin.video.vrt.nu/favorites/refresh')

    # Play on demand by id = '/play/id/<publication_id>/<video_id>'
    # Achterflap episode 8 available until 31/12/2025
    def test_play_on_demand_by_id_route(self):
        plugin.run(['plugin://plugin.video.vrt.nu/play/id/pbs-pub-1a170972-dea3-4ea3-8c27-62d2442ee8a3/vid-f80fa527-6759-45a7-908d-ec6f0a7b164e', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_id,
                                        publication_id='pbs-pub-1a170972-dea3-4ea3-8c27-62d2442ee8a3',
                                        video_id='vid-f80fa527-6759-45a7-908d-ec6f0a7b164e'),
                         'plugin://plugin.video.vrt.nu/play/id/pbs-pub-1a170972-dea3-4ea3-8c27-62d2442ee8a3/vid-f80fa527-6759-45a7-908d-ec6f0a7b164e')

    # Play livestream by id = '/play/id/<video_id>'
    # Canvas livestream
    def test_play_livestream_by_id_route(self):
        plugin.run(['plugin://plugin.video.vrt.nu/play/id/vualto_canvas_geo', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_id, video_id='vualto_canvas_geo'), 'plugin://plugin.video.vrt.nu/play/id/vualto_canvas_geo')

    # Play on demand by url = '/play/url/<vrtnuwebsite_url>'
    # Achterflap episode 8 available until 31/12/2025
    def test_play_on_demand_by_url_route(self):
        plugin.run(['plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtnu/a-z/achterflap/1/achterflap-s1a8/', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_url,
                                        video_url='https://www.vrt.be/vrtnu/a-z/achterflap/1/achterflap-s1a8/'),
                         'plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtnu/a-z/achterflap/1/achterflap-s1a8/')

    # Play livestream by url = '/play/url/<vrtnuwebsite_url>'
    # Canvas livestream
    def test_play_livestream_by_url_route(self):
        plugin.run(['plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtnu/kanalen/canvas/', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_url,
                                        video_url='https://www.vrt.be/vrtnu/kanalen/canvas/'),
                         'plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtnu/kanalen/canvas/')

    # Play last episode method = '/play/lastepisode/<program>'
    def test_play_lastepisode_route(self):
        plugin.run(['plugin://plugin.video.vrt.nu/play/lastepisode/het-journaal', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_last, program='het-journaal'), 'plugin://plugin.video.vrt.nu/play/lastepisode/het-journaal')


if __name__ == '__main__':
    unittest.main()
