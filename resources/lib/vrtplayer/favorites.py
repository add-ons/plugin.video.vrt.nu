# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, unicode_literals
import json
import time

from resources.lib.vrtplayer import tokenresolver

try:
    from urllib.request import build_opener, install_opener, ProxyHandler, Request, urlopen
except ImportError:
    from urllib2 import build_opener, install_opener, ProxyHandler, Request, urlopen


class Favorites:

    def __init__(self, _kodiwrapper):
        self._kodiwrapper = _kodiwrapper
        self._tokenresolver = tokenresolver.TokenResolver(_kodiwrapper)
        self._proxies = _kodiwrapper.get_proxies()
        install_opener(build_opener(ProxyHandler(self._proxies)))
        self._cache_file = _kodiwrapper.get_userdata_path() + 'favorites.json'
        self._favorites = {}
        self.get_favorites()

    def get_favorites(self):
        if self._kodiwrapper.check_if_path_exists(self._cache_file):
            if self._kodiwrapper.stat_file(self._cache_file).st_mtime() > time.mktime(time.localtime()) - (2 * 60):
                self._kodiwrapper.log_notice('CACHE: %s vs %s' % (self._kodiwrapper.stat_file(self._cache_file).st_mtime(), time.mktime(time.localtime()) - (5 * 60)), 'Debug')
                with self._kodiwrapper.open_file(self._cache_file) as f:
                    self._favorites = json.loads(f.read())
                return
        self.update_favorites()

    def update_favorites(self):
        xvrttoken = self._tokenresolver.get_fav_xvrttoken()
        headers = {
            'authorization': 'Bearer ' + xvrttoken,
            'content-type': 'application/json',
            # 'Cookie': 'X-VRT-Token=' + xvrttoken,
            'Referer': 'https://www.vrt.be/vrtnu',
        }
        req = Request('https://video-user-data.vrt.be/favorites', headers=headers)
        self._favorites = json.loads(urlopen(req).read())
        self.write_favorites()

    def set_favorite(self, program, path, value=True):
        if value is not self.is_favorite(path):
            xvrttoken = self._tokenresolver.get_fav_xvrttoken()
            headers = {
                'authorization': 'Bearer ' + xvrttoken,
                'content-type': 'application/json',
                # 'Cookie': 'X-VRT-Token=' + xvrttoken,
                'Referer': 'https://www.vrt.be/vrtnu',
            }
            payload = dict(isFavorite=value, programUrl=path, title=program)
            self._kodiwrapper.log_notice('URL post: https://video-user-data.vrt.be/favorites/%s' % self.uuid(path), 'Verbose')
            req = Request('https://video-user-data.vrt.be/favorites/%s' % self.uuid(path), data=json.dumps(payload), headers=headers)
            # TODO: Test that we get a HTTP 200, otherwise log and fail graceful
            result = urlopen(req)
            if result.getcode() != 200:
                self._kodiwrapper.log_error("Failed to follow program '%s' at VRT NU" % path)
            # NOTE: Updates to favorites take a longer time to take effect, so we keep our own cache and use it
            self._favorites[self.uuid(path)] = dict(value=payload)
            self.write_favorites()

    def write_favorites(self):
        with self._kodiwrapper.open_file(self._cache_file, 'w') as f:
            f.write(json.dumps(self._favorites))

    def is_favorite(self, path):
        value = False
        favorite = self._favorites.get(self.uuid(path))
        if favorite:
            value = favorite.get('value', dict(isFavorite=False)).get('isFavorite', False)
        return value

    def follow(self, program, path):
        self._kodiwrapper.show_notification('Follow ' + program)
        self.set_favorite(program, path, True)
        self._kodiwrapper.container_refresh()

    def unfollow(self, program, path):
        self._kodiwrapper.show_notification('Unfollow ' + program)
        self.set_favorite(program, path, False)
        self._kodiwrapper.container_refresh()

    def uuid(self, path):
        return path.replace('/', '').replace('-', '')

    def name(self, path):
        return path.replace('.relevant/', '/').split('/')[-2]

    def names(self):
        return [self.name(p.get('value').get('programUrl')) for p in self._favorites.values() if p.get('value').get('isFavorite')]

    def titles(self):
        return [p.get('value').get('title') for p in self._favorites.values() if p.get('value').get('isFavorite')]
