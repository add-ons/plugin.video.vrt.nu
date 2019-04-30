# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, unicode_literals
from bs4 import BeautifulSoup, SoupStrainer
import os
import requests

from resources.lib.helperobjects import helperobjects
from resources.lib.vrtplayer import CATEGORIES, CHANNELS, actions, statichelper


def get_categories(proxies=None):
    response = requests.get('https://www.vrt.be/vrtnu/categorieen/', proxies=proxies)
    tiles = SoupStrainer('a', {'class': 'nui-tile'})
    soup = BeautifulSoup(response.content, 'html.parser', parse_only=tiles)

    categories = []
    for tile in soup.find_all(class_='nui-tile'):
        categories.append(dict(
            id=tile.get('href').split('/')[-2],
            thumbnail=get_category_thumbnail(tile),
            name=get_category_title(tile),
        ))

    return categories


def get_category_thumbnail(element):
    raw_thumbnail = element.find(class_='media').get('data-responsive-image', 'DefaultGenre.png')
    return statichelper.add_https_method(raw_thumbnail)


def get_category_title(element):
    found_element = element.find('h3')
    if found_element is not None:
        return statichelper.strip_newlines(found_element.contents[0])
    return ''


class VRTPlayer:

    def __init__(self, addon_path, kodi_wrapper, stream_service, api_helper):
        self._addon_path = addon_path
        self._kodi_wrapper = kodi_wrapper
        self._proxies = self._kodi_wrapper.get_proxies()
        self._api_helper = api_helper
        self._stream_service = stream_service

    def show_main_menu_items(self):
        main_items = [
            helperobjects.TitleItem(title=self._kodi_wrapper.get_localized_string(32080),
                                    url_dict=dict(action=actions.LISTING_AZ_TVSHOWS),
                                    is_playable=False,
                                    art_dict=dict(thumb='DefaultMovieTitle.png', icon='DefaultMovieTitle.png', fanart='DefaultMovieTitle.png'),
                                    video_dict=dict(plot=self._kodi_wrapper.get_localized_string(32081))),
            helperobjects.TitleItem(title=self._kodi_wrapper.get_localized_string(32082),
                                    url_dict=dict(action=actions.LISTING_CATEGORIES),
                                    is_playable=False,
                                    art_dict=dict(thumb='DefaultGenre.png', icon='DefaultGenre.png', fanart='DefaultGenre.png'),
                                    video_dict=dict(plot=self._kodi_wrapper.get_localized_string(32083))),
            helperobjects.TitleItem(title=self._kodi_wrapper.get_localized_string(32084),
                                    url_dict=dict(action=actions.LISTING_LIVE),
                                    is_playable=False,
                                    art_dict=dict(thumb='DefaultAddonPVRClient.png', icon='DefaultAddonPVRClient.png', fanart='DefaultAddonPVRClient.png'),
                                    video_dict=dict(plot=self._kodi_wrapper.get_localized_string(32085))),
            helperobjects.TitleItem(title=self._kodi_wrapper.get_localized_string(32086),
                                    url_dict=dict(action=actions.LISTING_EPISODES, video_url='recent'),
                                    is_playable=False,
                                    art_dict=dict(thumb='DefaultYear.png', icon='DefaultYear.png', fanart='DefaultYear.png'),
                                    video_dict=dict(plot=self._kodi_wrapper.get_localized_string(32087))),
            helperobjects.TitleItem(title=self._kodi_wrapper.get_localized_string(32088),
                                    url_dict=dict(action=actions.LISTING_TVGUIDE),
                                    is_playable=False,
                                    art_dict=dict(thumb='DefaultAddonTvInfo.png', icon='DefaultAddonTvInfo.png', fanart='DefaultAddonTvInfo.png'),
                                    video_dict=dict(plot=self._kodi_wrapper.get_localized_string(32089))),
        ]
        self._kodi_wrapper.show_listing(main_items, sort='unsorted', content_type='files')

    def show_tvshow_menu_items(self, path):
        tvshow_items = self._api_helper.get_tvshow_items(path)
        self._kodi_wrapper.show_listing(tvshow_items, sort='label', content_type='tvshows')

    def show_category_menu_items(self):
        category_items = self.__get_category_menu_items()
        self._kodi_wrapper.show_listing(category_items, sort='label', content_type='files')

    def show_livestream_items(self):
        livestream_items = []
        for channel in ['een', 'canvas', 'ketnet', 'stubru', 'mnm']:
            if channel in ['een', 'canvas', 'ketnet']:
                thumbnail = self.__get_media(channel + '.png')
                fanart = self._api_helper.get_live_screenshot(channel)
                plot = self._kodi_wrapper.get_localized_string(32201) + '\n' + self._kodi_wrapper.get_localized_string(32102) % CHANNELS[channel].get('name')
            else:
                thumbnail = 'DefaultAddonMusic.png'
                fanart = 'DefaultAddonPVRClient.png'
                plot = self._kodi_wrapper.get_localized_string(32102) % CHANNELS[channel].get('name')
            livestream_items.append(helperobjects.TitleItem(
                title=self._kodi_wrapper.get_localized_string(32101) % CHANNELS[channel].get('name'),
                url_dict=dict(action=actions.PLAY, video_url=CHANNELS[channel].get('live_stream')),
                is_playable=True,
                art_dict=dict(thumb=thumbnail, icon='DefaultAddonPVRClient.png', fanart=fanart),
                video_dict=dict(
                    title=self._kodi_wrapper.get_localized_string(32101) % CHANNELS[channel].get('name'),
                    plot=plot,
                    studio=CHANNELS[channel].get('studio'),
                    mediatype='video',
                ),
            ))

        self._kodi_wrapper.show_listing(livestream_items, sort='unsorted', content_type='videos', cache=False)

    def show_episodes(self, path):
        episode_items, sort, ascending = self._api_helper.get_episode_items(path)
        self._kodi_wrapper.show_listing(episode_items, sort=sort, ascending=ascending, content_type='episodes', cache=False)

    def play(self, params):
        stream = self._stream_service.get_stream(params)
        if stream is not None:
            self._kodi_wrapper.play(stream)

    def __get_media(self, file_name):
        return os.path.join(self._addon_path, 'resources', 'media', file_name)

    def __get_category_menu_items(self):
        try:
            categories = get_categories(self._proxies)
        except Exception:
            categories = []

        # Fallback to internal categories if web-scraping fails
        if not categories:
            categories = CATEGORIES

        category_items = []
        for category in categories:
            thumbnail = category.get('thumbnail', 'DefaultGenre.png')
            category_items.append(helperobjects.TitleItem(title=category.get('name'),
                                                          url_dict=dict(action=actions.LISTING_CATEGORY_TVSHOWS, video_url=category.get('id')),
                                                          is_playable=False,
                                                          art_dict=dict(thumb=thumbnail, icon='DefaultGenre.png', fanart=thumbnail),
                                                          video_dict=dict(plot='[B]%s[/B]' % category.get('name'), studio='VRT')))
        return category_items
