# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for TokenResolver functionality"""

import unittest
from tokenresolver import TokenResolver

import xbmcaddon

ADDON = xbmcaddon.Addon()


class TestTokenResolver(unittest.TestCase):
    """TestCase class"""

    _tokenresolver = TokenResolver()
    username = None
    password = None

    def setUp(self):
        """Build up  function for TestCase class"""
        # Save password
        self.username = ADDON.getSetting('username')
        self.password = ADDON.getSetting('password')

    def tearDown(self):
        """Clean up function for TestCase class"""
        # Restore password
        ADDON.setSetting('username', self.username)
        ADDON.setSetting('password', self.password)

    def test_refresh_login(self):
        """Test refreshing login"""
        self._tokenresolver.refresh_login()

    def test_cleanup_userdata(self):
        """Test cleaning up userdata"""
        self._tokenresolver.cleanup_userdata()

    def test_successful_login(self):
        """Test successful login"""
        self.username = ADDON.getSetting('username')
        self.password = ADDON.getSetting('password')
        self._tokenresolver.login(refresh=False)

    def test_invalid_login(self):
        """Test invalid login"""
        ADDON.setSetting('username', 'foo')
        ADDON.setSetting('password', 'bar')
        self._tokenresolver.login(refresh=False)

    def test_missing_username(self):
        """Test missing username"""
        ADDON.setSetting('username', '')
        ADDON.setSetting('password', self.password)
        self._tokenresolver.login(refresh=True)
        self._tokenresolver.login(refresh=False)

    def test_missing_password(self):
        """Test missing password"""
        ADDON.setSetting('username', self.username)
        ADDON.setSetting('password', '')
        self._tokenresolver.login(refresh=True)
        self._tokenresolver.login(refresh=False)


if __name__ == '__main__':
    unittest.main()
