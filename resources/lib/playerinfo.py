# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
''' Implementation of PlayerInfo class '''

from __future__ import absolute_import, division, unicode_literals
from threading import Thread
from xbmc import Monitor, Player, sleep
from statichelper import to_unicode


class PlayerInfo(Player):
    ''' Class for communication with Kodi player '''

    def __init__(self, **kwargs):
        ''' PlayerInfo initialisation '''
        self._info = kwargs['info']
        self._monitor = Monitor()
        self._tracker = None
        self._last_pos = 0
        self._total = None
        self._stop = False
        Player.__init__(self)

    def run(self):
        ''' Main loop '''
        while not self._monitor.abortRequested() and not self._stop:
            if self._monitor.waitForAbort(0.5):
                break

    def onAVStarted(self):  # pylint: disable=invalid-name
        ''' called when Kodi has a video or audiostream '''
        self._total = self.getTotalTime()
        self._tracker = Thread(target=self.stream_position, name='StreamPositionThread')
        self._tracker.start()
        tag = self.getVideoInfoTag()
        self._info(dict(
            season=tag.getSeason(),
            episode=tag.getEpisode(),
            program=to_unicode(tag.getTVShowTitle()),
            playcount=tag.getPlayCount(),
            rating=tag.getRating(),
            runtime=self._total,
        ))

    def onPlayBackStopped(self):  # pylint: disable=invalid-name
        ''' called when user stops Kodi playing a file '''
        self._info(dict(position=self._last_pos, total=self._total, event='playbackstopped'))
        self._stop = True

    def onAVChange(self):  # pylint: disable=invalid-name
        ''' called when Kodi has a video, audio or subtitle stream. Also happens when the stream changes. '''

    def onPlayBackEnded(self):  # pylint: disable=invalid-name
        ''' called when Kodi stops playing a file '''
        self._info(dict(position=self._total, total=self._total, event='playbackended'))
        self._stop = True

    def onPlayBackError(self):  # pylint: disable=invalid-name
        ''' called when playback stops due to an error '''
        self._info(dict(position=self._last_pos, total=self._total, event='playbackerror'))
        self._stop = True

    def onPlayBackPaused(self):  # pylint: disable=invalid-name
        ''' called when user pauses a playing file '''
        self._info(dict(position=self._last_pos, total=self._total, event='playbackpaused'))

    def onPlayBackResumed(self):  # pylint: disable=invalid-name
        '''called when user resumes a paused file '''

    def stream_position(self):
        ''' get latest stream position while playing '''
        while self.isPlaying():
            self._last_pos = self.getTime()
            sleep(500)
