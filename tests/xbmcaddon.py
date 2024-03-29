# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""This file implements the Kodi xbmcaddon module, either using stubs or alternative functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
from xbmcextra import ADDON_ID, ADDON_INFO, addon_settings

try:  # Python 2
    basestring  # pylint: disable=used-before-assignment
except NameError:  # Python 3
    basestring = str  # pylint: disable=redefined-builtin

# Ensure the addon settings are retained (as we don't write to disk)
ADDON_SETTINGS = addon_settings(ADDON_ID)


class Addon:
    """A reimplementation of the xbmcaddon Addon class"""

    def __init__(self, id=ADDON_ID):  # pylint: disable=redefined-builtin
        """A stub constructor for the xbmcaddon Addon class"""
        self.id = id
        if id == ADDON_ID:
            self.settings = ADDON_SETTINGS
        else:
            self.settings = addon_settings(id)

    def getAddonInfo(self, key):
        """A working implementation for the xbmcaddon Addon class getAddonInfo() method"""
        assert isinstance(key, basestring)
        stub_info = {
            'id': self.id,
            'name': self.id,
            'version': '2.3.4',
            'type': 'kodi.inputstream',
            'profile': 'special://userdata',
            'path': 'special://userdata',
        }
        # Add stub_info values to ADDON_INFO when missing (e.g. path and profile)
        addon_info = dict(stub_info, **ADDON_INFO)
        return addon_info.get(self.id, stub_info).get(key)

    @staticmethod
    def getLocalizedString(msgctxt):
        """A working implementation for the xbmcaddon Addon class getLocalizedString() method"""
        assert isinstance(msgctxt, int)
        from xbmc import getLocalizedString
        return getLocalizedString(msgctxt)

    def getSetting(self, key):
        """A working implementation for the xbmcaddon Addon class getSetting() method"""
        assert isinstance(key, basestring)
        return self.settings.get(key, '')

    def getSettingBool(self, key):
        """A working implementation for the xbmcaddon Addon class getSettingBool() method"""
        assert isinstance(key, basestring)
        return bool(self.settings.get(key, False))

    def getSettingInt(self, key):
        """A working implementation for the xbmcaddon Addon class getSettingInt() method"""
        assert isinstance(key, basestring)
        return int(self.settings.get(key, 0))

    def getSettingNumber(self, key):
        """A working implementation for the xbmcaddon Addon class getSettingNumber() method"""
        assert isinstance(key, basestring)
        return float(self.settings.get(key, 0.0))

    @staticmethod
    def openSettings():
        """A stub implementation for the xbmcaddon Addon class openSettings() method"""

    def setSetting(self, key, value):
        """A stub implementation for the xbmcaddon Addon class setSetting() method"""
        assert isinstance(key, basestring)
        assert isinstance(value, basestring)
        self.settings[key] = value
        # NOTE: Disable actual writing as it is no longer needed for testing
        # with open('test/userdata/addon_settings.json', 'w') as fd:
        #     json.dump(filtered_settings, fd, sort_keys=True, indent=4)

    def setSettingBool(self, key, value):
        """A stub implementation for the xbmcaddon Addon class setSettingBool() method"""
        assert isinstance(key, basestring)
        assert isinstance(value, bool)
        self.settings[key] = value

    def setSettingInt(self, key, value):
        """A stub implementation for the xbmcaddon Addon class setSettingInt() method"""
        assert isinstance(key, basestring)
        assert isinstance(value, int)
        self.settings[key] = value

    def setSettingNumber(self, key, value):
        """A stub implementation for the xbmcaddon Addon class setSettingNumber() method"""
        assert isinstance(key, basestring)
        assert isinstance(value, float)
        self.settings[key] = value
