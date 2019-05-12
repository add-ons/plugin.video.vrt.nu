# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function, unicode_literals
import mock
import os
import polib
import unittest

from resources.lib.vrtplayer import vrtapihelper

PO = polib.pofile('resources/language/resource.language.en_gb/strings.po')


def get_localized_string(msgctxt):
    for entry in PO:
        if entry.msgctxt == '#%s' % msgctxt:
            return entry.msgstr
    return 'vrttest'


def log_notice(msg, level):
    print('%s: %s' % (level, msg))


class ApiHelperTests(unittest.TestCase):

    _kodiwrapper = mock.MagicMock()

    _kodiwrapper.check_if_path_exists = mock.MagicMock(side_effect=os.path.exists)
    _kodiwrapper.get_localized_dateshort = mock.MagicMock(return_value='%d-%m-%Y')
    _kodiwrapper.get_localized_string = mock.MagicMock(side_effect=get_localized_string)
    _kodiwrapper.get_proxies = mock.MagicMock(return_value=dict())
    _kodiwrapper.log_notice = mock.MagicMock(side_effect=log_notice)
    _kodiwrapper.make_dir.return_value = None
    _apihelper = vrtapihelper.VRTApiHelper(_kodiwrapper)

    def test_get_api_data_single_season(self):
        title_items, sort, ascending = self._apihelper.get_episode_items(path='/vrtnu/a-z/het-journaal.relevant/')
        self.assertTrue(123 < len(title_items) < 129, 'We got %s items instead.' % len(title_items))
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)

    def test_get_api_data_multiple_seasons(self):
        title_items, sort, ascending = self._apihelper.get_episode_items(path='/vrtnu/a-z/thuis.relevant/')
        self.assertTrue(len(title_items) < 5)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)

    def test_get_api_data_specific_season(self):
        title_items, sort, ascending = self._apihelper.get_episode_items(path='/vrtnu/a-z/pano.relevant/')
        self.assertEqual(len(title_items), 4)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)

    def test_get_api_data_specific_season_without_broadcastdate(self):
        title_items, sort, ascending = self._apihelper.get_episode_items(path='/vrtnu/a-z/postbus-x.relevant/')
        self.assertEqual(len(title_items), 3)
        self.assertEqual(sort, 'label')
        self.assertTrue(ascending)


if __name__ == '__main__':
    unittest.main()
