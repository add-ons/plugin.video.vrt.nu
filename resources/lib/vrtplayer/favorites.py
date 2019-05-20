# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, unicode_literals

from resources.lib.vrtplayer import tokenresolver

try:
    from urllib.request import build_opener, install_opener, ProxyHandler, Request, urlopen
except ImportError:
    from urllib2 import build_opener, install_opener, ProxyHandler, Request, urlopen


class Favorites:

    def __init__(self, _kodi):
        self._kodi = _kodi
        self._tokenresolver = tokenresolver.TokenResolver(_kodi)
        self._proxies = _kodi.get_proxies()
        install_opener(build_opener(ProxyHandler(self._proxies)))
        self._favorites = None
        if _kodi.get_setting('usefavorites') == 'true' and _kodi.has_credentials():
            # Get favorites from cache if fresh
            self.get_favorites(ttl=60 * 60)

    def is_activated(self):
        return self._favorites is not None

    def get_favorites(self, ttl=None):
        import json
        api_json = self._kodi.get_cache('favorites.json', ttl)
        if not api_json:
            xvrttoken = self._tokenresolver.get_fav_xvrttoken()
            headers = {
                'authorization': 'Bearer ' + xvrttoken,
                'content-type': 'application/json',
                # 'Cookie': 'X-VRT-Token=' + xvrttoken,
                'Referer': 'https://www.vrt.be/vrtnu',
            }
            req = Request('https://video-user-data.vrt.be/favorites', headers=headers)
            self._kodi.log_notice('URL post: https://video-user-data.vrt.be/favorites', 'Verbose')
            try:
                api_json = json.load(urlopen(req))
            except Exception:
                # Force favorites from cache
                api_json = self._kodi.get_cache('favorites.json', ttl=None)
            else:
                self._kodi.update_cache('favorites.json', api_json)
        self._favorites = api_json

    def set_favorite(self, program, path, value=True):
        import json
        if value is not self.is_favorite(path):
            xvrttoken = self._tokenresolver.get_fav_xvrttoken()
            headers = {
                'authorization': 'Bearer ' + xvrttoken,
                'content-type': 'application/json',
                # 'Cookie': 'X-VRT-Token=' + xvrttoken,
                'Referer': 'https://www.vrt.be/vrtnu',
            }
            payload = dict(isFavorite=value, programUrl=path, title=program)
            data = json.dumps(payload).encode('utf-8')
            self._kodi.log_notice('URL post: https://video-user-data.vrt.be/favorites/%s' % self.uuid(path), 'Verbose')
            req = Request('https://video-user-data.vrt.be/favorites/%s' % self.uuid(path), data=data, headers=headers)
            # TODO: Test that we get a HTTP 200, otherwise log and fail graceful
            result = urlopen(req)
            if result.getcode() != 200:
                self._kodi.log_error("Failed to follow program '%s' at VRT NU" % path)
            # NOTE: Updates to favorites take a longer time to take effect, so we keep our own cache and use it
            self._favorites[self.uuid(path)] = dict(value=payload)
            self._kodi.update_cache('favorites.json', self._favorites)

    def is_favorite(self, path):
        value = False
        favorite = self._favorites.get(self.uuid(path))
        if favorite:
            value = favorite.get('value', dict(isFavorite=False)).get('isFavorite', False)
        return value

    def follow(self, program, path):
        self._kodi.show_notification(message='Follow ' + program)
        self.set_favorite(program, path, True)
        self._kodi.container_refresh()

    def unfollow(self, program, path):
        self._kodi.show_notification(message='Unfollow ' + program)
        self.set_favorite(program, path, False)
        self._kodi.container_refresh()

    def uuid(self, path):
        return path.replace('/', '').replace('-', '')

    def name(self, path):
        return path.replace('.relevant/', '/').split('/')[-2]

    def names(self):
        return [self.name(p.get('value').get('programUrl')) for p in self._favorites.values() if p.get('value').get('isFavorite')]

    def titles(self):
        return [p.get('value').get('title') for p in self._favorites.values() if p.get('value').get('isFavorite')]

    def invalidate_cache(self):
        self._kodi.invalidate_cache('offline-filtered.json')
        self._kodi.invalidate_cache('recent-filtered.json')
