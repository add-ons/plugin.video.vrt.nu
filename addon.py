# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

''' This is the actual VRT Nu video plugin entry point '''

from __future__ import absolute_import, division, unicode_literals
import sys

import xbmcaddon
from resources.lib.kodiwrappers import kodiwrapper
from resources.lib.vrtplayer import actions

try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl

_ADDON_URL = sys.argv[0]
_ADDON_HANDLE = int(sys.argv[1])


def router(params_string):
    ''' This is the main router for the video plugin menu '''
    addon = xbmcaddon.Addon()
    params = dict(parse_qsl(params_string))
    action = params.get('action')

    _kodi = kodiwrapper.KodiWrapper(_ADDON_HANDLE, _ADDON_URL, addon)
    _kodi.log_access(_ADDON_URL, params_string)

    if action == actions.CLEAR_COOKIES:
        from resources.lib.vrtplayer import tokenresolver
        _tokenresolver = tokenresolver.TokenResolver(_kodi)
        _tokenresolver.reset_cookies()
        return
    if action == actions.LISTING_TVGUIDE:
        from resources.lib.vrtplayer import tvguide
        _tvguide = tvguide.TVGuide(_kodi)
        _tvguide.show_tvguide(params)
        return

    from resources.lib.vrtplayer import favorites
    _favorites = favorites.Favorites(_kodi)
    if action == actions.FOLLOW:
        _favorites.follow(program=params.get('program'), path=params.get('path'))
        return
    if action == actions.UNFOLLOW:
        _favorites.unfollow(program=params.get('program'), path=params.get('path'))
        return
    if action == actions.REFRESH_FAVORITES:
        _favorites.update_favorites()
        return

    from resources.lib.vrtplayer import vrtapihelper, vrtplayer
    _apihelper = vrtapihelper.VRTApiHelper(_kodi, _favorites)
    _vrtplayer = vrtplayer.VRTPlayer(_kodi, _favorites, _apihelper)

    if action == actions.PLAY:
        _vrtplayer.play(params)
    elif action == actions.LISTING_AZ_TVSHOWS:
        _vrtplayer.show_tvshow_menu_items(filtered=params.get('filtered'))
    elif action == actions.LISTING_CATEGORIES:
        _vrtplayer.show_category_menu_items()
    elif action == actions.LISTING_CATEGORY_TVSHOWS:
        _vrtplayer.show_tvshow_menu_items(category=params.get('category'))
    elif action == actions.LISTING_CHANNELS:
        _vrtplayer.show_channels_menu_items(channel=params.get('channel'))
    elif action == actions.LISTING_FAVORITES:
        _vrtplayer.show_favorites_menu_items()
    elif action == actions.LISTING_LIVE:
        _vrtplayer.show_livestream_items()
    elif action == actions.LISTING_EPISODES:
        _vrtplayer.show_episodes(path=params.get('video_url'))
    elif action == actions.LISTING_ALL_EPISODES:
        _vrtplayer.show_all_episodes(path=params.get('video_url'))
    elif action == actions.LISTING_RECENT:
        _vrtplayer.show_recent(page=params.get('page', 1), filtered=params.get('filtered'))
    elif action == actions.SEARCH:
        _vrtplayer.search(search_string=params.get('query'), page=params.get('page', 1))
    else:
        _vrtplayer.show_main_menu_items()


if __name__ == '__main__':
    router(sys.argv[2][1:])
