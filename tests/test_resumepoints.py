# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for ResumePoints functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from api import get_continue_episodes
from resumepoints import ResumePoints

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

addon = xbmcaddon.Addon()
addon.settings['useresumepoints'] = True


class TestResumePoints(unittest.TestCase):
    """TestCase class"""

    _resumepoints = ResumePoints()

    @unittest.skipUnless(addon.settings.get('username'), 'Skipping as VRT username is missing.')
    @unittest.skipUnless(addon.settings.get('password'), 'Skipping as VRT password is missing.')
    def test_get_continue_episodes(self):
        """Test items, sort and order"""

        # Ensure a continue episode exists (Winteruur met Lize Feryn (beschikbaar tot 26 maart 2025))
        self._resumepoints.update_resumepoint(
            video_id='vid-271d7238-b7f2-4a3c-b3c7-17a5110be71a',
            asset_str='winteruur - 5 - lize feryn',
            title='Winteruur',
            position=38,
            total=635,
        )

        episode_items, sort, ascending, content = get_continue_episodes()
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_update_none(self):
        """Test updating empty resumepoints"""
        self.assertTrue(self._resumepoints.update_resumepoint(video_id=None, asset_str=None, title=None))


if __name__ == '__main__':
    unittest.main()
