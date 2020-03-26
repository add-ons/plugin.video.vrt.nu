# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for ResumePoints functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from apihelper import ApiHelper
from favorites import Favorites
from resumepoints import ResumePoints
from utils import assetpath_to_id

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

addon = xbmcaddon.Addon()
addon.settings['useresumepoints'] = True


class TestResumePoints(unittest.TestCase):
    """TestCase class"""

    _favorites = Favorites()
    _resumepoints = ResumePoints()
    _apihelper = ApiHelper(_favorites, _resumepoints)

    def test_assetpath_to_id(self):
        """Test converting assetpath to assetid"""
        self.assertEqual(None, assetpath_to_id(None))

        asset_path = '/content/dam/vrt/2019/08/14/woodstock-depot_WP00157456'
        asset_id = 'contentdamvrt20190814woodstockdepotwp00157456'
        self.assertEqual(asset_id, assetpath_to_id(asset_path))

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_get_continue_episodes(self):
        """Test items, sort and order"""

        # Ensure a continue episode exists (Winteruur met Lize Feryn (beschikbaar tot 26 maart 2025))
        self._resumepoints.update(asset_id='contentdamvrt20191015winteruurr005a0001depotwp00162177', title='Winteruur', url='/vrtnu/a-z/winteruur/5/winteruur-s5a1/', watch_later=True, position=38, total=635, whatson_id='705308178527')

        episode_items, sort, ascending, content = self._apihelper.list_episodes(page=1, variety='continue')
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_get_watchlater_episodes(self):
        """Test items, sort and order"""
        episode_items, sort, ascending, content = self._apihelper.list_episodes(page=1, variety='watchlater')
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_update_none(self):
        """Test updating empty resumepoints"""
        self.assertTrue(self._resumepoints.update(asset_id=None, title=None, url=None))

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_update_watchlater(self):
        """Test updating the watch later list"""
        self._resumepoints.refresh(ttl=0)
        asset_id, first_entry = next(iter(list(self._resumepoints._data.items())))  # pylint: disable=protected-access
        print('%s = %s' % (asset_id, first_entry))
        url = first_entry.get('value').get('url')
        self._resumepoints.unwatchlater(asset_id=asset_id, title='Foo bar', url=url)
        self._resumepoints.watchlater(asset_id=asset_id, title='Foo bar', url=url)
        self._resumepoints.refresh(ttl=0)
        asset_id, first_entry = next(iter(list(self._resumepoints._data.items())))  # pylint: disable=protected-access
        print('%s = %s' % (asset_id, first_entry))

        # Remove Winteruur met Lize Feryn (beschikbaar tot 26 maart 2025)
        self._resumepoints.update(asset_id='contentdamvrt20191015winteruurr005a0001depotwp00162177', title='Winteruur', url='/vrtnu/a-z/winteruur/5/winteruur-s5a1/', watch_later=False, position=635, total=635, whatson_id='705308178527')


if __name__ == '__main__':
    unittest.main()
