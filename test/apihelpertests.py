# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=unused-variable

from __future__ import absolute_import, division, unicode_literals
import mock
from resources.lib.vrtplayer import vrtapihelper
import unittest


class ApiHelperTests(unittest.TestCase):

    _kodi_wrapper = mock.MagicMock()
    _kodi_wrapper.get_proxies = mock.MagicMock(return_value=dict())
    _kodi_wrapper.get_localized_dateshort = mock.MagicMock(return_value='%d-%m-%Y')
    _kodi_wrapper.get_localized_string.return_value = '"[B][COLOR blue]Available until %s[/COLOR][/B]\n"'
    _api_helper = vrtapihelper.VRTApiHelper(_kodi_wrapper)

    def test_get_api_data_single_season(self):
        title_items, sort, ascending = self._api_helper.get_episode_items(path='/vrtnu/a-z/het-journaal.relevant/')
        self.assertEqual(len(title_items), 124)

    def test_get_api_data_multiple_seasons(self):
        title_items, sort, ascending = self._api_helper.get_episode_items(path='/vrtnu/a-z/thuis.relevant/')
        self.assertTrue(len(title_items) < 5)

    def test_get_api_data_specific_season(self):
        title_items, sort, ascending = self._api_helper.get_episode_items(path='/vrtnu/a-z/thuis.relevant/')
        self.assertTrue(len(title_items) == 2)

    def test_get_api_data_specific_season_without_broadcastdate(self):
        title_items, sort, ascending = self._api_helper.get_episode_items(path='/vrtnu/a-z/postbus-x.relevant/')
        self.assertTrue(len(title_items) == 3)


if __name__ == '__main__':
    unittest.main()
