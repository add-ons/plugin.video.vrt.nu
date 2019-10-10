# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
''' This is the actual VRT NU service entry point '''

# pylint: disable=non-parent-init-called,no-member,too-many-function-args

from __future__ import absolute_import, division, unicode_literals
from xbmc import Monitor
from kodiwrapper import KodiWrapper
from tokenresolver import TokenResolver


class VrtMonitor(Monitor):
    ''' This is the class that monitors Kodi for the VRT NU video plugin '''

    def __init__(self):
        ''' VRT Monitor initialisiation '''
        Monitor.__init__(self)
        while not self.abortRequested():
            if self.waitForAbort(10):
                break

    @staticmethod
    def onSettingsChanged():  # pylint: disable=invalid-name
        ''' Handler for changes to settings '''
        _kodi = KodiWrapper(None)
        _kodi.log('Settings changed')
        TokenResolver(_kodi).refresh_login()

        _kodi.invalidate_caches('continue-*.json', 'favorites.json', 'my-offline-*.json', 'my-recent-*.json', 'resume_points.json', 'watchlater-*.json')
        _kodi.container_refresh()
