import sys
from urlparse import parse_qsl
from resources.lib.vrtplayer import vrtplayer


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
    else:
        vrt_player.list_categories()


_url = sys.argv[0]
_handle = int(sys.argv[1])

if __name__ == '__main__':
    router(sys.argv[2][1:])

