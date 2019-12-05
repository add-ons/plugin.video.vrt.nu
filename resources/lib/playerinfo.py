# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
''' Implementation of PlayerInfo class '''

from __future__ import absolute_import, division, unicode_literals
from threading import Event, Thread
from xbmc import getInfoLabel, Player, PlayList
from apihelper import ApiHelper
from favorites import Favorites
from resumepoints import ResumePoints
from statichelper import play_url_to_id, to_unicode, url_to_episode
from kodiutils import addon_id, container_reload, get_setting, has_addon, log, notify


class PlayerInfo(Player):
    ''' Class for communication with Kodi player '''

    def __init__(self):
        ''' PlayerInfo initialisation '''
        self.resumepoints = ResumePoints()
        self.apihelper = ApiHelper(Favorites(), self.resumepoints)
        self.last_pos = None
        self.listen = False
        self.paused = False
        self.total = None
        self.positionthread = None
        self.quit = Event()

        self.asset_id = None
        self.path = None
        self.title = None
        self.ep_id = None
        self.url = None
        self.whatson_id = None
        from random import randint
        self.thread_id = randint(1, 10001)
        log(3, '[PlayerInfo %d] Initialized' % self.thread_id)
        Player.__init__(self)

    def onPlayBackStarted(self):  # pylint: disable=invalid-name
        ''' Called when user starts playing a file '''
        self.path = getInfoLabel('Player.Filenameandpath')
        if self.path.startswith('plugin://plugin.video.vrt.nu/'):
            self.listen = True
        else:
            self.listen = False
            return

        log(3, '[PlayerInfo %d] Event onPlayBackStarted' % self.thread_id)

        # Get asset_id, title and url from api
        ep_id = play_url_to_id(self.path)

        # Get episode data
        episode = self.apihelper.get_single_episode_data(video_id=ep_id.get('video_id'), whatson_id=ep_id.get('whatson_id'), video_url=ep_id.get('video_url'))

        self.asset_id = self.resumepoints.assetpath_to_id(episode.get('assetPath'))
        self.title = episode.get('program')
        self.url = url_to_episode(episode.get('url', ''))
        self.ep_id = 'S%sE%s' % (episode.get('seasonTitle'), episode.get('episodeNumber'))
        self.whatson_id = episode.get('whatsonId') if episode.get('whatsonId') else None
        self.update_position()
        self.update_total()

        # Reset VRT NU resumepoint
        self.push_position()

    def onAVStarted(self):  # pylint: disable=invalid-name
        ''' Called when Kodi has a video or audiostream '''
        if not self.listen:
            return
        log(3, '[PlayerInfo %d] Event onAVStarted' % self.thread_id)
        self.quit.clear()
        self.update_position()
        self.update_total()
        self.push_upnext()

        # StreamPosition thread keeps running when watching multiple episode with "Up Next"
        # only start StreamPosition thread when it doesn't exist yet.
        if not self.positionthread:
            self.positionthread = Thread(target=self.stream_position, name='StreamPosition')
            self.positionthread.start()

    def onAVChange(self):  # pylint: disable=invalid-name
        ''' Called when Kodi has a video, audio or subtitle stream. Also happens when the stream changes. '''

    def onPlayBackSeek(self, time, seekOffset):  # pylint: disable=invalid-name
        ''' Called when user seeks to a time '''
        if not self.listen:
            return
        log(3, '[PlayerInfo %d] Event onPlayBackSeek time=%d offset=%d' % (self.thread_id, time, seekOffset))
        self.last_pos = time // 1000

        # If we seek beyond the end, quit Player
        if self.last_pos >= self.total:
            self.quit.set()
            self.stop()

    def onPlayBackPaused(self):  # pylint: disable=invalid-name
        ''' Called when user pauses a playing file '''
        if not self.listen:
            return
        log(3, '[PlayerInfo %d] Event onPlayBackPaused' % self.thread_id)
        self.update_position()
        self.push_position(position=self.last_pos, total=self.total)
        self.paused = True

    def onPlayBackResumed(self):  # pylint: disable=invalid-name
        ''' Called when user resumes a paused file or a next playlist item is started '''
        if not self.listen:
            return
        suffix = 'after pausing' if self.paused else 'after playlist change'
        log(3, '[PlayerInfo %d] Event onPlayBackResumed %s' % (self.thread_id, suffix))
        if not self.paused:
            self.push_position(position=self.last_pos, total=self.total)
        self.paused = False

    def onPlayBackEnded(self):  # pylint: disable=invalid-name
        ''' Called when Kodi has ended playing a file '''
        if not self.listen:
            return
        self.quit.set()
        log(3, '[PlayerInfo %d] Event onPlayBackEnded' % self.thread_id)
        self.last_pos = self.total

    def onPlayBackError(self):  # pylint: disable=invalid-name
        ''' Called when playback stops due to an error '''
        if not self.listen:
            return
        self.quit.set()
        log(3, '[PlayerInfo %d] Event onPlayBackError' % self.thread_id)

    def onPlayBackStopped(self):  # pylint: disable=invalid-name
        ''' Called when user stops Kodi playing a file '''
        if not self.listen:
            return
        self.quit.set()
        log(3, '[PlayerInfo %d] Event onPlayBackStopped' % self.thread_id)

    def onThreadExit(self):  # pylint: disable=invalid-name
        ''' Called when player stops, before the player exited, so before the menu refresh '''
        log(3, '[PlayerInfo %d] Event onThreadExit' % self.thread_id)
        self.positionthread = None
        self.push_position(position=self.last_pos, total=self.total)

    def stream_position(self):
        ''' Get latest stream position while playing '''
        while self.isPlaying() and not self.quit.is_set():
            self.update_position()
            if self.quit.wait(timeout=0.2):
                break
        self.onThreadExit()

    def add_upnext(self, video_id):
        ''' Add Up Next url to Kodi Player '''
        url = 'plugin://plugin.video.vrt.nu/play/upnext/%s' % video_id
        self.update_position()
        self.update_total()
        if self.isPlaying() and self.total - self.last_pos < 1:
            log(3, '[PlayerInfo] %d Add %s to Kodi Playlist' % (self.thread_id, url))
            PlayList(1).add(url)
        else:
            log(3, '[PlayerInfo] %d Add %s to Kodi Player' % (self.thread_id, url))
            self.play(url)

    def push_upnext(self):
        ''' Push episode info to Up Next service add-on'''
        if has_addon('service.upnext') and get_setting('useupnext', 'true') == 'true':
            info_tag = self.getVideoInfoTag()
            next_info = self.apihelper.get_upnext(dict(
                program=to_unicode(info_tag.getTVShowTitle()),
                playcount=info_tag.getPlayCount(),
                rating=info_tag.getRating(),
                path=self.path,
                runtime=self.total,
            ))
            if next_info:
                from base64 import b64encode
                from json import dumps
                data = [to_unicode(b64encode(dumps(next_info).encode()))]
                sender = '%s.SIGNAL' % addon_id()
                notify(sender=sender, message='upnext_data', data=data)

    def update_position(self):
        ''' Update the player position, when possible '''
        try:
            self.last_pos = self.getTime()
        except RuntimeError:
            pass

    def update_total(self):
        ''' Update the total video time '''
        try:
            self.total = self.getTotalTime()
        except RuntimeError:
            pass

    def push_position(self, position=0, total=100):
        ''' Push player position to VRT NU resumepoints API '''
        # Not all content has an asset_id
        if not self.asset_id:
            return

        # Push resumepoint to VRT NU
        self.resumepoints.update(
            asset_id=self.asset_id,
            title=self.title,
            url=self.url,
            position=position,
            total=total,
            whatson_id=self.whatson_id,
            asynchronous=True
        )

        # Do not reload container and rely on Kodi internal watch status, when watching a single episode.
        # Kodi internal watch status is only updated when the play action is initiated from the GUI, so this only works for single episodes.
        if not self.path.startswith('plugin://plugin.video.vrt.nu/play/upnext'):
            return

        # Do not reload container when playing or not stopped
        if self.isPlaying() or not self.quit.is_set():
            return

        # A container reload is needed when watching multiple episodes with "Up Next", because Kodi doesn't update the last watched episode.
        # Only reload container we originated from this menu
        container_reload()
