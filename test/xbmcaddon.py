# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import os
import json
import polib

# FIXME: Get information from addon.xml
ADDON_INFO = {
    'author': 'Martijn Moreel',
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

# FIXME: Maybe move this to test/userdata/settings.xml ?
SETTINGS = {
    # credentials
    'username': 'qsdfdsq',
    'password': 'qsdfqsdfds',
    # interface
    'usefavorites': 'false',
    'showpermalink': 'true',
    'usemenucaching': 'true',
    'usehttpcaching': 'true',
    # playback
    'showsubtitles': 'true',
    'max_bandwidth': 0,
    'usedrm': 'false',
    # channels
    'een': 'true',
    'canvas': 'true',
    'ketnet': 'false',
    'ketnet-jr': 'false',
    'sporza': 'true',
    'radio1': 'true',
    'radio2': 'true',
    'klara': 'true',
    'stubru': 'true',
    'mnm': 'true',
    'vrtnws': 'true',
    'vrtnxt': 'true',
    # troubleshooting
    'log_level': 'Verbose',
}

# Read credentials from credentials.json
if os.path.exists('test/credentials.json'):
    SETTINGS.update(json.load(open('test/credentials.json')))
else:
    print('Credentials not found in credentials.json', file=sys.stderr)


class Addon:
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

    @staticmethod
    def setSetting(key, value):
        pass
