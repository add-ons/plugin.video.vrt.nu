# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

''' This file implements the Kodi xbmcgui module, either using stubs or alternative functionality '''

from __future__ import absolute_import, division, print_function, unicode_literals


class Dialog:
    ''' A reimplementation of the xbmcgui Dialog class '''

    def notification(self, heading='', message='', icon='', time=''):
        ''' A working implementation for the xbmcgui Dialog class notification() method '''
        print('[37;100mNOTIFICATION:[35;0m [%s] [35;0m%s[0m' % (heading, message))

    def ok(self, heading='', line1=''):
        ''' A stub implementation for the xbmcgui Dialog class ok() method '''
        return

    def yesno(self, heading='', line1=''):
        ''' A stub implementation for the xbmcgui Dialog class yesno() method '''
        return True


class ListItem:
    ''' A reimplementation of the xbmcgui ListItem class '''

    def __init__(self, label='', label2='', iconImage='', thumbnailImage='', path='', offscreen=False):
        ''' A stub constructor for the xbmcgui ListItem class '''
        self.label = label
        self.label2 = label2
        self.path = path

    def addContextMenuItems(self, items, replaceItems=False):
        ''' A stub implementation for the xbmcgui ListItem class addContextMenuItems() method '''
        return

    def setArt(self, key):
        ''' A stub implementation for the xbmcgui ListItem class setArt() method '''
        return

    def setContentLookup(self, enable):
        ''' A stub implementation for the xbmcgui ListItem class setContentLookup() method '''
        return

    def setInfo(self, type, infoLabels):  # pylint: disable=redefined-builtin
        ''' A stub implementation for the xbmcgui ListItem class setInfo() method '''
        return

    def setMimeType(self, mimetype):
        ''' A stub implementation for the xbmcgui ListItem class setMimeType() method '''
        return

    def setProperty(self, key, value):
        ''' A stub implementation for the xbmcgui ListItem class setProperty() method '''
        return

    def setSubtitles(self, subtitleFiles):
        ''' A stub implementation for the xbmcgui ListItem class setSubtitles() method '''
        return
