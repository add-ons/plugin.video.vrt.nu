# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, unicode_literals
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time

from resources.lib.vrtplayer import statichelper, metadatacreator, actions
from resources.lib.helperobjects import helperobjects
from resources.lib.kodiwrappers import sortmethod


class VRTApiHelper:

    _VRT_BASE = 'https://www.vrt.be'
    _VRTNU_API_BASE = 'https://vrtnu-api.vrt.be'
    _VRTNU_SEARCH_URL = ''.join((_VRTNU_API_BASE, '/search'))
    _VRTNU_SUGGEST_URL = ''.join((_VRTNU_API_BASE, '/suggest'))
    _VRTNU_SCREENSHOT_URL = ''.join((_VRTNU_API_BASE, '/screenshots'))

    def __init__(self, kodi_wrapper):
        self._kodi_wrapper = kodi_wrapper
        self._proxies = self._kodi_wrapper.get_proxies()

    def get_tvshow_items(self, path):
        if path == 'az':
            api_url = ''.join((self._VRTNU_SUGGEST_URL, '?facets[transcodingStatus]=AVAILABLE'))
        else:
            api_url = ''.join((self._VRTNU_SUGGEST_URL, '?facets[categories]=', path))
        tvshows = requests.get(api_url, proxies=self._proxies).json()
        tvshow_items = []
        for tvshow in tvshows:
            metadata_creator = metadatacreator.MetadataCreator()
            metadata_creator.mediatype = 'tvshow'
            metadata_creator.tvshowtitle = tvshow.get('title')
            metadata_creator.plot = statichelper.unescape(tvshow.get('description'))
            metadata_creator.brands = tvshow.get('brands')
            thumbnail = statichelper.add_https_method(tvshow.get('thumbnail'))
            # Cut vrtbase url off since it will be added again when searching for episodes
            # (with a-z we dont have the full url)
            video_url = statichelper.add_https_method(tvshow.get('targetUrl')).replace(self._VRT_BASE, '')
            tvshow_items.append(helperobjects.TitleItem(title=tvshow.get('title'),
                                                        url_dict=dict(action=actions.LISTING_EPISODES, video_url=video_url),
                                                        is_playable=False,
                                                        art_dict=dict(thumb=thumbnail, icon='DefaultAddonVideo.png', fanart=thumbnail),
                                                        video_dict=metadata_creator.get_video_dict()))
        return tvshow_items

    def _get_season_items(self, api_url, api_json):
        season_items = []
        if api_json.get('results'):
            episode = api_json['results'][0]
        else:
            episode = dict()
        facets = api_json.get('facets', dict()).get('facets', [])
        # Check if program has seasons
        for facet in facets:
            if facet.get('name') == 'seasons' and len(facet.get('buckets', [])) > 1:
                # Found multiple seasons, make list of seasons
                season_items = self._map_to_season_items(api_url, facet.get('buckets', []), episode)
        return season_items

    def get_episode_items(self, path):
        episode_items = []
        sort = None
        if path == 'recent':
            params = {
                'i': 'video',
                'size': '100',
                'facets[transcodingStatus]': 'AVAILABLE',
                'facets[brands]': '[een,canvas,sporza,vrtnws,vrtnxt,radio1,radio2,klara,stubru,mnm]',
            }
            api_url = self._VRTNU_SEARCH_URL + '?' + '&'.join(['='.join(t) for t in params.items()])
            api_json = requests.get(api_url, proxies=self._proxies).json()
            episode_items, sort = self._map_to_episode_items(api_json.get('results', []), path)
        else:
            if '.relevant/' in path:
                params = {
                    'i': 'video',
                    'size': '150',
                    'facets[programUrl]': '//www.vrt.be' + path.replace('.relevant/', '/'),
                }
                api_url = self._VRTNU_SEARCH_URL + '?' + '&'.join(['='.join(t) for t in params.items()])
            else:
                api_url = path
            api_json = requests.get(api_url, proxies=self._proxies).json()
            season_key = None
            # Look for seasons items if not yet done
            if 'facets[seasonTitle]' not in path:
                episode_items = self._get_season_items(api_url, api_json)
            else:
                season_key = path.split('facets[seasonTitle]=')[1]
            # No season items, generate episode items
            if not episode_items:
                episode_items, sort = self._map_to_episode_items(api_json.get('results', []), season_key=season_key)

        return episode_items, sort

    def _map_to_episode_items(self, episodes, titletype=None, season_key=None):
        episode_items = []
        sort = None
        for episode in episodes:
            # VRT API workaround: seasonTitle facet behaves as a partial match regex,
            # so we have to filter out the episodes from seasons that don't exactly match.
            if season_key and episode.get('seasonTitle') != season_key:
                continue

            display_options = episode.get('displayOptions', dict())

            if episode.get('programType') == 'reeksoplopend' and titletype is None:
                titletype = 'reeksoplopend'

            metadata_creator = metadatacreator.MetadataCreator()
            metadata_creator.tvshowtitle = episode.get('program')
            if episode.get('broadcastDate') != -1:
                metadata_creator.datetime = datetime.fromtimestamp(episode.get('broadcastDate', 0) / 1000)

            metadata_creator.duration = (episode.get('duration', 0) * 60)  # Minutes to seconds
            metadata_creator.plot = BeautifulSoup(episode.get('description'), 'html.parser').text
            metadata_creator.brands = episode.get('programBrands', episode.get('brands'))
            metadata_creator.geolocked = episode.get('allowedRegion') == 'BE'
            if display_options.get('showShortDescription'):
                short_description = BeautifulSoup(episode.get('shortDescription'), 'html.parser').text
                metadata_creator.plotoutline = short_description
                metadata_creator.subtitle = short_description
            else:
                metadata_creator.plotoutline = episode.get('subtitle')
                metadata_creator.subtitle = episode.get('subtitle')
            metadata_creator.season = episode.get('seasonName')
            metadata_creator.episode = episode.get('episodeNumber')
            metadata_creator.mediatype = episode.get('type', 'episode')
            if episode.get('assetOnTime'):
                metadata_creator.ontime = datetime(*time.strptime(episode.get('assetOnTime'), '%Y-%m-%dT%H:%M:%S+0000')[0:6])
            if episode.get('assetOffTime'):
                metadata_creator.offtime = datetime(*time.strptime(episode.get('assetOffTime'), '%Y-%m-%dT%H:%M:%S+0000')[0:6])

            # Add additional metadata to plot
            plot_meta = ''
            if metadata_creator.geolocked:
                # Show Geo-locked
                plot_meta += self._kodi_wrapper.get_localized_string(32201)
            # Only display when a video disappears if it is within the next 3 months
            if metadata_creator.offtime is not None and (metadata_creator.offtime - datetime.utcnow()).days < 93:
                # Show date when episode is removed
                plot_meta += self._kodi_wrapper.get_localized_string(32202) \
                             % metadata_creator.offtime.strftime(self._kodi_wrapper.get_localized_dateshort())
                # Show the remaining days/hours the episode is still available
                if (metadata_creator.offtime - datetime.utcnow()).days > 0:
                    plot_meta += self._kodi_wrapper.get_localized_string(32203) % (metadata_creator.offtime - datetime.utcnow()).days
                else:
                    plot_meta += self._kodi_wrapper.get_localized_string(32204) % int((metadata_creator.offtime - datetime.utcnow()).seconds / 3600)
            if plot_meta:
                metadata_creator.plot = plot_meta + '\n' + metadata_creator.plot

            thumb = statichelper.add_https_method(episode.get('videoThumbnailUrl'))
            fanart = statichelper.add_https_method(episode.get('programImageUrl', thumb))
            video_url = statichelper.add_https_method(episode.get('url'))
            title, sort = self._make_title(episode, titletype)
            metadata_creator.title = title
            episode_items.append(helperobjects.TitleItem(
                title=title,
                url_dict=dict(action=actions.PLAY, video_url=video_url, video_id=episode.get('videoId'), publication_id=episode.get('publicationId')),
                is_playable=True,
                art_dict=dict(thumb=thumb, icon='DefaultAddonVideo.png', fanart=fanart),
                video_dict=metadata_creator.get_video_dict(),
            ))
        return episode_items, sort

    def _map_to_season_items(self, api_url, seasons, episode):
        season_items = []
        fanart = statichelper.add_https_method(episode.get('programImageUrl'))
        program_type = episode.get('programType')
        metadata_creator = metadatacreator.MetadataCreator()
        metadata_creator.mediatype = 'season'

        # Reverse sort seasons if program_type is 'reeksaflopend' or 'daily'
        if program_type in ('daily', 'reeksaflopend'):
            seasons = sorted(seasons, key=lambda k: k['key'], reverse=True)

        for season in seasons:
            season_key = season.get('key')
            title = ''.join((self._kodi_wrapper.get_localized_string(32094), ' ', season_key))
            season_facet = '&facets[seasonTitle]='
            path = ''.join((api_url, season_facet, season_key))
            season_items.append(helperobjects.TitleItem(
                title=title,
                url_dict=dict(action=actions.LISTING_EPISODES, video_url=path),
                is_playable=False,
                art_dict=dict(thumb=fanart, icon='DefaultSets.png', fanart=fanart),
                video_dict=metadata_creator.get_video_dict(),
            ))
        return season_items

    def get_live_screenshot(self, channel):
        url = ''.join((self._VRTNU_SCREENSHOT_URL, '/', channel, '.jpg'))
        self.__delete_cached_thumbnail(url)
        return url

    def __delete_cached_thumbnail(self, url):
        crc = self.__get_crc32(url)
        ext = url.split('.')[-1]
        path = ''.join(('special://thumbnails/', crc[0], '/', crc, '.', ext))
        self._kodi_wrapper.delete_path(path)

    @staticmethod
    def __get_crc32(string):
        string = string.lower()
        string_bytes = bytearray(string.encode())
        crc = 0xffffffff
        for b in string_bytes:
            crc = crc ^ (b << 24)
            for _ in range(8):
                if crc & 0x80000000:
                    crc = (crc << 1) ^ 0x04C11DB7
                else:
                    crc = crc << 1
            crc = crc & 0xFFFFFFFF
        return '%08x' % crc

    def _make_title(self, result, titletype):
        short_description = BeautifulSoup(result.get('shortDescription') or result.get('title'), 'html.parser').text

        if titletype == 'recent':
            title = '%s - %s' % (result.get('program'), short_description)
            sort = None
        elif titletype == 'reeksoplopend' or result.get('formattedBroadcastShortDate') == '':
            title = '%s %s - %s' % (self._kodi_wrapper.get_localized_string(32095), result.get('episodeNumber'), short_description)
            sort = sortmethod.ALPHABET
        else:
            title = '%s - %s' % (result.get('formattedBroadcastShortDate'), short_description)
            sort = None

        return title, sort
