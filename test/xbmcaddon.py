# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
''' This file implements the Kodi xbmcaddon module, either using stubs or alternative functionality '''

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import json
import xml.etree.ElementTree as ET
import polib

PO = polib.pofile('resources/language/resource.language.en_gb/strings.po')

# Use the addon_settings file
try:
    with open('test/userdata/addon_settings.json') as f:
        ADDON_SETTINGS = json.load(f)
except Exception as e:
    print("Error using 'test/userdata/addon_settings.json': %s" % e, file=sys.stderr)
    ADDON_SETTINGS = {}

# Read credentials from credentials.json
try:
    with open('test/userdata/credentials.json') as f:
        ADDON_SETTINGS.update(json.load(f))
except Exception as e:
    print("Error using 'test/userdata/credentials.json': %s" % e, file=sys.stderr)


def __read_addon_xml(path):
    ''' Parse the addon.xml and return an info dictionary '''
    info = dict(
        path='./',  # '/storage/.kodi/addons/plugin.video.vrt.nu',
        profile='./test/userdata/',  # 'special://profile/addon_data/plugin.video.vrt.nu/',
        type='xbmc.python.pluginsource',
    )

    tree = ET.parse(path)
    root = tree.getroot()

    info.update(root.attrib)  # Add 'id', 'name' and 'version'
    info['author'] = info.pop('provider-name')

    for child in root:
        if child.attrib.get('point') != 'xbmc.addon.metadata':
            continue
        for grandchild in child:
            # Handle assets differently
            if grandchild.tag == 'assets':
                for asset in grandchild:
                    info[asset.tag] = asset.text
                continue
            # Not in English ?  Drop it
            if grandchild.attrib.get('lang', 'en_GB') != 'en_GB':
                continue
            # Add metadata
            info[grandchild.tag] = grandchild.text

    return info


ADDON_INFO = __read_addon_xml('addon.xml')


class Addon:
    ''' A reimplementation of the xbmcaddon Addon class '''

    @staticmethod
    def __init__():
        ''' A stub constructor for the xbmcaddon Addon class '''

    @staticmethod
    def getAddonInfo(key):
        ''' A working implementation for the xbmcaddon Addon class getAddonInfo() method '''
        return ADDON_INFO.get(key)

    @staticmethod
    def getLocalizedString(msgctxt):
        ''' A working implementation for the xbmcaddon Addon class getLocalizedString() method '''
        for entry in PO:
            if entry.msgctxt == '#%s' % msgctxt:
                return entry.msgstr or entry.msgid
        return 'vrttest'

    @staticmethod
    def getSetting(key):
        ''' A working implementation for the xbmcaddon Addon class getSetting() method '''
        return ADDON_SETTINGS.get(key, '')

    @staticmethod
    def openSettings():
        ''' A stub implementation for the xbmcaddon Addon class openSettings() method '''

    @staticmethod
    def setSetting(key, value):
        ''' A stub implementation for the xbmcaddon Addon class setSetting() method '''
