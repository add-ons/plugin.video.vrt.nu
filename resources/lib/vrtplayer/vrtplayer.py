# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, unicode_literals
from resources.lib.helperobjects import helperobjects
from resources.lib.vrtplayer import actions

try:
    from urllib.request import build_opener, install_opener, ProxyHandler, urlopen
except ImportError:
    from urllib2 import build_opener, install_opener, ProxyHandler, urlopen


def get_categories(proxies=None):
    from bs4 import BeautifulSoup, SoupStrainer
    response = urlopen('https://www.vrt.be/vrtnu/categorieen/')
    tiles = SoupStrainer('a', {'class': 'nui-tile'})
    soup = BeautifulSoup(response.read(), 'html.parser', parse_only=tiles)

    categories = []
    for tile in soup.find_all(class_='nui-tile'):
        categories.append(dict(
            id=tile.get('href').split('/')[-2],
            thumbnail=get_category_thumbnail(tile),
            name=get_category_title(tile),
        ))

    return categories


def get_category_thumbnail(element):
    from resources.lib.vrtplayer import statichelper
    raw_thumbnail = element.find(class_='media').get('data-responsive-image', 'DefaultGenre.png')
    return statichelper.add_https_method(raw_thumbnail)


def get_category_title(element):
    from resources.lib.vrtplayer import statichelper
    found_element = element.find('h3')
    if found_element is not None:
        return statichelper.strip_newlines(found_element.contents[0])
    return ''


class VRTPlayer:

    def __init__(self, kodi_wrapper, api_helper):
        self._kodi_wrapper = kodi_wrapper
        self._proxies = self._kodi_wrapper.get_proxies()
        install_opener(build_opener(ProxyHandler(self._proxies)))
        self._api_helper = api_helper

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
        self._kodi_wrapper.show_listing(main_items)

    def show_tvshow_menu_items(self, path):
        tvshow_items = self._api_helper.get_tvshow_items(path)
        self._kodi_wrapper.show_listing(tvshow_items, sort='label', content_type='tvshows')

    def show_category_menu_items(self):
        category_items = self.__get_category_menu_items()
        self._kodi_wrapper.show_listing(category_items, sort='label', content_type='files')

    def show_livestream_items(self):
        from resources.lib.vrtplayer import CHANNELS

        fanart_path = 'resource://resource.images.studios.white/%(studio)s.png'
        icon_path = 'resource://resource.images.studios.white/%(studio)s.png'
        # NOTE: Wait for resource.images.studios.coloured v0.16 to be released
        # icon_path = 'resource://resource.images.studios.coloured/%(studio)s.png'

        livestream_items = []
        for channel in ['een', 'canvas', 'ketnet', 'sporza', 'stubru', 'mnm']:

            icon = icon_path % CHANNELS[channel]
            if channel in ['een', 'canvas', 'ketnet']:
                fanart = self._api_helper.get_live_screenshot(channel)
                plot = self._kodi_wrapper.get_localized_string(32201) + '\n' + self._kodi_wrapper.get_localized_string(32102) % CHANNELS[channel].get('name')
            else:
                fanart = fanart_path % CHANNELS[channel]
                plot = self._kodi_wrapper.get_localized_string(32102) % CHANNELS[channel].get('name')

            url_dict = dict(action=actions.PLAY)
            if CHANNELS[channel].get('live_stream'):
                url_dict['video_url'] = CHANNELS[channel].get('live_stream')
            if CHANNELS[channel].get('live_stream_id'):
                url_dict['video_id'] = CHANNELS[channel].get('live_stream_id')

            livestream_items.append(helperobjects.TitleItem(
                title=self._kodi_wrapper.get_localized_string(32101) % CHANNELS[channel].get('name'),
                url_dict=url_dict,
                is_playable=True,
                art_dict=dict(thumb=icon, icon=icon, fanart=fanart),
                video_dict=dict(
                    title=self._kodi_wrapper.get_localized_string(32101) % CHANNELS[channel].get('name'),
                    plot=plot,
                    studio=CHANNELS[channel].get('studio'),
                    mediatype='video',
                ),
            ))

        self._kodi_wrapper.show_listing(livestream_items, cache=False)

    def show_episodes(self, path):
        episode_items, sort, ascending = self._api_helper.get_episode_items(path)
        self._kodi_wrapper.show_listing(episode_items, sort=sort, ascending=ascending, content_type='episodes', cache=False)

    def play(self, params):
        from resources.lib.vrtplayer import streamservice, tokenresolver
        token_resolver = tokenresolver.TokenResolver(self._kodi_wrapper)
        stream_service = streamservice.StreamService(self._kodi_wrapper, token_resolver)
        stream = stream_service.get_stream(params)
        if stream is not None:
            self._kodi_wrapper.play(stream)

    def __get_category_menu_items(self):
        try:
            categories = get_categories(self._proxies)
        except Exception:
            categories = []

        # Fallback to internal categories if web-scraping fails
        if not categories:
            from resources.lib.vrtplayer import CATEGORIES
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
