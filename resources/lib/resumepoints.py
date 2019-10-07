# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
''' Implementation of ResumePoints class '''

from __future__ import absolute_import, division, unicode_literals

try:  # Python 3
    from urllib.request import build_opener, install_opener, ProxyHandler, Request, urlopen
except ImportError:  # Python 2
    from urllib2 import build_opener, install_opener, ProxyHandler, Request, urlopen


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

    def get_resumepoints(self, ttl=None):
        ''' Get a cached copy or a newer resumepoints from VRT, or fall back to a cached file '''
        if not self.is_activated():
            return None
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
        return self._resumepoints

    def set_resumepoint(self, uuid, title, url, watch_later=None, position=0, total=100):
        ''' Set a program as watchlater, and update local copy '''

        self.get_resumepoints(ttl=60 * 60)
        if watch_later is not None and not position and watch_later is self.is_watchlater(uuid):
            # Already followed/unfollowed, nothing to do
            return True

        if watch_later is None and position == self.get_position(uuid):
            # Already followed/unfollowed, nothing to do
            return True

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
            payload = self._resumepoints[uuid]['value']

        payload = dict(position=position, total=total, url=url)

        if watch_later is not None:
            payload['watchLater'] = watch_later

        import json
        data = json.dumps(payload).encode('utf-8')
        self._kodi.log('URL post: https://video-user-data.vrt.be/resume_points/{uuid}', 'Verbose', uuid=uuid)
        req = Request('https://video-user-data.vrt.be/resume_points/%s' % uuid, data=data, headers=headers)
        result = urlopen(req)
        if result.getcode() != 200:
            self._kodi.log_error("Failed to (un)watch episode' at VRT NU")
            self._kodi.show_notification(message=self._kodi.localize(30976))
            return False
        # NOTE: Updates to resumepoints take a longer time to take effect, so we keep our own cache and use it
        self._resumepoints[uuid] = dict(value=payload)
        self._kodi.update_cache('resume_points.json', self._resumepoints)
        self.invalidate_caches()
        return True

    def is_watchlater(self, uuid):
        ''' Is a program set to watch later ? '''
        value = False
        entry = self._resumepoints.get(uuid)
        if entry:
            value = entry.get('value', {}).get('watchLater')
        return value is True

    def watchlater(self, uuid, title, url):
        ''' Watch an episode later '''
        succeeded = self.set_resumepoint(uuid=uuid, title=title, url=url, watch_later=True)
        if succeeded:
            self._kodi.show_notification(message=self._kodi.localize(30401, title=title))
            self._kodi.container_refresh()

    def unwatchlater(self, uuid, title, url, move_down=False):
        ''' Unwatch an episode later '''
        succeeded = self.set_resumepoint(uuid=uuid, title=title, url=url, watch_later=False)
        if succeeded:
            self._kodi.show_notification(message=self._kodi.localize(30402, title=title))
            # If the current item is selected and we need to move down before removing
            if move_down:
                self._kodi.input_down()
            self._kodi.container_refresh()

    def get_position(self, uuid):
        ''' Return the stored position of a video '''
        position = 0
        entry = self._resumepoints.get(uuid)
        if entry:
            position = entry.get('value', {}).get('position', 0)
        return position

    @staticmethod
    def assetpath_to_uuid(assetpath):
        ''' Convert an assetpath (e.g. /content/dam/vrt/2019/08/14/woodstock-depot_WP00157456)
            to a resumepoint uuid (e.g. contentdamvrt20190814woodstockdepotwp00157456) '''
        return assetpath.translate({ord(char): None for char in '/-_'}).lower()

    def watchlater_uuids(self):
        ''' Return all watchlater uuids '''
        return [key for key, value in list(self._resumepoints.items()) if value.get('value').get('watchLater') is True]

    def resumepoints_uuids(self):
        ''' Return all resumepoints uuids and their resume point '''
        return {key: value.get('value').get('position') for key, value in list(self._resumepoints.items()) if value.get('value').get('position', 0) != 0}

    def invalidate_caches(self):
        ''' Invalidate caches that rely on resumepoints '''
        self._kodi.invalidate_caches('resume_points.json')
        self._kodi.invalidate_caches('watchlater-*.json')

    def refresh_resumepoints(self):
        ''' External API call to refresh resumepoints, used in Troubleshooting section '''
        self.get_resumepoints(ttl=0)
        self._kodi.show_notification(message=self._kodi.localize(30982))

    def manage_watchlater(self):
        ''' Allow the user to unselect watchlater to be removed from the listing '''
        self.get_resumepoints(ttl=0)
        if not self._resumepoints:
            self._kodi.show_ok_dialog(heading=self._kodi.localize(30418), message=self._kodi.localize(30419))  # No watchlater list found
            return

#        def by_title(item):
#            ''' Sort by title '''
#            return item.get('value').get('title')
#
#        items = [dict(program=url_to_program(value.get('value').get('programUrl')),
#                      title=unquote(value.get('value').get('title')),
#                      enabled=value.get('value').get('watchLater')) for value in list(sorted(self._resumepoints.values(), key=by_title))]
#        titles = [item['title'] for item in items]
#        preselect = [idx for idx in range(0, len(items) - 1) if items[idx]['enabled']]
#        selected = self._kodi.show_multiselect(self._kodi.localize(30420), options=titles, preselect=preselect)  # Please select/unselect to follow/unfollow
#        if selected is not None:
#            for idx in set(preselect).difference(set(selected)):
#                self.unwatch(program=items[idx]['program'], title=items[idx]['title'])
#            for idx in set(selected).difference(set(preselect)):
#                self.watch(program=items[idx]['program'], title=items[idx]['title'])
