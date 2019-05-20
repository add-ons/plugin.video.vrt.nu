# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function, unicode_literals

import json
import polib
import time


LOGERROR = 'Error'
LOGNOTICE = 'Notice'

GLOBAL_SETTINGS = {
    'locale.language': 'resource.language.en_gb',
    'network.bandwidth': 0,
}

INFO_LABELS = {
    'System.BuildVersion': '18.2',
}

PO = polib.pofile('resources/language/resource.language.en_gb/strings.po')

REGIONS = {
    'datelong': '%A, %e %B %Y',
    'dateshort': '%Y-%m-%d',
}


class Keyboard():
    pass


class Monitor():
    def abortRequested(self):
        return

    def waitForAbort(self):
        return


class Player():
    pass


def executebuiltin(s):
    return


def executeJSONRPC(jsonrpccommand):
    command = json.loads(jsonrpccommand)
    if command.get('method') == 'Settings.GetSettingValue':
        key = command.get('params').get('setting')
        return '{"id":1,"jsonrpc":"2.0","result":{"value":"%s"}}' % GLOBAL_SETTINGS.get(key)
    return 'executeJSONRPC'


def getCondVisibility(s):
    return 1


def getInfoLabel(key):
    return INFO_LABELS.get(key)


def getLocalizedString(msgctxt):
    for entry in PO:
        if entry.msgctxt == '#%s' % msgctxt:
            return entry.msgstr or entry.msgid
    return 'vrttest'


def getRegion(key):
    return REGIONS.get(key)


def setContent(self, content):
    return


def sleep(seconds):
    time.sleep(seconds)


def translatePath(path):
    return path


def log(msg, level):
    print('%s: %s' % (level, msg))
