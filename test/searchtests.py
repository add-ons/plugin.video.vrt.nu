# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function, unicode_literals
from contextlib import contextmanager
import mock
import os
import unittest

from resources.lib.vrtplayer import vrtapihelper


@contextmanager
def open_file(path, flags='r'):
    f = open(path, flags)
    yield f
    f.close()


def log_notice(msg, level):
    print('%s: %s' % (level, msg))


class TestVRTPlayer(unittest.TestCase):

    _kodiwrapper = mock.MagicMock()
    _kodiwrapper.check_if_path_exists = mock.MagicMock(side_effect=os.path.exists)
    _kodiwrapper.get_localized_dateshort = mock.MagicMock(return_value='%d-%m-%Y')
    _kodiwrapper.get_localized_string.return_value = '"[B][COLOR blue]Available until %s[/COLOR][/B]\n"'
    _kodiwrapper.get_proxies = mock.MagicMock(return_value=dict())
    _kodiwrapper.get_userdata_path.return_value = './userdata/'
    _kodiwrapper.log_notice = mock.MagicMock(side_effect=log_notice)
    _kodiwrapper.make_dir.return_value = None
    _kodiwrapper.open_file = mock.MagicMock(side_effect=open_file)
    _kodiwrapper.stat_file = mock.MagicMock(side_effect=os.stat)
    _apihelper = vrtapihelper.VRTApiHelper(_kodiwrapper)

    def test_search_journaal(self):
        ''' Test for journaal '''
        search_items, sort, ascending = self._apihelper.search('journaal', page=1)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)

    def test_search_journaal_page2(self):
        ''' Test for journaal '''
        search_items, sort, ascending = self._apihelper.search('journaal', page=2)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)

    def test_search_weer(self):
        ''' Test for journaal '''
        search_items, sort, ascending = self._apihelper.search('weer', page=1)

        # Test we get a non-empty search result
        self.assertEqual(len(search_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)


if __name__ == '__main__':
    unittest.main()
