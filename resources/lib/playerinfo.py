# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
''' Implementation of PlayerInfo class '''

from __future__ import absolute_import, division, unicode_literals
from threading import Event, Thread
from kodiutils import (addon_id, current_container_url, container_update, get_property, get_setting, has_addon, log, notify)
from xbmc import getInfoLabel, Player
from statichelper import play_url_to_id, to_unicode, url_to_episode
from apihelper import ApiHelper
from favorites import Favorites
from resumepoints import ResumePoints
from data import SECONDS_MARGIN


class PlayerInfo(Player):
    ''' Class for communication with Kodi player '''

    def __init__(self):
        ''' PlayerInfo initialisation '''
        self.path = None
        self.resumepoints = ResumePoints()
        self.apihelper = ApiHelper(Favorites(), self.resumepoints)
        self.paused = False
        self.last_pos = None
        self.total = 900
        self.stop = Event()
        self.asset_id = None
        self.title = None
        self.url = None
        self.whatson_id = None
        from random import randint
        self.thread_id = randint(1, 10001)
        log(3, '[PlayerInfo] %d initialized' % self.thread_id)
        Player.__init__(self)

    def onPlayBackStarted(self):  # pylint: disable=invalid-name
        ''' Called when user starts playing a file '''
        # Get asset_id, title and url from api
        self.path = getInfoLabel('Player.Filenameandpath')
        ep_id = play_url_to_id(self.path)

        if ep_id.get('video_id'):
            episode = self.apihelper.get_episodes(video_id=ep_id.get('video_id'), variety='single')[0]
        elif ep_id.get('whatson_id'):
            episode = self.apihelper.get_episodes(whatson_id=ep_id.get('whatson_id'), variety='single')[0]
        elif ep_id.get('video_url'):
            episode = self.apihelper.get_episodes(video_url=ep_id.get('video_url'), variety='single')[0]

        self.asset_id = self.resumepoints.assetpath_to_id(episode.get('assetPath'))
        self.title = episode.get('program')
        self.url = url_to_episode(episode.get('url', ''))
        self.whatson_id = episode.get('whatsonId')

    def onAVStarted(self):  # pylint: disable=invalid-name
        ''' Called when Kodi has a video or audiostream '''
        log(3, '[PlayerInfo] %d onAVStarted' % self.thread_id)
        self.stop.clear()
        self.last_pos = 0
        self.total = self.getTotalTime()
        self.push_upnext()
        Thread(target=self.stream_position, name='StreamPosition').start()

    def onAVChange(self):  # pylint: disable=invalid-name
        ''' Called when Kodi has a video, audio or subtitle stream. Also happens when the stream changes. '''

    def onPlayBackSeek(self, time, seekOffset):  # pylint: disable=invalid-name
        ''' Called when user seeks to a time '''
        log(3, '[PlayerInfo] %d onPlayBackSeek time=%d offset=%d' % (self.thread_id, time, seekOffset))
        self.last_pos = time // 1000

    def onPlayBackPaused(self):  # pylint: disable=invalid-name
        ''' Called when user pauses a playing file '''
        log(3, '[PlayerInfo] %d onPlayBackPaused' % self.thread_id)
        self.paused = True
        self.push_position(position=self.last_pos, total=self.total)

    def onPlayBackResumed(self):  # pylint: disable=invalid-name
        ''' Called when user resumes a paused file or a next playlist item is started '''
        suffix = 'after pausing' if self.paused else 'after playlist change'
        log(3, '[PlayerInfo] %d onPlayBackResumed %s' % (self.thread_id, suffix))
        if not self.paused:
            self.push_position(position=self.last_pos, total=self.total)
        self.paused = False

    def onPlayBackEnded(self):  # pylint: disable=invalid-name
        ''' Called when Kodi has ended playing a file '''
        log(3, '[PlayerInfo] %d onPlayBackEnded' % self.thread_id)
        self.push_position(position=self.total, total=self.total)
        self.stop.set()

    def onPlayBackError(self):  # pylint: disable=invalid-name
        ''' Called when playback stops due to an error '''
        log(3, '[PlayerInfo] %d onPlayBackError' % self.thread_id)
        self.push_position(position=self.last_pos, total=self.total)
        self.stop.set()

    def onPlayBackStopped(self):  # pylint: disable=invalid-name
        ''' Called when user stops Kodi playing a file '''
        log(3, '[PlayerInfo] %d onPlayBackStopped' % self.thread_id)
        self.push_position(position=self.last_pos, total=self.total)
        self.stop.set()

    def onThreadExit(self):  # pylint: disable=invalid-name
        ''' Called when player stops, before the player exited, so before the menu refresh '''
        log(3, '[PlayerInfo] %d onThreadExit' % self.thread_id)

    def stream_position(self):
        ''' Get latest stream position while playing '''
        while self.isPlaying() and not self.stop.is_set():
            self.last_pos = self.getTime()
            if self.stop.wait(timeout=0.5):
                break
        self.onThreadExit()

    def push_upnext(self):
        ''' Push episode info to Up Next service add-on'''
        if has_addon('service.upnext') and get_setting('useupnext', 'true') == 'true':
            tag = self.getVideoInfoTag()
            info = dict(
                program=to_unicode(tag.getTVShowTitle()),
                playcount=tag.getPlayCount(),
                rating=tag.getRating(),
                path=self.path,
                runtime=self.total,
            )
            next_info = self.apihelper.get_upnext(info)
            if next_info:
                from base64 import b64encode
                from json import dumps
                data = [to_unicode(b64encode(dumps(next_info).encode()))]
                sender = '%s.SIGNAL' % addon_id()
                notify(sender=sender, message='upnext_data', data=data)

    def push_position(self, position=0, total=100):
        ''' Push player position to VRT NU resumepoints API '''
        # Push resumepoint to VRT NU
        self.resumepoints.update(
            asset_id=self.asset_id,
            title=self.title,
            url=self.url,
            watch_later=None,
            position=position,
            total=total,
            whatson_id=self.whatson_id,
            asynchronous=True
        )
        # Refresh Kodi watch status only needed after playing Up Next episodes
        # or to overwrite watched/unwatched
        if ((self.path and self.path.startswith('plugin://plugin.video.vrt.nu/play/upnext/'))
                or SECONDS_MARGIN > position or position > total - SECONDS_MARGIN):
            # Only update container if the play action was initiated from it
            original_container = get_property('container.url')
            current_container = current_container_url()
            if current_container is None or current_container == original_container:
                log(3, '[PlayerInfo] %d Reload container' % self.thread_id)
                container_update(original_container)
