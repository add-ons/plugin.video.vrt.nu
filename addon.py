import sys
import xbmcaddon
import os
from urlparse import parse_qsl
from resources.lib.vrtplayer import vrtplayer
from resources.lib.helperobjects import helperobjects

_addon_ = xbmcaddon.Addon()
_addon_path = xbmcaddon.Addon().getAddonInfo("path")
_url = sys.argv[0]
_handle = int(sys.argv[1])

_VRT_LIVESTREAM_URL = "http://live.stream.vrt.be/vrt_video1_live/smil:vrt_video1_live.smil/playlist.m3u8"
_CANVAS_LIVESTREAM_ = "http://live.stream.vrt.be/vrt_video2_live/smil:vrt_video2_live.smil/playlist.m3u8"
_KETNET_VRT = "http://live.stream.vrt.be/vrt_events3_live/smil:vrt_events3_live.smil/playlist.m3u8"


def __get_media(file_name):
    return os.path.join(_addon_path, 'resources', 'media', file_name)


def __get_title_items():
    return {helperobjects.TitleItem(_addon_.getLocalizedString(32091), '{0}?action=listingaz', False, None),
            helperobjects.TitleItem(_addon_.getLocalizedString(32100), '{0}?action=listinglive', False, None)}


def __get_livestream_items():
    return {helperobjects.TitleItem(_addon_.getLocalizedString(32101),
                                    '{0}?action=playlive&video={1}'.format(_url, _VRT_LIVESTREAM_URL),
                                    True, __get_media("een.png")),
            helperobjects.TitleItem(_addon_.getLocalizedString(32102),
                                    '{0}?action=playlive&video={1}'.format(_url, _CANVAS_LIVESTREAM_),
                                    True, __get_media("canvas.png")),
            helperobjects.TitleItem(_addon_.getLocalizedString(32103),
                                    '{0}?action=playlive&video={1}'.format(_url, _KETNET_VRT),
                                    True, __get_media("ketnet.png"))}


def router( params_string):
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
            vrt_player.list_categories(__get_livestream_items())
        elif params['action'] == 'playlive':
            vrt_player.play_livestream(params['video'])
    else:
        vrt_player.list_categories(__get_title_items())

if __name__ == '__main__':
    router(sys.argv[2][1:])

