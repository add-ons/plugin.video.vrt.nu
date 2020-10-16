# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""This is the actual VRT NU service entry point"""

from __future__ import absolute_import, division, unicode_literals
from xbmc import Monitor
from apihelper import ApiHelper
from favorites import Favorites
from kodiutils import container_refresh, invalidate_caches, log
from playerinfo import PlayerInfo
from resumepoints import ResumePoints
from tokenresolver import TokenResolver


class VrtMonitor(Monitor, object):  # pylint: disable=useless-object-inheritance
    """This is the class that monitors Kodi for the VRT NU video plugin"""

    def __init__(self):
        """VRT Monitor initialisation"""
        self._resumepoints = ResumePoints()
        self._playerinfo = None
        self._favorites = None
        self._apihelper = None
        self.init_watching_activity()
        super(VrtMonitor, self).__init__()

    def run(self):
        """Main loop"""
        while not self.abortRequested():
            if self.waitForAbort(10):
                break

    def init_watching_activity(self):
        """Only load components for watching activity when needed"""

        if self._resumepoints.is_activated():
            if not self._playerinfo:
                self._playerinfo = PlayerInfo()
            if not self._favorites:
                self._favorites = Favorites()
            if not self._apihelper:
                self._apihelper = ApiHelper(self._favorites, self._resumepoints)
        else:
            self._playerinfo = None

    def onSettingsChanged(self):  # pylint: disable=invalid-name
        """Handler for changes to settings"""

        log(1, 'Settings changed')
        TokenResolver().refresh_login()

        invalidate_caches('continue-*.json', 'favorites.json', 'my-offline-*.json', 'my-recent-*.json', 'resume_points.json', 'watchlater-*.json')

        # Init watching activity again when settings change
        self.init_watching_activity()

        # Refresh container when settings change
        container_refresh()
