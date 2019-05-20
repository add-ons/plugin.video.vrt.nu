# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function, unicode_literals
import json
import os
import polib
import sys

# FIXME: Get information from addon.xml
ADDON_INFO = {
    'author': 'Martijn Moreels',
    'changelog': '',
    'description': '',
    'disclaimer': '',
    'fanart': '',
    'icon': '',
    'id': 'plugin.video.vrt.nu',
    'name': 'VRT NU',
    # 'path': '/storage/.kodi/addons/plugin.video.vrt.nu',
    'path': './',
    # 'profile': 'special://profile/addon_data/plugin.video.vrt.nu/',
    'profile': 'test/userdata/',
    'stars': '',
    'summary': '',
    'type': 'xbmc.python.pluginsource',
    'version': '1.10.0',
}

PO = polib.pofile('resources/language/resource.language.en_gb/strings.po')

SETTINGS = {
    'username': 'qsdfdsq',
    'password': 'qsdfqsdfds',
    'log_level': 'Verbose',
    'max_bandwidth': 0,
    'showpermalink': 'true',
    'showsubtitles': 'true',
    'usedrm': 'false',
    'usefavorites': 'false',
}

# Read credentials from credentials.json
if os.path.exists('test/credentials.json'):
    SETTINGS.update(json.loads(open('test/credentials.json').read()))
else:
    print('Credentials not found in credentials.json', file=sys.stderr)


class Addon():
    @staticmethod
    def __init__(id):  # pylint: disable=redefined-builtin
        pass

    @staticmethod
    def getAddonInfo(key):
        return ADDON_INFO.get(key)

    @staticmethod
    def getLocalizedString(msgctxt):
        for entry in PO:
            if entry.msgctxt == '#%s' % msgctxt:
                return entry.msgstr or entry.msgid
        return 'vrttest'

    @staticmethod
    def getSetting(key):
        return SETTINGS.get(key)
