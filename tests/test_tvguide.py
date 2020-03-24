# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for TVGuide functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime, timedelta
import random
import unittest
import dateutil.tz
from xbmcextra import kodi_to_ansi, uri_to_path

from tvguide import TVGuide

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

channels = ['een', 'canvas', 'ketnet']


class TestTVGuide(unittest.TestCase):
    """TestCase class"""

    _tvguide = TVGuide()

    def test_tvguide_date_menu(self):
        """Test TV guide main menu"""
        date_items = self._tvguide.get_date_items()
        self.assertEqual(len(date_items), 33)
        date_item = random.choice(date_items)
        print('- %s%s' % (kodi_to_ansi(date_item.label), uri_to_path(date_item.path)))
        date_items = self._tvguide.get_date_items('today')
        self.assertEqual(len(date_items), 33)
        date_item = random.choice(date_items)
        print('- %s%s' % (kodi_to_ansi(date_item.label), uri_to_path(date_item.path)))

    def test_tvguide_channel_menu(self):
        """Test channel menu"""
        channel_items = self._tvguide.get_channel_items(channel='een')
        self.assertTrue(channel_items)
        channel_item = random.choice(channel_items)
        print('- %s%s' % (kodi_to_ansi(channel_item.label), uri_to_path(channel_item.path)))

        date = (datetime.now(dateutil.tz.tzlocal()) + timedelta(days=-10)).strftime('%Y-%m-%d')
        channel_items = self._tvguide.get_channel_items(date=date)
        self.assertTrue(channel_items)
        channel_item = random.choice(channel_items)
        print('- %s%s' % (kodi_to_ansi(channel_item.label), uri_to_path(channel_item.path)))

    def test_tvguide_episode_menu(self):
        """Test episode menu"""
        date = (datetime.now(dateutil.tz.tzlocal()) + timedelta(days=-10)).strftime('%Y-%m-%d')
        channel = random.choice(channels)
        episode_items = self._tvguide.get_episode_items(date, channel)
        self.assertTrue(episode_items)

    def test_tvguide_invalid_episode_menu(self):
        """Test episode menu"""
        date = (datetime.now(dateutil.tz.tzlocal()) + timedelta(days=-40)).strftime('%Y-%m-%d')
        channel = random.choice(channels)
        episode_items = self._tvguide.get_episode_items(date, channel)
        self.assertEqual(episode_items, [])

    def test_livetv_description(self):
        """Test Live TV description"""
        description = self._tvguide.live_description('een')
        print(kodi_to_ansi(description))
        description = self._tvguide.live_description('canvas')
        print(kodi_to_ansi(description))
        description = self._tvguide.live_description('ketnet')
        print(kodi_to_ansi(description))

    def test_tvguide_all(self):
        """Test episode menu"""
        episode_items = self._tvguide.get_episode_items('yesterday', 'een')
        self.assertTrue(episode_items)
        episode_items = self._tvguide.get_episode_items('today', 'canvas')
        self.assertTrue(episode_items)
        episode_items = self._tvguide.get_episode_items('tomorrow', 'ketnet')
        self.assertTrue(episode_items)

    def test_parse(self):
        """Test parsing date"""
        now = datetime.now(dateutil.tz.tzlocal())
        date = self._tvguide.parse('2019-05-11', now)
        print(date)


if __name__ == '__main__':
    unittest.main()
