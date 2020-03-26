# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Integration tests for Routing functionality"""

# pylint: disable=invalid-name

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
    """TestCase class"""

    def test_main_menu(self):
        """Main menu: /"""
        addon.run(['plugin://plugin.video.vrt.nu/', '0', ''])
        self.assertEqual(plugin.url_for(addon.main_menu), 'plugin://plugin.video.vrt.nu/')

    def test_noop(self):
        """No operation: /noop"""
        addon.run(['plugin://plugin.video.vrt.nu/noop', '0', ''])
        self.assertEqual(plugin.url_for(addon.noop), 'plugin://plugin.video.vrt.nu/noop')

    def test_favorites(self):
        """Favorites menu: /favorites"""
        addon.run(['plugin://plugin.video.vrt.nu/favorites', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/favorites/programs', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/favorites/recent', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/favorites/recent/2', '0', ''])
        self.assertEqual(plugin.url_for(addon.favorites_recent, page=2), 'plugin://plugin.video.vrt.nu/favorites/recent/2')
        addon.run(['plugin://plugin.video.vrt.nu/favorites/offline', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/resumepoints/watchlater', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/resumepoints/continue', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/favorites/docu', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/favorites/music', '0', ''])

    def test_az_menu(self):
        """Programs menu: /programs"""
        addon.run(['plugin://plugin.video.vrt.nu/programs', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs), 'plugin://plugin.video.vrt.nu/programs')

    def test_episodes_menu(self):
        """Episodes menu: /programs/<program>"""
        addon.run(['plugin://plugin.video.vrt.nu/programs/thuis', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs, program='thuis'), 'plugin://plugin.video.vrt.nu/programs/thuis')
        addon.run(['plugin://plugin.video.vrt.nu/programs/pano/2019', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs, program='pano', season='2019'), 'plugin://plugin.video.vrt.nu/programs/pano/2019')
        addon.run(['plugin://plugin.video.vrt.nu/programs/pano/allseasons', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs, program='pano', season='allseasons'), 'plugin://plugin.video.vrt.nu/programs/pano/allseasons')

    def test_categories_menu(self):
        """Categories menu: /categories"""
        addon.run(['plugin://plugin.video.vrt.nu/categories', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories), 'plugin://plugin.video.vrt.nu/categories')

    def test_categories_tvshow_menu(self):
        """Categories programs menu: /categories/<category>"""
        addon.run(['plugin://plugin.video.vrt.nu/categories/docu', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories, category='docu'), 'plugin://plugin.video.vrt.nu/categories/docu')
        addon.run(['plugin://plugin.video.vrt.nu/categories/voor-kinderen', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories, category='voor-kinderen'), 'plugin://plugin.video.vrt.nu/categories/voor-kinderen')

    def test_featured_menu(self):
        """Featured menu: /featured"""
        addon.run(['plugin://plugin.video.vrt.nu/featured', '0', ''])
        self.assertEqual(plugin.url_for(addon.featured), 'plugin://plugin.video.vrt.nu/featured')

    def test_featured_tvshow_menu(self):
        """Featured programs menu: /featured/<cfeatured>"""
        addon.run(['plugin://plugin.video.vrt.nu/featured/kortfilm', '0', ''])
        self.assertEqual(plugin.url_for(addon.featured, feature='kortfilm'), 'plugin://plugin.video.vrt.nu/featured/kortfilm')

    def test_channels_menu(self):
        """Channels menu = /channels/<channel>"""
        addon.run(['plugin://plugin.video.vrt.nu/channels', '0', ''])
        self.assertEqual(plugin.url_for(addon.channels), 'plugin://plugin.video.vrt.nu/channels')
        addon.run(['plugin://plugin.video.vrt.nu/channels/ketnet', '0', ''])
        self.assertEqual(plugin.url_for(addon.channels, channel='ketnet'), 'plugin://plugin.video.vrt.nu/channels/ketnet')

    def test_livetv_menu(self):
        """Live TV menu: /livetv"""
        addon.run(['plugin://plugin.video.vrt.nu/livetv', '0', ''])
        self.assertEqual(plugin.url_for(addon.livetv), 'plugin://plugin.video.vrt.nu/livetv')

    def test_recent_menu(self):
        """Most recent menu: /recent/<page>"""
        addon.run(['plugin://plugin.video.vrt.nu/recent', '0', ''])
        self.assertEqual(plugin.url_for(addon.recent), 'plugin://plugin.video.vrt.nu/recent')
        addon.run(['plugin://plugin.video.vrt.nu/recent/2', '0', ''])
        self.assertEqual(plugin.url_for(addon.recent, page=2), 'plugin://plugin.video.vrt.nu/recent/2')

    def test_offline_menu(self):
        """Soon offline menu: /offline/<page>"""
        addon.run(['plugin://plugin.video.vrt.nu/offline', '0', ''])
        self.assertEqual(plugin.url_for(addon.offline), 'plugin://plugin.video.vrt.nu/offline')

    def test_tvguide_date_menu(self):
        """TV guide menu: /tvguide/<date>/<channel>"""
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

    def test_search_history(self):
        """Add search keyword: /search/add/<keywords>
            Clear search history: /search/clear
            Remove search keyword: /search/remove/<keywords>"""
        addon.run(['plugin://plugin.video.vrt.nu/search/add/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.add_search, keywords='foobar'), 'plugin://plugin.video.vrt.nu/search/add/foobar')
        addon.run(['plugin://plugin.video.vrt.nu/search/add/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.add_search, keywords='foobar'), 'plugin://plugin.video.vrt.nu/search/add/foobar')
        addon.run(['plugin://plugin.video.vrt.nu/search/query/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.add_search, keywords='foobar'), 'plugin://plugin.video.vrt.nu/search/add/foobar')
        addon.run(['plugin://plugin.video.vrt.nu/search/edit', '0', ''])
        self.assertEqual(plugin.url_for(addon.edit_search), 'plugin://plugin.video.vrt.nu/search/edit')
        addon.run(['plugin://plugin.video.vrt.nu/search/edit/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.edit_search, keywords='foobar'), 'plugin://plugin.video.vrt.nu/search/edit/foobar')
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

    def test_search_menu(self):
        """Search VRT NU menu: /search/query/<keywords>/<page>"""
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

    def test_follow_route(self):
        """Follow method: /follow/<program>/<title>"""
        addon.run(['plugin://plugin.video.vrt.nu/follow/thuis/Thuis', '0', ''])
        self.assertEqual(plugin.url_for(addon.follow, program='thuis', title='Thuis'), 'plugin://plugin.video.vrt.nu/follow/thuis/Thuis')

    def test_unfollow_route(self):
        """Unfollow method: /unfollow/<program>/<title>"""
        addon.run(['plugin://plugin.video.vrt.nu/unfollow/thuis/Thuis', '0', ''])
        self.assertEqual(plugin.url_for(addon.unfollow, program='thuis', title='Thuis'), 'plugin://plugin.video.vrt.nu/unfollow/thuis/Thuis')

    def test_clear_cookies_route(self):
        """Delete tokens method: /tokens/delete"""
        addon.run(['plugin://plugin.video.vrt.nu/tokens/delete', '0', ''])
        self.assertEqual(plugin.url_for(addon.delete_tokens), 'plugin://plugin.video.vrt.nu/tokens/delete')

    def test_invalidate_caches_route(self):
        """Delete cache method: /cache/delete"""
        addon.run(['plugin://plugin.video.vrt.nu/cache/delete', '0', ''])
        self.assertEqual(plugin.url_for(addon.delete_cache), 'plugin://plugin.video.vrt.nu/cache/delete')

    def test_refresh_favorites_route(self):
        """Refresh favorites method: /favorites/refresh"""
        addon.run(['plugin://plugin.video.vrt.nu/favorites/refresh', '0', ''])
        self.assertEqual(plugin.url_for(addon.favorites_refresh), 'plugin://plugin.video.vrt.nu/favorites/refresh')

    def test_refresh_resumepoints_route(self):
        """Refresh resumepoints method: /resumepoints/refresh"""
        addon.run(['plugin://plugin.video.vrt.nu/resumepoints/refresh', '0', ''])
        self.assertEqual(plugin.url_for(addon.resumepoints_refresh), 'plugin://plugin.video.vrt.nu/resumepoints/refresh')

    def test_manage_favorites_route(self):
        """Manage favorites method: /favorites/manage"""
        addon.run(['plugin://plugin.video.vrt.nu/favorites/manage', '0', ''])
        self.assertEqual(plugin.url_for(addon.favorites_manage), 'plugin://plugin.video.vrt.nu/favorites/manage')

    def test_watchlater_route(self):
        """Watch and unwatch later method: plugin://plugin.video.vrt.nu/watchlater/<url>/<asset_id>/<title>"""

        # Watchlater Winteruur met Lize Feryn (beschikbaar tot 26 maart 2025)
        addon.run(['plugin://plugin.video.vrt.nu/watchlater//vrtnu/a-z/winteruur/5/winteruur-s5a1//contentdamvrt20191015winteruurr005a0001depotwp00162177/Winteruur', '0', ''])
        self.assertEqual(plugin.url_for(addon.watchlater, url='/vrtnu/a-z/winteruur/5/winteruur-s5a1', asset_id='/contentdamvrt20191015winteruurr005a0001depotwp00162177', title='Winteruur'), 'plugin://plugin.video.vrt.nu/watchlater//vrtnu/a-z/winteruur/5/winteruur-s5a1//contentdamvrt20191015winteruurr005a0001depotwp00162177/Winteruur')

        # Unwatchlater Winteruur met Lize Feryn (beschikbaar tot 26 maart 2025)
        addon.run(['plugin://plugin.video.vrt.nu/unwatchlater//vrtnu/a-z/winteruur/5/winteruur-s5a1//contentdamvrt20191015winteruurr005a0001depotwp00162177/Winteruur', '0', ''])
        self.assertEqual(plugin.url_for(addon.unwatchlater, url='/vrtnu/a-z/winteruur/5/winteruur-s5a1', asset_id='/contentdamvrt20191015winteruurr005a0001depotwp00162177', title='Winteruur'), 'plugin://plugin.video.vrt.nu/unwatchlater//vrtnu/a-z/winteruur/5/winteruur-s5a1//contentdamvrt20191015winteruurr005a0001depotwp00162177/Winteruur')

    def test_play_on_demand_by_id_route(self):
        """Play on demand by id: /play/id/<publication_id>/<video_id>"""
        # Achterflap episode 8 available until 31/12/2025
        addon.run(['plugin://plugin.video.vrt.nu/play/id/vid-f80fa527-6759-45a7-908d-ec6f0a7b164e/pbs-pub-1a170972-dea3-4ea3-8c27-62d2442ee8a3', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_id,
                                        video_id='vid-f80fa527-6759-45a7-908d-ec6f0a7b164e',
                                        publication_id='pbs-pub-1a170972-dea3-4ea3-8c27-62d2442ee8a3'),
                         'plugin://plugin.video.vrt.nu/play/id/vid-f80fa527-6759-45a7-908d-ec6f0a7b164e/pbs-pub-1a170972-dea3-4ea3-8c27-62d2442ee8a3')

    def test_play_livestream_by_id_route(self):
        """Play livestream by id: /play/id/<video_id>"""
        # Canvas livestream
        addon.run(['plugin://plugin.video.vrt.nu/play/id/vualto_canvas_geo', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_id, video_id='vualto_canvas_geo'), 'plugin://plugin.video.vrt.nu/play/id/vualto_canvas_geo')

    def test_play_on_demand_by_url_route(self):
        """Play on demand by url: /play/url/<vrtnuwebsite_url>"""
        # Achterflap episode 8 available until 31/12/2025
        addon.run(['plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtnu/a-z/achterflap/1/achterflap-s1a8/', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_url,
                                        video_url='https://www.vrt.be/vrtnu/a-z/achterflap/1/achterflap-s1a8/'),
                         'plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtnu/a-z/achterflap/1/achterflap-s1a8/')

    def test_play_livestream_by_url_route(self):
        """Play livestream by url: /play/url/<vrtnuwebsite_url>"""
        # Canvas livestream
        addon.run(['plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtnu/kanalen/canvas/', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_url,
                                        video_url='https://www.vrt.be/vrtnu/kanalen/canvas/'),
                         'plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtnu/kanalen/canvas/')

    def test_play_latestepisode_route(self):
        """Play last episode method: /play/lastepisode/<program>"""
        addon.run(['plugin://plugin.video.vrt.nu/play/latest/het-journaal', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_latest, program='het-journaal'), 'plugin://plugin.video.vrt.nu/play/latest/het-journaal')
        addon.run(['plugin://plugin.video.vrt.nu/play/latest/terzake', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_latest, program='terzake'), 'plugin://plugin.video.vrt.nu/play/latest/terzake')
        addon.run(['plugin://plugin.video.vrt.nu/play/latest/winteruur', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_latest, program='winteruur'), 'plugin://plugin.video.vrt.nu/play/latest/winteruur')

    def test_play_airdateepisode_route(self):
        """Play episode by air date method: /play/airdate/<channel>/<start_date>"""
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

    def test_play_upnext_route(self):
        """Play Up Next episode method: /play/upnext/<video_id>"""
        addon.run(['plugin://plugin.video.vrt.nu/play/upnext/vid-a39ab219-9598-4a79-b676-98b724cceff1', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_upnext, video_id='vid-a39ab219-9598-4a79-b676-98b724cceff1'), 'plugin://plugin.video.vrt.nu/play/upnext/vid-a39ab219-9598-4a79-b676-98b724cceff1')


if __name__ == '__main__':
    unittest.main()
