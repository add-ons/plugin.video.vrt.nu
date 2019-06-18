# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=missing-docstring

from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime, timedelta
import random
import unittest
import dateutil.tz

from resources.lib import kodiwrapper, tvguide

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

channels = ['een', 'canvas', 'ketnet']


class TestTVGuide(unittest.TestCase):

    _kodi = kodiwrapper.KodiWrapper(None)
    _tvguide = tvguide.TVGuide(_kodi)

    def test_tvguide_date_menu(self):
        ''' Test TV guide main menu '''
        date_items = self._tvguide.show_date_menu()
        self.assertEqual(len(date_items), 37)
        date_item = random.choice(date_items)
        print(date_item.title, date_item.path)

    def test_tvguide_channel_menu(self):
        ''' Test channel menu '''
        date = (datetime.now(dateutil.tz.tzlocal()) + timedelta(days=-10)).strftime('%Y-%m-%d')
        channel_items = self._tvguide.show_channel_menu(date)
        self.assertTrue(channel_items)

    def test_tvguide_episode_menu(self):
        ''' Test episode menu '''
        date = (datetime.now(dateutil.tz.tzlocal()) + timedelta(days=-10)).strftime('%Y-%m-%d')
        channel = random.choice(channels)
        episode_items = self._tvguide.show_episodes(date, channel)
        self.assertTrue(episode_items)

    def test_tvguide_invalid_episode_menu(self):
        ''' Test episode menu '''
        date = (datetime.now(dateutil.tz.tzlocal()) + timedelta(days=-40)).strftime('%Y-%m-%d')
        channel = random.choice(channels)
        episode_items = self._tvguide.show_episodes(date, channel)
        self.assertEqual(episode_items, [])

    def test_livetv_description(self):
        description = self._tvguide.live_description('een')
        print(description)
        description = self._tvguide.live_description('canvas')
        print(description)
        description = self._tvguide.live_description('ketnet')
        print(description)

    def test_tvguide_all(self):
        ''' Test episode menu '''
        episode_items = self._tvguide.show_episodes('yesterday', 'een')
        self.assertTrue(episode_items)
        episode_items = self._tvguide.show_episodes('today', 'canvas')
        self.assertTrue(episode_items)
        episode_items = self._tvguide.show_episodes('tomorrow', 'ketnet')
        self.assertTrue(episode_items)

    def test_parse(self):
        now = datetime.now(dateutil.tz.tzlocal())
        date = self._tvguide.parse('2019-05-11', now)
        print(date)


if __name__ == '__main__':
    unittest.main()
