# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime
import dateutil.tz
import mock
import random
import unittest

from resources.lib.vrtplayer import tvguide
from test import log_notice

channels = ['een', 'canvas', 'ketnet']


class TestTVGuide(unittest.TestCase):

    _kodi = mock.MagicMock()
    _kodi.get_proxies = mock.MagicMock(return_value=dict())
    _kodi.get_userdata_path.return_value = './test/userdata/'
    _kodi.localize_datelong = mock.MagicMock(return_value='%a %d-%m-%Y')
    _kodi.log_notice = mock.MagicMock(side_effect=log_notice)
    _kodi.make_dir.return_value = None
    _tvguide = tvguide.TVGuide(_kodi)

    def test_tvguide_date_menu(self):
        ''' Test TV guide main menu '''
        date_items = self._tvguide.show_date_menu()
        self.assertEqual(len(date_items), 38)

    def test_tvguide_channel_menu(self):
        ''' Test channel menu '''
        now = datetime.now(dateutil.tz.tzlocal())
        date = now.strftime('%Y-%m-%d')
        channel_items = self._tvguide.show_channel_menu(date)
        self.assertTrue(channel_items)

    def test_tvguide_episode_menu(self):
        ''' Test episode menu '''
        now = datetime.now(dateutil.tz.tzlocal())
        date = now.strftime('%Y-%m-%d')
        channel = random.choice(channels)
        episode_items = self._tvguide.show_episodes(date, channel)
        self.assertTrue(episode_items)

    def test_livetv_description(self):
        description = self._tvguide.live_description('een')
        print(description)
        description = self._tvguide.live_description('canvas')
        print(description)
        description = self._tvguide.live_description('ketnet')
        print(description)


if __name__ == '__main__':
    unittest.main()
