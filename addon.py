import sys
import xbmcaddon
import os
import requests
from urlparse import parse_qsl
from resources.lib.vrtplayer import vrtplayer
from resources.lib.kodiwrappers import kodiwrapper
from resources.lib.vrtplayer import actions
from resources.lib.helperobjects import helperobjects

_addon_ = xbmcaddon.Addon()
_url = sys.argv[0]
_handle = int(sys.argv[1])

def router(params_string):

    kodi_wrapper = kodiwrapper.KodiWrapper(_handle, _url)
    vrt_player = vrtplayer.VRTPlayer(_handle, _url)
    params = dict(parse_qsl(params_string))
    if params:
        if params['action'] == actions.LISTING_AZ:
            kodi_wrapper.show_listing(vrt_player.get_az_menu_items())
        elif params['action'] == actions.LISTING_CATEGORIES:
            kodi_wrapper.show_listing(vrt_player.get_category_menu_items())
        elif params['action'] == actions.LISTING_LIVE:
            kodi_wrapper.show_listing(vrt_player.get_livestream_items())
        elif params['action'] == actions.GET_EPISODES:
            kodi_wrapper.get_video_episodes(params['video'])
        elif params['action'] == actions.GET_CATEGORY_EPISODES:
            kodi_wrapper.show_listing(vrt_player.get_video_category_episodes(params['video']))
        elif params['action'] == actions.PLAY:
            kodi_wrapper.play_video(params['video'])
        elif params['action'] == actions.PLAY_LIVE:
            kodi_wrapper.play_livestream(params['video'])
    else:
        kodi_wrapper.show_listing(vrt_player.get_main_menu_items())

if __name__ == '__main__':
    router(sys.argv[2][1:])

