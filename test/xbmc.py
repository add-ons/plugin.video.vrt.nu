# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

''' This file implements the Kodi xbmc module, either using stubs or alternative functionality '''

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import json
import time
import polib


LOGDEBUG = 'Debug'
LOGERROR = 'Error'
LOGNOTICE = 'Notice'

INFO_LABELS = {
    'System.BuildVersion': '18.2',
}

PO = polib.pofile('resources/language/resource.language.en_gb/strings.po')

REGIONS = {
    'datelong': '%A, %e %B %Y',
    'dateshort': '%Y-%m-%d',
}

# Use the global_settings file
try:
    with open('test/userdata/global_settings.json') as f:
        GLOBAL_SETTINGS = json.load(f)
except Exception as e:
    print("Error using 'test/userdata/global_settings.json' : %s" % e, file=sys.stderr)
    GLOBAL_SETTINGS = {
        'locale.language': 'resource.language.en_gb',
        'network.bandwidth': 0,
    }


class Keyboard:
    ''' A stub implementation of the xbmc Keyboard class '''

    def __init__(self, line='', heading=''):
        ''' A stub constructor for the xbmc Keyboard class '''

    def doModal(self, autoclose=0):
        ''' A stub implementation for the xbmc Keyboard class doModal() method '''

    def isConfirmed(self):
        ''' A stub implementation for the xbmc Keyboard class isConfirmed() method '''
        return True

    def getText(self):
        ''' A stub implementation for the xbmc Keyboard class getText() method '''
        return 'unittest'


class Monitor:
    ''' A stub implementation of the xbmc Monitor class '''

    def abortRequested(self):
        ''' A stub implementation for the xbmc Keyboard class abortRequested() method '''
        return

    def waitForAbort(self):
        ''' A stub implementation for the xbmc Keyboard class waitForAbort() method '''
        return


class Player:
    ''' A stub implementation of the xbmc Player class '''

    def isPlaying(self):
        ''' A stub implementation for the xbmc Player class isPlaying() method '''
        return True

    def showSubtitles(self, bVisible):
        ''' A stub implementation for the xbmc Player class showSubtitles() method '''
        return


def executebuiltin(s):
    ''' A stub implementation of the xbmc executebuiltin() function '''
    return


def executeJSONRPC(jsonrpccommand):
    ''' A reimplementation of the xbmc executeJSONRPC() function '''
    command = json.loads(jsonrpccommand)
    if command.get('method') == 'Settings.GetSettingValue':
        key = command.get('params').get('setting')
        return '{"id":1,"jsonrpc":"2.0","result":{"value":"%s"}}' % GLOBAL_SETTINGS.get(key)
    return 'executeJSONRPC'


def getCondVisibility(s):
    ''' A reimplementation of the xbmc getCondVisibility() function '''
    return 1


def getInfoLabel(key):
    ''' A reimplementation of the xbmc getInfoLabel() function '''
    return INFO_LABELS.get(key)


def getLocalizedString(msgctxt):
    ''' A reimplementation of the xbmc getLocalizedString() function '''
    for entry in PO:
        if entry.msgctxt == '#%s' % msgctxt:
            return entry.msgstr or entry.msgid
    return 'smurf'


def getRegion(key):
    ''' A reimplementation of the xbmc getRegion() function '''
    return REGIONS.get(key)


def setContent(self, content):
    ''' A stub implementation of the xbmc setContent() function '''
    return


def sleep(seconds):
    ''' A reimplementation of the xbmc sleep() function '''
    time.sleep(seconds)


def translatePath(path):
    ''' A stub implementation of the xbmc translatePath() function '''
    return path


def log(msg, level):
    ''' A reimplementation of the xbmc log() function '''
    print('[32;1m%s: [32;0m%s[0m' % (level, msg))
