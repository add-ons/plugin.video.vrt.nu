# -*- coding: utf-8 -*-

# GNU General Public License v2.0 (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

import requests
from resources.lib.vrtplayer import statichelper, metadatacreator, actions
from resources.lib.helperobjects import helperobjects
from resources.lib.kodiwrappers import sortmethod
from bs4 import BeautifulSoup
import time


class VRTApiHelper:

    def __init__(self, kodi_wrapper):
        self._kodi_wrapper = kodi_wrapper

    _VRT_BASE = 'https://www.vrt.be'
    _VRTNU_API_BASE = 'https://vrtnu-api.vrt.be'
    _API_URL = ''.join((_VRTNU_API_BASE, '/search'))
    _VRTNU_SUGGEST_URL = ''.join((_VRTNU_API_BASE, '/suggest'))
    _VRTNU_SCREENSHOT_URL = ''.join((_VRTNU_API_BASE, '/screenshots'))

    def get_tvshow_items(self, path):
        if path == 'az':
            api_url = ''.join((self._VRTNU_SUGGEST_URL, '?facets[transcodingStatus]=AVAILABLE'))
        else:
            api_url = ''.join((self._VRTNU_SUGGEST_URL, '?facets[categories]=', path))
        tvshows = requests.get(api_url).json()
        menu_items = []
        for tvshow in tvshows:
            metadata_creator = metadatacreator.MetadataCreator()
            metadata_creator.mediatype = 'tvshow'
            metadata_creator.plot = tvshow['description']
            thumbnail = statichelper.replace_double_slashes_with_https(tvshow['thumbnail'])
            # Cut vrtbase url off since it will be added again when searching for episodes (with a-z we dont have the
            # full url)
            video_url = statichelper.replace_double_slashes_with_https(tvshow['targetUrl']).replace(self._VRT_BASE, '')
            item = helperobjects.TitleItem(tvshow['title'], {'action': actions.LISTING_EPISODES, 'video_url': video_url},
                                           False, thumbnail, metadata_creator.get_video_dictionary())
            menu_items.append(item)
        return menu_items

    def _get_season_items(self, api_url, facets):
        title_items = None
        # Check if program has seasons
        for facet in facets:
            if facet['name'] == 'seasons' and len(facet['buckets']) > 1:
                # Found multiple seasons, make list of seasons
                title_items = []
                for bucket in facet['buckets']:
                    # Make season list
                    title_items.append(self._map_to_season_title_item(api_url, bucket))
        return title_items

    def get_episode_items(self, path):
        if path == 'recent':
            api_url = ''.join((self._API_URL, '?i=video&size=50&facets[transcodingStatus]=AVAILABLE&facets[brands]=[een,canvas,sporza,radio1,klara,stubru,mnm]'))
            api_json = requests.get(api_url).json()
            title_items, sort_method = self._map_to_episode_items(api_json['results'], path)
        else:
            api_url = ''.join((self._API_URL, '?i=video&size=150&facets[programUrl]=//www.vrt.be', path.replace('.relevant', ''))) if '.relevant/' in path else path
            api_json = requests.get(api_url).json()
            title_items = self._get_season_items(api_url, api_json['facets']['facets'])
            sort_method = None
            if title_items is None:
                #only one season, make list of episodes
                title_items, sort_method = self._map_to_episode_items(api_json['results'])

        return title_items, sort_method

    def _map_to_episode_items(self, results, titletype=None):
        title_items = []
        sort = None
        for result in results:
            metadata_creator = metadatacreator.MetadataCreator()
            metadata_creator.tvshowtitle = result['program']
            json_broadcast_date = result['broadcastDate']
            if json_broadcast_date != -1:
                metadata_creator.datetime = time.localtime(result['broadcastDate']/1000)

            metadata_creator.duration = (result['duration'] * 60) # Minutes to seconds
            metadata_creator.plot = BeautifulSoup(result['description'], 'html.parser').text
            metadata_creator.plotoutline = result['shortDescription']
            metadata_creator.season = result['seasonName']
            metadata_creator.episode = result['episodeNumber']
            metadata_creator.mediatype = result['type']
            thumb = statichelper.replace_double_slashes_with_https(result['videoThumbnailUrl']) if result['videoThumbnailUrl'].startswith("//") else result['videoThumbnailUrl']
            video_url = statichelper.replace_double_slashes_with_https(result['url']) if result['url'].startswith("//") else result['url']
            title, sort = self._make_title(result, titletype)
            title_items.append(helperobjects.TitleItem(title, {'action': actions.PLAY, 'video_url': video_url, 'video_id' : result['videoId'], 'publication_id' : result['publicationId']}, True, thumb, metadata_creator.get_video_dictionary()))
        return title_items, sort

    def _map_to_season_title_item(self, api_url, bucket):
        metadata_creator = metadatacreator.MetadataCreator()
        metadata_creator.mediatype = 'season'
        season_title = bucket['key']
        title = ''.join((self._kodi_wrapper.get_localized_string(32094), ' ', season_title))
        path = ''.join((api_url, '&facets[seasonName]=', season_title.replace(' ', '-')))
        return helperobjects.TitleItem(title, {'action': actions.LISTING_EPISODES, 'video_url': path}, False, None, metadata_creator.get_video_dictionary())

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
        sort = None
        if titletype == 'recent':
            title = result['program'] + ' - ' + BeautifulSoup(result['shortDescription'], 'html.parser').text
        else:
            if result['formattedBroadcastShortDate'] != '' and result['shortDescription'] != '':
                title = result['formattedBroadcastShortDate'] + ' - ' + BeautifulSoup(result['shortDescription'], 'html.parser').text
            elif result['formattedBroadcastShortDate'] != '' and result['title'] != '':
                title = result['formattedBroadcastShortDate'] + ' - ' + BeautifulSoup(result['title'], 'html.parser').text
            else:
                title = ''.join((self._kodi_wrapper.get_localized_string(32095), ' ', str(result['episodeNumber']), ' - ', BeautifulSoup(result['title'], 'html.parser').text))
                sort = sortmethod.ALPHABET
        return title, sort
