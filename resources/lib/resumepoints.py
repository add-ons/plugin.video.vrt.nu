# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
''' Implementation of ResumePoints class '''

from __future__ import absolute_import, division, unicode_literals

try:  # Python 3
    from urllib.error import HTTPError
    from urllib.request import build_opener, install_opener, ProxyHandler, Request, urlopen
except ImportError:  # Python 2
    from urllib2 import build_opener, HTTPError, install_opener, ProxyHandler, Request, urlopen

from data import SECONDS_MARGIN
from kodiutils import (container_refresh, get_cache, get_proxies, get_setting,
                       get_url_json, has_credentials, input_down, invalidate_caches, localize, log,
                       log_error, notification, update_cache)


class ResumePoints:
    ''' Track, cache and manage VRT resume points and watch list '''

    def __init__(self):
        ''' Initialize resumepoints, relies on XBMC vfs and a special VRT token '''
        self._data = dict()  # Our internal representation
        install_opener(build_opener(ProxyHandler(get_proxies())))

    @staticmethod
    def is_activated():
        ''' Is resumepoints activated in the menu and do we have credentials ? '''
        return get_setting('useresumepoints') == 'true' and has_credentials()

    @staticmethod
    def resumepoint_headers(url=None):
        ''' Generate http headers for VRT NU Resumepoints API '''
        from tokenresolver import TokenResolver
        xvrttoken = TokenResolver().get_xvrttoken(token_variant='user')
        headers = dict()
        if xvrttoken:
            url = 'https://www.vrt.be' + url if url else 'https://www.vrt.be/vrtnu'
            headers = {
                'authorization': 'Bearer ' + xvrttoken,
                'content-type': 'application/json',
                'Referer': url,
            }
        return headers

    def refresh(self, ttl=None):
        ''' Get a cached copy or a newer resumepoints from VRT, or fall back to a cached file '''
        if not self.is_activated():
            return
        resumepoints_json = get_cache('resume_points.json', ttl)
        if not resumepoints_json:
            resumepoints_url = 'https://video-user-data.vrt.be/resume_points'
            resumepoints_json = get_url_json(url=resumepoints_url, cache='resume_points.json', headers=self.resumepoint_headers())
        if resumepoints_json is not None:
            self._data = resumepoints_json

    def update(self, asset_id, title, url, watch_later=None, position=None, total=None, whatson_id=None, asynchronous=False):
        ''' Set program resumepoint or watchLater status and update local copy '''
        log(3, "[Resumepoints] Update resumepoint '{asset_id}' {position}/{total}", asset_id=asset_id, position=position, total=total)
        # The video has no assetPath, so we cannot update resumepoints
        if asset_id is None:
            return True

        # Survive any recent updates
        self.refresh(ttl=5)

        # Disable watch_later when completely watched
        if position is not None and total is not None and position >= total - SECONDS_MARGIN:
            watch_later = False

        if watch_later is not None and position is None and total is None and watch_later is self.is_watchlater(asset_id):
            # watchLater status is not changed, nothing to do
            return True

        if watch_later is None and position == self.get_position(asset_id) and total == self.get_total(asset_id):
            # Resumepoint is not changed, nothing to do
            return True

        # Preserve watchLater status if not set
        if watch_later is None:
            watch_later = self.is_watchlater(asset_id)

        # Check if there is still a need to keep this entry
        if not watch_later:
            if position is None and total is None:
                return self.delete(asset_id, watch_later, asynchronous=asynchronous)
            if not self.still_watching(position, total):
                return self.delete(asset_id, watch_later, asynchronous=asynchronous)

        from utils import reformat_url
        url = reformat_url(url, 'short')

        if asset_id in self._data:
            # Update existing resumepoint values
            payload = self._data[asset_id]['value']
            payload['url'] = url
        else:
            # Create new resumepoint values
            payload = dict(url=url, position=0, total=100, watchLater=watch_later)

        if position is not None:
            payload['position'] = position

        if total is not None:
            payload['total'] = total

        if whatson_id is not None:
            payload['whatsonId'] = whatson_id

        removes = []
        if position is not None or total is not None:
            removes.append('continue-*.json')

        if watch_later is not None:
            # Add watchLater status to payload
            payload['watchLater'] = watch_later
            removes.append('watchlater-*.json')

        # NOTE: Updates to resumepoints take a longer time to take effect, so we keep our own cache and use it
        self._data[asset_id] = dict(value=payload)
        from json import dumps
        update_cache('resume_points.json', dumps(self._data))
        invalidate_caches(*removes)

        if asynchronous:
            from threading import Thread
            Thread(target=self.update_online, name='ResumePointsUpdate', args=(asset_id, title, url, payload)).start()
            return True
        return self.update_online(asset_id, title, url, payload)

    def update_online(self, asset_id, title, url, payload):
        ''' Update resumepoint online '''
        from json import dumps
        try:
            get_url_json('https://video-user-data.vrt.be/resume_points/%s' % asset_id, headers=self.resumepoint_headers(url), data=dumps(payload).encode())
        except HTTPError as exc:
            log_error('Failed to (un)watch episode {title} at VRT NU ({error})', title=title, error=exc)
            notification(message=localize(30977, title=title))
            return False
        return True

    def delete(self, asset_id, watch_later, asynchronous=False):
        ''' Remove an entry from resumepoints '''
        # Do nothing if there is no resumepoint for this asset_id
        if not self._data.get(asset_id):
            log(3, "[Resumepoints] '{asset_id}' not present, nothing to delete", asset_id=asset_id)
            return True

        log(3, "[Resumepoints] Remove '{asset_id}' from resumepoints", asset_id=asset_id)
        # Delete local representation and update cache
        try:
            del self._data[asset_id]
            from json import dumps
            update_cache('resume_points.json', dumps(self._data))
        except KeyError:
            pass

        if watch_later is False:
            self.refresh_watchlater()

        self.refresh_continuewatching()

        if asynchronous:
            from threading import Thread
            Thread(target=self.delete_online, name='ResumePointsDelete', args=(asset_id,)).start()
            return True
        return self.delete_online(asset_id)

    def delete_online(self, asset_id):
        ''' Delete resumepoint online '''
        req = Request('https://video-user-data.vrt.be/resume_points/%s' % asset_id, headers=self.resumepoint_headers())
        req.get_method = lambda: 'DELETE'
        try:
            urlopen(req)
        except HTTPError as exc:
            log_error("Failed to remove '{asset_id}' from resumepoints: {error}", asset_id=asset_id, error=exc)
            return False
        return True

    @staticmethod
    def refresh_watchlater():
        ''' Refresh Watch Later menu '''
        invalidate_caches('watchlater-*.json')
        container_refresh()

    @staticmethod
    def refresh_continuewatching():
        ''' Refresh Continue Watching menu '''
        invalidate_caches('continue-*.json')
        container_refresh()

    def is_watchlater(self, asset_id):
        ''' Is a program set to watch later ? '''
        return self._data.get(asset_id, {}).get('value', {}).get('watchLater') is True

    def watchlater(self, asset_id, title, url):
        ''' Watch an episode later '''
        succeeded = self.update(asset_id=asset_id, title=title, url=url, watch_later=True)
        if succeeded:
            notification(message=localize(30403, title=title))
            container_refresh()

    def unwatchlater(self, asset_id, title, url, move_down=False):
        ''' Unwatch an episode later '''
        succeeded = self.update(asset_id=asset_id, title=title, url=url, watch_later=False)
        if succeeded:
            notification(message=localize(30404, title=title))
            # If the current item is selected and we need to move down before removing
            if move_down:
                input_down()
            container_refresh()

    def get_position(self, asset_id):
        ''' Return the stored position of a video '''
        return self._data.get(asset_id, {}).get('value', {}).get('position', 0)

    def get_total(self, asset_id):
        ''' Return the stored total length of a video '''
        return self._data.get(asset_id, {}).get('value', {}).get('total', 100)

    def get_url(self, asset_id, url_type='medium'):
        ''' Return the stored url a video '''
        from utils import reformat_url
        return reformat_url(self._data.get(asset_id, {}).get('value', {}).get('url'), url_type)

    def watchlater_urls(self):
        ''' Return all watchlater urls '''
        return [self.get_url(asset_id) for asset_id in self._data if self.is_watchlater(asset_id)]

    def resumepoints_urls(self):
        ''' Return all urls that have not been finished watching '''
        return [self.get_url(asset_id) for asset_id in self._data
                if SECONDS_MARGIN < self.get_position(asset_id) < (self.get_total(asset_id) - SECONDS_MARGIN)]

    @staticmethod
    def still_watching(position, total):
        ''' Determine if the video is still being watched '''

        if position <= SECONDS_MARGIN:
            return False

        if position >= total - SECONDS_MARGIN:
            return False

        return True
