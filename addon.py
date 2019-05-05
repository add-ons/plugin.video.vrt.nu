# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

''' This is the actual VRT Nu video plugin entry point '''

from __future__ import absolute_import, division, unicode_literals
import sys

from vrtnu.kodiwrapper import KodiWrapper
from vrtnu.helperobjects import TitleItem
import routing
from xbmcaddon import Addon

try:
    from urllib.request import build_opener, install_opener, ProxyHandler, urlopen
except ImportError:
    from urllib2 import build_opener, install_opener, ProxyHandler, urlopen

plugin = routing.Plugin()

_ADDON_URL = sys.argv[0]
addon = Addon()
kodi_wrapper = KodiWrapper(_ADDON_URL, addon, plugin)


#    if action == actions.LISTING_AZ_TVSHOWS:
#        vrt_player.show_tvshow_menu_items()
#    elif action == actions.LISTING_CATEGORIES:
#        vrt_player.show_category_menu_items()
#    elif action == actions.LISTING_CHANNELS:
#        vrt_player.show_channels_menu_items(channel=params.get('channel'))
#    elif action == actions.LISTING_LIVE:
#        vrt_player.show_livestream_items()
#    elif action == actions.LISTING_EPISODES:
#        vrt_player.show_episodes(path=params.get('video_url'))
#    elif action == actions.LISTING_RECENT:
#        vrt_player.show_recent(page=params.get('page', 1))
#    elif action == actions.LISTING_CATEGORY_TVSHOWS:
#        vrt_player.show_tvshow_menu_items(category=params.get('category'))
#    elif action == actions.PLAY:
#        vrt_player.play(params)
#    else:
#        vrt_player.show_main_menu_items()


@plugin.route('/')
def main():
    main_items = [
        # TitleItem(title=kodi_wrapper.get_localized_string(30080),
        #           url=plugin.url_for(programs),
        #           is_playable=False,
        #           art_dict=dict(thumb='DefaultMovieTitle.png', icon='DefaultMovieTitle.png', fanart='DefaultMovieTitle.png'),
        #           video_dict=dict(plot=kodi_wrapper.get_localized_string(30081))),
        # TitleItem(title=kodi_wrapper.get_localized_string(30082),
        #           url=plugin.url_for(categories),
        #           is_playable=False,
        #           art_dict=dict(thumb='DefaultGenre.png', icon='DefaultGenre.png', fanart='DefaultGenre.png'),
        #           video_dict=dict(plot=kodi_wrapper.get_localized_string(30083))),
        TitleItem(title=kodi_wrapper.get_localized_string(30084),
                  url=plugin.url_for(channels, channel=None),
                  is_playable=False,
                  art_dict=dict(thumb='DefaultTags.png', icon='DefaultTags.png', fanart='DefaultTags.png'),
                  video_dict=dict(plot=kodi_wrapper.get_localized_string(30085))),
        TitleItem(title=kodi_wrapper.get_localized_string(30086),
                  url=plugin.url_for(livetv, channel=None),
                  is_playable=False,
                  art_dict=dict(thumb='DefaultAddonPVRClient.png', icon='DefaultAddonPVRClient.png', fanart='DefaultAddonPVRClient.png'),
                  video_dict=dict(plot=kodi_wrapper.get_localized_string(30087))),
        TitleItem(title=kodi_wrapper.get_localized_string(30088),
                  url=plugin.url_for(recent, page=None),
                  is_playable=False,
                  art_dict=dict(thumb='DefaultYear.png', icon='DefaultYear.png', fanart='DefaultYear.png'),
                  video_dict=dict(plot=kodi_wrapper.get_localized_string(30089))),
        TitleItem(title=kodi_wrapper.get_localized_string(30090),
                  url=plugin.url_for(tvguide, date=None, channel=None),
                  is_playable=False,
                  art_dict=dict(thumb='DefaultAddonTvInfo.png', icon='DefaultAddonTvInfo.png', fanart='DefaultAddonTvInfo.png'),
                  video_dict=dict(plot=kodi_wrapper.get_localized_string(30091))),
    ]
    kodi_wrapper.show_listing(main_items)


