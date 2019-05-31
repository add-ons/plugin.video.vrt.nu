# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

''' This is the router module '''

from __future__ import absolute_import, division, unicode_literals

import xbmcaddon
from resources.lib import actions, kodiwrapper

try:  # Python 3
    from urllib.parse import parse_qsl
except ImportError:  # Python 2
    from urlparse import parse_qsl


def router(argv):
    ''' This is the main router for the video plugin menu '''

    addon_url = argv[0]
    addon_handle = int(argv[1])
    params_string = argv[2][1:]

    addon = xbmcaddon.Addon()
    params = dict(parse_qsl(params_string))
    action = params.get('action')

    _kodi = kodiwrapper.KodiWrapper(addon_handle, addon_url, addon)
    _kodi.log_access(addon_url, params_string)

    # Actions that only require _kodi
    if action == actions.INVALIDATE_CACHES:
        _kodi.invalidate_caches()
        return
    if action == actions.CLEAR_COOKIES:
        from resources.lib import tokenresolver
        _tokenresolver = tokenresolver.TokenResolver(_kodi)
        _tokenresolver.reset_cookies()
        return
    if action == actions.LISTING_TVGUIDE:
        from resources.lib import tvguide
        _tvguide = tvguide.TVGuide(_kodi)
        _tvguide.show_tvguide(params)
        return
    if action == actions.INSTALL_WIDEVINE:
        _kodi.install_widevine()
        return

    from resources.lib import favorites
    _favorites = favorites.Favorites(_kodi)

    # Actions requiring _favorites as well
    if action == actions.FOLLOW:
        _favorites.follow(program=params.get('program'), path=params.get('path'))
        return
    if action == actions.UNFOLLOW:
        _favorites.unfollow(program=params.get('program'), path=params.get('path'))
        return
    if action == actions.REFRESH_FAVORITES:
        _favorites.get_favorites(ttl=0)
        return

    from resources.lib import vrtapihelper, vrtplayer
    _apihelper = vrtapihelper.VRTApiHelper(_kodi, _favorites)
    _vrtplayer = vrtplayer.VRTPlayer(_kodi, _favorites, _apihelper)

    # Actions requiring menu's or playback, but not favorites
    if not action:
        _vrtplayer.show_main_menu_items()
        return
    if action == actions.PLAY:
        _vrtplayer.play(params)
        return
    if action == actions.LISTING_CATEGORIES:
        _vrtplayer.show_category_menu_items()
        return
    if action == actions.LISTING_LIVE:
        _vrtplayer.show_livestream_items()
        return

    # My programs menus may need more up-to-date favorites
    if params.get('use_favorites'):
        _favorites.get_favorites(ttl=5 * 60)
    elif params.get('category') or params.get('channel'):
        _favorites.get_favorites(ttl=60 * 60)

    # Actions that optionally use favorites
    if action == actions.LISTING_AZ_TVSHOWS:
        _vrtplayer.show_tvshow_menu_items(use_favorites=params.get('use_favorites'))
        return
    if action == actions.LISTING_OFFLINE:
        _vrtplayer.show_offline(page=params.get('page'), use_favorites=params.get('use_favorites'))
        return
    if action == actions.LISTING_RECENT:
        _vrtplayer.show_recent(page=params.get('page'), use_favorites=params.get('use_favorites'))
        return
    if action == actions.LISTING_CATEGORY_TVSHOWS:
        _vrtplayer.show_tvshow_menu_items(category=params.get('category'))
        return
    if action == actions.LISTING_CHANNELS:
        _vrtplayer.show_channels_menu_items(channel=params.get('channel'))
        return

    # Actions that expose follow/unfollow context menus
    if action == actions.LISTING_FAVORITES:
        _favorites.get_favorites(ttl=60 * 60)
        _vrtplayer.show_favorites_menu_items()
        return
    if action == actions.LISTING_EPISODES:
        _favorites.get_favorites(ttl=60 * 60)
        _vrtplayer.show_episodes(path=params.get('video_url'))
        return
    if action == actions.LISTING_ALL_EPISODES:
        _favorites.get_favorites(ttl=60 * 60)
        _vrtplayer.show_all_episodes(path=params.get('video_url'))
        return
    if action == actions.SEARCH:
        _favorites.get_favorites(ttl=60 * 60)
        _vrtplayer.search(search_string=params.get('query'), page=params.get('page'))
        return

    # Show main menu, if nothing else
    _vrtplayer.show_main_menu_items()
