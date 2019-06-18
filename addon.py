# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

''' This is the actual VRT NU video plugin entry point '''

# pylint: disable=missing-docstring

from __future__ import absolute_import, division, unicode_literals
import sys
import routing
from resources.lib import kodiwrapper

plugin = routing.Plugin()
kodi = kodiwrapper.KodiWrapper(globals())


@plugin.route('/')
def main_menu():
    from resources.lib import vrtplayer
    _vrtplayer = vrtplayer.VRTPlayer(kodi)
    _vrtplayer.show_main_menu_items()


@plugin.route('/cache/delete')
@plugin.route('/cache/delete/<cache_file>')
def delete_cache(cache_file=None):
    if cache_file:
        kodi.refresh_caches(cache_file)
        return
    kodi.invalidate_caches()


@plugin.route('/widevine/install')
def install_widevine():
    kodi.install_widevine()


@plugin.route('/tokens/delete')
def delete_tokens():
    from resources.lib import tokenresolver
    _tokenresolver = tokenresolver.TokenResolver(kodi)
    _tokenresolver.delete_tokens()


@plugin.route('/follow/<title>/<program>')
def follow(title, program):
    from resources.lib import favorites
    _favorites = favorites.Favorites(kodi)
    _favorites.follow(title=title, program=program)


@plugin.route('/unfollow/<title>/<program>')
def unfollow(title, program):
    from resources.lib import favorites
    _favorites = favorites.Favorites(kodi)
    _favorites.unfollow(title=title, program=program)


@plugin.route('/play/id/<video_id>')
@plugin.route('/play/id/<publication_id>/<video_id>')
def play_id(video_id, publication_id=None):
    from resources.lib import vrtplayer
    _vrtplayer = vrtplayer.VRTPlayer(kodi)

    if video_id and publication_id:
        _vrtplayer.play(dict(publication_id=publication_id, video_id=video_id))
    elif video_id:
        _vrtplayer.play(dict(video_id=video_id))


@plugin.route('/play/url/<path:video_url>')
def play_url(video_url):
    from resources.lib import vrtplayer
    _vrtplayer = vrtplayer.VRTPlayer(kodi)
    _vrtplayer.play(dict(video_url=video_url))


@plugin.route('/play/lastepisode/<program>')
def play_last(program):
    from resources.lib import vrtplayer
    _vrtplayer = vrtplayer.VRTPlayer(kodi)
    _vrtplayer.play_latest_episode(program)


@plugin.route('/favorites')
def favorites_menu():
    from resources.lib import vrtplayer
    _vrtplayer = vrtplayer.VRTPlayer(kodi)
    _vrtplayer.show_favorites_menu_items()


@plugin.route('/favorites/programs')
def favorites_programs():
    from resources.lib import vrtplayer
    _vrtplayer = vrtplayer.VRTPlayer(kodi)
    _vrtplayer.show_tvshow_menu_items(use_favorites=True)


@plugin.route('/favorites/recent')
@plugin.route('/favorites/recent/<page>')
def favorites_recent(page=1):
    from resources.lib import vrtplayer
    _vrtplayer = vrtplayer.VRTPlayer(kodi)
    _vrtplayer.show_recent(page=page, use_favorites=True)


@plugin.route('/favorites/offline')
@plugin.route('/favorites/offline/<page>')
def favorites_offline(page=1):
    from resources.lib import vrtplayer
    _vrtplayer = vrtplayer.VRTPlayer(kodi)
    _vrtplayer.show_offline(page=page, use_favorites=True)


@plugin.route('/favorites/refresh')
def favorites_refresh():
    from resources.lib import favorites
    _favorites = favorites.Favorites(kodi)
    _favorites.get_favorites(ttl=0)


@plugin.route('/programs')
@plugin.route('/programs/<program>')
@plugin.route('/programs/<program>/<season>')
def programs(program=None, season=None):
    from resources.lib import vrtplayer
    _vrtplayer = vrtplayer.VRTPlayer(kodi)
    if program:
        _vrtplayer.show_episodes(program, season)
        return
    _vrtplayer.show_tvshow_menu_items()


@plugin.route('/categories')
@plugin.route('/categories/<category>')
def categories(category=None):
    from resources.lib import vrtplayer
    _vrtplayer = vrtplayer.VRTPlayer(kodi)
    if category:
        _vrtplayer.show_tvshow_menu_items(category=category)
        return
    _vrtplayer.show_category_menu_items()


@plugin.route('/channels')
@plugin.route('/channels/<channel>')
def channels(channel=None):
    from resources.lib import vrtplayer
    _vrtplayer = vrtplayer.VRTPlayer(kodi)
    _vrtplayer.show_channels_menu_items(channel=channel)


@plugin.route('/livetv')
def livetv():
    from resources.lib import vrtplayer
    _vrtplayer = vrtplayer.VRTPlayer(kodi)
    _vrtplayer.show_livestream_items()


@plugin.route('/recent')
@plugin.route('/recent/<page>')
def recent(page=1):
    from resources.lib import vrtplayer
    _vrtplayer = vrtplayer.VRTPlayer(kodi)
    _vrtplayer.show_recent(page=page)


@plugin.route('/offline')
@plugin.route('/offline/<page>')
def offline(page=1):
    from resources.lib import vrtplayer
    _vrtplayer = vrtplayer.VRTPlayer(kodi)
    _vrtplayer.show_offline(page=page)


@plugin.route('/tvguide')
@plugin.route('/tvguide/<date>')
@plugin.route('/tvguide/<date>/<channel>')
def tv_guide(date=None, channel=None):
    from resources.lib import tvguide
    _tvguide = tvguide.TVGuide(kodi)
    _tvguide.show_tvguide(date=date, channel=channel)


@plugin.route('/search')
@plugin.route('/search/<search_string>')
@plugin.route('/search/<search_string>/<page>')
def search(search_string=None, page=1):
    from resources.lib import vrtplayer
    _vrtplayer = vrtplayer.VRTPlayer(kodi)
    _vrtplayer.search(search_string=search_string, page=page)


def test(path):
    plugin.run(path)


if __name__ == '__main__':
    kodi.log_access(sys.argv[0])
    plugin.run(sys.argv)
