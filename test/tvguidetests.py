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

    _kodiwrapper = mock.MagicMock()
    _kodiwrapper.get_localized_datelong = mock.MagicMock(return_value='%a %d-%m-%Y')
    _kodiwrapper.get_proxies = mock.MagicMock(return_value=dict())
    _kodiwrapper.get_userdata_path.return_value = './userdata/'
    _kodiwrapper.log_notice = mock.MagicMock(side_effect=log_notice)
    _kodiwrapper.make_dir.return_value = None
    _tvguide = tvguide.TVGuide(_kodiwrapper)

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


if __name__ == '__main__':
    unittest.main()
