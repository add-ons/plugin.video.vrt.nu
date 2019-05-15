# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function, unicode_literals
import mock
import os
import unittest

from resources.lib.vrtplayer import favorites, vrtapihelper
from test import get_setting, log_notice, open_file, stat_file


class TestSearch(unittest.TestCase):

    _kodi = mock.MagicMock()
    _kodi.check_if_path_exists = mock.MagicMock(side_effect=os.path.exists)
    _kodi.check_inputstream_adaptive.return_value = True
    _kodi.get_proxies = mock.MagicMock(return_value=dict())
    _kodi.get_setting = mock.MagicMock(side_effect=get_setting)
    _kodi.get_userdata_path.return_value = './test/userdata/'
    _kodi.localize_dateshort = mock.MagicMock(return_value='%d-%m-%Y')
    _kodi.log_notice = mock.MagicMock(side_effect=log_notice)
    _kodi.make_dir.return_value = None
    _kodi.open_file = mock.MagicMock(side_effect=open_file)
    _kodi.stat_file = mock.MagicMock(side_effect=stat_file)
    _favorites = favorites.Favorites(_kodi)
    _apihelper = vrtapihelper.VRTApiHelper(_kodi, _favorites)

    def test_search_journaal(self):
        ''' Test for journaal '''
        search_items, sort, ascending, content = self._apihelper.search('journaal', page=1)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_search_journaal_page2(self):
        ''' Test for journaal '''
        search_items, sort, ascending, content = self._apihelper.search('journaal', page=2)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_search_weer(self):
        ''' Test for journaal '''
        search_items, sort, ascending, content = self._apihelper.search('weer', page=1)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')


if __name__ == '__main__':
    unittest.main()
