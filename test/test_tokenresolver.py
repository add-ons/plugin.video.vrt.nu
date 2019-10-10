# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=invalid-name,missing-docstring

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from addon import kodi
from tokenresolver import TokenResolver

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')


class TokenResolverTests(unittest.TestCase):

    _tokenresolver = TokenResolver(kodi)

    def test_refresh_login(self):
        self._tokenresolver.refresh_login()

    def test_cleanup_userdata(self):
        self._tokenresolver.cleanup_userdata()


if __name__ == '__main__':
    unittest.main()
