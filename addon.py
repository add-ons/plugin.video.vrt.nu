import sys
import xbmcaddon
import os
import requests
from urlparse import parse_qsl
from resources.lib.vrtplayer import vrtplayer
from resources.lib.helperobjects import helperobjects

_addon_ = xbmcaddon.Addon()
_addon_path = xbmcaddon.Addon().getAddonInfo("path")
_url = sys.argv[0]
_handle = int(sys.argv[1])

def router(params_string):

    vrt_player = vrtplayer.VRTPlayer(_handle, _url)
    params = dict(parse_qsl(params_string))
    if params:
        if params['action'] == 'listingaz':
            vrt_player.list_videos_az()
        elif params['action'] == 'getepisodes':
            vrt_player.get_video_episodes(params['video'])
        elif params['action'] == 'play':
            vrt_player.play_video(params['video'])
        elif params['action'] == 'listinglive':
            vrt_player.show_listing(vrt_player.get_livestream_items())
        elif params['action'] == 'playlive':
            vrt_player.play_livestream(params['video'])
    else:
        vrt_player.show_listing(vrt_player.get_main_menu_items())

if __name__ == '__main__':
    router(sys.argv[2][1:])

