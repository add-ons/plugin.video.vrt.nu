# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for language-related functionality"""

import unittest
from addon import plugin

import xbmc


class TestLanguage(unittest.TestCase):
    """TestCase class"""

    def tearDown(self):
        """Clean up function for TestCase class"""
        xbmc.settings['locale.language'] = 'resource.language.nl_nl'

    @staticmethod
    def test_dutch():
        """Test the principal add-on language"""
        xbmc.settings['locale.language'] = 'resource.language.nl_nl'
        plugin.run(['plugin://plugin.video.vrt.nu/', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/categories', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/tvguide', '0', ''])

    @staticmethod
    def test_german():
        """Test an unsupported language"""
        xbmc.settings['locale.language'] = 'resource.language.de_de'
        plugin.run(['plugin://plugin.video.vrt.nu/', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/categories', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/tvguide', '0', ''])

    @staticmethod
    def test_english():
        """Test the default Kodi language"""
        xbmc.settings['locale.language'] = 'resource.language.en_gb'
        plugin.run(['plugin://plugin.video.vrt.nu/', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/categories', '0', ''])
        plugin.run(['plugin://plugin.video.vrt.nu/tvguide', '0', ''])


if __name__ == '__main__':
    unittest.main()
