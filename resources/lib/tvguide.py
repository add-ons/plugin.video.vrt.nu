# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
''' Implements a VRT NU TV guide '''

from __future__ import absolute_import, division, unicode_literals
import json
from datetime import datetime, timedelta
import dateutil.parser
import dateutil.tz

try:  # Python 3
    from urllib.request import build_opener, install_opener, ProxyHandler, urlopen
except ImportError:  # Python 2
    from urllib2 import build_opener, install_opener, ProxyHandler, urlopen

from data import CHANNELS
from favorites import Favorites
from helperobjects import TitleItem
from metadata import Metadata

DATE_STRINGS = {
    '-2': 30330,  # 2 days ago
    '-1': 30331,  # Yesterday
    '0': 30332,  # Today
    '1': 30333,  # Tomorrow
    '2': 30334,  # In 2 days
}

DATES = {
    '-1': 'yesterday',
    '0': 'today',
    '1': 'tomorrow',
}


class TVGuide:
    ''' This implements a VRT TV-guide that offers Kodi menus and TV guide info '''

    VRT_TVGUIDE = 'https://www.vrt.be/bin/epg/schedule.%Y-%m-%d.json'

    def __init__(self, _kodi):
        ''' Initializes TV-guide object '''
        self._kodi = _kodi
        self._favorites = Favorites(_kodi)
        self._metadata = Metadata(self._kodi, self._favorites)

        self._proxies = _kodi.get_proxies()
        install_opener(build_opener(ProxyHandler(self._proxies)))
        self._showfanart = _kodi.get_setting('showfanart', 'true') == 'true'

    def show_tvguide(self, date=None, channel=None):
        ''' Offer a menu depending on the information provided '''

        if not date and not channel:
            date_items = self.get_date_items()
            self._kodi.show_listing(date_items, category=30026, content='files')  # TV guide

        elif not channel:
            channel_items = self.get_channel_items(date=date)
            self._kodi.show_listing(channel_items, category=date)

        elif not date:
            date_items = self.get_date_items(channel=channel)
            self._kodi.show_listing(date_items, category=channel, content='files')

        else:
            episode_items = self.get_episode_items(date, channel)
            self._kodi.show_listing(episode_items, category='%s / %s' % (channel, date), content='episodes', cache=False)

    def get_date_items(self, channel=None):
        ''' Offer a menu to select the TV-guide date '''

        epg = datetime.now(dateutil.tz.tzlocal())
        # Daily EPG information shows information from 6AM until 6AM
        if epg.hour < 6:
            epg += timedelta(days=-1)
        date_items = []
        for i in range(7, -30, -1):
            day = epg + timedelta(days=i)
            title = self._kodi.localize_datelong(day)

            # Highlight today with context of 2 days
            if str(i) in DATE_STRINGS:
                if i == 0:
                    title = '[COLOR yellow][B]%s[/B], %s[/COLOR]' % (self._kodi.localize(DATE_STRINGS[str(i)]), title)
                else:
                    title = '[B]%s[/B], %s' % (self._kodi.localize(DATE_STRINGS[str(i)]), title)

            # Make permalinks for today, yesterday and tomorrow
            if str(i) in DATES:
                date = DATES[str(i)]
            else:
                date = day.strftime('%Y-%m-%d')

            # Show channel list or channel episodes
            if channel:
                path = self._kodi.url_for('tvguide', date=date, channel=channel)
            else:
                path = self._kodi.url_for('tvguide', date=date)

            cache_file = 'schedule.%s.json' % date
            date_items.append(TitleItem(
                title=title,
                path=path,
                art_dict=dict(thumb='DefaultYear.png'),
                info_dict=dict(plot=self._kodi.localize_datelong(day)),
                context_menu=[(self._kodi.localize(30413), 'RunPlugin(%s)' % self._kodi.url_for('delete_cache', cache_file=cache_file))],
            ))
        return date_items

    def get_channel_items(self, date=None, channel=None):
        ''' Offer a menu to select the channel '''
        if date:
            now = datetime.now(dateutil.tz.tzlocal())
            epg = self.parse(date, now)
            datelong = self._kodi.localize_datelong(epg)

        channel_items = []
        for chan in CHANNELS:
            # Only some channels are supported
            if not chan.get('has_tvguide'):
                continue

            # If a channel is requested, stop processing if it is no match
            if channel and channel != chan.get('name'):
                continue

            art_dict = {}

            # Try to use the white icons for thumbnails (used for icons as well)
            if self._kodi.get_cond_visibility('System.HasAddon(resource.images.studios.white)') == 1:
                art_dict['thumb'] = 'resource://resource.images.studios.white/{studio}.png'.format(**chan)
            else:
                art_dict['thumb'] = 'DefaultTags.png'

            if date:
                title = chan.get('label')
                path = self._kodi.url_for('tvguide', date=date, channel=chan.get('name'))
                plot = '%s\n%s' % (self._kodi.localize(30302, **chan), datelong)
            else:
                title = '[B]%s[/B]' % self._kodi.localize(30303, **chan)
                path = self._kodi.url_for('tvguide_channel', channel=chan.get('name'))
                plot = '%s\n\n%s' % (self._kodi.localize(30302, **chan), self.live_description(chan.get('name')))

            channel_items.append(TitleItem(
                title=title,
                path=path,
                art_dict=art_dict,
                info_dict=dict(plot=plot, studio=chan.get('studio')),
            ))
        return channel_items

    def get_episode_items(self, date, channel):
        ''' Show episodes for a given date and channel '''
        now = datetime.now(dateutil.tz.tzlocal())
        epg = self.parse(date, now)
        epg_url = epg.strftime(self.VRT_TVGUIDE)

        self._favorites.get_favorites(ttl=60 * 60)

        cache_file = 'schedule.%s.json' % date
        if date in ('today', 'yesterday', 'tomorrow'):
            # Try the cache if it is fresh
            schedule = self._kodi.get_cache(cache_file, ttl=60 * 60)
            if not schedule:
                self._kodi.log_notice('URL get: ' + epg_url, 'Verbose')
                schedule = json.load(urlopen(epg_url))
                self._kodi.update_cache(cache_file, schedule)
        else:
            self._kodi.log_notice('URL get: ' + epg_url, 'Verbose')
            schedule = json.load(urlopen(epg_url))

        name = channel
        try:
            channel = next(c for c in CHANNELS if c.get('name') == name)
            episodes = schedule.get(channel.get('id'), [])
        except StopIteration:
            episodes = []
        episode_items = []
        for episode in episodes:

            label = self._metadata.get_label(episode)

            context_menu = []
            path = None
            if episode.get('url'):
                from statichelper import add_https_method, url_to_program
                video_url = add_https_method(episode.get('url'))
                path = self._kodi.url_for('play_url', video_url=video_url)
                program = url_to_program(episode.get('url'))
                context_menu, favorite_marker = self._metadata.get_context_menu(episode, program, cache_file)
                label += favorite_marker

            info_labels = self._metadata.get_info_labels(episode, date=date, channel=channel)
            info_labels['title'] = label

            episode_items.append(TitleItem(
                title=label,
                path=path,
                art_dict=self._metadata.get_art(episode),
                info_dict=info_labels,
                is_playable=True,
                context_menu=context_menu,
            ))
        return episode_items

    def episode_description(self, episode):
        ''' Return a formatted description for an episode '''
        return '{start} - {end}\n» {title}'.format(**episode)

    def live_description(self, channel):
        ''' Return the EPG information for current and next live program '''
        now = datetime.now(dateutil.tz.tzlocal())
        epg = now
        # Daily EPG information shows information from 6AM until 6AM
        if epg.hour < 6:
            epg += timedelta(days=-1)
        # Try the cache if it is fresh
        schedule = self._kodi.get_cache('schedule.today.json', ttl=60 * 60)
        if not schedule:
            epg_url = epg.strftime(self.VRT_TVGUIDE)
            self._kodi.log_notice('URL get: ' + epg_url, 'Verbose')
            schedule = json.load(urlopen(epg_url))
            self._kodi.update_cache('schedule.today.json', schedule)
        name = channel
        try:
            channel = next(c for c in CHANNELS if c.get('name') == name)
            episodes = iter(schedule[channel.get('id')])
        except StopIteration:
            return ''

        description = ''
        while True:
            try:
                episode = next(episodes)
            except StopIteration:
                break
            start_date = dateutil.parser.parse(episode.get('startTime'))
            end_date = dateutil.parser.parse(episode.get('endTime'))
            if start_date <= now <= end_date:  # Now playing
                description = '[COLOR yellow][B]%s[/B] %s[/COLOR]\n' % (self._kodi.localize(30421), self.episode_description(episode))
                try:
                    description += '[B]%s[/B] %s' % (self._kodi.localize(30422), self.episode_description(next(episodes)))
                except StopIteration:
                    break
                break
            elif now < start_date:  # Nothing playing now, but this may be next
                description = '[B]%s[/B] %s\n' % (self._kodi.localize(30422), self.episode_description(episode))
                try:
                    description += '[B]%s[/B] %s' % (self._kodi.localize(30422), self.episode_description(next(episodes)))
                except StopIteration:
                    break
                break
        if not description:
            # Add a final 'No transmission' program
            description = '[COLOR yellow][B]%s[/B] %s - 06:00\n» %s[/COLOR]' % (self._kodi.localize(30421), episode.get('end'), self._kodi.localize(30423))
        return description

    def parse(self, date, now):
        ''' Parse a given string and return a datetime object
            This supports 'today', 'yesterday' and 'tomorrow'
            It also compensates for TV-guides covering from 6AM to 6AM
        '''
        if date == 'today':
            if now.hour < 6:
                return now + timedelta(days=-1)
            return now
        if date == 'yesterday':
            if now.hour < 6:
                return now + timedelta(days=-2)
            return now + timedelta(days=-1)
        if date == 'tomorrow':
            if now.hour < 6:
                return now
            return now + timedelta(days=1)

        return dateutil.parser.parse(date)
