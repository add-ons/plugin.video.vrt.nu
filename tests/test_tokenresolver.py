# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for TokenResolver functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from tokenresolver import TokenResolver

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

addon = xbmcaddon.Addon()


class TestTokenResolver(unittest.TestCase):
    """TestCase class"""

    _tokenresolver = TokenResolver()
    username = None
    password = None

    def setUp(self):
        """Build up  function for TestCase class"""
        # Save password
        self.username = addon.settings['username']
        self.password = addon.settings['password']

    def tearDown(self):
        """Clean up function for TestCase class"""
        # Restore password
        addon.settings['username'] = self.username
        addon.settings['password'] = self.password

    def test_refresh_login(self):
        """Test refreshing login"""
        self._tokenresolver.refresh_login()

    def test_cleanup_userdata(self):
        """Test cleaning up userdata"""
        self._tokenresolver.cleanup_userdata()

    def test_successful_login(self):
        """Test successful login"""
        self.username = addon.settings['username']
        self.password = addon.settings['password']
        self._tokenresolver.login(refresh=False)

    def test_invalid_login(self):
        """Test invalid login"""
        addon.settings['username'] = 'foo'
        addon.settings['password'] = 'bar'
        self._tokenresolver.login(refresh=False)

    def test_missing_username(self):
        """Test missing username"""
        addon.settings['username'] = ''
        addon.settings['password'] = self.password
        self._tokenresolver.login(refresh=True)
        self._tokenresolver.login(refresh=False)

    def test_missing_password(self):
        """Test missing password"""
        addon.settings['username'] = self.username
        addon.settings['password'] = ''
        self._tokenresolver.login(refresh=True)
        self._tokenresolver.login(refresh=False)


if __name__ == '__main__':
    unittest.main()
