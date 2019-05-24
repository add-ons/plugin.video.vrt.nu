# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function, unicode_literals


class Dialog:
    def notification(self, heading='', message='', icon='', time=''):
        print('GUI NOTIFICATION: [%s] %s' % (heading, message))

    def ok(self, heading='', line1=''):
        return

    def yesno(self, heading='', line1=''):
        return True


class ListItem:
    def __init__(self, label='', label2='', iconImage='', thumbnailImage='', path='', offScreen=False):
        return

    def addContextMenuItems(self, items, replaceItems=False):
        return

    def setArt(self, key):
        return

    def setContentLookup(self, enable):
        return

    def setInfo(self, type, infoLabels):  # pylint: disable=redefined-builtin
        return

    def setMimeType(self, mimetype):
        return

    def setProperty(self, key, value):
        return

    def setSubtitles(self, subtitleFiles):
        return
