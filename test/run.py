#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Run any Kodi VRT NU plugin:// URL on the commandline"""

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import os

# Add current working directory to import paths
CWD = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(os.path.realpath(__file__))), os.pardir, 'resources/lib'))
sys.path.insert(0, CWD)
import addon  # noqa: E402  pylint: disable=wrong-import-position

# pylint: disable=invalid-name
xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

if len(sys.argv) <= 1:
    print("%s: URI argument missing\nTry '%s plugin://plugin.video.vrt.nu/recent/1' to test." % (sys.argv[0], sys.argv[0]))
    sys.exit(1)

# Also support bare paths like /recent/2
if not sys.argv[1].startswith('plugin://'):
    sys.argv[1] = 'plugin://plugin.video.vrt.nu' + sys.argv[1]

# Split path and args
path, _, args = sys.argv[1].partition('?')

print('** Running URI %s with args %s' % (path, args))
addon.run([sys.argv[1], 0, args])
