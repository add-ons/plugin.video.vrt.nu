# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

''' This is the actual VRT NU service entry point '''

from __future__ import absolute_import, division, unicode_literals

from vrtnu.kodiwrapper import KodiWrapper
from vrtnu.tokenresolver import TokenResolver
from xbmc import Monitor
from xbmcaddon import Addon


class VrtMonitor(Monitor):
    ''' This is the class that monitors Kodi for the VRT NU video plugin '''

    def __init__(self):
        ''' VRT Monitor initialisiation '''
        Monitor.__init__(self)

    def onSettingsChanged(self):
        ''' Handler for changes to settings '''
        addon = Addon(id='plugin.video.vrt.nu')
        kodi_wrapper = KodiWrapper(None, addon)
        kodi_wrapper.log_notice('VRT NU Addon: settings changed')
        TokenResolver(kodi_wrapper).reset_cookies()


if __name__ == '__main__':
    monitor = VrtMonitor()

    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            break
