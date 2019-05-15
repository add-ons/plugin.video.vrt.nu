# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, unicode_literals
from datetime import datetime, timedelta
import dateutil.parser
import dateutil.tz
import json

try:
    from urllib.request import build_opener, install_opener, ProxyHandler, urlopen
except ImportError:
    from urllib2 import build_opener, install_opener, ProxyHandler, urlopen

from resources.lib.helperobjects import helperobjects
from resources.lib.vrtplayer import CHANNELS, actions, metadatacreator, statichelper

DATE_STRINGS = {
    '-2': 30330,  # 2 days ago
    '-1': 30331,  # Yesterday
    '0': 30332,  # Today
    '1': 30333,  # Tomorrow
    '2': 30334,  # In 2 days
}


class TVGuide:

    VRT_TVGUIDE = 'https://www.vrt.be/bin/epg/schedule.%Y-%m-%d.json'

    def __init__(self, _kodi):
        self._kodi = _kodi
        self._proxies = _kodi.get_proxies()
        install_opener(build_opener(ProxyHandler(self._proxies)))

    def show_tvguide(self, params):
        date = params.get('date')
        channel = params.get('channel')

        if not date:
            date_items = self.show_date_menu()
            self._kodi.show_listing(date_items, content='files')

        elif not channel:
            channel_items = self.show_channel_menu(date)
            self._kodi.show_listing(channel_items)

        else:
            episode_items = self.show_episodes(date, channel)
            self._kodi.show_listing(episode_items, content='episodes', cache=False)

    def show_date_menu(self):
        now = datetime.now(dateutil.tz.tzlocal())
        date_items = []
        for i in range(7, -31, -1):
            day = now + timedelta(days=i)
            title = self._kodi.localize_datelong(day)
            if str(i) in DATE_STRINGS:
                if i == 0:
                    title = '[COLOR yellow][B]%s[/B], %s[/COLOR]' % (self._kodi.localize(DATE_STRINGS[str(i)]), title)
                else:
                    title = '[B]%s[/B], %s' % (self._kodi.localize(DATE_STRINGS[str(i)]), title)
            date_items.append(helperobjects.TitleItem(
                title=title,
                url_dict=dict(action=actions.LISTING_TVGUIDE, date=day.strftime('%Y-%m-%d')),
                is_playable=False,
                art_dict=dict(thumb='DefaultYear.png', icon='DefaultYear.png', fanart='DefaultYear.png'),
                video_dict=dict(plot=self._kodi.localize_datelong(day)),
            ))
        return date_items

    def show_channel_menu(self, date):
        dateobj = dateutil.parser.parse(date)
        datelong = self._kodi.localize_datelong(dateobj)

        fanart_path = 'resource://resource.images.studios.white/%(studio)s.png'
        icon_path = 'resource://resource.images.studios.white/%(studio)s.png'
        # NOTE: Wait for resource.images.studios.coloured v0.16 to be released
        # icon_path = 'resource://resource.images.studios.coloured/%(studio)s.png'

        channel_items = []
        for channel in CHANNELS:
            if channel.get('name') not in ('een', 'canvas', 'ketnet'):
                continue

            icon = icon_path % channel
            fanart = fanart_path % channel
            plot = self._kodi.localize(30301) % channel.get('label') + '\n' + datelong
            channel_items.append(helperobjects.TitleItem(
                title=channel.get('label'),
                url_dict=dict(action=actions.LISTING_TVGUIDE, date=date, channel=channel.get('name')),
                is_playable=False,
                art_dict=dict(thumb=icon, icon=icon, fanart=fanart),
                video_dict=dict(plot=plot, studio=channel.get('studio')),
            ))
        return channel_items

    def show_episodes(self, date, channel):
        now = datetime.now(dateutil.tz.tzlocal())
        dateobj = dateutil.parser.parse(date)
        datelong = self._kodi.localize_datelong(dateobj)
        api_url = dateobj.strftime(self.VRT_TVGUIDE)
        self._kodi.log_notice('URL get: ' + api_url, 'Verbose')
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
            title = episode.get('title', 'Untitled')
            start = episode.get('start')
            end = episode.get('end')
            start_date = dateutil.parser.parse(episode.get('startTime'))
            end_date = dateutil.parser.parse(episode.get('endTime'))
            url = episode.get('url')
            label = '%s - %s' % (start, title)
            metadata.tvshowtitle = title
            metadata.datetime = dateobj
            # NOTE: Do not use startTime and endTime as we don't want duration with seconds granularity
            start_time = dateutil.parser.parse(start)
            end_time = dateutil.parser.parse(end)
            if end_time < start_time:
                end_time = end_time + timedelta(days=1)
            metadata.duration = (end_time - start_time).total_seconds()
            metadata.plot = '[B]%s[/B]\n%s\n%s - %s\n[I]%s[/I]' % (title, datelong, start, end, channel.get('label'))
            metadata.brands = [channel.get('studio')]
            metadata.mediatype = 'episode'
            thumb = episode.get('image', 'DefaultAddonVideo.png')
            metadata.icon = thumb
            if url:
                video_url = statichelper.add_https_method(url)
                url_dict = dict(action=actions.PLAY, video_url=video_url)
                if start_date < now <= end_date:  # Now playing
                    metadata.title = '[COLOR yellow]%s[/COLOR] %s' % (label, self._kodi.localize(30302))
                else:
                    metadata.title = label
            else:
                # FIXME: Find a better solution for non-actionable items
                url_dict = dict(action=actions.LISTING_TVGUIDE, date=date, channel=channel.get('name'))
                if start_date < now <= end_date:  # Now playing
                    metadata.title = '[COLOR brown]%s[/COLOR] %s' % (label, self._kodi.localize(30302))
                else:
                    metadata.title = '[COLOR gray]%s[/COLOR]' % label
            episode_items.append(helperobjects.TitleItem(
                title=metadata.title,
                url_dict=url_dict,
                is_playable=bool(url),
                art_dict=dict(thumb=thumb, icon='DefaultAddonVideo.png', fanart=thumb),
                video_dict=metadata.get_video_dict(),
            ))
        return episode_items
