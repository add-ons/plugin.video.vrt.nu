# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

''' Implements a router function as entrypoint for the add-on '''

from __future__ import absolute_import, division, unicode_literals

from resources.lib import routes, kodiwrapper, tokenresolver


def get_params(path, route, params_length):
    ''' Get a fixed size list of parameters '''
    max_split = -1
    params_data = path.split(route, 1)[1]
    params = []
    if params_data != '':
        if params_data.startswith('/url'):
            max_split = 1
        params = params_data.lstrip('/').split('/', max_split)
    params.extend([None] * (params_length - len(params)))
    return params


def router(argv):
    ''' This is the main router for the video plugin menu '''

    addon_url = argv[0]
    addon_handle = int(argv[1])
    path = '/' + addon_url.split('/', 3)[3]

    _kodi = kodiwrapper.KodiWrapper(addon_handle, addon_url)
    _tokenresolver = tokenresolver.TokenResolver(_kodi)
    _kodi.log_access(addon_url)

    # Cache delete method
    if path.startswith(routes.CACHE_DELETE):
        params = get_params(path, routes.CACHE_DELETE, 1)
        if params[0]:
            _kodi.refresh_caches(params[0])
            return
        _kodi.invalidate_caches()
        return

    # Tokens delete method
    if path == 'routes.TOKENS_DELETE':
        _tokenresolver.delete_tokens()
        return

    # Widevine install method
    if path == routes.WIDEVINE_INSTALL:
        _kodi.install_widevine()
        return

    from resources.lib import favorites
    _favorites = favorites.Favorites(_kodi, _tokenresolver)

    # Follow method
    if path.startswith(routes.FOLLOW):
        params = get_params(path, routes.FOLLOW, 2)
        _favorites.follow(title=params[0], program=params[1])
        return

    # Unfollow method
    if path.startswith(routes.UNFOLLOW):
        params = get_params(path, routes.UNFOLLOW, 2)
        _favorites.unfollow(title=params[0], program=params[1])
        return

    from resources.lib import vrtapihelper, vrtplayer
    _apihelper = vrtapihelper.VRTApiHelper(_kodi, _favorites)
    _vrtplayer = vrtplayer.VRTPlayer(_kodi, _favorites, _apihelper)

    # Play methods
    if path.startswith(routes.PLAY):
        params = get_params(path, routes.PLAY, 3)
        if params[0] == 'id':
            if params[2]:
                video = dict(publication_id=params[1], video_id=params[2])
            else:
                video = dict(video_id=params[1])
            _vrtplayer.play(video)
        elif params[0] == 'url':
            video = dict(video_url=params[1])
            _vrtplayer.play(video)
        elif params[0] == 'latestepisode':
            _vrtplayer.play_latest_episode(params[1])
        return

    # Main menu
    if path == routes.MAIN:
        _vrtplayer.show_main_menu_items()
        return

    # Favorites menu
    if path.startswith(routes.FAVORITES):
        params = get_params(path, routes.FAVORITES, 2)
        if not params[0]:
            _favorites.get_favorites(ttl=60 * 60)
            _vrtplayer.show_favorites_menu_items()
            return
        if params[0] == 'programs':
            # My programs menus may need more up-to-date favorites
            _favorites.get_favorites(ttl=5 * 60)
            _vrtplayer.show_tvshow_menu_items(use_favorites=True)
            return
        if params[0] == 'offline':
            # My programs menus may need more up-to-date favorites
            _favorites.get_favorites(ttl=5 * 60)
            _vrtplayer.show_offline(use_favorites=True, page=params[1])
            return
        if params[0] == 'recent':
            # My programs menus may need more up-to-date favorites
            _favorites.get_favorites(ttl=5 * 60)
            _vrtplayer.show_recent(use_favorites=True, page=params[1])
            return
        if params[0] == 'refresh':
            _favorites.get_favorites(ttl=0)
            return

    # A-Z menu, episode and season menu
    if path.startswith(routes.PROGRAMS):
        params = get_params(path, routes.PROGRAMS, 2)
        if params[0]:
            _favorites.get_favorites(ttl=60 * 60)
            _vrtplayer.show_episodes(params[0], params[1])
        else:
            _vrtplayer.show_tvshow_menu_items()
        return

    # Categories menu
    if path.startswith(routes.CATEGORIES):
        params = get_params(path, routes.CATEGORIES, 1)
        if params[0]:
            _favorites.get_favorites(ttl=60 * 60)
            _vrtplayer.show_tvshow_menu_items(category=params[0])
            return
        _vrtplayer.show_category_menu_items()
        return

    # Channels menu
    if path.startswith(routes.CHANNELS):
        params = get_params(path, routes.CHANNELS, 1)
        if params[0]:
            _favorites.get_favorites(ttl=60 * 60)
        _vrtplayer.show_channels_menu_items(params[0])
        return

    # Live TV menu
    if path == routes.LIVETV:
        _vrtplayer.show_livestream_items()
        return

    # Most recent menu
    if path.startswith(routes.RECENT):
        params = get_params(path, routes.RECENT, 1)
        _vrtplayer.show_recent(page=params[0])
        return

    # Soon offline menu
    if path.startswith(routes.OFFLINE):
        params = get_params(path, routes.OFFLINE, 1)
        _vrtplayer.show_offline(page=params[0])
        return

    # TV guide menu
    if path.startswith(routes.TVGUIDE):
        from resources.lib import tvguide
        _tvguide = tvguide.TVGuide(_kodi)
        params = get_params(path, routes.TVGUIDE, 2)
        _tvguide.show_tvguide(params[0], params[1])
        return

    # Search VRT NU menu
    if path.startswith(routes.SEARCH):
        params = get_params(path, routes.SEARCH, 2)
        _favorites.get_favorites(ttl=60 * 60)
        _vrtplayer.search(search_string=params[0], page=params[1])
        return
