# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Integration tests for Routing functionality"""

# pylint: disable=invalid-name,line-too-long

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
        addon.run(['plugin://plugin.video.vrtmax/', '0', ''])
        self.assertEqual(plugin.url_for(addon.main_menu), 'plugin://plugin.video.vrtmax/')

    def test_noop(self):
        """No operation: /noop"""
        addon.run(['plugin://plugin.video.vrtmax/noop', '0', ''])
        self.assertEqual(plugin.url_for(addon.noop), 'plugin://plugin.video.vrtmax/noop')

    def test_favorites(self):
        """Favorites menu: /favorites"""
        addon.run(['plugin://plugin.video.vrtmax/favorites', '0', ''])
        addon.run(['plugin://plugin.video.vrtmax/favorites/programs', '0', ''])
        addon.run(['plugin://plugin.video.vrtmax/favorites/recent', '0', ''])
        addon.run(['plugin://plugin.video.vrtmax/favorites/recent/2', '0', ''])
        self.assertEqual(plugin.url_for(addon.favorites_recent, page=2), 'plugin://plugin.video.vrtmax/favorites/recent/2')
        addon.run(['plugin://plugin.video.vrtmax/favorites/offline', '0', ''])
        addon.run(['plugin://plugin.video.vrtmax/resumepoints/watchlater', '0', ''])
        addon.run(['plugin://plugin.video.vrtmax/resumepoints/continue', '0', ''])
        addon.run(['plugin://plugin.video.vrtmax/favorites/docu', '0', ''])
        addon.run(['plugin://plugin.video.vrtmax/favorites/music', '0', ''])

    def test_az_menu(self):
        """Programs menu: /programs"""
        addon.run(['plugin://plugin.video.vrtmax/programs', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs), 'plugin://plugin.video.vrtmax/programs')

    def test_episodes_menu(self):
        """Episodes menu: /programs/<program>"""
        addon.run(['plugin://plugin.video.vrtmax/programs/thuis', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs, program='thuis'), 'plugin://plugin.video.vrtmax/programs/thuis')
        addon.run(['plugin://plugin.video.vrtmax/programs/pano/2019', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs, program='pano', season='2019'), 'plugin://plugin.video.vrtmax/programs/pano/2019')
        addon.run(['plugin://plugin.video.vrtmax/programs/pano/allseasons', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs, program='pano', season='allseasons'), 'plugin://plugin.video.vrtmax/programs/pano/allseasons')

    def test_categories_menu(self):
        """Categories menu: /categories"""
        addon.run(['plugin://plugin.video.vrtmax/categories', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories), 'plugin://plugin.video.vrtmax/categories')

    def test_categories_tvshow_menu(self):
        """Categories programs menu: /categories/<category>"""
        addon.run(['plugin://plugin.video.vrtmax/categories/docu', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories, category='docu'), 'plugin://plugin.video.vrtmax/categories/docu')
        addon.run(['plugin://plugin.video.vrtmax/categories/voor-kinderen', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories, category='voor-kinderen'), 'plugin://plugin.video.vrtmax/categories/voor-kinderen')

    def test_featured_menu(self):
        """Featured menu: /featured"""
        addon.run(['plugin://plugin.video.vrtmax/featured', '0', ''])
        self.assertEqual(plugin.url_for(addon.featured), 'plugin://plugin.video.vrtmax/featured')

    def test_featured_tvshow_menu(self):
        """Featured programs menu: /featured/<cfeatured>"""
        addon.run(['plugin://plugin.video.vrtmax/featured/kortfilm', '0', ''])
        self.assertEqual(plugin.url_for(addon.featured, feature='kortfilm'), 'plugin://plugin.video.vrtmax/featured/kortfilm')

    def test_featured_episode_menu(self):
        """Featured episodes menu: /featured/<cfeatured>"""
        addon.run(['plugin://plugin.video.vrtmax/featured/jcr_list', '0', ''])
        self.assertEqual(plugin.url_for(addon.featured, feature='jcr_list'), 'plugin://plugin.video.vrtmax/featured/jcr_list')

    def test_channels_menu(self):
        """Channels menu = /channels/<channel>"""
        addon.run(['plugin://plugin.video.vrtmax/channels', '0', ''])
        self.assertEqual(plugin.url_for(addon.channels), 'plugin://plugin.video.vrtmax/channels')
        addon.run(['plugin://plugin.video.vrtmax/channels/ketnet', '0', ''])
        self.assertEqual(plugin.url_for(addon.channels, channel='ketnet'), 'plugin://plugin.video.vrtmax/channels/ketnet')

    def test_livetv_menu(self):
        """Live TV menu: /livetv"""
        addon.run(['plugin://plugin.video.vrtmax/livetv', '0', ''])
        self.assertEqual(plugin.url_for(addon.livetv), 'plugin://plugin.video.vrtmax/livetv')

    def test_recent_menu(self):
        """Most recent menu: /recent/<page>"""
        addon.run(['plugin://plugin.video.vrtmax/recent', '0', ''])
        self.assertEqual(plugin.url_for(addon.recent), 'plugin://plugin.video.vrtmax/recent')
        addon.run(['plugin://plugin.video.vrtmax/recent/2', '0', ''])
        self.assertEqual(plugin.url_for(addon.recent, page=2), 'plugin://plugin.video.vrtmax/recent/2')

    def test_offline_menu(self):
        """Soon offline menu: /offline/<page>"""
        addon.run(['plugin://plugin.video.vrtmax/offline', '0', ''])
        self.assertEqual(plugin.url_for(addon.offline), 'plugin://plugin.video.vrtmax/offline')

    def test_tvguide_date_menu(self):
        """TV guide menu: /tvguide/<date>/<channel>"""
        addon.run(['plugin://plugin.video.vrtmax/tvguide', '0', ''])
        self.assertEqual(plugin.url_for(addon.tvguide), 'plugin://plugin.video.vrtmax/tvguide/date')
        addon.run(['plugin://plugin.video.vrtmax/tvguide/date/today', '0', ''])
        self.assertEqual(plugin.url_for(addon.tvguide, date='today'), 'plugin://plugin.video.vrtmax/tvguide/date/today')
        addon.run(['plugin://plugin.video.vrtmax/tvguide/date/today/canvas', '0', ''])
        self.assertEqual(plugin.url_for(addon.tvguide, date='today', channel='canvas'), 'plugin://plugin.video.vrtmax/tvguide/date/today/canvas')
        addon.run(['plugin://plugin.video.vrtmax/tvguide/channel/canvas', '0', ''])
        self.assertEqual(plugin.url_for(addon.tvguide_channel, channel='canvas'), 'plugin://plugin.video.vrtmax/tvguide/channel/canvas')
        addon.run(['plugin://plugin.video.vrtmax/tvguide/channel/canvas/today', '0', ''])
        self.assertEqual(plugin.url_for(addon.tvguide_channel, channel='canvas', date='today'), 'plugin://plugin.video.vrtmax/tvguide/channel/canvas/today')

    def test_search_history(self):
        """Add search keyword: /search/add/<keywords>
            Clear search history: /search/clear
            Remove search keyword: /search/remove/<keywords>"""
        addon.run(['plugin://plugin.video.vrtmax/search/add/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.add_search, keywords='foobar'), 'plugin://plugin.video.vrtmax/search/add/foobar')
        addon.run(['plugin://plugin.video.vrtmax/search/add/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.add_search, keywords='foobar'), 'plugin://plugin.video.vrtmax/search/add/foobar')
        addon.run(['plugin://plugin.video.vrtmax/search/query/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.add_search, keywords='foobar'), 'plugin://plugin.video.vrtmax/search/add/foobar')
        addon.run(['plugin://plugin.video.vrtmax/search/edit', '0', ''])
        self.assertEqual(plugin.url_for(addon.edit_search), 'plugin://plugin.video.vrtmax/search/edit')
        addon.run(['plugin://plugin.video.vrtmax/search/edit/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.edit_search, keywords='foobar'), 'plugin://plugin.video.vrtmax/search/edit/foobar')
        addon.run(['plugin://plugin.video.vrtmax/search/remove/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.remove_search, keywords='foobar'), 'plugin://plugin.video.vrtmax/search/remove/foobar')
        addon.run(['plugin://plugin.video.vrtmax/search/remove/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.remove_search, keywords='foobar'), 'plugin://plugin.video.vrtmax/search/remove/foobar')
        addon.run(['plugin://plugin.video.vrtmax/search/clear', '0', ''])
        self.assertEqual(plugin.url_for(addon.clear_search), 'plugin://plugin.video.vrtmax/search/clear')
        addon.run(['plugin://plugin.video.vrtmax/search', '0', ''])
        self.assertEqual(plugin.url_for(addon.search), 'plugin://plugin.video.vrtmax/search')
        addon.run(['plugin://plugin.video.vrtmax/search/add/foobar', '0', ''])
        self.assertEqual(plugin.url_for(addon.add_search, keywords='foobar'), 'plugin://plugin.video.vrtmax/search/add/foobar')

    def test_search_menu(self):
        """Search VRT MAX menu: /search/query/<keywords>/<page>"""
        addon.run(['plugin://plugin.video.vrtmax/search', '0', ''])
        self.assertEqual(plugin.url_for(addon.search), 'plugin://plugin.video.vrtmax/search')
        addon.run(['plugin://plugin.video.vrtmax/search/query', '0', ''])
        self.assertEqual(plugin.url_for(addon.search_query), 'plugin://plugin.video.vrtmax/search/query')
        addon.run(['plugin://plugin.video.vrtmax/search/query/dag', '0', ''])
        self.assertEqual(plugin.url_for(addon.search_query, keywords='dag'), 'plugin://plugin.video.vrtmax/search/query/dag')
        addon.run(['plugin://plugin.video.vrtmax/search/query/dag/2', '0', ''])
        self.assertEqual(plugin.url_for(addon.search_query, keywords='dag', page=2), 'plugin://plugin.video.vrtmax/search/query/dag/2')
        addon.run(['plugin://plugin.video.vrtmax/search/query/winter', '0', ''])
        self.assertEqual(plugin.url_for(addon.search_query, keywords='winter'), 'plugin://plugin.video.vrtmax/search/query/winter')

    def test_follow_route(self):
        """Follow method: /follow/<program>/<title>"""
        addon.run(['plugin://plugin.video.vrtmax/follow/thuis/Thuis', '0', ''])
        self.assertEqual(plugin.url_for(addon.follow, program_name='thuis', title='Thuis'), 'plugin://plugin.video.vrtmax/follow/thuis/Thuis')

    def test_unfollow_route(self):
        """Unfollow method: /unfollow/<program>/<title>"""
        addon.run(['plugin://plugin.video.vrtmax/unfollow/thuis/Thuis', '0', ''])
        self.assertEqual(plugin.url_for(addon.unfollow, program_name='thuis', title='Thuis'), 'plugin://plugin.video.vrtmax/unfollow/thuis/Thuis')

    def test_clear_cookies_route(self):
        """Delete tokens method: /tokens/delete"""
        addon.run(['plugin://plugin.video.vrtmax/tokens/delete', '0', ''])
        self.assertEqual(plugin.url_for(addon.delete_tokens), 'plugin://plugin.video.vrtmax/tokens/delete')

    def test_invalidate_caches_route(self):
        """Delete cache method: /cache/delete"""
        addon.run(['plugin://plugin.video.vrtmax/cache/delete', '0', ''])
        self.assertEqual(plugin.url_for(addon.delete_cache), 'plugin://plugin.video.vrtmax/cache/delete')

    def test_refresh_favorites_route(self):
        """Refresh favorites method: /favorites/refresh"""
        addon.run(['plugin://plugin.video.vrtmax/favorites/refresh', '0', ''])
        self.assertEqual(plugin.url_for(addon.favorites_refresh), 'plugin://plugin.video.vrtmax/favorites/refresh')

    def test_refresh_resumepoints_route(self):
        """Refresh resumepoints method: /resumepoints/refresh"""
        addon.run(['plugin://plugin.video.vrtmax/resumepoints/refresh', '0', ''])
        self.assertEqual(plugin.url_for(addon.resumepoints_refresh), 'plugin://plugin.video.vrtmax/resumepoints/refresh')

    def test_manage_favorites_route(self):
        """Manage favorites method: /favorites/manage"""
        addon.run(['plugin://plugin.video.vrtmax/favorites/manage', '0', ''])
        self.assertEqual(plugin.url_for(addon.favorites_manage), 'plugin://plugin.video.vrtmax/favorites/manage')

    def test_watchlater_route(self):
        """Watch and unwatch later method: plugin://plugin.video.vrtmax/watchlater/<episode_id>/<title>"""

        # Watchlater Winteruur met Lize Feryn (beschikbaar tot 26 maart 2025)
        addon.run(['plugin://plugin.video.vrtmax/watchlater/1571140659165/Lize Feryn', '0', ''])
        self.assertEqual(plugin.url_for(addon.watchlater, episode_id='1571140659165', title='Lize Feryn'),
                         'plugin://plugin.video.vrtmax/watchlater/1571140659165/Lize Feryn')

        # Unwatchlater Winteruur met Lize Feryn (beschikbaar tot 26 maart 2025)
        addon.run(['plugin://plugin.video.vrtmax/unwatchlater/1571140659165/Lize Feryn', '0', ''])
        self.assertEqual(plugin.url_for(addon.unwatchlater, episode_id='1571140659165', title='Lize Feryn'),
                         'plugin://plugin.video.vrtmax/unwatchlater/1571140659165/Lize Feryn')

    def test_play_on_demand_by_id_route(self):
        """Play on demand by id: /play/id/<publication_id>/<video_id>"""
        # Achterflap episode 8 available until 31/12/2025
        addon.run(['plugin://plugin.video.vrtmax/play/id/vid-f80fa527-6759-45a7-908d-ec6f0a7b164e/pbs-pub-1a170972-dea3-4ea3-8c27-62d2442ee8a3', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_id,
                                        video_id='vid-f80fa527-6759-45a7-908d-ec6f0a7b164e',
                                        publication_id='pbs-pub-1a170972-dea3-4ea3-8c27-62d2442ee8a3'),
                         'plugin://plugin.video.vrtmax/play/id/vid-f80fa527-6759-45a7-908d-ec6f0a7b164e/pbs-pub-1a170972-dea3-4ea3-8c27-62d2442ee8a3')

    def test_play_livestream_by_id_route(self):
        """Play livestream by id: /play/id/<video_id>"""
        # Canvas livestream
        addon.run(['plugin://plugin.video.vrtmax/play/id/vualto_canvas_geo', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_id, video_id='vualto_canvas_geo'), 'plugin://plugin.video.vrtmax/play/id/vualto_canvas_geo')

    def test_play_on_demand_by_url_route(self):
        """Play on demand by url: /play/url/<vrtmaxwebsite_url>"""
        # Achterflap episode 8 available until 31/12/2025
        addon.run(['plugin://plugin.video.vrtmax/play/url/https://www.vrt.be/vrtmax/a-z/achterflap/1/achterflap-s1a8/', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_url,
                                        video_url='https://www.vrt.be/vrtmax/a-z/achterflap/1/achterflap-s1a8/'),
                         'plugin://plugin.video.vrtmax/play/url/https://www.vrt.be/vrtmax/a-z/achterflap/1/achterflap-s1a8/')

    def test_play_livestream_by_url_route(self):
        """Play livestream by url: /play/url/<vrtmaxwebsite_url>"""
        # Canvas livestream
        addon.run(['plugin://plugin.video.vrtmax/play/url/https://www.vrt.be/vrtmax/kanalen/canvas/', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_url,
                                        video_url='https://www.vrt.be/vrtmax/kanalen/canvas/'),
                         'plugin://plugin.video.vrtmax/play/url/https://www.vrt.be/vrtmax/kanalen/canvas/')

    def test_play_latestepisode_route(self):
        """Play last episode method: /play/lastepisode/<program>"""
        addon.run(['plugin://plugin.video.vrtmax/play/latest/het-journaal', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_latest, program='het-journaal'), 'plugin://plugin.video.vrtmax/play/latest/het-journaal')
        addon.run(['plugin://plugin.video.vrtmax/play/latest/terzake', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_latest, program='terzake'), 'plugin://plugin.video.vrtmax/play/latest/terzake')
        addon.run(['plugin://plugin.video.vrtmax/play/latest/winteruur', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_latest, program='winteruur'), 'plugin://plugin.video.vrtmax/play/latest/winteruur')

    def test_play_airdateepisode_route(self):
        """Play episode by air date method: /play/airdate/<channel>/<start_date>/<end_date>"""
        # Test Het Journaal
        addon.run([lastweek.strftime('plugin://plugin.video.vrtmax/play/airdate/een/%Y-%m-%dT19:00:00'), '0', ''])
        self.assertEqual(plugin.url_for(addon.play_air_date,
                                        channel='een',
                                        start_date=lastweek.strftime('%Y-%m-%dT19:00:00')),
                         lastweek.strftime('plugin://plugin.video.vrtmax/play/airdate/een/%Y-%m-%dT19:00:00'))
        # Test TerZake
        addon.run([lastweek.strftime('plugin://plugin.video.vrtmax/play/airdate/canvas/%Y-%m-%dT20:00:00'), '0', ''])
        self.assertEqual(plugin.url_for(addon.play_air_date,
                                        channel='canvas',
                                        start_date=lastweek.strftime('%Y-%m-%dT20:00:00')),
                         lastweek.strftime('plugin://plugin.video.vrtmax/play/airdate/canvas/%Y-%m-%dT20:00:00'))
        # Test Livestream cache for morning tv from 9h to 10h
        if now.hour < 10:
            mostrecent = now + timedelta(days=-1)
        else:
            mostrecent = now
        addon.run([mostrecent.strftime('plugin://plugin.video.vrtmax/play/airdate/een/%Y-%m-%dT09:00:00/%Y-%m-%dT10:00:00'), '0', ''])
        self.assertEqual(plugin.url_for(addon.play_air_date,
                                        channel='een',
                                        start_date=mostrecent.strftime('%Y-%m-%dT09:00:00'),
                                        end_date=mostrecent.strftime('%Y-%m-%dT10:00:00')),
                         mostrecent.strftime('plugin://plugin.video.vrtmax/play/airdate/een/%Y-%m-%dT09:00:00/%Y-%m-%dT10:00:00'))

    def test_play_upnext_route(self):
        """Play Up Next episode method: /play/upnext/<episode_id>"""
        addon.run(['plugin://plugin.video.vrtmax/play/upnext/1571140659165', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_upnext, episode_id='1571140659165'), 'plugin://plugin.video.vrtmax/play/upnext/1571140659165')

    def test_update_repos(self):
        """Update repositories: /update/repos"""
        addon.run(['plugin://plugin.video.vrtmax/update/repos', '0', ''])
        self.assertEqual(plugin.url_for(addon.update_repos), 'plugin://plugin.video.vrtmax/update/repos')

    def test_show_settings_addons(self):
        """Open the Kodi System settings: /show/settings/addons"""
        addon.run(['plugin://plugin.video.vrtmax/show/settings/addons', '0', ''])
        self.assertEqual(plugin.url_for(addon.show_settings_addons), 'plugin://plugin.video.vrtmax/show/settings/addons')


if __name__ == '__main__':
    unittest.main()
