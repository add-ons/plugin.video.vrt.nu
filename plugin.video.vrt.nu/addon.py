# -*- coding: UTF-8 -*-

# GNU General Public License v2.0 (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

''' This is the actual VRT Nu video plugin entry point '''

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

import xbmcaddon
from resources.lib.kodiwrappers import kodiwrapper
from resources.lib.vrtplayer import vrtplayer, urltostreamservice, tokenresolver, actions, vrtapihelper

try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl


_url = sys.argv[0]
_handle = int(sys.argv[1])


def router(params_string):
    ''' This is the main router for the video plugin menu '''
    addon = xbmcaddon.Addon()
    kodi_wrapper = kodiwrapper.KodiWrapper(_handle, _url, addon)
    token_resolver = tokenresolver.TokenResolver(kodi_wrapper)
    stream_service = urltostreamservice.UrlToStreamService(vrtplayer.VRTPlayer.VRT_BASE,
                                                           vrtplayer.VRTPlayer.VRTNU_BASE_URL,
                                                           kodi_wrapper, token_resolver)
    api_helper = vrtapihelper.VRTApiHelper()
    vrt_player = vrtplayer.VRTPlayer(addon.getAddonInfo('path'), kodi_wrapper, stream_service, api_helper)
    params = dict(parse_qsl(params_string))
    if params:
        if params['action'] == actions.LISTING_AZ:
            vrt_player.show_az_menu_items()
        elif params['action'] == actions.LISTING_CATEGORIES:
            vrt_player.show_category_menu_items()
        elif params['action'] == actions.LISTING_LIVE:
            vrt_player.show_livestream_items()
        elif params['action'] == actions.LISTING_VIDEOS:
            season = params['season'] if 'season' in params else None
            vrt_player.show_videos(params['video'], season)
        elif params['action'] == actions.LISTING_CATEGORY_VIDEOS:
            vrt_player.show_video_category_episodes(params['video'])
        elif params['action'] == actions.PLAY:
            vrt_player.play(params['video'])
    else:
        vrt_player.show_main_menu_items()


if __name__ == '__main__':
    router(sys.argv[2][1:])
