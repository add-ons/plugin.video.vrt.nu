# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
''' Implementation of PlayerInfo class '''

from __future__ import absolute_import, division, unicode_literals
from threading import Event, Thread
from kodiutils import log
from xbmc import getInfoLabel, Player
from statichelper import to_unicode


class PlayerInfo(Player):
    ''' Class for communication with Kodi player '''

    def __init__(self, **kwargs):
        ''' PlayerInfo initialisation '''
        self._info = kwargs['info']
        self._path = None
        self._paused = False
        self._last_pos = None
        self._total = None
        self._stop = Event()
        from random import randint
        self._id = randint(1, 10001)
        log(2, '[PlayerInfo] %d initialized' % self._id)
        Player.__init__(self)

    def onAVStarted(self):  # pylint: disable=invalid-name
        ''' Called when Kodi has a video or audiostream '''
        log(2, '[PlayerInfo] %d onAVStarted' % self._id)
        self._stop.clear()
        self._last_pos = 0
        self._total = self.getTotalTime()
        self._path = getInfoLabel('Player.Filenameandpath')
        tag = self.getVideoInfoTag()
        self._info(dict(
            program=to_unicode(tag.getTVShowTitle()),
            playcount=tag.getPlayCount(),
            rating=tag.getRating(),
            path=self._path,
            runtime=self._total,
        ))
        Thread(target=self.stream_position, name='StreamPosition').start()

    def onPlayBackStopped(self):  # pylint: disable=invalid-name
        ''' Called when user stops Kodi playing a file '''
        log(2, '[PlayerInfo] %d onPlayBackStopped' % self._id)
        self._info(dict(path=self._path, position=self._last_pos, total=self._total, event='playbackstopped'))
        self._stop.set()

    def onAVChange(self):  # pylint: disable=invalid-name
        ''' Called when Kodi has a video, audio or subtitle stream. Also happens when the stream changes. '''

    def onPlayBackEnded(self):  # pylint: disable=invalid-name
        ''' Called when Kodi has ended playing a file '''
        log(2, '[PlayerInfo] %d onPlayBackEnded' % self._id)
        self._info(dict(path=self._path, position=self._total, total=self._total, event='playbackended'))
        self._stop.set()

    def onPlayBackError(self):  # pylint: disable=invalid-name
        ''' Called when playback stops due to an error '''
        log(2, '[PlayerInfo] %d onPlayBackError' % self._id)
        self._info(dict(path=self._path, position=self._last_pos, total=self._total, event='playbackerror'))
        self._stop.set()

    def onPlayBackPaused(self):  # pylint: disable=invalid-name
        ''' Called when user pauses a playing file '''
        log(2, '[PlayerInfo] %d onPlayBackPaused' % self._id)
        self._paused = True
        self._info(dict(path=self._path, position=self._last_pos, total=self._total, event='playbackpaused'))

    def onPlayBackResumed(self):  # pylint: disable=invalid-name
        '''called when user resumes a paused file or a next playlist item is started '''
        suffix = 'after pausing' if self._paused else 'after playlist change'
        log(2, '[PlayerInfo] %d onPlayBackResumed %s' % (self._id, suffix))
        if not self._paused:
            self._info(dict(path=self._path, position=self._last_pos, total=self._total, event='playbackresumed'))
        self._paused = False

    def stream_position(self):
        ''' get latest stream position while playing '''
        while self.isPlaying() and not self._stop.is_set():
            self._last_pos = self.getTime()
            if self._stop.wait(timeout=0.5):
                break
        log(2, '[PlayerInfo] %d stream position loop exited' % self._id)
