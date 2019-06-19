# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

''' Implements a VRTPlayer class '''

from __future__ import absolute_import, division, unicode_literals
from resources.lib import favorites, vrtapihelper
from resources.lib.helperobjects import TitleItem
from resources.lib.statichelper import realpage


class VRTPlayer:
    ''' An object providing all methods for Kodi menu generation '''

    def __init__(self, _kodi):
        ''' Initialise object '''
        self._kodi = _kodi
        self._favorites = favorites.Favorites(_kodi)
        self._apihelper = vrtapihelper.VRTApiHelper(_kodi, self._favorites)

        self._addmymovies = _kodi.get_setting('addmymovies', 'true') == 'true'
        self._addmydocu = _kodi.get_setting('addmydocu', 'true') == 'true'

    def show_main_menu_items(self):
        ''' The VRT NU add-on main menu '''
        self._favorites.get_favorites(ttl=60 * 60)
        main_items = []

        # Only add 'My programs' when it has been activated
        if self._favorites.is_activated():
            main_items.append(TitleItem(
                title=self._kodi.localize(30010),  # My programs
                path=self._kodi.url_for('favorites_menu'),
                is_playable=False,
                art_dict=dict(thumb='icons/settings/profiles.png', icon='icons/settings/profiles.png', fanart='icons/settings/profiles.png'),
                video_dict=dict(plot=self._kodi.localize(30011))
            ))

        main_items.extend([
            TitleItem(title=self._kodi.localize(30012),  # A-Z listing
                      path=self._kodi.url_for('programs'),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultMovieTitle.png', icon='DefaultMovieTitle.png', fanart='DefaultMovieTitle.png'),
                      video_dict=dict(plot=self._kodi.localize(30013))),
            TitleItem(title=self._kodi.localize(30014),  # Categories
                      path=self._kodi.url_for('categories'),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultGenre.png', icon='DefaultGenre.png', fanart='DefaultGenre.png'),
                      video_dict=dict(plot=self._kodi.localize(30015))),
            TitleItem(title=self._kodi.localize(30016),  # Channels
                      is_playable=False,
                      path=self._kodi.url_for('channels'),
                      art_dict=dict(thumb='DefaultTags.png', icon='DefaultTags.png', fanart='DefaultTags.png'),
                      video_dict=dict(plot=self._kodi.localize(30017))),
            TitleItem(title=self._kodi.localize(30018),  # Live TV
                      path=self._kodi.url_for('livetv'),
                      is_playable=False,
                      # art_dict=dict(thumb='DefaultAddonPVRClient.png', icon='DefaultAddonPVRClient.png', fanart='DefaultAddonPVRClient.png'),
                      art_dict=dict(thumb='DefaultTVShows.png', icon='DefaultTVShows.png', fanart='DefaultTVShows.png'),
                      video_dict=dict(plot=self._kodi.localize(30019))),
            TitleItem(title=self._kodi.localize(30020),  # Recent items
                      path=self._kodi.url_for('recent'),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultRecentlyAddedEpisodes.png',
                                    icon='DefaultRecentlyAddedEpisodes.png',
                                    fanart='DefaultRecentlyAddedEpisodes.png'),
                      video_dict=dict(plot=self._kodi.localize(30021))),
            TitleItem(title=self._kodi.localize(30022),  # Soon offline
                      path=self._kodi.url_for('offline'),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultYear.png', icon='DefaultYear.png', fanart='DefaultYear.png'),
                      video_dict=dict(plot=self._kodi.localize(30023))),
            TitleItem(title=self._kodi.localize(30024),  # Featured content
                      path=self._kodi.url_for('featured'),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultCountry.png', icon='DefaultCountry.png', fanart='DefaultCountry.png'),
                      video_dict=dict(plot=self._kodi.localize(30025))),
            TitleItem(title=self._kodi.localize(30026),  # TV guide
                      path=self._kodi.url_for('tv_guide'),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultAddonTvInfo.png', icon='DefaultAddonTvInfo.png', fanart='DefaultAddonTvInfo.png'),
                      video_dict=dict(plot=self._kodi.localize(30027))),
            TitleItem(title=self._kodi.localize(30028),  # Search
                      path=self._kodi.url_for('search'),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultAddonsSearch.png', icon='DefaultAddonsSearch.png', fanart='DefaultAddonsSearch.png'),
                      video_dict=dict(plot=self._kodi.localize(30029))),
        ])
        self._kodi.show_listing(main_items)

    def show_favorites_menu_items(self):
        ''' The VRT NU addon 'My Programs' menu '''
        self._favorites.get_favorites(ttl=60 * 60)
        favorites_items = [
            TitleItem(title=self._kodi.localize(30040),  # My A-Z listing
                      path=self._kodi.url_for('favorites_programs'),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultMovieTitle.png', icon='DefaultMovieTitle.png', fanart='DefaultMovieTitle.png'),
                      video_dict=dict(plot=self._kodi.localize(30041))),
        ]

        if self._addmymovies:
            favorites_items.append(
                TitleItem(title=self._kodi.localize(30042),  # My movies
                          path=self._kodi.url_for('categories', category='films'),
                          is_playable=False,
                          art_dict=dict(thumb='DefaultAddonVideo.png', icon='DefaultAddonVideo.png', fanart='DefaultAddonVideo.png'),
                          video_dict=dict(plot=self._kodi.localize(30043))),
            )

        if self._addmydocu:
            favorites_items.append(
                TitleItem(title=self._kodi.localize(30044),  # My documentaries
                          path=self._kodi.url_for('favorites_docu'),
                          is_playable=False,
                          art_dict=dict(thumb='DefaultMovies.png', icon='DefaultMovies.png', fanart='DefaultMovies.png'),
                          video_dict=dict(plot=self._kodi.localize(30045))),
            )

        favorites_items.extend([
            TitleItem(title=self._kodi.localize(30046),  # My recent items
                      path=self._kodi.url_for('favorites_recent'),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultRecentlyAddedEpisodes.png',
                                    icon='DefaultRecentlyAddedEpisodes.png',
                                    fanart='DefaultRecentlyAddedEpisodes.png'),
                      video_dict=dict(plot=self._kodi.localize(30047))),
            TitleItem(title=self._kodi.localize(30048),  # My soon offline
                      path=self._kodi.url_for('favorites_offline'),
                      is_playable=False,
                      art_dict=dict(thumb='DefaultYear.png', icon='DefaultYear.png', fanart='DefaultYear.png'),
                      video_dict=dict(plot=self._kodi.localize(30049))),
        ])

        self._kodi.show_listing(favorites_items)

        # Show dialog when no favorites were found
        if not self._favorites.titles():
            self._kodi.show_ok_dialog(heading=self._kodi.localize(30415), message=self._kodi.localize(30416))

    def show_favorites_docu_menu_items(self):
        ''' The VRT NU add-on 'My documentaries' listing menu '''
        self._favorites.get_favorites(ttl=60 * 60)
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(category='docu', season='allseasons', programtype='oneoff')
        self._kodi.show_listing(episode_items, sort=sort, ascending=ascending, content=content)

    def show_tvshow_menu_items(self, use_favorites=False):
        ''' The VRT NU add-on 'A-Z' listing menu '''
        # My programs menus may need more up-to-date favorites
        self._favorites.get_favorites(ttl=5 * 60 if use_favorites else 60 * 60)
        tvshow_items = self._apihelper.get_tvshow_items(use_favorites=use_favorites)
        self._kodi.show_listing(tvshow_items, sort='label', content='tvshows')

    def show_category_menu_items(self, category=None):
        ''' The VRT NU add-on 'Categories' listing menu '''
        if category == 'films':
            self._favorites.get_favorites(ttl=60 * 60)
            episode_items, sort, ascending, content = self._apihelper.get_episode_items(category=category, season='allseasons')
            self._kodi.show_listing(episode_items, sort=sort, ascending=ascending, content=content)
        elif category:
            self._favorites.get_favorites(ttl=60 * 60)
            tvshow_items = self._apihelper.get_tvshow_items(category=category)
            self._kodi.show_listing(tvshow_items, sort='label', content='tvshows')
        else:
            category_items = self._apihelper.get_category_items()
            self._kodi.show_listing(category_items, sort='label', content='files')

    def show_channels_menu_items(self, channel=None):
        ''' The VRT NU add-on 'Channels' listing menu '''
        if channel:
            self._favorites.get_favorites(ttl=60 * 60)
            # Add Live TV channel entry
            channel_item = self._apihelper.get_channel_items(channels=[channel])
            tvshow_items = self._apihelper.get_tvshow_items(channel=channel)
            self._kodi.show_listing(channel_item + tvshow_items, sort='unsorted', content='tvshows')
        else:
            channel_items = self._apihelper.get_channel_items(live=False)
            self._kodi.show_listing(channel_items, cache=False)

    def show_featured_menu_items(self, feature=None):
        ''' The VRT NU add-on 'Featured content' listing menu '''
        if feature == 'kortfilm':
            self._favorites.get_favorites(ttl=60 * 60)
            episode_items, sort, ascending, content = self._apihelper.get_episode_items(feature=feature, season='allseasons')
            self._kodi.show_listing(episode_items, sort=sort, ascending=ascending, content=content)
        elif feature:
            self._favorites.get_favorites(ttl=60 * 60)
            tvshow_items = self._apihelper.get_tvshow_items(feature=feature)
            self._kodi.show_listing(tvshow_items, sort='label', content='tvshows')
        else:
            featured_items = self._apihelper.get_featured_items()
            self._kodi.show_listing(featured_items, sort='label', content='files')

    def show_livestream_items(self):
        ''' The VRT NU add-on 'Live TV' listing menu '''
        channel_items = self._apihelper.get_channel_items()
        self._kodi.show_listing(channel_items, cache=False)

    def show_episodes(self, program, season=None):
        ''' The VRT NU add-on episodes listing menu '''
        self._favorites.get_favorites(ttl=60 * 60)
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(program=program, season=season)
        self._kodi.show_listing(episode_items, sort=sort, ascending=ascending, content=content)

    def show_recent(self, page=0, use_favorites=False):
        ''' The VRT NU add-on 'Most recent' and 'My most recent' listing menu '''
        # My programs menus may need more up-to-date favorites
        self._favorites.get_favorites(ttl=5 * 60 if use_favorites else 60 * 60)
        page = realpage(page)
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(page=page, use_favorites=use_favorites, variety='recent')

        # Add 'More...' entry at the end
        if len(episode_items) == 50:
            if use_favorites:
                recent = 'favorites_recent'
            else:
                recent = 'recent'
            episode_items.append(TitleItem(
                title=self._kodi.localize(30300),
                path=self._kodi.url_for(recent, page=page + 1),
                is_playable=False,
                art_dict=dict(thumb='DefaultRecentlyAddedEpisodes.png', icon='DefaultRecentlyAddedEpisodes.png', fanart='DefaultRecentlyAddedEpisodes.png'),
                video_dict=dict(),
            ))

        self._kodi.show_listing(episode_items, sort=sort, ascending=ascending, content=content, cache=False)

    def show_offline(self, page=0, use_favorites=False):
        ''' The VRT NU add-on 'Soon offline' and 'My soon offline' listing menu '''
        # My programs menus may need more up-to-date favorites
        self._favorites.get_favorites(ttl=5 * 60 if use_favorites else 60 * 60)
        page = realpage(page)
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(page=page, use_favorites=use_favorites, variety='offline')

        # Add 'More...' entry at the end
        if len(episode_items) == 50:
            if use_favorites:
                offline = 'favorites_offline'
            else:
                offline = 'offline'
            episode_items.append(TitleItem(
                title=self._kodi.localize(30300),
                path=self._kodi.url_for(offline, page=page + 1),
                is_playable=False,
                art_dict=dict(thumb='DefaultYear.png', icon='DefaultYear.png', fanart='DefaultYear.png'),
                video_dict=dict(),
            ))

        self._kodi.show_listing(episode_items, sort=sort, ascending=ascending, content=content)

    def search(self, search_string=None, page=None):
        ''' The VRT NU add-on Search functionality and results '''
        self._favorites.get_favorites(ttl=60 * 60)
        page = realpage(page)

        if search_string is None:
            search_string = self._kodi.get_search_string()

        if not search_string:
            self._kodi.end_of_directory()
            return

        search_items, sort, ascending, content = self._apihelper.search(search_string, page=page)
        if not search_items:
            self._kodi.show_ok_dialog(heading=self._kodi.localize(30098), message=self._kodi.localize(30099).format(keywords=search_string))
            self._kodi.end_of_directory()
            return

        # Add 'More...' entry at the end
        if len(search_items) == 50:
            search_items.append(TitleItem(
                title=self._kodi.localize(30300),
                path=self._kodi.url_for('search', search_string=search_string, page=page + 1),
                is_playable=False,
                art_dict=dict(thumb='DefaultAddonSearch.png', icon='DefaultAddonSearch.png', fanart='DefaultAddonSearch.png'),
                video_dict=dict(),
            ))

        self._kodi.container_update(replace=True)
        self._kodi.show_listing(search_items, sort=sort, ascending=ascending, content=content, cache=False)

    def play_latest_episode(self, program):
        ''' A hidden feature in the VRT NU add-on to play the latest episode of a program '''
        video = self._apihelper.get_latest_episode(program)
        if not video:
            self._kodi.log_error('Play latest episode failed, program %s' % program)
            self._kodi.show_ok_dialog(message=self._kodi.localize(30954))
            self._kodi.end_of_directory()
            return
        self.play(video)

    def play(self, params):
        ''' A wrapper for playing video items '''
        from resources.lib import streamservice, tokenresolver
        _tokenresolver = tokenresolver.TokenResolver(self._kodi)
        _streamservice = streamservice.StreamService(self._kodi, _tokenresolver)
        stream = _streamservice.get_stream(params)
        if stream is not None:
            self._kodi.play(stream)
