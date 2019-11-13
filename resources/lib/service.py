# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
''' This is the actual VRT NU service entry point '''

# pylint: disable=non-parent-init-called,no-member,too-many-function-args

from __future__ import absolute_import, division, unicode_literals
from xbmc import Monitor
from apihelper import ApiHelper
from favorites import Favorites
from kodiwrapper import KodiWrapper
from playerinfo import PlayerInfo
from resumepoints import ResumePoints
from statichelper import play_url_to_id, to_unicode, url_to_episode
from tokenresolver import TokenResolver


class VrtMonitor(Monitor):
    ''' This is the class that monitors Kodi for the VRT NU video plugin '''

    def __init__(self):
        ''' VRT Monitor initialisiation '''
        self._kodi = KodiWrapper(None)
        self._resumepoints = ResumePoints(self._kodi)
        self._container = None
        self._playerinfo = None
        self._favorites = None
        self._apihelper = None
        self.init_watching_activity()
        Monitor.__init__(self)

    def run(self):
        ''' Main loop '''
        while not self.abortRequested():
            if self.waitForAbort(10):
                break

    def init_watching_activity(self):
        ''' Only load components for watching activity when needed '''

        if self._resumepoints.is_activated():
            if not self._playerinfo:
                self._playerinfo = PlayerInfo(info=self.handle_info)
            if not self._favorites:
                self._favorites = Favorites(self._kodi)
            if not self._apihelper:
                self._apihelper = ApiHelper(self._kodi, self._favorites, self._resumepoints)

    def onNotification(self, sender, method, data):  # pylint: disable=invalid-name
        ''' Handler for notifications '''
        self._kodi.log(2, '[Notification] sender={sender}, method={method}, data={data}', sender=sender, method=method, data=to_unicode(data))
        if method.endswith('source_container'):
            import json
            self._container = json.loads(data).get('container')
            return

        if not sender.startswith('upnextprovider'):
            return
        if not method.endswith('plugin.video.vrt.nu_play_action'):
            return

        import json
        hexdata = json.loads(data)

        if not hexdata:
            return

        from binascii import unhexlify
        data = json.loads(unhexlify(hexdata[0]))
        self._kodi.log(2, '[Up Next notification] sender={sender}, method={method}, data={data}', sender=sender, method=method, data=to_unicode(data))
        self._kodi.jsonrpc(method='Player.Open', params=dict(item=dict(file='plugin://plugin.video.vrt.nu/play/whatson/%s' % data.get('whatson_id'))))

    def onSettingsChanged(self):  # pylint: disable=invalid-name
        ''' Handler for changes to settings '''

        self._kodi.log(1, 'Settings changed')
        TokenResolver(self._kodi).refresh_login()

        self._kodi.invalidate_caches('continue-*.json', 'favorites.json', 'my-offline-*.json', 'my-recent-*.json', 'resume_points.json', 'watchlater-*.json')

        # Init watching activity again when settings change
        self.init_watching_activity()

        # Refresh container when settings change
        self._kodi.container_refresh()

    def handle_info(self, info):
        ''' Handle information from PlayerInfo class '''
        self._kodi.log(2, 'Got VRT NU Player info: {info}', info=str(info))

        # Push resume position
        if info.get('position'):
            self.push_position(info)

        # Push up next episode info
        if info.get('program'):
            self.push_upnext(info)

    def push_position(self, info):
        ''' Push player position to VRT NU resumepoints API '''
        # Get uuid, title and url from api based on video.get('publication_id') or video.get('video_url')
        ep_id = play_url_to_id(info.get('path'))

        if ep_id.get('video_id'):
            episode = self._apihelper.get_episodes(video_id=ep_id.get('video_id'), variety='single')[0]
        elif ep_id.get('whatson_id'):
            episode = self._apihelper.get_episodes(whatson_id=ep_id.get('whatson_id'), variety='single')[0]
        elif ep_id.get('video_url'):
            episode = self._apihelper.get_episodes(video_url=ep_id.get('video_url'), variety='single')[0]

        uuid = self._resumepoints.assetpath_to_uuid(episode.get('assetPath'))
        title = episode.get('program')
        url = url_to_episode(episode.get('url', ''))
        # Push resumepoint to VRT NU
        self._resumepoints.update(uuid=uuid, title=title, url=url, watch_later=None, position=info.get('position'), total=info.get('total'))
        # Only update container if the play action was initiated from it
        current_container = self._kodi.current_container_url()
        self._kodi.log(2, '[PlayerPosition] resumepoint update {info} {container}', info=episode.get('title'), container=current_container)
        if current_container is None or self._container == current_container:
            self._kodi.log(2, '[PlayerPosition] update container {info}', info=self._container)
            self._kodi.container_update(self._container)

    def push_upnext(self, info):
        ''' Push episode info to Up Next service add-on'''
        if self._kodi.has_addon('service.upnext') and self._kodi.get_setting('useupnext', 'true') == 'true':
            next_info = self._apihelper.get_upnext(info)
            if next_info:
                from binascii import hexlify
                import json
                data = [to_unicode(hexlify(json.dumps(next_info).encode()))]
                sender = '%s.SIGNAL' % self._kodi.addon_id()
                self._kodi.notify(sender=sender, message='upnext_data', data=data)
