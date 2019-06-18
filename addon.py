# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

''' This is the actual VRT NU video plugin entry point '''

from __future__ import absolute_import, division, unicode_literals
import sys
import routing
from resources.lib import kodiwrapper

plugin = routing.Plugin()
kodi = kodiwrapper.KodiWrapper(globals())


@plugin.route('/')
def main_menu():
    ''' The VRT NU plugin main menu '''
    from resources.lib import vrtplayer
    vrtplayer.VRTPlayer(kodi).show_main_menu_items()


@plugin.route('/cache/delete')
@plugin.route('/cache/delete/<cache_file>')
def delete_cache(cache_file=None):
    ''' The API interface to delete caches '''
    if cache_file:
        kodi.refresh_caches(cache_file)
    else:
        kodi.invalidate_caches()


@plugin.route('/tokens/delete')
def delete_tokens():
    ''' The API interface to delete all VRT tokens '''
    from resources.lib import tokenresolver
    tokenresolver.TokenResolver(kodi).delete_tokens()


@plugin.route('/widevine/install')
def install_widevine():
    ''' The API interface to install Widevine '''
    kodi.install_widevine()


@plugin.route('/follow/<title>/<program>')
def follow(title, program):
    ''' The API interface to follow a program used by the context menu '''
    from resources.lib import favorites
    favorites.Favorites(kodi).follow(title=title, program=program)


@plugin.route('/unfollow/<title>/<program>')
def unfollow(title, program):
    ''' The API interface to unfollow a program used by the context menu '''
    from resources.lib import favorites
    favorites.Favorites(kodi).unfollow(title=title, program=program)


@plugin.route('/favorites')
def favorites_menu():
    ''' The favorites My program menu '''
    from resources.lib import vrtplayer
    vrtplayer.VRTPlayer(kodi).show_favorites_menu_items()


@plugin.route('/favorites/programs')
def favorites_programs():
    ''' The favorites A-Z listing '''
    from resources.lib import vrtplayer
    vrtplayer.VRTPlayer(kodi).show_tvshow_menu_items(use_favorites=True)


@plugin.route('/favorites/recent')
@plugin.route('/favorites/recent/<page>')
def favorites_recent(page=1):
    ''' The favorites recent listing '''
    from resources.lib import vrtplayer
    vrtplayer.VRTPlayer(kodi).show_recent(page=page, use_favorites=True)


@plugin.route('/favorites/offline')
@plugin.route('/favorites/offline/<page>')
def favorites_offline(page=1):
    ''' The favorites offline listing '''
    from resources.lib import vrtplayer
    vrtplayer.VRTPlayer(kodi).show_offline(page=page, use_favorites=True)


@plugin.route('/favorites/refresh')
def favorites_refresh():
    ''' The API interface to refresh the favorites cache '''
    from resources.lib import favorites
    favorites.Favorites(kodi).get_favorites(ttl=0)


@plugin.route('/programs')
@plugin.route('/programs/<program>')
@plugin.route('/programs/<program>/<season>')
def programs(program=None, season=None):
    ''' The programs A-Z / seasons / episode listing '''
    from resources.lib import vrtplayer
    if program:
        vrtplayer.VRTPlayer(kodi).show_episodes(program, season)
    else:
        vrtplayer.VRTPlayer(kodi).show_tvshow_menu_items()


@plugin.route('/categories')
@plugin.route('/categories/<category>')
def categories(category=None):
    ''' The categories menu and listing '''
    from resources.lib import vrtplayer
    if category:
        vrtplayer.VRTPlayer(kodi).show_tvshow_menu_items(category=category)
    else:
        vrtplayer.VRTPlayer(kodi).show_category_menu_items()


@plugin.route('/channels')
@plugin.route('/channels/<channel>')
def channels(channel=None):
    ''' The channels menu and listing '''
    from resources.lib import vrtplayer
    vrtplayer.VRTPlayer(kodi).show_channels_menu_items(channel=channel)


@plugin.route('/livetv')
def livetv():
    ''' The livetv menu '''
    from resources.lib import vrtplayer
    vrtplayer.VRTPlayer(kodi).show_livestream_items()


@plugin.route('/recent')
@plugin.route('/recent/<page>')
def recent(page=1):
    ''' The most recent items listing '''
    from resources.lib import vrtplayer
    vrtplayer.VRTPlayer(kodi).show_recent(page=page)


@plugin.route('/offline')
@plugin.route('/offline/<page>')
def offline(page=1):
    ''' The soon ogline listing '''
    from resources.lib import vrtplayer
    vrtplayer.VRTPlayer(kodi).show_offline(page=page)


@plugin.route('/tvguide')
@plugin.route('/tvguide/<date>')
@plugin.route('/tvguide/<date>/<channel>')
def tv_guide(date=None, channel=None):
    ''' The TV guide menu and listings '''
    from resources.lib import tvguide
    tvguide.TVGuide(kodi).show_tvguide(date=date, channel=channel)


@plugin.route('/search')
@plugin.route('/search/<search_string>')
@plugin.route('/search/<search_string>/<page>')
def search(search_string=None, page=1):
    ''' The Search interface and query listing '''
    from resources.lib import vrtplayer
    vrtplayer.VRTPlayer(kodi).search(search_string=search_string, page=page)


@plugin.route('/play/id/<video_id>')
@plugin.route('/play/id/<publication_id>/<video_id>')
def play_id(video_id, publication_id=None):
    ''' The API interface to play a video by video_id and/or publication_id '''
    from resources.lib import vrtplayer
    if video_id and publication_id:
        vrtplayer.VRTPlayer(kodi).play(dict(publication_id=publication_id, video_id=video_id))
    elif video_id:
        vrtplayer.VRTPlayer(kodi).play(dict(video_id=video_id))


@plugin.route('/play/url/<path:video_url>')
def play_url(video_url):
    ''' The API interface to play a video by using a URL '''
    from resources.lib import vrtplayer
    vrtplayer.VRTPlayer(kodi).play(dict(video_url=video_url))


@plugin.route('/play/lastepisode/<program>')
def play_last(program):
    ''' The API interface to play the latest episode of a program '''
    from resources.lib import vrtplayer
    vrtplayer.VRTPlayer(kodi).play_latest_episode(program)


if __name__ == '__main__':
    kodi.log_access(sys.argv[0])
    plugin.run(sys.argv)
