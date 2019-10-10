# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
''' Implementation of ResumePoints class '''

from __future__ import absolute_import, division, unicode_literals

try:  # Python 3
    from urllib.error import HTTPError
    from urllib.request import build_opener, install_opener, ProxyHandler, Request, urlopen
except ImportError:  # Python 2
    from urllib2 import build_opener, install_opener, ProxyHandler, Request, HTTPError, urlopen


class ResumePoints:
    ''' Track, cache and manage VRT resume points and watch list '''

    def __init__(self, _kodi):
        ''' Initialize resumepoints, relies on XBMC vfs and a special VRT token '''
        self._kodi = _kodi
        self._proxies = _kodi.get_proxies()
        install_opener(build_opener(ProxyHandler(self._proxies)))
        # This is our internal representation
        self._resumepoints = dict()

    def is_activated(self):
        ''' Is resumepoints activated in the menu and do we have credentials ? '''
        return self._kodi.get_setting('useresumepoints') == 'true' and self._kodi.credentials_filled_in()

    def refresh(self, ttl=None):
        ''' Get a cached copy or a newer resumepoints from VRT, or fall back to a cached file '''
        if not self.is_activated():
            return
        resumepoints_json = self._kodi.get_cache('resume_points.json', ttl)
        if not resumepoints_json:
            from tokenresolver import TokenResolver
            xvrttoken = TokenResolver(self._kodi).get_xvrttoken(token_variant='user')
            if xvrttoken:
                headers = {
                    'authorization': 'Bearer ' + xvrttoken,
                    'content-type': 'application/json',
                    'Referer': 'https://www.vrt.be/vrtnu',
                }
                req = Request('https://video-user-data.vrt.be/resume_points', headers=headers)
                self._kodi.log('URL post: https://video-user-data.vrt.be/resume_points', 'Verbose')
                import json
                try:
                    resumepoints_json = json.load(urlopen(req))
                except Exception:  # pylint: disable=broad-except
                    # Force resumepoints from cache
                    resumepoints_json = self._kodi.get_cache('resume_points.json', ttl=None)
                else:
                    self._kodi.update_cache('resume_points.json', resumepoints_json)
        if resumepoints_json:
            self._resumepoints = resumepoints_json

    def update(self, uuid, title, url, watch_later=None, position=None, total=None):
        ''' Set program resumepoint or watchLater status and update local copy '''
        removes = []
        self.refresh(ttl=0)

        # The video has no assetPath, so we cannot update resumepoints
        if uuid is None:
            return True

        if position is not None and position >= total - 30:
            watch_later = False

        if watch_later is not None and position is None and total is None and watch_later is self.is_watchlater(uuid):
            # watchLater status is not changed, nothing to do
            return True

        if watch_later is None and position == self.get_position(uuid) and total == self.get_total(uuid):
            # resumepoint is not changed, nothing to do
            return True

        # Collect header info for POST Request
        from tokenresolver import TokenResolver
        xvrttoken = TokenResolver(self._kodi).get_xvrttoken(token_variant='user')
        if xvrttoken is None:
            self._kodi.log_error('Failed to get usertoken from VRT NU')
            self._kodi.show_notification(message=self._kodi.localize(30975) + title)
            return False

        headers = {
            'authorization': 'Bearer ' + xvrttoken,
            'content-type': 'application/json',
            'Referer': 'https://www.vrt.be' + url,
        }

        if uuid in self._resumepoints:
            # Update existing resumepoint values
            payload = self._resumepoints[uuid]['value']
            payload['url'] = url
        else:
            # Create new resumepoint values
            payload = dict(position=0, total=100, url=url, watchLater=False)

        if position is not None:
            payload['position'] = position

        if total is not None:
            payload['total'] = total

        if position is not None or total is not None:
            removes.append('continue-*.json')

        if watch_later is not None:
            # Add watchLater status to payload
            payload['watchLater'] = watch_later
            removes.append('watchlater-*.json')

        import json
        data = json.dumps(payload).encode()
        self._kodi.log('URL post: https://video-user-data.vrt.be/resume_points/{uuid}', 'Verbose', uuid=uuid)
        self._kodi.log('URL post data:: {data}', 'Verbose', data=data)
        try:
            req = Request('https://video-user-data.vrt.be/resume_points/%s' % uuid, data=data, headers=headers)
            urlopen(req)
        except HTTPError as exc:
            self._kodi.log_error('Failed to (un)watch episode at VRT NU (%s)' % exc)
            self._kodi.show_notification(message=self._kodi.localize(30977))
            return False

        # NOTE: Updates to resumepoints take a longer time to take effect, so we keep our own cache and use it
        self._resumepoints[uuid] = dict(value=payload)
        self._kodi.update_cache('resume_points.json', self._resumepoints)
        self._kodi.invalidate_caches(*removes)
        return True

    def is_watchlater(self, uuid):
        ''' Is a program set to watch later ? '''
        return self._resumepoints.get(uuid, {}).get('value', {}).get('watchLater') is True

    def watchlater(self, uuid, title, url):
        ''' Watch an episode later '''
        succeeded = self.update(uuid=uuid, title=title, url=url, watch_later=True)
        if succeeded:
            self._kodi.show_notification(message=self._kodi.localize(30403, title=title))
            self._kodi.container_refresh()

    def unwatchlater(self, uuid, title, url, move_down=False):
        ''' Unwatch an episode later '''
        succeeded = self.update(uuid=uuid, title=title, url=url, watch_later=False)
        if succeeded:
            self._kodi.show_notification(message=self._kodi.localize(30404, title=title))
            # If the current item is selected and we need to move down before removing
            if move_down:
                self._kodi.input_down()
            self._kodi.container_refresh()

    def get_position(self, uuid):
        ''' Return the stored position of a video '''
        return self._resumepoints.get(uuid, {}).get('value', {}).get('position', 0)

    def get_total(self, uuid):
        ''' Return the stored total length of a video '''
        return self._resumepoints.get(uuid, {}).get('value', {}).get('total', 100)

    def get_url(self, uuid, url_type='medium'):
        ''' Return the stored url a video '''
        from statichelper import reformat_url
        return reformat_url(self._resumepoints.get(uuid, {}).get('value', {}).get('url'), url_type)

    @staticmethod
    def assetpath_to_uuid(assetpath):
        ''' Convert an assetpath (e.g. /content/dam/vrt/2019/08/14/woodstock-depot_WP00157456)
            to a resumepoint uuid (e.g. contentdamvrt20190814woodstockdepotwp00157456) '''
        # The video has no assetPath, so we return None instead
        if assetpath is None:
            return None
        return assetpath.translate({ord(char): None for char in '/-_'}).lower()

    def watchlater_urls(self):
        ''' Return all watchlater urls '''
        return [self.get_url(uuid) for uuid in self._resumepoints if self.is_watchlater(uuid)]

    def resumepoints_urls(self):
        ''' Return all urls that have not been finished watching '''
        seconds_margin = 30  # Margin in seconds
        return [self.get_url(uuid) for uuid in self._resumepoints if seconds_margin < self.get_position(uuid) < (self.get_total(uuid) - seconds_margin)]

    def invalidate_caches(self):
        ''' Invalidate caches that rely on favorites '''
        # Delete resumepoints-related caches
        self._kodi.invalidate_caches('continue-*.json', 'resume_points.json', 'watchlater-*.json')
