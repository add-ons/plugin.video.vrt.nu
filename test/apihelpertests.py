# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=unused-variable

from __future__ import absolute_import, division, unicode_literals
import mock
import unittest

from resources.lib.vrtplayer import vrtapihelper


class ApiHelperTests(unittest.TestCase):

    _kodiwrapper = mock.MagicMock()
    _kodiwrapper.get_proxies = mock.MagicMock(return_value=dict())
    _kodiwrapper.get_localized_dateshort = mock.MagicMock(return_value='%d-%m-%Y')
    _kodiwrapper.get_localized_string.return_value = '"[B][COLOR blue]Available until %s[/COLOR][/B]\n"'
    _apihelper = vrtapihelper.VRTApiHelper(_kodiwrapper)

    def test_get_api_data_single_season(self):
        title_items, sort, ascending = self._apihelper.get_episode_items(path='/vrtnu/a-z/het-journaal.relevant/')
        self.assertTrue(123 < len(title_items) < 129)

    def test_get_api_data_multiple_seasons(self):
        title_items, sort, ascending = self._apihelper.get_episode_items(path='/vrtnu/a-z/thuis.relevant/')
        self.assertTrue(len(title_items) < 5)

    def test_get_api_data_specific_season(self):
        title_items, sort, ascending = self._apihelper.get_episode_items(path='/vrtnu/a-z/pano.relevant/')
        self.assertEqual(len(title_items), 4)

    def test_get_api_data_specific_season_without_broadcastdate(self):
        title_items, sort, ascending = self._apihelper.get_episode_items(path='/vrtnu/a-z/postbus-x.relevant/')
        self.assertEqual(len(title_items), 3)


if __name__ == '__main__':
    unittest.main()
