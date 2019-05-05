# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, unicode_literals
from vrtnu.helperobjects import actions, TitleItem
from vrtnu.statichelper import add_https_method, strip_newlines
from vrtnu.vrtapihelper import VRTApiHelper

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
    raw_thumbnail = element.find(class_='media').get('data-responsive-image', 'DefaultGenre.png')
    return add_https_method(raw_thumbnail)


def get_category_title(element):
    found_element = element.find('h3')
    if found_element is not None:
        return strip_newlines(found_element.contents[0])
    return ''


class VRTPlayer:

    def __init__(self, kodi_wrapper):
        self._kodi_wrapper = kodi_wrapper
        self._proxies = self._kodi_wrapper.get_proxies()
        install_opener(build_opener(ProxyHandler(self._proxies)))
        self._api_helper = VRTApiHelper(kodi_wrapper)
        self._plugin = kodi_wrapper._plugin

    def show_tvshow_menu_items(self, category=None):
        tvshow_items = self._api_helper.get_tvshow_items(category=category)
        self._kodi_wrapper.show_listing(tvshow_items, sort='label', content_type='tvshows')

    def show_category_menu_items(self):
        category_items = self.__get_category_menu_items()
        self._kodi_wrapper.show_listing(category_items, sort='label', content_type='files')

    def show_channels_menu_items(self, channel=None):
        if channel:
            tvshow_items = self._api_helper.get_tvshow_items(channel=channel)
            self._kodi_wrapper.show_listing(tvshow_items, sort='label', content_type='tvshows')
        else:
            from vrtnu.data import CHANNELS
            self.show_channels(action=actions.LISTING_CHANNELS, channels=[c.get('name') for c in CHANNELS])

    def show_livestream_items(self):
        self.show_channels(action=actions.PLAY, channels=['een', 'canvas', 'sporza', 'ketnet', 'stubru', 'mnm'])

    def show_channels(self, action=actions.PLAY, channels=None):
        from vrtnu.data import CHANNELS

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
                label = self._kodi_wrapper.get_localized_string(30101) % channel.get('label')
                is_playable = True
                if channel.get('name') in ['een', 'canvas', 'ketnet']:
                    fanart = self._api_helper.get_live_screenshot(channel.get('name'))
                    plot = '%s\n%s' % (self._kodi_wrapper.get_localized_string(30201),
                                       self._kodi_wrapper.get_localized_string(30102) % channel.get('label'))
                else:
                    plot = self._kodi_wrapper.get_localized_string(30102) % channel.get('label')
                if channel.get('live_stream'):
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

        self._kodi_wrapper.show_listing(channel_items, cache=False)

    def show_episodes(self, path):
        episode_items, sort, ascending = self._api_helper.get_episode_items(path=path)
        self._kodi_wrapper.show_listing(episode_items, sort=sort, ascending=ascending, content_type='episodes')

    def show_recent(self, page):
        try:
            page = int(page)
        except TypeError:
            page = 1

        episode_items, sort, ascending = self._api_helper.get_episode_items(page=page)

        # Add 'More...' entry at the end
        episode_items.append(TitleItem(
            title=self._kodi_wrapper.get_localized_string(30300),
            url_dict=dict(action=actions.LISTING_RECENT, page=page + 1),
            is_playable=False,
            art_dict=dict(thumb='DefaultYear.png', icon='DefaultYear.png', fanart='DefaultYear.png'),
            video_dict=dict(),
        ))

        self._kodi_wrapper.show_listing(episode_items, sort=sort, ascending=ascending, content_type='episodes', cache=False)

    def __get_category_menu_items(self):
        try:
            categories = get_categories(self._proxies)
        except Exception:
            categories = []

        # Fallback to internal categories if web-scraping fails
        if not categories:
            from channels import CATEGORIES
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
