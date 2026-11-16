# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for TVGuide functionality"""

from datetime import datetime, timedelta
import random
import unittest
import dateutil.tz
from xbmcextra import kodi_to_ansi, uri_to_path

from api import convert_episode
from tvguide import TVGuide

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

addon = xbmcaddon.Addon()
channels = ['een', 'canvas', 'ketnet']


class TestTVGuide(unittest.TestCase):
    """TestCase class"""

    _tvguide = TVGuide()

    def test_tvguide_date_menu(self):
        """Test TV guide main menu"""
        date_items = self._tvguide.get_date_items()
        self.assertEqual(len(date_items), 15)
        date_item = random.choice(date_items)
        print('- %s%s' % (kodi_to_ansi(date_item.label), uri_to_path(date_item.path)))
        date_items = self._tvguide.get_date_items('today')
        self.assertEqual(len(date_items), 15)
        date_item = random.choice(date_items)
        print('- %s%s' % (kodi_to_ansi(date_item.label), uri_to_path(date_item.path)))

    def test_tvguide_channel_menu(self):
        """Test channel menu"""
        channel_items = self._tvguide.get_channel_items(channel='een')
        self.assertTrue(channel_items)
        channel_item = random.choice(channel_items)
        print('- %s%s' % (kodi_to_ansi(channel_item.label), uri_to_path(channel_item.path)))

        date = (datetime.now(dateutil.tz.gettz('Europe/Brussels')) + timedelta(days=-7)).strftime('%Y-%m-%d')
        channel_items = self._tvguide.get_channel_items(date=date)
        self.assertTrue(channel_items)
        channel_item = random.choice(channel_items)
        print('- %s%s' % (kodi_to_ansi(channel_item.label), uri_to_path(channel_item.path)))

    def test_tvguide_today_channel_paths_include_end_cursor(self):
        """Selecting Vandaag then a channel must open page 1 (end_cursor=1)"""
        channel_items = self._tvguide.get_channel_items(date='today')
        self.assertTrue(channel_items)
        for channel_item in channel_items:
            self.assertTrue(channel_item.path.endswith('/1'), channel_item.path)
            self.assertIn('/tvguide/date/today/', channel_item.path)

    def test_convert_episode_aired_dutch_date(self):
        """Parse Dutch aired metadata without using datetime.strptime (broken on some Kodi builds)"""
        from unittest import mock
        import api as api_module

        episode = {
            'title': 'Het Journaal',
            'available': True,
            'active': False,
            'preview': {
                'heading': {
                    'title': 'Het Journaal',
                    'description': '19u',
                    'tertiaryMeta': [],
                }
            },
            'primaryMeta': [
                {'shortValue': 'zo 15/11', 'longValue': 'zondag 15 november'},
            ],
            'action': {'link': 'https://www.vrt.be/vrtmax/a-z/het-journaal/'},
            'actionItems': [],
            'trackingData': {'data': '{}'},
            'image': None,
            'progress': {'durationInSeconds': 1800},
            'statusMeta': [{'value': '30 min'}],
        }

        real_datetime = api_module.datetime

        class BrokenDateTime:  # pylint: disable=too-few-public-methods
            """datetime stand-in reproducing broken strptime TypeError on some Kodi builds"""

            strptime = None

            @staticmethod
            def now(*args, **kwargs):
                """Proxy datetime.now"""
                return real_datetime.now(*args, **kwargs)

            @staticmethod
            def fromtimestamp(*args, **kwargs):
                """Proxy datetime.fromtimestamp"""
                return real_datetime.fromtimestamp(*args, **kwargs)

        with mock.patch.object(api_module, 'datetime', BrokenDateTime):
            with self.assertRaises(TypeError):
                BrokenDateTime.strptime('15/11/2026', '%d/%m/%Y')  # pylint: disable=not-callable
            _, _, _, title_item = convert_episode(episode, destination='tvguide')

        year = datetime.now(dateutil.tz.gettz('Europe/Brussels')).year
        self.assertEqual(title_item.info_dict.get('aired'), '%s-11-15' % year)
        self.assertTrue(title_item.label)

    def test_convert_episode_aired_with_year(self):
        """Parse shortValue that already includes a year"""
        episode = {
            'title': 'Thuis',
            'available': True,
            'active': False,
            'preview': {
                'heading': {
                    'title': 'Thuis',
                    'description': 'Aflevering',
                    'tertiaryMeta': [],
                }
            },
            'primaryMeta': [
                {'shortValue': 'zo 15/11/2025', 'longValue': 'zondag 15 november 2025'},
            ],
            'action': {'link': 'https://www.vrt.be/vrtmax/a-z/thuis/'},
            'actionItems': [],
            'trackingData': {'data': '{}'},
            'image': None,
            'progress': {'durationInSeconds': 1800},
            'statusMeta': [{'value': '30 min'}],
        }
        _, _, _, title_item = convert_episode(episode, destination='tvguide')
        self.assertEqual(title_item.info_dict.get('aired'), '2025-11-15')

    def test_convert_episode_aired_invalid_does_not_crash(self):
        """Invalid aired shortValue must not raise"""
        episode = {
            'title': 'Dummy',
            'available': True,
            'active': False,
            'preview': {
                'heading': {
                    'title': 'Dummy',
                    'description': 'x',
                    'tertiaryMeta': [],
                }
            },
            'primaryMeta': [
                {'shortValue': 'zo', 'longValue': 'november'},
            ],
            'action': {'link': 'https://www.vrt.be/vrtmax/a-z/dummy/'},
            'actionItems': [],
            'trackingData': {'data': '{}'},
            'image': None,
            'progress': {'durationInSeconds': 60},
            'statusMeta': [{'value': '1 min'}],
        }
        _, _, _, title_item = convert_episode(episode, destination='tvguide')
        self.assertIsNone(title_item.info_dict.get('aired'))

    def test_convert_episode_livestream_keeps_brussels_wall_clock(self):
        """Livestream EPG HH:MM is Brussels local and must not shift with host TZ"""
        # Regression: replace(tzinfo=None).timestamp() treated Brussels HH:MM as the
        # host timezone, shifting CET/CEST labels by one hour when TZ=UTC.
        episode = {
            'title': 'VRT NWS journaal',
            'available': True,
            'active': True,
            'tileType': 'livestream',
            'brand': 'een',
            'preview': {
                'heading': {
                    'title': 'VRT NWS journaal',
                    'description': 'VRT NWS journaal 19u',
                    'tertiaryMeta': [],
                }
            },
            'status': {'text': {'small': '19:00 - 19:45', 'default': '19:00 - 19:45'}},
            'progress': {'durationInSeconds': 2700},
            'indexMeta': [{'type': 'default', 'value': '19:00u'}],
            'action': {'link': 'https://www.vrt.be/vrtmax/livestream/video/vrt1/'},
            'actionItems': [],
            'trackingData': {'data': '{}'},
            'image': None,
            'statusMeta': [],
            'primaryMeta': [],
        }
        _, _, _, title_item = convert_episode(episode, destination='tvguide')
        self.assertIn('19:00', title_item.label)
        self.assertNotIn('20:00', title_item.label)
        self.assertIn('19:00 - 19:45', title_item.info_dict.get('plot', ''))

    def _journaal_component_episode(self, start_ms=1794852000000):
        """Build a non-live EPG episode whose componentId encodes the given unix ms"""
        from base64 import b64encode

        decoded = (
            'o%26|episode|o#30#0n#34#0n#30#0o#1349#10O8#10d#13{start_ms}#10#10#13#3|epg|'
            '||||episode||||o%31|scheduleNext|O8|2026-11-16|'
        ).format(start_ms=start_ms)
        component_id = '#' + b64encode(decoded.encode('utf-8')).decode('utf-8')
        return {
            'title': 'VRT NWS journaal',
            'available': True,
            'active': False,
            'tileType': 'episode',
            'preview': {
                'heading': {
                    'title': 'VRT NWS journaal',
                    'description': 'VRT NWS journaal 19u',
                    'tertiaryMeta': [],
                }
            },
            'componentId': component_id,
            'status': {'text': {'small': '45 min', 'default': '45 minuten'}},
            'progress': {'durationInSeconds': 2700},
            'indexMeta': [{'type': 'default', 'value': '19:00u'}],
            'action': {'link': 'https://www.vrt.be/vrtmax/a-z/journaal/'},
            'actionItems': [],
            'trackingData': {'data': '{}'},
            'image': None,
            'statusMeta': [{'value': '45 min'}],
            'primaryMeta': [],
        }

    def test_convert_episode_componentid_unix_ts_to_brussels(self):
        """Non-live EPG entries decode absolute unix ms and show Brussels local time"""
        # 2026-11-16 19:00:00 CET == 18:00:00 UTC
        _, _, _, title_item = convert_episode(self._journaal_component_episode(), destination='tvguide')
        self.assertTrue(title_item.label.startswith('19:00'), title_item.label)

    def test_convert_episode_componentid_without_zoneinfo(self):
        """Host TZ=UTC must still show Brussels labels (TV screenshot: 18:00 vs 19u)"""
        import utils

        # Even if something clears/replaces zoneinfo lookups, labels stay on POSIX Brussels.
        utils._BRUSSELS_TZ = None  # pylint: disable=protected-access
        _, _, _, title_item = convert_episode(self._journaal_component_episode(), destination='tvguide')
        self.assertTrue(title_item.label.startswith('19:00'), title_item.label)
        self.assertNotIn('18:00', title_item.label)
        self.assertIn('19:00 -', title_item.info_dict.get('plot', ''))

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_tvguide_episode_menu(self):
        """Test episode menu"""
        date = (datetime.now(dateutil.tz.gettz('Europe/Brussels')) + timedelta(days=-7)).strftime('%Y-%m-%d')
        channel = random.choice(channels)
        episode_items = self._tvguide.get_episode_items(date, channel)
        self.assertTrue(episode_items)

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_tvguide_invalid_episode_menu(self):
        """Test episode menu"""
        date = (datetime.now(dateutil.tz.gettz('Europe/Brussels')) + timedelta(days=-40)).strftime('%Y-%m-%d')
        channel = random.choice(channels)
        episode_items = self._tvguide.get_episode_items(date, channel)
        self.assertEqual(episode_items, [])

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_tvguide_all(self):
        """Test episode menu for relative dates including Vandaag"""
        episode_items = self._tvguide.get_episode_items('yesterday', 'een')
        self.assertTrue(episode_items)
        episode_items = self._tvguide.get_episode_items('today', 'canvas')
        self.assertTrue(episode_items)
        episode_items = self._tvguide.get_episode_items('tomorrow', 'ketnet')
        self.assertTrue(episode_items)

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_tvguide_today_with_end_cursor(self):
        """Deeper click: Vandaag -> channel uses end_cursor=1 (paged EPG)"""
        for channel in channels:
            episode_items = self._tvguide.get_episode_items('today', channel, end_cursor='1')
            self.assertTrue(episode_items, 'No episodes for today/%s/1' % channel)

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_epg_data(self):
        """ Test epg data"""
        epg_data = self._tvguide.get_epg_data()
        print(epg_data)
        self.assertIsInstance(epg_data, dict)

    def test_parse(self):
        """Test parsing date"""
        now = datetime.now(dateutil.tz.gettz('Europe/Brussels'))
        date = self._tvguide.parse('2026-08-30', now)
        print(date)


if __name__ == '__main__':
    unittest.main()
