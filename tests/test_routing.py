# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Integration tests for Routing functionality"""

from datetime import datetime, timedelta
import unittest
import dateutil.tz
import addon

import xbmcaddon

ADDON = xbmcaddon.Addon()
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

    @staticmethod
    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_favorites():
        """Favorites menu: /favorites"""
        addon.run(['plugin://plugin.video.vrt.nu/favorites', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/favorites/programs', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/favorites/recent', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/favorites/offline', '0', ''])
        addon.run(['plugin://plugin.video.vrt.nu/resumepoints/continue', '0', ''])
        # addon.run(['plugin://plugin.video.vrt.nu/favorites/docu', '0', ''])
        # addon.run(['plugin://plugin.video.vrt.nu/favorites/music', '0', ''])

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_episodes_menu(self):
        """Episodes menu: /programs/<program>"""
        addon.run(['plugin://plugin.video.vrt.nu/programs/thuis', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs, program_name='thuis'), 'plugin://plugin.video.vrt.nu/programs/thuis')
        addon.run(['plugin://plugin.video.vrt.nu/programs/pano/2019', '0', ''])
        self.assertEqual(plugin.url_for(addon.programs, program_name='pano', season_name='2019'), 'plugin://plugin.video.vrt.nu/programs/pano/2019')
        addon.run(['plugin://plugin.video.vrt.nu/programs/de-smurfen0/2021/1655824964821', '0', ''])
        self.assertEqual(
            plugin.url_for(
                addon.programs,
                program_name='de-smurfen0',
                season_name='2021',
                end_cursor='1655824964821'
            ),
            'plugin://plugin.video.vrt.nu/programs/de-smurfen0/2021/1655824964821'
        )

    def test_categories_menu(self):
        """Categories menu: /categories"""
        addon.run(['plugin://plugin.video.vrt.nu/categories', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories), 'plugin://plugin.video.vrt.nu/categories')

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_categories_tvshow_menu(self):
        """Categories programs menu: /categories/<category>"""
        addon.run(['plugin://plugin.video.vrt.nu/categories/docu', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories, category='docu'), 'plugin://plugin.video.vrt.nu/categories/docu')
        addon.run(['plugin://plugin.video.vrt.nu/categories/voor-kinderen', '0', ''])
        self.assertEqual(plugin.url_for(addon.categories, category='voor-kinderen'), 'plugin://plugin.video.vrt.nu/categories/voor-kinderen')

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_featured_menu(self):
        """Featured menu: /featured"""
        addon.run(['plugin://plugin.video.vrt.nu/featured', '0', ''])
        self.assertEqual(plugin.url_for(addon.featured), 'plugin://plugin.video.vrt.nu/featured')

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_featured_tvshow_menu(self):
        """Featured programs menu: /featured/<cfeatured>"""
        addon.run(['plugin://plugin.video.vrt.nu/featured/program_par_list_789470835_copy', '0', ''])
        self.assertEqual(plugin.url_for(addon.featured,
                                        feature='program_par_list_789470835_copy'),
                         'plugin://plugin.video.vrt.nu/featured/program_par_list_789470835_copy')

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_featured_episode_menu(self):
        """Featured episodes menu: /featured/<cfeatured>"""
        addon.run(['plugin://plugin.video.vrt.nu/featured/episode_par_list_copy_copy_copy', '0', ''])
        self.assertEqual(plugin.url_for(addon.featured,
                                        feature='episode_par_list_copy_copy_copy'),
                         'plugin://plugin.video.vrt.nu/featured/episode_par_list_copy_copy_copy')

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
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

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_recent_menu(self):
        """Most recent menu: /recent"""
        addon.run(['plugin://plugin.video.vrt.nu/recent', '0', ''])
        self.assertEqual(plugin.url_for(addon.recent), 'plugin://plugin.video.vrt.nu/recent')

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_offline_menu(self):
        """Soon offline menu: /offline"""
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

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
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

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_search_menu(self):
        """Search VRT MAX menu: /search/query/<keywords>"""
        addon.run(['plugin://plugin.video.vrt.nu/search', '0', ''])
        self.assertEqual(plugin.url_for(addon.search), 'plugin://plugin.video.vrt.nu/search')
        addon.run(['plugin://plugin.video.vrt.nu/search/query', '0', ''])
        self.assertEqual(plugin.url_for(addon.search_query), 'plugin://plugin.video.vrt.nu/search/query')
        addon.run(['plugin://plugin.video.vrt.nu/search/query/dag', '0', ''])
        self.assertEqual(plugin.url_for(addon.search_query, keywords='dag'), 'plugin://plugin.video.vrt.nu/search/query/dag')
        addon.run(['plugin://plugin.video.vrt.nu/search/query/winter', '0', ''])
        self.assertEqual(plugin.url_for(addon.search_query, keywords='winter'), 'plugin://plugin.video.vrt.nu/search/query/winter')

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_follow_route(self):
        """Follow method: /follow/<program_id>/<program_title>"""
        addon.run(['plugin://plugin.video.vrt.nu/follow/1459955889901/Thuis', '0', ''])
        self.assertEqual(
            plugin.url_for(
                addon.follow,
                program_id='1459955889901',
                program_title='Thuis'
            ),
            'plugin://plugin.video.vrt.nu/follow/1459955889901/Thuis'
        )

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_unfollow_route(self):
        """Unfollow method: /unfollow/<program_id>/<program_title>"""
        addon.run(['plugin://plugin.video.vrt.nu/unfollow/1459955889901/Thuis', '0', ''])
        self.assertEqual(
            plugin.url_for(
                addon.unfollow,
                program_id='1459955889901',
                program_title='Thuis'
            ),
            'plugin://plugin.video.vrt.nu/unfollow/1459955889901/Thuis'
        )

    def test_clear_cookies_route(self):
        """Delete tokens method: /tokens/delete"""
        addon.run(['plugin://plugin.video.vrt.nu/tokens/delete', '0', ''])
        self.assertEqual(plugin.url_for(addon.delete_tokens), 'plugin://plugin.video.vrt.nu/tokens/delete')

    def test_invalidate_caches_route(self):
        """Delete cache method: /cache/delete"""
        addon.run(['plugin://plugin.video.vrt.nu/cache/delete', '0', ''])
        self.assertEqual(plugin.url_for(addon.delete_cache), 'plugin://plugin.video.vrt.nu/cache/delete')

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

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_play_latestepisode_route(self):
        """Play last episode method: /play/lastepisode/<program>"""
        addon.run(['plugin://plugin.video.vrt.nu/play/latest/vrt-nws-journaal', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_latest, program_name='vrt-nws-journaal'), 'plugin://plugin.video.vrt.nu/play/latest/vrt-nws-journaal')
        addon.run(['plugin://plugin.video.vrt.nu/play/latest/terzake', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_latest, program_name='terzake'), 'plugin://plugin.video.vrt.nu/play/latest/terzake')
        addon.run(['plugin://plugin.video.vrt.nu/play/latest/winteruur', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_latest, program_name='winteruur'), 'plugin://plugin.video.vrt.nu/play/latest/winteruur')

    def test_play_airdateepisode_route(self):
        """Play episode by air date method: /play/airdate/<channel>/<start_date>/<end_date>"""
        # Test Het Journaal
        addon.run([lastweek.strftime('plugin://plugin.video.vrt.nu/play/airdate/een/%Y-%m-%dT19:00:00'), '0', ''])
        self.assertEqual(plugin.url_for(addon.play_air_date,
                                        channel='een',
                                        start_date=lastweek.strftime('%Y-%m-%dT19:00:00')),
                         lastweek.strftime('plugin://plugin.video.vrt.nu/play/airdate/een/%Y-%m-%dT19:00:00'))
        # Test TerZake
        addon.run([lastweek.strftime('plugin://plugin.video.vrt.nu/play/airdate/canvas/%Y-%m-%dT20:00:00'), '0', ''])
        self.assertEqual(plugin.url_for(addon.play_air_date,
                                        channel='canvas',
                                        start_date=lastweek.strftime('%Y-%m-%dT20:00:00')),
                         lastweek.strftime('plugin://plugin.video.vrt.nu/play/airdate/canvas/%Y-%m-%dT20:00:00'))
        # Test Livestream cache for morning tv from 9h to 10h
        if now.hour < 10:
            mostrecent = now + timedelta(days=-1)
        else:
            mostrecent = now
        addon.run([mostrecent.strftime('plugin://plugin.video.vrt.nu/play/airdate/een/%Y-%m-%dT09:00:00/%Y-%m-%dT10:00:00'), '0', ''])
        self.assertEqual(plugin.url_for(addon.play_air_date,
                                        channel='een',
                                        start_date=mostrecent.strftime('%Y-%m-%dT09:00:00'),
                                        end_date=mostrecent.strftime('%Y-%m-%dT10:00:00')),
                         mostrecent.strftime('plugin://plugin.video.vrt.nu/play/airdate/een/%Y-%m-%dT09:00:00/%Y-%m-%dT10:00:00'))

    @unittest.skipUnless(ADDON.getSetting('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(ADDON.getSetting('password'), 'Skipping as VRT password is missing.')
    def test_play_upnext_route(self):
        """Play Up Next episode method: /play/upnext/<episode_id>"""
        addon.run(['plugin://plugin.video.vrt.nu/play/upnext/1571140659165', '0', ''])
        self.assertEqual(plugin.url_for(addon.play_upnext, episode_id='1571140659165'), 'plugin://plugin.video.vrt.nu/play/upnext/1571140659165')

    def test_update_repos(self):
        """Update repositories: /update/repos"""
        addon.run(['plugin://plugin.video.vrt.nu/update/repos', '0', ''])
        self.assertEqual(plugin.url_for(addon.update_repos), 'plugin://plugin.video.vrt.nu/update/repos')

    def test_show_settings_addons(self):
        """Open the Kodi System settings: /show/settings/addons"""
        addon.run(['plugin://plugin.video.vrt.nu/show/settings/addons', '0', ''])
        self.assertEqual(plugin.url_for(addon.show_settings_addons), 'plugin://plugin.video.vrt.nu/show/settings/addons')


if __name__ == '__main__':
    unittest.main()
