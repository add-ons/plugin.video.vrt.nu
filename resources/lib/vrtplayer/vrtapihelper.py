# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, unicode_literals
from resources.lib.helperobjects.helperobjects import TitleItem
from resources.lib.vrtplayer import actions, favorites, metadatacreator, statichelper

try:
    from urllib.parse import urlencode, unquote
    from urllib.request import build_opener, install_opener, ProxyHandler, urlopen
except ImportError:
    from urllib2 import build_opener, install_opener, ProxyHandler, urlopen, unquote
    from urllib import urlencode  # pylint: disable=ungrouped-imports


class VRTApiHelper:

    _VRT_BASE = 'https://www.vrt.be'
    _VRTNU_SEARCH_URL = 'https://vrtnu-api.vrt.be/search'
    _VRTNU_SUGGEST_URL = 'https://vrtnu-api.vrt.be/suggest'
    _VRTNU_SCREENSHOT_URL = 'https://vrtnu-api.vrt.be/screenshots'

    def __init__(self, _kodi):
        self._kodi = _kodi
        self._proxies = _kodi.get_proxies()
        install_opener(build_opener(ProxyHandler(self._proxies)))
        self._showpermalink = _kodi.get_setting('showpermalink') == 'true'
        if _kodi.get_setting('usefavorites') == 'true':
            self._favorites = favorites.Favorites(self._kodi)
        else:
            self._favorites = None

    def get_tvshow_items(self, category=None, channel=None, filtered=False):
        import json
        params = dict()

        if category:
            params['facets[categories]'] = category

        if channel:
            params['facets[programBrands]'] = channel

        # If no facet-selection is done, we return the A-Z listing
        if not category and not channel:
            params['facets[transcodingStatus]'] = 'AVAILABLE'

        api_url = self._VRTNU_SUGGEST_URL + '?' + urlencode(params)
        self._kodi.log_notice('URL get: ' + unquote(api_url), 'Verbose')
        api_json = json.loads(urlopen(api_url).read())
        return self._map_to_tvshow_items(api_json, filtered=filtered)

    def _map_to_tvshow_items(self, tvshows, filtered=False):
        tvshow_items = []
        if filtered:
            favorite_names = self._favorites.names()
        for tvshow in tvshows:
            if filtered and tvshow.get('programName') not in favorite_names:
                continue
            metadata = metadatacreator.MetadataCreator()
            metadata.mediatype = 'tvshow'
            metadata.tvshowtitle = tvshow.get('title', '???')
            metadata.plot = statichelper.unescape(tvshow.get('description', '???'))
            metadata.brands = tvshow.get('brands')
            metadata.permalink = statichelper.shorten_link(tvshow.get('targetUrl'))
            # NOTE: This adds episode_count to label, would be better as metadata
            # title = '%s  [LIGHT][COLOR yellow]%s[/COLOR][/LIGHT]' % (tvshow.get('title', '???'), tvshow.get('episode_count', '?'))
            label = tvshow.get('title', '???')
            thumbnail = statichelper.add_https_method(tvshow.get('thumbnail', 'DefaultAddonVideo.png'))
            program_path = statichelper.unique_path(tvshow.get('targetUrl'))
            if self._favorites:
                if self._favorites.is_favorite(program_path):
                    params = dict(action='unfollow', program=tvshow.get('title'), path=program_path)
                    context_menu = [(self._kodi.localize(30412), 'RunPlugin(plugin://plugin.video.vrt.nu?%s)' % urlencode(params))]
                else:
                    params = dict(action='follow', program=tvshow.get('title'), path=program_path)
                    context_menu = [(self._kodi.localize(30411), 'RunPlugin(plugin://plugin.video.vrt.nu?%s)' % urlencode(params))]
            else:
                context_menu = []
            # Cut vrtbase url off since it will be added again when searching for episodes
            # (with a-z we dont have the full url)
            video_url = statichelper.add_https_method(tvshow.get('targetUrl')).replace(self._VRT_BASE, '')
            tvshow_items.append(TitleItem(
                title=label,
                url_dict=dict(action=actions.LISTING_EPISODES, video_url=video_url),
                is_playable=False,
                art_dict=dict(thumb=thumbnail, icon='DefaultAddonVideo.png', fanart=thumbnail),
                video_dict=metadata.get_video_dict(),
                context_menu=context_menu,
            ))
        return tvshow_items

    def _get_season_items(self, api_url, api_json):
        season_items = []
        sort = 'label'
        ascending = True
        content = 'seasons'
        episodes = api_json.get('results')
        facets = api_json.get('facets', dict()).get('facets')
        if episodes and facets:
            try:
                # Check if program has seasons
                facet = next(f for f in facets if f.get('name') == 'seasons' and len(f.get('buckets', [])) > 1)
                # Found multiple seasons, make list of seasons
                season_items, sort, ascending, content = self._map_to_season_items(api_url, facet.get('buckets', []), episodes)
            except StopIteration:
                pass
        return season_items, sort, ascending, content

    def get_episode_items(self, path=None, page=None, all_seasons=False, filtered=False):
        import json
        episode_items = []
        sort = 'episode'
        ascending = True

        # Recent items
        if page:
            params = {
                'from': ((page - 1) * 50) + 1,
                'i': 'video',
                'size': 50,
                # 'facets[transcodingStatus]': 'AVAILABLE',
            }

            if filtered:
                params['facets[programName]'] = '[%s]' % (','.join(self._favorites.names()))
            else:
                params['facets[programBrands]'] = '[een,canvas,sporza,vrtnws,vrtnxt,radio1,radio2,klara,stubru,mnm]'

            api_url = self._VRTNU_SEARCH_URL + '?' + urlencode(params)
            self._kodi.log_notice('URL get: ' + unquote(api_url), 'Verbose')
            api_json = json.loads(urlopen(api_url).read())
            episode_items, sort, ascending, content = self._map_to_episode_items(api_json.get('results', []), titletype='recent', filtered=filtered)

        if path:
            if '.relevant/' in path:
                params = {
                    'i': 'video',
                    'size': '150',
                    'facets[programUrl]': '//www.vrt.be' + path.replace('.relevant/', '/'),
                }
                api_url = self._VRTNU_SEARCH_URL + '?' + urlencode(params)
            else:
                api_url = path
            self._kodi.log_notice('URL get: ' + unquote(api_url), 'Verbose')
            api_json = json.loads(urlopen(api_url).read())

            episodes = api_json.get('results', [{}])
            if episodes:
                episode = episodes[0]
            else:
                episode = dict()
            display_options = episode.get('displayOptions', dict())

            # NOTE: Hard-code showing seasons because it is unreliable (i.e; Thuis or Down the Road have it disabled)
            display_options['showSeason'] = True

            # Look for seasons items if not yet done
            season_key = None

            # path = requests.utils.unquote(path)
            path = unquote(path)
            if all_seasons is True:
                episode_items, sort, ascending, content = self._map_to_episode_items(episodes, season_key=None)
            elif 'facets[seasonTitle]' in path:
                season_key = path.split('facets[seasonTitle]=')[1]
            elif display_options.get('showSeason') is True:
                episode_items, sort, ascending, content = self._get_season_items(api_url, api_json)

            # No season items, generate episode items
            if not episode_items:
                episode_items, sort, ascending, content = self._map_to_episode_items(episodes, season_key=season_key)

        return episode_items, sort, ascending, content

    def _map_to_episode_items(self, episodes, titletype=None, season_key=None, filtered=False):
        from datetime import datetime
        import dateutil.parser
        import dateutil.tz
        now = datetime.now(dateutil.tz.tzlocal())
        sort = 'episode'
        ascending = True
        if filtered:
            favorite_names = self._favorites.names()
        episode_items = []
        for episode in episodes:
            # VRT API workaround: seasonTitle facet behaves as a partial match regex,
            # so we have to filter out the episodes from seasons that don't exactly match.
            if season_key and episode.get('seasonTitle') != season_key:
                continue

            if filtered and episode.get('programName') not in favorite_names:
                continue

            # Support search highlights
            highlight = episode.get('highlight')
            if highlight:
                for key in highlight:
                    episode[key] = statichelper.convert_html_to_kodilabel(highlight.get(key)[0])

            display_options = episode.get('displayOptions', dict())

            # NOTE: Hard-code showing seasons because it is unreliable (i.e; Thuis or Down the Road have it disabled)
            display_options['showSeason'] = True

            if titletype is None:
                titletype = episode.get('programType')

            metadata = metadatacreator.MetadataCreator()
            metadata.tvshowtitle = episode.get('program')
            if episode.get('broadcastDate') != -1:
                metadata.datetime = datetime.fromtimestamp(episode.get('broadcastDate', 0) / 1000, dateutil.tz.UTC)

            metadata.duration = (episode.get('duration', 0) * 60)  # Minutes to seconds
            metadata.plot = statichelper.convert_html_to_kodilabel(episode.get('description'))
            metadata.brands = episode.get('programBrands') or episode.get('brands')
            metadata.geolocked = episode.get('allowedRegion') == 'BE'
            if display_options.get('showShortDescription'):
                short_description = statichelper.convert_html_to_kodilabel(episode.get('shortDescription'))
                metadata.plotoutline = short_description
                metadata.subtitle = short_description
            else:
                metadata.plotoutline = episode.get('subtitle')
                metadata.subtitle = episode.get('subtitle')
            metadata.season = episode.get('seasonTitle')
            metadata.episode = episode.get('episodeNumber')
            metadata.mediatype = episode.get('type', 'episode')
            metadata.permalink = statichelper.shorten_link(episode.get('permalink')) or episode.get('externalPermalink')
            if episode.get('assetOnTime'):
                metadata.ontime = dateutil.parser.parse(episode.get('assetOnTime'))
            if episode.get('assetOffTime'):
                metadata.offtime = dateutil.parser.parse(episode.get('assetOffTime'))

            # Add additional metadata to plot
            plot_meta = ''
            if metadata.geolocked:
                # Show Geo-locked
                plot_meta += self._kodi.localize(30201)
            # Only display when a video disappears if it is within the next 3 months
            if metadata.offtime is not None and (metadata.offtime - now).days < 93:
                # Show date when episode is removed
                plot_meta += self._kodi.localize(30202) % self._kodi.localize_dateshort(metadata.offtime)
                # Show the remaining days/hours the episode is still available
                if (metadata.offtime - now).days > 0:
                    plot_meta += self._kodi.localize(30203) % (metadata.offtime - now).days
                else:
                    plot_meta += self._kodi.localize(30204) % int((metadata.offtime - now).seconds / 3600)

            if plot_meta:
                metadata.plot = '%s\n%s' % (plot_meta, metadata.plot)

            if self._showpermalink and metadata.permalink:
                metadata.plot = '%s\n\n[COLOR yellow]%s[/COLOR]' % (metadata.plot, metadata.permalink)

            program_path = statichelper.unique_path(episode.get('programUrl'))
            if self._favorites:
                if self._favorites.is_favorite(program_path):
                    params = dict(action='unfollow', program=episode.get('program'), path=program_path)
                    context_menu = [(self._kodi.localize(30412), 'RunPlugin(plugin://plugin.video.vrt.nu?%s)' % urlencode(params))]
                else:
                    params = dict(action='follow', program=episode.get('program'), path=program_path)
                    context_menu = [(self._kodi.localize(30411), 'RunPlugin(plugin://plugin.video.vrt.nu?%s)' % urlencode(params))]
            else:
                context_menu = []

            thumb = statichelper.add_https_method(episode.get('videoThumbnailUrl', 'DefaultAddonVideo.png'))
            fanart = statichelper.add_https_method(episode.get('programImageUrl', thumb))
            video_url = statichelper.add_https_method(episode.get('url'))
            label, sort, ascending = self._make_label(episode, titletype, options=display_options)
            metadata.title = label
            episode_items.append(TitleItem(
                title=label,
                url_dict=dict(action=actions.PLAY, video_url=video_url, video_id=episode.get('videoId'), publication_id=episode.get('publicationId')),
                is_playable=True,
                art_dict=dict(thumb=thumb, icon='DefaultAddonVideo.png', fanart=fanart),
                video_dict=metadata.get_video_dict(),
                context_menu=context_menu,
            ))
        return episode_items, sort, ascending, 'episodes'

    def _map_to_season_items(self, api_url, seasons, episodes):
        import random

        season_items = []
        sort = 'label'
        ascending = True

        episode = random.choice(episodes)
        program_type = episode.get('programType')
        fanart = statichelper.add_https_method(episode.get('programImageUrl', 'DefaultSets.png'))

        metadata = metadatacreator.MetadataCreator()
        metadata.tvshowtitle = episode.get('program')
        metadata.plot = statichelper.convert_html_to_kodilabel(episode.get('programDescription'))
        metadata.plotoutline = statichelper.convert_html_to_kodilabel(episode.get('programDescription'))
        metadata.mediatype = 'season'
        metadata.brands = episode.get('programBrands') or episode.get('brands')
        metadata.geolocked = episode.get('allowedRegion') == 'BE'
        metadata.season = episode.get('seasonTitle')

        # Add additional metadata to plot
        plot_meta = ''
        if metadata.geolocked:
            # Show Geo-locked
            plot_meta += self._kodi.localize(30201) + '\n'
        metadata.plot = '%s[B]%s[/B]\n%s' % (plot_meta, episode.get('program'), metadata.plot)

        # Reverse sort seasons if program_type is 'reeksaflopend' or 'daily'
        if program_type in ('daily', 'reeksaflopend'):
            ascending = False

        # Add an "* All seasons" list item
        if self._kodi.get_global_setting('videolibrary.showallitems') is True:
            season_items.append(TitleItem(
                title=self._kodi.localize(30096),
                url_dict=dict(action=actions.LISTING_ALL_EPISODES, video_url=api_url),
                is_playable=False,
                art_dict=dict(thumb=fanart, icon='DefaultSets.png', fanart=fanart),
                video_dict=metadata.get_video_dict(),
            ))

        # NOTE: Sort the episodes ourselves, because Kodi does not allow to set to 'ascending'
        seasons = sorted(seasons, key=lambda k: k['key'], reverse=not ascending)

        for season in seasons:
            season_key = season['key']
            try:
                # If more than 150 episodes exist, we may end up with an empty season (Winteruur)
                episode = random.choice([e for e in episodes if e.get('seasonName') == season_key])
            except IndexError:
                episode = episodes[0]
            fanart = statichelper.add_https_method(episode.get('programImageUrl', 'DefaultSets.png'))
            thumbnail = statichelper.add_https_method(episode.get('videoThumbnailUrl', fanart))
            label = '%s %s' % (self._kodi.localize(30094), season_key)
            params = {'facets[seasonTitle]': season_key}
            path = api_url + '&' + urlencode(params)
            season_items.append(TitleItem(
                title=label,
                url_dict=dict(action=actions.LISTING_EPISODES, video_url=path),
                is_playable=False,
                art_dict=dict(thumb=thumbnail, icon='DefaultSets.png', fanart=fanart),
                video_dict=metadata.get_video_dict(),
            ))
        return season_items, sort, ascending, 'seasons'

    def search(self, search_string, page=1):
        import json

        params = {
            'from': ((page - 1) * 50) + 1,
            'i': 'video',
            'size': 50,
            'q': search_string,
            'highlight': 'true',
        }
        api_url = 'https://search.vrt.be/search?' + urlencode(params)
        self._kodi.log_notice('URL get: ' + unquote(api_url), 'Verbose')
        api_json = json.loads(urlopen(api_url).read())

        episodes = api_json.get('results', [{}])
        episode_items, sort, ascending, content = self._map_to_episode_items(episodes, titletype='recent')
        return episode_items, sort, ascending, content

    def get_live_screenshot(self, channel):
        url = '%s/%s.jpg' % (self._VRTNU_SCREENSHOT_URL, channel)
        self.__delete_cached_thumbnail(url)
        return url

    def __delete_cached_thumbnail(self, url):
        crc = self.__get_crc32(url)
        ext = url.split('.')[-1]
        path = 'special://thumbnails/%s/%s.%s' % (crc[0], crc, ext)
        self._kodi.delete_file(path)

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

    def _make_label(self, result, titletype, options=None):
        if options is None:
            options = dict()

        if options.get('showEpisodeTitle'):
            label = statichelper.convert_html_to_kodilabel(result.get('title') or result.get('shortDescription'))
        elif options.get('showShortDescription'):
            label = statichelper.convert_html_to_kodilabel(result.get('shortDescription') or result.get('title'))
        else:
            label = statichelper.convert_html_to_kodilabel(result.get('title') or result.get('shortDescription'))

        sort = 'unsorted'
        ascending = True

        if titletype == 'recent':
            ascending = False
            sort = 'dateadded'
            label = '%s - %s' % (result.get('program'), label)

        elif titletype in ('reeksaflopend', 'reeksoplopend'):

            if titletype == 'reeksaflopend':
                ascending = False

            # NOTE: This is disable on purpose as 'showSeason' is not reliable
            if options.get('showSeason') is False and options.get('showEpisodeNumber') and result.get('seasonName') and result.get('episodeNumber'):
                try:
                    sort = 'dateadded'
                    label = 'S%02dE%02d: %s' % (int(result.get('seasonName')), int(result.get('episodeNumber')), label)
                except Exception:
                    # Season may not always be a perfect number
                    sort = 'episode'
            elif options.get('showEpisodeNumber') and result.get('episodeNumber') and ascending:
                # NOTE: Sort the episodes ourselves, because Kodi does not allow to set to 'descending'
                # sort = 'episode'
                sort = 'label'
                label = '%s %s: %s' % (self._kodi.localize(30095), result.get('episodeNumber'), label)
            elif options.get('showBroadcastDate') and result.get('formattedBroadcastShortDate'):
                sort = 'dateadded'
                label = '%s - %s' % (result.get('formattedBroadcastShortDate'), label)
            else:
                sort = 'dateadded'

        elif titletype == 'daily':
            ascending = False
            sort = 'dateadded'
            label = '%s - %s' % (result.get('formattedBroadcastShortDate'), label)

        elif titletype == 'oneoff':
            sort = 'label'

        return label, sort, ascending
