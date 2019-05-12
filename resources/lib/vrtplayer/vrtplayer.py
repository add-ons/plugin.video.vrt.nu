# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, unicode_literals
from resources.lib.helperobjects.helperobjects import TitleItem
from resources.lib.vrtplayer import actions

try:
    from urllib.request import build_opener, install_opener, ProxyHandler, urlopen
except ImportError:
    from urllib2 import build_opener, install_opener, ProxyHandler, urlopen


class VRTPlayer:

    def __init__(self, _kodiwrapper, _apihelper):
        self._kodiwrapper = _kodiwrapper
        self._proxies = _kodiwrapper.get_proxies()
        install_opener(build_opener(ProxyHandler(self._proxies)))
        self._apihelper = _apihelper

    def show_main_menu_items(self):
        main_items = [
            TitleItem(title=self._kodiwrapper.get_localized_string(30080),
                      url_dict=dict(action=actions.LISTING_AZ_TVSHOWS),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultMovieTitle.png', icon='DefaultMovieTitle.png', fanart='DefaultMovieTitle.png'),
                      video_dict=dict(plot=self._kodiwrapper.get_localized_string(30081))),
            TitleItem(title=self._kodiwrapper.get_localized_string(30082),
                      url_dict=dict(action=actions.LISTING_CATEGORIES),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultGenre.png', icon='DefaultGenre.png', fanart='DefaultGenre.png'),
                      video_dict=dict(plot=self._kodiwrapper.get_localized_string(30083))),
            TitleItem(title=self._kodiwrapper.get_localized_string(30084),
                      url_dict=dict(action=actions.LISTING_CHANNELS),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultTags.png', icon='DefaultTags.png', fanart='DefaultTags.png'),
                      video_dict=dict(plot=self._kodiwrapper.get_localized_string(30085))),
            TitleItem(title=self._kodiwrapper.get_localized_string(30086),
                      url_dict=dict(action=actions.LISTING_LIVE),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultAddonPVRClient.png', icon='DefaultAddonPVRClient.png', fanart='DefaultAddonPVRClient.png'),
                      video_dict=dict(plot=self._kodiwrapper.get_localized_string(30087))),
            TitleItem(title=self._kodiwrapper.get_localized_string(30088),
                      url_dict=dict(action=actions.LISTING_RECENT, page='1'),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultYear.png', icon='DefaultYear.png', fanart='DefaultYear.png'),
                      video_dict=dict(plot=self._kodiwrapper.get_localized_string(30089))),
            TitleItem(title=self._kodiwrapper.get_localized_string(30090),
                      url_dict=dict(action=actions.LISTING_TVGUIDE),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultAddonTvInfo.png', icon='DefaultAddonTvInfo.png', fanart='DefaultAddonTvInfo.png'),
                      video_dict=dict(plot=self._kodiwrapper.get_localized_string(30091))),
            TitleItem(title=self._kodiwrapper.get_localized_string(30092),
                      url_dict=dict(action=actions.SEARCH),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultAddonsSearch.png', icon='DefaultAddonsSearch.png', fanart='DefaultAddonsSearch.png'),
                      video_dict=dict(plot=self._kodiwrapper.get_localized_string(30093))),
        ]
        self._kodiwrapper.show_listing(main_items)

    def show_tvshow_menu_items(self, category=None):
        tvshow_items = self._apihelper.get_tvshow_items(category=category)
        self._kodiwrapper.show_listing(tvshow_items, sort='label', content_type='tvshows')

    def show_category_menu_items(self):
        category_items = self.__get_category_menu_items()
        self._kodiwrapper.show_listing(category_items, sort='label', content_type='files')

    def show_channels_menu_items(self, channel=None):
        if channel:
            tvshow_items = self._apihelper.get_tvshow_items(channel=channel)
            self._kodiwrapper.show_listing(tvshow_items, sort='label', content_type='tvshows')
        else:
            from resources.lib.vrtplayer import CHANNELS
            self.show_channels(action=actions.LISTING_CHANNELS, channels=[c.get('name') for c in CHANNELS])

    def show_livestream_items(self):
        self.show_channels(action=actions.PLAY, channels=['een', 'canvas', 'sporza', 'ketnet-jr', 'ketnet', 'stubru', 'mnm'])

    def show_channels(self, action=actions.PLAY, channels=None):
        from resources.lib.vrtplayer import CHANNELS

        fanart_path = 'resource://resource.images.studios.white/%(studio)s.png'
        icon_path = 'resource://resource.images.studios.white/%(studio)s.png'
        # NOTE: Wait for resource.images.studios.coloured v0.16 to be released
        # icon_path = 'resource://resource.images.studios.coloured/%(studio)s.png'

        channel_items = []
        for channel in CHANNELS:
            if channel.get('name') not in channels:
                continue

            icon = icon_path % channel
            fanart = fanart_path % channel

            if action == actions.LISTING_CHANNELS:
                url_dict = dict(action=action, channel=channel.get('name'))
                label = channel.get('label')
                plot = '[B]%s[/B]' % channel.get('label')
                is_playable = False
            else:
                url_dict = dict(action=action)
                label = self._kodiwrapper.get_localized_string(30101) % channel.get('label')
                is_playable = True
                if channel.get('name') in ['een', 'canvas', 'ketnet']:
                    fanart = self._apihelper.get_live_screenshot(channel.get('name'))
                    plot = '%s\n%s' % (self._kodiwrapper.get_localized_string(30201),
                                       self._kodiwrapper.get_localized_string(30102) % channel.get('label'))
                else:
                    plot = self._kodiwrapper.get_localized_string(30102) % channel.get('label')
                if channel.get('live_stream_url'):
                    url_dict['video_url'] = channel.get('live_stream_url')
                elif channel.get('live_stream'):
                    url_dict['video_url'] = channel.get('live_stream')
                if channel.get('live_stream_id'):
                    url_dict['video_id'] = channel.get('live_stream_id')

            channel_items.append(TitleItem(
                title=label,
                url_dict=url_dict,
                is_playable=is_playable,
                art_dict=dict(thumb=icon, icon=icon, fanart=fanart),
                video_dict=dict(
                    title=label,
                    plot=plot,
                    studio=channel.get('studio'),
                    mediatype='video',
                ),
            ))

        self._kodiwrapper.show_listing(channel_items, cache=False)

    def show_episodes(self, path):
        episode_items, sort, ascending = self._apihelper.get_episode_items(path=path)
        self._kodiwrapper.show_listing(episode_items, sort=sort, ascending=ascending, content_type='episodes')

    def show_all_episodes(self, path):
        episode_items, sort, ascending = self._apihelper.get_episode_items(path=path, all_seasons=True)
        self._kodiwrapper.show_listing(episode_items, sort=sort, ascending=ascending, content_type='episodes')

    def show_recent(self, page):
        try:
            page = int(page)
        except TypeError:
            page = 1

        episode_items, sort, ascending = self._apihelper.get_episode_items(page=page)

        # Add 'More...' entry at the end
        episode_items.append(TitleItem(
            title=self._kodiwrapper.get_localized_string(30300),
            url_dict=dict(action=actions.LISTING_RECENT, page=page + 1),
            is_playable=False,
            art_dict=dict(thumb='DefaultYear.png', icon='DefaultYear.png', fanart='DefaultYear.png'),
            video_dict=dict(),
        ))

        self._kodiwrapper.show_listing(episode_items, sort=sort, ascending=ascending, content_type='episodes', cache=False)

    def play(self, params):
        from resources.lib.vrtplayer import streamservice, tokenresolver
        _tokenresolver = tokenresolver.TokenResolver(self._kodiwrapper)
        _streamservice = streamservice.StreamService(self._kodiwrapper, _tokenresolver)
        stream = _streamservice.get_stream(params)
        if stream is not None:
            self._kodiwrapper.play(stream)

    def search(self, search_string=None, page=1):
        try:
            page = int(page)
        except TypeError:
            page = 1

        if search_string is None:
            search_string = self._kodiwrapper.get_search_string()

        if not search_string:
            return

        search_items, sort, ascending = self._apihelper.search(search_string, page=page)
        if not search_items:
            self._kodiwrapper.show_ok_dialog(self._kodiwrapper.get_localized_string(30098), self._kodiwrapper.get_localized_string(30099) % search_string)
            return

        # Add 'More...' entry at the end
        if len(search_items) == 50:
            search_items.append(TitleItem(
                title=self._kodiwrapper.get_localized_string(30300),
                url_dict=dict(action=actions.SEARCH, query=search_string, page=page + 1),
                is_playable=False,
                art_dict=dict(thumb='DefaultAddonSearch.png', icon='DefaultAddonSearch.png', fanart='DefaultAddonSearch.png'),
                video_dict=dict(),
            ))

        self._kodiwrapper.show_listing(search_items, sort=sort, ascending=ascending, content_type='episodes', cache=False)

    def __get_category_menu_items(self):
        try:
            categories = self.get_categories(self._proxies)
        except Exception:
            categories = []

        # Fallback to internal categories if web-scraping fails
        if not categories:
            from resources.lib.vrtplayer import CATEGORIES
            categories = CATEGORIES

        category_items = []
        for category in categories:
            thumbnail = category.get('thumbnail', 'DefaultGenre.png')
            category_items.append(TitleItem(
                title=category.get('name'),
                url_dict=dict(action=actions.LISTING_CATEGORY_TVSHOWS, category=category.get('id')),
                is_playable=False,
                art_dict=dict(thumb=thumbnail, icon='DefaultGenre.png', fanart=thumbnail),
                video_dict=dict(plot='[B]%s[/B]' % category.get('name'), studio='VRT'),
            ))
        return category_items

    def get_categories(self, proxies=None):
        from bs4 import BeautifulSoup, SoupStrainer
        self._kodiwrapper.log_notice('URL get: https://www.vrt.be/vrtnu/categorieen/', 'Verbose')
        response = urlopen('https://www.vrt.be/vrtnu/categorieen/')
        tiles = SoupStrainer('a', {'class': 'nui-tile'})
        soup = BeautifulSoup(response.read(), 'html.parser', parse_only=tiles)

        categories = []
        for tile in soup.find_all(class_='nui-tile'):
            categories.append(dict(
                id=tile.get('href').split('/')[-2],
                thumbnail=self.get_category_thumbnail(tile),
                name=self.get_category_title(tile),
            ))

        return categories

    @staticmethod
    def get_category_thumbnail(element):
        from resources.lib.vrtplayer import statichelper
        raw_thumbnail = element.find(class_='media').get('data-responsive-image', 'DefaultGenre.png')
        return statichelper.add_https_method(raw_thumbnail)

    @staticmethod
    def get_category_title(element):
        from resources.lib.vrtplayer import statichelper
        found_element = element.find('h3')
        if found_element is not None:
            return statichelper.strip_newlines(found_element.contents[0])
        return ''