# @plugin.route('/categories/<category>')
# def categories(category=None):
#     from vrtnu.vrtplayer import VRTPlayer
#     if category:
#         VRTPlayer(kodi_wrapper).show_tvshow_menu_items(category=category)
#     else:
#         VRTPlayer(kodi_wrapper).show_category_menu_items()


@plugin.route('/channels/<channel>')
def channels(channel=None):
    from vrtnu.vrtplayer import VRTPlayer
    VRTPlayer(kodi_wrapper).show_channels_menu_items(channel=channel)


@plugin.route('/livetv/<channel>')
def livetv(channel=None):
    from vrtnu.vrtplayer import VRTPlayer
    if channel:
        pass  # play()
    else:
        VRTPlayer(kodi_wrapper).show_livestream_items()


# /play/id/<video_id>
# /play/video/<video_url>
@plugin.route('/play/url/<video_url>')
@plugin.route('/play/id/<video_id>')
@plugin.route('/play/pub/<video_id>')
@plugin.route('/play/url/<video_url>/id/<video_id>/pub/<publication_id>')
def play(video_url=None, video_id=None, publication_id=None):
    import streamservice
    import tokenresolver
    token_resolver = tokenresolver.TokenResolver(kodi_wrapper)
    stream_service = streamservice.StreamService(kodi_wrapper, token_resolver)
    stream = stream_service.get_stream(video_url, video_id, publication_id)
    if stream is not None:
        kodi_wrapper.play(stream)


# @plugin.route('/programs/<program>/<season>')
# def programs(program=None, season=None):
#     from vrtnu.vrtplayer import VRTPlayer
#     if program and season:
#         pass
#     elif program:
#         pass
#     else:
#         VRTPlayer(kodi_wrapper).show_tvshow_menu_items()


@plugin.route('/recent/<page>')
def recent(page=None):
    from vrtnu.vrtplayer import VRTPlayer
    VRTPlayer(kodi_wrapper).show_recent(page=page)

