# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function, unicode_literals
import mock
import os
import unittest

from resources.lib.vrtplayer import vrtapihelper
from test import get_localized_string, get_setting, log_notice, open_file


class ApiHelperTests(unittest.TestCase):

    _kodiwrapper = mock.MagicMock()
    _kodiwrapper.check_if_path_exists = mock.MagicMock(side_effect=os.path.exists)
    _kodiwrapper.get_localized_dateshort = mock.MagicMock(return_value='%d-%m-%Y')
    _kodiwrapper.get_localized_string = mock.MagicMock(side_effect=get_localized_string)
    _kodiwrapper.get_proxies = mock.MagicMock(return_value=dict())
    _kodiwrapper.get_setting = mock.MagicMock(side_effect=get_setting)
    _kodiwrapper.get_userdata_path.return_value = './userdata/'
    _kodiwrapper.log_notice = mock.MagicMock(side_effect=log_notice)
    _kodiwrapper.make_dir.return_value = None
    _kodiwrapper.open_file = mock.MagicMock(side_effect=open_file)
    _apihelper = vrtapihelper.VRTApiHelper(_kodiwrapper)

    def test_get_api_data_single_season(self):
        title_items, sort, ascending, content = self._apihelper.get_episode_items(path='/vrtnu/a-z/het-journaal.relevant/')
        self.assertTrue(123 < len(title_items) < 129, 'We got %s items instead.' % len(title_items))
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_get_api_data_multiple_seasons(self):
        title_items, sort, ascending, content = self._apihelper.get_episode_items(path='/vrtnu/a-z/thuis.relevant/')
        self.assertTrue(len(title_items) < 5)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)
        self.assertEqual(content, 'seasons')

    def test_get_api_data_specific_season(self):
        title_items, sort, ascending, content = self._apihelper.get_episode_items(path='/vrtnu/a-z/pano.relevant/')
        self.assertEqual(len(title_items), 4)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)
        self.assertEqual(content, 'seasons')

    def test_get_api_data_specific_season_without_broadcastdate(self):
        title_items, sort, ascending, content = self._apihelper.get_episode_items(path='/vrtnu/a-z/postbus-x.relevant/')
        self.assertEqual(len(title_items), 3)
        self.assertEqual(sort, 'label')
        self.assertTrue(ascending)
        self.assertEqual(content, 'seasons')


if __name__ == '__main__':
    unittest.main()
