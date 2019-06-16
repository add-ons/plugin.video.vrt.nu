# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=missing-docstring

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

from resources.lib import router

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')


class TestRouter(unittest.TestCase):

    def test_main_menu(self):
        router.router(['plugin://plugin.video.vrt.nu/', '0', ''])

    # Favorites menu: '/favorites'
    def test_favorites(self):
        router.router(['plugin://plugin.video.vrt.nu/favorites', '0', ''])
        router.router(['plugin://plugin.video.vrt.nu/favorites/programs', '0', ''])
        router.router(['plugin://plugin.video.vrt.nu/favorites/recent', '0', ''])
        router.router(['plugin://plugin.video.vrt.nu/favorites/recent/2', '0', ''])
        router.router(['plugin://plugin.video.vrt.nu/favorites/offline', '0', ''])

    # A-Z menu: '/programs'
    def test_az_menu(self):
        router.router(['plugin://plugin.video.vrt.nu/programs', '0', ''])

    # Episodes menu: '/programs/<program>'
    def test_episodes_menu(self):
        router.router(['plugin://plugin.video.vrt.nu/programs/thuis', '0', ''])
        router.router(['plugin://plugin.video.vrt.nu/programs/de-campus-cup', '0', ''])

    # Categories menu: '/categories'
    def test_categories_menu(self):
        router.router(['plugin://plugin.video.vrt.nu/categories', '0', ''])

    # Categories programs menu: '/categories/<category>'
    def test_categories_tvshow_menu(self):
        router.router(['plugin://plugin.video.vrt.nu/categories/docu', '0', ''])
        router.router(['plugin://plugin.video.vrt.nu/categories/kinderen', '0', ''])

    # Channels menu = '/channels/<channel>'
    def test_channels_menu(self):
        router.router(['plugin://plugin.video.vrt.nu/channels', '0', ''])
        router.router(['plugin://plugin.video.vrt.nu/ketnet', '0', ''])

    # Live TV menu: '/livetv'
    def test_livetv_menu(self):
        router.router(['plugin://plugin.video.vrt.nu/livetv', '0', ''])

    # Most recent menu: '/recent/<page>'
    def test_recent_menu(self):
        router.router(['plugin://plugin.video.vrt.nu/recent', '0', ''])
        router.router(['plugin://plugin.video.vrt.nu/recent/2', '0', ''])

    # Soon offline menu: '/offline/<page>'
    def test_offline_menu(self):
        router.router(['plugin://plugin.video.vrt.nu/offline', '0', ''])

    # TV guide menu: '/tvguide/<date>/<channel>'
    def test_tvguide_date_menu(self):
        router.router(['plugin://plugin.video.vrt.nu/tvguide', '0', ''])
        router.router(['plugin://plugin.video.vrt.nu/tvguide/today', '0', ''])
        router.router(['plugin://plugin.video.vrt.nu/tvguide/today/canvas', '0', ''])

    # Search VRT NU menu: '/search/<search_string>/<page>'
    def test_search_menu(self):
        router.router(['plugin://plugin.video.vrt.nu/search', '0', ''])
        router.router(['plugin://plugin.video.vrt.nu/search/dag', '0', ''])
        router.router(['plugin://plugin.video.vrt.nu/search/dag/2', '0', ''])

    # Follow method: '/follow/<program_title>/<program>'
    def test_follow_router(self):
        router.router(['plugin://plugin.video.vrt.nu/follow/Thuis/thuis', '0', ''])

    # Unfollow method: '/unfollow/<program_title>/<program>'
    def test_unfollow_router(self):
        router.router(['plugin://plugin.video.vrt.nu/unfollow/Thuis/thuis', '0', ''])

    # Delete tokens method: '/tokens/delete'
    def test_clear_cookies_router(self):
        router.router(['plugin://plugin.video.vrt.nu/tokens/delete', '0', ''])

    # Delete cache method: '/cache/delete'
    def test_invalidate_caches_router(self):
        router.router(['plugin://plugin.video.vrt.nu/cache/delete', '0', ''])

    # Refresh favorites method: '/favorites/refresh'
    def test_refresh_favorites_router(self):
        router.router(['plugin://plugin.video.vrt.nu/favorites/refresh', '0', ''])

    # Play on demand by id = '/play/id/<publication_id>/<video_id>'
    # Achterflap episode 8 available until 31/12/2025
    def test_play_on_demand_by_id_router(self):
        router.router(['plugin://plugin.video.vrt.nu/play/id/pbs-pub-1a170972-dea3-4ea3-8c27-62d2442ee8a3/vid-f80fa527-6759-45a7-908d-ec6f0a7b164e', '0', ''])

    # Play livestream by id = '/play/id/<video_id>'
    # Canvas livestream
    def test_play_livestream_by_id_router(self):
        router.router(['plugin://plugin.video.vrt.nu/play/id/vualto_canvas_geo', '0', ''])

    # Play on demand by url = '/play/url/<vrtnuwebsite_url>'
    # Achterflap episode 8 available until 31/12/2025
    def test_play_on_demand_by_url_router(self):
        router.router(['plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtnu/a-z/achterflap/1/achterflap-s1a8/', '0', ''])

    # Play livestream by url = '/play/url/<vrtnuwebsite_url>'
    # Canvas livestream
    def test_play_livestream_by_url_router(self):
        router.router(['plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtnu/kanalen/canvas/', '0', ''])

    # Play last episode method = '/play/lastepisode/<program>'
    def test_play_lastepisode_router(self):
        router.router(['plugin://plugin.video.vrt.nu/play/lastepisode/het-journaal', '0', ''])


if __name__ == '__main__':
    unittest.main()
