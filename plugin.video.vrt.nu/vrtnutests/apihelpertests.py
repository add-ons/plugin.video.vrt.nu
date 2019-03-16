# -*- coding: UTF-8 -*-

# GNU General Public License v2.0 (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

''' This is the actual VRT Nu video plugin entry point '''

from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
from resources.lib.vrtplayer import vrtapihelper


class ApiHelperTests(unittest.TestCase):

    def test_get_api_data_single_season(self):
        api_helper = vrtapihelper.VRTApiHelper()
        title_items = api_helper.get_video_items('/vrtnu/a-z/piet-piraat.relevant/', None)
        self.assertEqual(3, len(title_items))

    def test_get_api_data_multiple_seasons(self):
        api_helper = vrtapihelper.VRTApiHelper()
        title_items = api_helper.get_video_items('/vrtnu/a-z/thuis.relevant/', None)
        self.assertTrue(len(title_items) < 5)

    def test_get_api_data_specific_season(self):
        api_helper = vrtapihelper.VRTApiHelper()
        title_items = api_helper.get_video_items('/vrtnu/a-z/thuis.relevant/', '24')
        self.assertTrue(len(title_items) > 5)

    def test_get_api_data_specific_season_without_broadcastdate(self):
        api_helper = vrtapihelper.VRTApiHelper()
        title_items = api_helper.get_video_items('/vrtnu/a-z/postbus-x.relevant/', '1')
        self.assertTrue(len(title_items) > 5)


if __name__ == '__main__':
    unittest.main()
