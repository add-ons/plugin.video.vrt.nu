# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
''' Implementation of PlayerInfo class '''

from __future__ import absolute_import, division, unicode_literals
from threading import Thread
from xbmc import Monitor, Player, sleep


class PlayerInfo(Player):
    ''' Class for communication with Kodi player '''

    def __init__(self, **kwargs):
        ''' PlayerInfo initialisation '''
        self._info = kwargs['position']
        self._monitor = Monitor()
        self._tracker = None
        self._last_pos = 0
        self._total = None
        Player.__init__(self)
        while not self._monitor.abortRequested():
            if self._monitor.waitForAbort(10):
                break

    def onAVStarted(self):  # pylint: disable=invalid-name
        ''' called when Kodi has a video or audiostream '''
        self._total = self.getTotalTime()
        self._tracker = Thread(target=self.stream_position)
        self._tracker.start()

    def onPlayBackStopped(self):  # pylint: disable=invalid-name
        ''' called when user stops Kodi playing a file '''
        self._info((self._last_pos, self._total))

    def onAVChange(self):  # pylint: disable=invalid-name
        ''' called when Kodi has a video, audio or subtitle stream. Also happens when the stream changes. '''

    def onPlayBackEnded(self):  # pylint: disable=invalid-name
        ''' called when Kodi stops playing a file '''
        self._info((self._total, self._total))

    def onPlayBackError(self):  # pylint: disable=invalid-name
        ''' called when playback stops due to an error '''

    def onPlayBackPaused(self):  # pylint: disable=invalid-name
        ''' called when user pauses a playing file '''
        self._info((self._last_pos, self._total))

    def onPlayBackResumed(self):  # pylint: disable=invalid-name
        '''called when user resumes a paused file '''

    def stream_position(self):
        ''' get latest stream position while playing '''
        while self.isPlaying():
            self._last_pos = self.getTime()
            sleep(100)
