# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
''' This file implements the Kodi xbmc module, either using stubs or alternative functionality '''

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os
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
except OSError as e:
    print("Error using 'test/userdata/global_settings.json' : %s" % e, file=sys.stderr)
    GLOBAL_SETTINGS = {
        'locale.language': 'resource.language.en_gb',
        'network.bandwidth': 0,
    }

if 'PROXY_SERVER' in os.environ:
    GLOBAL_SETTINGS['network.usehttpproxy'] = 'true'
    GLOBAL_SETTINGS['network.httpproxytype'] = '0'
    print('Using proxy server from environment variable PROXY_SERVER')
    GLOBAL_SETTINGS['network.httpproxyserver'] = os.environ.get('PROXY_SERVER')
    if 'PROXY_PORT' in os.environ:
        print('Using proxy server from environment variable PROXY_PORT')
        GLOBAL_SETTINGS['network.httpproxyport'] = os.environ.get('PROXY_PORT')
    if 'PROXY_USERNAME' in os.environ:
        print('Using proxy server from environment variable PROXY_USERNAME')
        GLOBAL_SETTINGS['network.httpproxyusername'] = os.environ.get('PROXY_USERNAME')
    if 'PROXY_PASSWORD' in os.environ:
        print('Using proxy server from environment variable PROXY_PASSWORD')
        GLOBAL_SETTINGS['network.httpproxypassword'] = os.environ.get('PROXY_PASSWORD')
else:
    print('No proxy server being used')
    GLOBAL_SETTINGS['network.usehttpproxy'] = 'false'


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

    def play(self, item='', listitem=None, windowed=False, startpos=-1):
        ''' A stub implementation for the xbmc Player class play() method '''
        return

    def isPlaying(self):
        ''' A stub implementation for the xbmc Player class isPlaying() method '''
        return True

    def showSubtitles(self, bVisible):
        ''' A stub implementation for the xbmc Player class showSubtitles() method '''
        return


def executebuiltin(string, wait=False):  # pylint: disable=unused-argument
    ''' A stub implementation of the xbmc executebuiltin() function '''
    return


def executeJSONRPC(jsonrpccommand):
    ''' A reimplementation of the xbmc executeJSONRPC() function '''
    command = json.loads(jsonrpccommand)
    if command.get('method') == 'Settings.GetSettingValue':
        key = command.get('params').get('setting')
        print("Access global setting '{setting}'".format(setting=key), file=sys.stderr)
        return '{"id":1,"jsonrpc":"2.0","result":{"value":"%s"}}' % GLOBAL_SETTINGS.get(key)
    print("Error in executeJSONRPC, method '{method}' is not implemented".format(**command), file=sys.stderr)
    return '{"error":{"code":-1,"message":"Not implemented."},"id":1,"jsonrpc":"2.0"}'


def getCondVisibility(string):  # pylint: disable=unused-argument
    ''' A reimplementation of the xbmc getCondVisibility() function '''
    if string == 'system.platform.android':
        return False
    return True


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


def log(msg, level):
    ''' A reimplementation of the xbmc log() function '''
    print('[32;1m%s: [32;0m%s[0m' % (level, msg))


def setContent(self, content):
    ''' A stub implementation of the xbmc setContent() function '''
    return


def sleep(seconds):
    ''' A reimplementation of the xbmc sleep() function '''
    time.sleep(seconds)


def translatePath(path):
    ''' A stub implementation of the xbmc translatePath() function '''
    if path.startswith('special://home'):
        return path.replace('special://home', os.path.join(os.getcwd(), 'test/'))
    if path.startswith('special://profile'):
        return path.replace('special://profile', os.path.join(os.getcwd(), 'test/usedata/'))
    if path.startswith('special://userdata'):
        return path.replace('special://userdata', os.path.join(os.getcwd(), 'test/userdata/'))
    return path