# /tvguide/yesterday
# /tvguide/today
# /tvguide/tomorrow
@plugin.route('/tvguide/<date>/<channel>')
def tvguide(date=None, channel=None):
    from datetime import datetime, timedelta
    import dateutil.parser
    import dateutil.tz
    import json

    from vrtnu import metadatacreator, statichelper
    from vrtnu.data import CHANNELS, DATE_STRINGS

    VRT_TVGUIDE = 'https://www.vrt.be/bin/epg/schedule.%Y-%m-%d.json'

    proxies = kodi_wrapper.get_proxies()
    install_opener(build_opener(ProxyHandler(proxies)))
    kodi_wrapper.set_locale()

    if not date:
        now = datetime.now(dateutil.tz.tzlocal())
        date_items = []
        for i in range(7, -31, -1):
            day = now + timedelta(days=i)
            title = day.strftime(kodi_wrapper.get_localized_datelong())
            if str(i) in DATE_STRINGS:
                if i == 0:
                    title = '[COLOR yellow][B]%s[/B], %s[/COLOR]' % (kodi_wrapper.get_localized_string(DATE_STRINGS[str(i)]), title)
                else:
                    title = '[B]%s[/B], %s' % (kodi_wrapper.get_localized_string(DATE_STRINGS[str(i)]), title)
            date_items.append(TitleItem(
                title=title,
                url=plugin.url_for(tvguide, date=day.strftime('%Y-%m-%d')),
                is_playable=False,
                art_dict=dict(thumb='DefaultYear.png', icon='DefaultYear.png', fanart='DefaultYear.png'),
                video_dict=dict(plot=day.strftime(kodi_wrapper.get_localized_datelong()))
            ))
        kodi_wrapper.show_listing(date_items, content_type='files')

    elif not channel:
        dateobj = dateutil.parser.parse(date)
        datelong = dateobj.strftime(kodi_wrapper.get_localized_datelong())

        fanart_path = 'resource://resource.images.studios.white/%(studio)s.png'
        icon_path = 'resource://resource.images.studios.white/%(studio)s.png'
        # NOTE: Wait for resource.images.studios.coloured v0.16 to be released
        # icon_path = 'resource://resource.images.studios.coloured/%(studio)s.png'

        channel_items = []
        for chan in CHANNELS:
            if chan.get('name') not in ('een', 'canvas', 'ketnet'):
                continue

            icon = icon_path % chan
            fanart = fanart_path % chan
            plot = kodi_wrapper.get_localized_string(30301) % chan.get('label') + '\n' + datelong
            channel_items.append(TitleItem(
                title=chan.get('label'),
                url=plugin.url_for(tvguide, date=date, channel=chan.get('name')),
                is_playable=False,
                art_dict=dict(thumb=icon, icon=icon, fanart=fanart),
                video_dict=dict(plot=plot, studio=chan.get('studio')),
            ))
        kodi_wrapper.show_listing(channel_items)

    else:
        now = datetime.now(dateutil.tz.tzlocal())
        dateobj = dateutil.parser.parse(date)
        datelong = dateobj.strftime(kodi_wrapper.get_localized_datelong())
        api_url = dateobj.strftime(VRT_TVGUIDE)
        schedule = json.loads(urlopen(api_url).read())
        name = channel
        try:
            channel = next(c for c in CHANNELS if c.get('name') == name)
            episodes = schedule[channel.get('id')]
        except StopIteration:
            episodes = []
        episode_items = []
        for episode in episodes:
            metadata = metadatacreator.MetadataCreator()
            title = episode.get('title')
            start = episode.get('start')
            end = episode.get('end')
            start_date = dateutil.parser.parse(episode.get('startTime'))
            end_date = dateutil.parser.parse(episode.get('endTime'))
            url = episode.get('url')
            label = '%s - %s' % (start, title)
            metadata.tvshowtitle = title
            metadata.datetime = dateobj
            # NOTE: Do not use startTime and endTime as we don't want duration in seconds
            metadata.duration = (dateutil.parser.parse(end) - dateutil.parser.parse(start)).total_seconds()
            metadata.plot = '[B]%s[/B]\n%s\n%s - %s\n[I]%s[/I]' % (title, datelong, start, end, channel.get('label'))
            metadata.brands = [channel]
            metadata.mediatype = 'episode'
            thumb = episode.get('image', 'DefaultAddonVideo.png')
            metadata.icon = thumb
            if url:
                video_url = statichelper.add_https_method(url)
                url = plugin.url_for(play, video_url=video_url)
                if start_date < now <= end_date:  # Now playing
                    metadata.title = '[COLOR yellow]%s[/COLOR] %s' % (label, kodi_wrapper.get_localized_string(30302))
                else:
                    metadata.title = label
            else:
                # FIXME: Find a better solution for non-actionable items
                url = plugin.url_for(tvguide, date=date, channel=channel)
                if start_date < now <= end_date:  # Now playing
                    metadata.title = '[COLOR brown]%s[/COLOR] %s' % (label, kodi_wrapper.get_localized_string(30302))
                else:
                    metadata.title = '[COLOR gray]%s[/COLOR]' % label
            episode_items.append(TitleItem(
                title=metadata.title,
                url=url,
                is_playable=bool(url),
                art_dict=dict(thumb=thumb, icon='DefaultAddonVideo.png', fanart=thumb),
                video_dict=metadata.get_video_dict(),
            ))
        kodi_wrapper.show_listing(episode_items, content_type='episodes', cache=False)


if __name__ == '__main__':
    plugin.run()
