# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=invalid-name,missing-docstring

from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime, timedelta
import unittest
import dateutil.tz
import addon


xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

plugin = addon.plugin
now = datetime.now(dateutil.tz.tzlocal())
lastweek = now + timedelta(days=-7)


class TestRouting(unittest.TestCase):

    def test_main_menu(self):
        addon.run(['plugin://plugin.video.vrt.nu/', '0', ''])
        self.assertEqual(plugin.url_for(addon.main_menu), 'plugin://plugin.video.vrt.nu/')

    # Favorites menu: '/favorites'
    def test_favorites(self):
        addon.run(['plugin://plugin.video.vrt.nu/favorites', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/favorites/programs', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/favorites/recent', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/favorites/recent/2', '0', ''])
        self.assertEqual(plugin.url_for(addon.favorites_recent, page=2), 'plugin://plugin.video.vrt.nu/favorites/recent/2')
        addon.run(['plugin://plugin.video.vrt.nu/favorites/offline', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/resumepoints/watchlater', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/resumepoints/continue', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/favorites/docu', '0', ''])

    # A-Z menu: '/programs'
    def test_az_menu(self):
        addon.run(['plugin://plugin.video.vrt.nu/programs', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs), 'plugin://plugin.video.vrt.nu/programs')

    # Episodes menu: '/programs/<program>'
    def test_episodes_menu(self):
        addon.run(['plugin://plugin.video.vrt.nu/programs/thuis', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs, program='thuis'), 'plugin://plugin.video.vrt.nu/programs/thuis')
        addon.run(['plugin://plugin.video.vrt.nu/programs/pano/allseasons', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs, program='pano', season='allseasons'), 'plugin://plugin.video.vrt.nu/programs/pano/allseasons')

    # Categories menu: '/categories'
    def test_categories_menu(self):
        addon.run(['plugin://plugin.video.vrt.nu/categories', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories), 'plugin://plugin.video.vrt.nu/categories')

    # Categories programs menu: '/categories/<category>'
    def test_categories_tvshow_menu(self):
        addon.run(['plugin://plugin.video.vrt.nu/categories/docu', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories, category='docu'), 'plugin://plugin.video.vrt.nu/categories/docu')
        addon.run(['plugin://plugin.video.vrt.nu/categories/voor-kinderen', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories, category='voor-kinderen'), 'plugin://plugin.video.vrt.nu/categories/voor-kinderen')

    # Featured menu: '/featured'
    def test_featured_menu(self):
        addon.run(['plugin://plugin.video.vrt.nu/featured', '0', ''])
        self.assertEqual(plugin.url_for(addon.featured), 'plugin://plugin.video.vrt.nu/featured')

    # Featured programs menu: '/featured/<cfeatured>'
    def test_featured_tvshow_menu(self):
        addon.run(['plugin://plugin.video.vrt.nu/featured/kortfilm', '0', ''])
        self.assertEqual(plugin.url_for(addon.featured, feature='kortfilm'), 'plugin://plugin.video.vrt.nu/featured/kortfilm')

    # Channels menu = '/channels/<channel>'
    def test_channels_menu(self):
        addon.run(['plugin://plugin.video.vrt.nu/channels', '0', ''])
        self.assertEqual(plugin.url_for(addon.channels), 'plugin://plugin.video.vrt.nu/channels')
        addon.run(['plugin://plugin.video.vrt.nu/channels/ketnet', '0', ''])
        self.assertEqual(plugin.url_for(addon.channels, channel='ketnet'), 'plugin://plugin.video.vrt.nu/channels/ketnet')

    # Live TV menu: '/livetv'
    def test_livetv_menu(self):
        addon.run(['plugin://plugin.video.vrt.nu/livetv', '0', ''])
        self.assertEqual(plugin.url_for(addon.livetv), 'plugin://plugin.video.vrt.nu/livetv')

    # Most recent menu: '/recent/<page>'
    def test_recent_menu(self):
        addon.run(['plugin://plugin.video.vrt.nu/recent', '0', ''])
        self.assertEqual(plugin.url_for(addon.recent), 'plugin://plugin.video.vrt.nu/recent')
        addon.run(['plugin://plugin.video.vrt.nu/recent/2', '0', ''])
        self.assertEqual(plugin.url_for(addon.recent, page=2), 'plugin://plugin.video.vrt.nu/recent/2')

    # Soon offline menu: '/offline/<page>'
    def test_offline_menu(self):
        addon.run(['plugin://plugin.video.vrt.nu/offline', '0', ''])
        self.assertEqual(plugin.url_for(addon.offline), 'plugin://plugin.video.vrt.nu/offline')

    # TV guide menu: '/tvguide/<date>/<channel>'
    def test_tvguide_date_menu(self):
        addon.run(['plugin://plugin.video.vrt.nu/tvguide', '0', ''])
        self.assertEqual(plugin.url_for(addon.tvguide), 'plugin://plugin.video.vrt.nu/tvguide/date')
        addon.run(['plugin://plugin.video.vrt.nu/tvguide/date/today', '0', ''])
        self.assertEqual(plugin.url_for(addon.tvguide, date='today'), 'plugin://plugin.video.vrt.nu/tvguide/date/today')
        addon.run(['plugin://plugin.video.vrt.nu/tvguide/date/today/canvas', '0', ''])
        self.assertEqual(plugin.url_for(addon.tvguide, date='today', channel='canvas'), 'plugin://plugin.video.vrt.nu/tvguide/date/today/canvas')
        addon.run(['plugin://plugin.video.vrt.nu/tvguide/channel/canvas', '0', ''])
        self.assertEqual(plugin.url_for(addon.tvguide_channel, channel='canvas'), 'plugin://plugin.video.vrt.nu/tvguide/channel/canvas')
        addon.run(['plugin://plugin.video.vrt.nu/tvguide/channel/canvas/today', '0', ''])
        self.assertEqual(plugin.url_for(addon.tvguide_channel, channel='canvas', date='today'), 'plugin://plugin.video.vrt.nu/tvguide/channel/canvas/today')

    # Clear search history: '/search/clear'
    # Add search keyword: '/search/add/<keywords>'
    # Remove search keyword: '/search/remove/<keywords>'
    def test_search_history(self):
        addon.run(['plugin://plugin.video.vrt.nu/search/add/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.add_search, keywords='foobar'), 'plugin://plugin.video.vrt.nu/search/add/foobar')
        addon.run(['plugin://plugin.video.vrt.nu/search/add/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.add_search, keywords='foobar'), 'plugin://plugin.video.vrt.nu/search/add/foobar')
        addon.run(['plugin://plugin.video.vrt.nu/search/query/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.add_search, keywords='foobar'), 'plugin://plugin.video.vrt.nu/search/add/foobar')
        addon.run(['plugin://plugin.video.vrt.nu/search/remove/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.remove_search, keywords='foobar'), 'plugin://plugin.video.vrt.nu/search/remove/foobar')
        addon.run(['plugin://plugin.video.vrt.nu/search/remove/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.remove_search, keywords='foobar'), 'plugin://plugin.video.vrt.nu/search/remove/foobar')
        addon.run(['plugin://plugin.video.vrt.nu/search/clear', '0', ''])
        self.assertEqual(plugin.url_for(addon.clear_search), 'plugin://plugin.video.vrt.nu/search/clear')
        addon.run(['plugin://plugin.video.vrt.nu/search', '0', ''])
        self.assertEqual(plugin.url_for(addon.search), 'plugin://plugin.video.vrt.nu/search')
        addon.run(['plugin://plugin.video.vrt.nu/search/add/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.add_search, keywords='foobar'), 'plugin://plugin.video.vrt.nu/search/add/foobar')

    # Search VRT NU menu: '/search/query/<keywords>/<page>'
    def test_search_menu(self):
        addon.run(['plugin://plugin.video.vrt.nu/search', '0', ''])
        self.assertEqual(plugin.url_for(addon.search), 'plugin://plugin.video.vrt.nu/search')
        addon.run(['plugin://plugin.video.vrt.nu/search/query', '0', ''])
        self.assertEqual(plugin.url_for(addon.search_query), 'plugin://plugin.video.vrt.nu/search/query')
        addon.run(['plugin://plugin.video.vrt.nu/search/query/dag', '0', ''])
        self.assertEqual(plugin.url_for(addon.search_query, keywords='dag'), 'plugin://plugin.video.vrt.nu/search/query/dag')
        addon.run(['plugin://plugin.video.vrt.nu/search/query/dag/2', '0', ''])
        self.assertEqual(plugin.url_for(addon.search_query, keywords='dag', page=2), 'plugin://plugin.video.vrt.nu/search/query/dag/2')
        addon.run(['plugin://plugin.video.vrt.nu/search/query/winter', '0', ''])
        self.assertEqual(plugin.url_for(addon.search_query, keywords='winter'), 'plugin://plugin.video.vrt.nu/search/query/winter')

    # Follow method: '/follow/<program>/<title>'
    def test_follow_route(self):
        addon.run(['plugin://plugin.video.vrt.nu/follow/thuis/Thuis', '0', ''])
        self.assertEqual(plugin.url_for(addon.follow, program='thuis', title='Thuis'), 'plugin://plugin.video.vrt.nu/follow/thuis/Thuis')

    # Unfollow method: '/unfollow/<program>/<title>'
    def test_unfollow_route(self):
        addon.run(['plugin://plugin.video.vrt.nu/unfollow/thuis/Thuis', '0', ''])
        self.assertEqual(plugin.url_for(addon.unfollow, program='thuis', title='Thuis'), 'plugin://plugin.video.vrt.nu/unfollow/thuis/Thuis')

    # Delete tokens method: '/tokens/delete'
    def test_clear_cookies_route(self):
        addon.run(['plugin://plugin.video.vrt.nu/tokens/delete', '0', ''])
        self.assertEqual(plugin.url_for(addon.delete_tokens), 'plugin://plugin.video.vrt.nu/tokens/delete')

    # Delete cache method: '/cache/delete'
    def test_invalidate_caches_route(self):
        addon.run(['plugin://plugin.video.vrt.nu/cache/delete', '0', ''])
        self.assertEqual(plugin.url_for(addon.delete_cache), 'plugin://plugin.video.vrt.nu/cache/delete')

    # Refresh favorites method: '/favorites/refresh'
    def test_refresh_favorites_route(self):
        addon.run(['plugin://plugin.video.vrt.nu/favorites/refresh', '0', ''])
        self.assertEqual(plugin.url_for(addon.favorites_refresh), 'plugin://plugin.video.vrt.nu/favorites/refresh')

    # Refresh resumepoints method: '/resumepoints/refresh'
    def test_refresh_resumepoints_route(self):
        addon.run(['plugin://plugin.video.vrt.nu/resumepoints/refresh', '0', ''])
        self.assertEqual(plugin.url_for(addon.resumepoints_refresh), 'plugin://plugin.video.vrt.nu/resumepoints/refresh')

    # Manage favorites method: '/favorites/manage'
    def test_manage_favorites_route(self):
        addon.run(['plugin://plugin.video.vrt.nu/favorites/manage', '0', ''])
        self.assertEqual(plugin.url_for(addon.favorites_manage), 'plugin://plugin.video.vrt.nu/favorites/manage')

    # Watch later method: 'plugin://plugin.video.vrt.nu/watchlater/<url>/<uuid>/<title>'
    def test_watchlater_route(self):
        addon.run(['plugin://plugin.video.vrt.nu/watchlater//vrtnu/a-z/winteruur/5/winteruur-s5a1//contentdamvrt20191015winteruurr005a0001depotwp00162177/Winteruur', '0', ''])
        self.assertEqual(plugin.url_for(addon.watchlater, url='/vrtnu/a-z/winteruur/5/winteruur-s5a1', uuid='/contentdamvrt20191015winteruurr005a0001depotwp00162177', title='Winteruur'), 'plugin://plugin.video.vrt.nu/watchlater//vrtnu/a-z/winteruur/5/winteruur-s5a1//contentdamvrt20191015winteruurr005a0001depotwp00162177/Winteruur')

    # Unwatch later method: 'plugin://plugin.video.vrt.nu/unwatchlater/<url>/<uuid>/<title>'
    def test_unwatchlater_route(self):
        addon.run(['plugin://plugin.video.vrt.nu/unwatchlater//vrtnu/a-z/winteruur/5/winteruur-s5a1//contentdamvrt20191015winteruurr005a0001depotwp00162177/Winteruur', '0', ''])
        self.assertEqual(plugin.url_for(addon.unwatchlater, url='/vrtnu/a-z/winteruur/5/winteruur-s5a1', uuid='/contentdamvrt20191015winteruurr005a0001depotwp00162177', title='Winteruur'), 'plugin://plugin.video.vrt.nu/unwatchlater//vrtnu/a-z/winteruur/5/winteruur-s5a1//contentdamvrt20191015winteruurr005a0001depotwp00162177/Winteruur')

    # Play on demand by id = '/play/id/<publication_id>/<video_id>'
    # Achterflap episode 8 available until 31/12/2025
    def test_play_on_demand_by_id_route(self):
        addon.run(['plugin://plugin.video.vrt.nu/play/id/vid-f80fa527-6759-45a7-908d-ec6f0a7b164e/pbs-pub-1a170972-dea3-4ea3-8c27-62d2442ee8a3', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_id,
                                        video_id='vid-f80fa527-6759-45a7-908d-ec6f0a7b164e',
                                        publication_id='pbs-pub-1a170972-dea3-4ea3-8c27-62d2442ee8a3'),
                         'plugin://plugin.video.vrt.nu/play/id/vid-f80fa527-6759-45a7-908d-ec6f0a7b164e/pbs-pub-1a170972-dea3-4ea3-8c27-62d2442ee8a3')

    # Play livestream by id = '/play/id/<video_id>'
    # Canvas livestream
    def test_play_livestream_by_id_route(self):
        addon.run(['plugin://plugin.video.vrt.nu/play/id/vualto_canvas_geo', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_id, video_id='vualto_canvas_geo'), 'plugin://plugin.video.vrt.nu/play/id/vualto_canvas_geo')

    # Play on demand by url = '/play/url/<vrtnuwebsite_url>'
    # Achterflap episode 8 available until 31/12/2025
    def test_play_on_demand_by_url_route(self):
        addon.run(['plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtnu/a-z/achterflap/1/achterflap-s1a8/', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_url,
                                        video_url='https://www.vrt.be/vrtnu/a-z/achterflap/1/achterflap-s1a8/'),
                         'plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtnu/a-z/achterflap/1/achterflap-s1a8/')

    # Play livestream by url = '/play/url/<vrtnuwebsite_url>'
    # Canvas livestream
    def test_play_livestream_by_url_route(self):
        addon.run(['plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtnu/kanalen/canvas/', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_url,
                                        video_url='https://www.vrt.be/vrtnu/kanalen/canvas/'),
                         'plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtnu/kanalen/canvas/')

    # Play last episode method = '/play/lastepisode/<program>'
    def test_play_latestepisode_route(self):
        addon.run(['plugin://plugin.video.vrt.nu/play/latest/het-journaal', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_latest, program='het-journaal'), 'plugin://plugin.video.vrt.nu/play/latest/het-journaal')
        addon.run(['plugin://plugin.video.vrt.nu/play/latest/terzake', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_latest, program='terzake'), 'plugin://plugin.video.vrt.nu/play/latest/terzake')
        addon.run(['plugin://plugin.video.vrt.nu/play/latest/winteruur', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_latest, program='winteruur'), 'plugin://plugin.video.vrt.nu/play/latest/winteruur')

    # Play episode by air date method = '/play/airdate/<channel>/<start_date>'
    def test_play_airdateepisode_route(self):
        # Test Het Journaal
        addon.run([lastweek.strftime('plugin://plugin.video.vrt.nu/play/airdate/een/%Y-%m-%dT19:00:00'), '0', ''])
        self.assertEqual(plugin.url_for(addon.play_by_air_date,
                                        channel='een',
                                        start_date=lastweek.strftime('%Y-%m-%dT19:00:00')),
                         lastweek.strftime('plugin://plugin.video.vrt.nu/play/airdate/een/%Y-%m-%dT19:00:00'))
        # Test TerZake
        addon.run([lastweek.strftime('plugin://plugin.video.vrt.nu/play/airdate/canvas/%Y-%m-%dT20:00:00'), '0', ''])
        self.assertEqual(plugin.url_for(addon.play_by_air_date,
                                        channel='canvas',
                                        start_date=lastweek.strftime('%Y-%m-%dT20:00:00')),
                         lastweek.strftime('plugin://plugin.video.vrt.nu/play/airdate/canvas/%Y-%m-%dT20:00:00'))

    # Play episode by whatsonid method = '/play/whatson/<whatson_id>'
    def test_play_whatsonid_route(self):
        addon.run(['plugin://plugin.video.vrt.nu/play/whatson/347056576527', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_whatson, whatson_id='347056576527'), 'plugin://plugin.video.vrt.nu/play/whatson/347056576527')


if __name__ == '__main__':
    unittest.main()
