# -*- coding: utf-8 -*-

# GNU General Public License v2.0 (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

import requests
from bs4 import BeautifulSoup, SoupStrainer
from resources.lib.helperobjects import helperobjects
from resources.lib.kodiwrappers import sortmethod
from resources.lib.vrtplayer import actions, statichelper


class VRTPlayer:

    # URLs van https://services.vrt.be/videoplayer/r/live.json
    _EEN_LIVESTREAM = 'https://www.vrt.be/vrtnu/kanalen/een/'
    _CANVAS_LIVESTREAM_ = 'https://www.vrt.be/vrtnu/kanalen/canvas/'
    _KETNET_LIVESTREAM = 'https://www.vrt.be/vrtnu/kanalen/ketnet/'

    VRT_BASE = 'https://www.vrt.be/'
    VRTNU_BASE_URL = ''.join((VRT_BASE, '/vrtnu'))

    def __init__(self, kodi_wrapper, stream_service, api_helper):
        self._kodi_wrapper = kodi_wrapper
        self._api_helper = api_helper
        self._stream_service = stream_service

    def show_main_menu_items(self):
        menu_items = [
            helperobjects.TitleItem(self._kodi_wrapper.get_localized_string(32080),
                                    dict(action=actions.LISTING_AZ_TVSHOWS), False,
                                    'DefaultMovieTitle.png',
                                    dict(plot=self._kodi_wrapper.get_localized_string(32081))),
            helperobjects.TitleItem(self._kodi_wrapper.get_localized_string(32082),
                                    dict(action=actions.LISTING_CATEGORIES), False,
                                    'DefaultGenre.png',
                                    dict(plot=self._kodi_wrapper.get_localized_string(32083))),
            helperobjects.TitleItem(self._kodi_wrapper.get_localized_string(32084),
                                    dict(action=actions.LISTING_LIVE), False,
                                    'DefaultAddonPVRClient.png',
                                    dict(plot=self._kodi_wrapper.get_localized_string(32085))),
            helperobjects.TitleItem(self._kodi_wrapper.get_localized_string(32086),
                                    dict(action=actions.LISTING_EPISODES, video_url='recent'), False,
                                    'DefaultYear.png',
                                    dict(plot=self._kodi_wrapper.get_localized_string(32087))),
        ]
        self._kodi_wrapper.show_listing(menu_items, content_type='files')

    def show_tvshow_menu_items(self, path):
        menu_items = self._api_helper.get_tvshow_items(path)
        self._kodi_wrapper.show_listing(menu_items, sortmethod.ALPHABET, content_type='tvshows')

    def show_category_menu_items(self):
        joined_url = ''.join((self.VRTNU_BASE_URL, '/categorieen/'))
        menu_items = self.__get_category_menu_items(joined_url, {'class': 'nui-tile title'}, actions.LISTING_CATEGORY_TVSHOWS)
        self._kodi_wrapper.show_listing(menu_items, sort=sortmethod.ALPHABET, content_type='files')

    def play(self, video):
        stream = self._stream_service.get_stream(video)
        if stream is not None:
            self._kodi_wrapper.play(stream)

    def show_livestream_items(self):
        livestream_items = [
            helperobjects.TitleItem(self._kodi_wrapper.get_localized_string(32101),
                                    {'action': actions.PLAY, 'video_url': self._EEN_LIVESTREAM},
                                    True, self._api_helper.get_live_screenshot('een'),
                                    dict(plot=self._kodi_wrapper.get_localized_string(32101))),
            helperobjects.TitleItem(self._kodi_wrapper.get_localized_string(32102),
                                    {'action': actions.PLAY, 'video_url': self._CANVAS_LIVESTREAM_},
                                    True, self._api_helper.get_live_screenshot('canvas'),
                                    dict(plot=self._kodi_wrapper.get_localized_string(32102))),
            helperobjects.TitleItem(self._kodi_wrapper.get_localized_string(32103),
                                    {'action': actions.PLAY, 'video_url': self._KETNET_LIVESTREAM},
                                    True, self._api_helper.get_live_screenshot('ketnet'),
                                    dict(plot=self._kodi_wrapper.get_localized_string(32103))),
        ]
        self._kodi_wrapper.show_listing(livestream_items, content_type='videos')

    def show_episodes(self, path):
        title_items, sort = self._api_helper.get_episode_items(path)
        self._kodi_wrapper.show_listing(title_items, sort=sort, content_type='episodes')

    def __get_category_menu_items(self, url, soupstrainer_parser_selector, routing_action, video_dictionary_action=None):
        response = requests.get(url)
        tiles = SoupStrainer('a', soupstrainer_parser_selector)
        soup = BeautifulSoup(response.content, 'html.parser', parse_only=tiles)
        listing = []
        for tile in soup.find_all(class_='nui-tile title'):
            category = tile['href'].split('/')[-2]
            thumbnail, title = self.__get_category_thumbnail_and_title(tile)
            video_dictionary = None
            if video_dictionary_action is not None:
                video_dictionary = video_dictionary_action(tile)

            item = helperobjects.TitleItem(title, {'action': routing_action, 'video_url': category},
                                           False, thumbnail, video_dictionary)
            listing.append(item)
        return listing

    @staticmethod
    def __format_category_image_url(element):
        raw_thumbnail = element.find(class_='nui-tile--image')['data-responsive-image']
        return statichelper.replace_double_slashes_with_https(raw_thumbnail)

    @staticmethod
    def __get_category_thumbnail_and_title(element):
        thumbnail = VRTPlayer.__format_category_image_url(element)
        found_element = element.find('h2')
        title = ''
        if found_element is not None:
            title = statichelper.replace_newlines_and_strip(found_element.contents[0])
        return thumbnail, title
