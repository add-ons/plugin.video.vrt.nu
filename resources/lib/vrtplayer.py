# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
''' Implements a VRTPlayer class '''

from __future__ import absolute_import, division, unicode_literals
from apihelper import ApiHelper
from favorites import Favorites
from helperobjects import TitleItem
from resumepoints import ResumePoints
from statichelper import find_entry, url_to_episode, video_to_api_url, to_unicode


class VRTPlayer:
    ''' An object providing all methods for Kodi menu generation '''

    def __init__(self, _kodi):
        ''' Initialise object '''
        self._kodi = _kodi
        self._favorites = Favorites(_kodi)
        self._resumepoints = ResumePoints(_kodi)
        self._apihelper = ApiHelper(_kodi, self._favorites, self._resumepoints)

    def show_main_menu(self):
        ''' The VRT NU add-on main menu '''
        # self._favorites.refresh(ttl=60 * 60)
        main_items = []

        # Only add 'My favorites' when it has been activated
        if self._favorites.is_activated():
            main_items.append(TitleItem(
                title=self._kodi.localize(30010),  # My favorites
                path=self._kodi.url_for('favorites_menu'),
                art_dict=dict(thumb='DefaultFavourites.png'),
                info_dict=dict(plot=self._kodi.localize(30011)),
            ))

        main_items.extend([
            TitleItem(title=self._kodi.localize(30012),  # A-Z listing
                      path=self._kodi.url_for('programs'),
                      art_dict=dict(thumb='DefaultMovieTitle.png'),
                      info_dict=dict(plot=self._kodi.localize(30013))),
            TitleItem(title=self._kodi.localize(30014),  # Categories
                      path=self._kodi.url_for('categories'),
                      art_dict=dict(thumb='DefaultGenre.png'),
                      info_dict=dict(plot=self._kodi.localize(30015))),
            TitleItem(title=self._kodi.localize(30016),  # Channels
                      path=self._kodi.url_for('channels'),
                      art_dict=dict(thumb='DefaultTags.png'),
                      info_dict=dict(plot=self._kodi.localize(30017))),
            TitleItem(title=self._kodi.localize(30018),  # Live TV
                      path=self._kodi.url_for('livetv'),
                      art_dict=dict(thumb='DefaultTVShows.png'),
                      info_dict=dict(plot=self._kodi.localize(30019))),
            TitleItem(title=self._kodi.localize(30020),  # Recent items
                      path=self._kodi.url_for('recent'),
                      art_dict=dict(thumb='DefaultRecentlyAddedEpisodes.png'),
                      info_dict=dict(plot=self._kodi.localize(30021))),
            TitleItem(title=self._kodi.localize(30022),  # Soon offline
                      path=self._kodi.url_for('offline'),
                      art_dict=dict(thumb='DefaultYear.png'),
                      info_dict=dict(plot=self._kodi.localize(30023))),
            TitleItem(title=self._kodi.localize(30024),  # Featured content
                      path=self._kodi.url_for('featured'),
                      art_dict=dict(thumb='DefaultCountry.png'),
                      info_dict=dict(plot=self._kodi.localize(30025))),
            TitleItem(title=self._kodi.localize(30026),  # TV guide
                      path=self._kodi.url_for('tvguide'),
                      art_dict=dict(thumb='DefaultAddonTvInfo.png'),
                      info_dict=dict(plot=self._kodi.localize(30027))),
            TitleItem(title=self._kodi.localize(30028),  # Search
                      path=self._kodi.url_for('search'),
                      art_dict=dict(thumb='DefaultAddonsSearch.png'),
                      info_dict=dict(plot=self._kodi.localize(30029))),
        ])
        self._kodi.show_listing(main_items)  # No category
        self._version_check()

    def _version_check(self):
        first_run, settings_version, addon_version = self._first_run()
        if first_run:
            # 2.0.0 version: changed plugin:// url interface: show warning that Kodi favourites and what-was-watched will break
            if settings_version == '' and self._kodi.credentials_filled_in():
                self._kodi.show_ok_dialog(self._kodi.localize(30978), self._kodi.localize(30979))
            if addon_version == '2.2.1':
                # 2.2.1 version: changed artwork: delete old cached artwork
                self._kodi.delete_cached_thumbnail(self._kodi.get_addon_info('fanart').replace('.png', '.jpg'))
                self._kodi.delete_cached_thumbnail(self._kodi.get_addon_info('icon'))
                # 2.2.1 version: moved tokens: delete old tokens
                from tokenresolver import TokenResolver
                TokenResolver(self._kodi).delete_tokens()

    def _first_run(self):
        '''Check if this add-on version is run for the first time'''

        # Get version from settings.xml
        settings_version = self._kodi.get_setting('version', '')

        # Get version from addon.xml
        addon_version = self._kodi.get_addon_info('version')

        # Compare versions (settings_version was not present in version 1.10.0 and older)
        settings_comp = tuple(map(int, settings_version.split('.'))) if settings_version != '' else (1, 10, 0)
        addon_comp = tuple(map(int, addon_version.split('.')))

        if addon_comp > settings_comp:
            # New version found, save addon version to settings
            self._kodi.set_setting('version', addon_version)
            return True, settings_version, addon_version

        return False, settings_version, addon_version

    def show_favorites_menu(self):
        ''' The VRT NU addon 'My Programs' menu '''
        self._favorites.refresh(ttl=60 * 60)
        favorites_items = [
            TitleItem(title=self._kodi.localize(30040),  # My A-Z listing
                      path=self._kodi.url_for('favorites_programs'),
                      art_dict=dict(thumb='DefaultMovieTitle.png'),
                      info_dict=dict(plot=self._kodi.localize(30041))),
            TitleItem(title=self._kodi.localize(30046),  # My recent items
                      path=self._kodi.url_for('favorites_recent'),
                      art_dict=dict(thumb='DefaultRecentlyAddedEpisodes.png'),
                      info_dict=dict(plot=self._kodi.localize(30047))),
            TitleItem(title=self._kodi.localize(30048),  # My soon offline
                      path=self._kodi.url_for('favorites_offline'),
                      art_dict=dict(thumb='DefaultYear.png'),
                      info_dict=dict(plot=self._kodi.localize(30049))),
        ]

        # Only add 'My watch later' and 'Continue watching' when it has been activated
        if self._resumepoints.is_activated():
            favorites_items.append(TitleItem(
                title=self._kodi.localize(30050),  # My watch later
                path=self._kodi.url_for('resumepoints_watchlater'),
                art_dict=dict(thumb='DefaultVideoPlaylists.png'),
                info_dict=dict(plot=self._kodi.localize(30051)),
            ))
            favorites_items.append(TitleItem(
                title=self._kodi.localize(30052),  # Continue Watching
                path=self._kodi.url_for('resumepoints_continue'),
                art_dict=dict(thumb='DefaultInProgressShows.png'),
                info_dict=dict(plot=self._kodi.localize(30053)),
            ))

        if self._kodi.get_setting('addmymovies', 'true') == 'true':
            favorites_items.append(
                TitleItem(title=self._kodi.localize(30042),  # My movies
                          path=self._kodi.url_for('categories', category='films'),
                          art_dict=dict(thumb='DefaultAddonVideo.png'),
                          info_dict=dict(plot=self._kodi.localize(30043))),
            )

        if self._kodi.get_setting('addmydocu', 'true') == 'true':
            favorites_items.append(
                TitleItem(title=self._kodi.localize(30044),  # My documentaries
                          path=self._kodi.url_for('favorites_docu'),
                          art_dict=dict(thumb='DefaultMovies.png'),
                          info_dict=dict(plot=self._kodi.localize(30045))),
            )

        self._kodi.show_listing(favorites_items, category=30010)  # My favorites

        # Show dialog when no favorites were found
        if not self._favorites.titles():
            self._kodi.show_ok_dialog(heading=self._kodi.localize(30415), message=self._kodi.localize(30416))

    def show_favorites_docu_menu(self):
        ''' The VRT NU add-on 'My documentaries' listing menu '''
        self._favorites.refresh(ttl=60 * 60)
        self._resumepoints.refresh(ttl=60 * 60)
        episode_items, sort, ascending, content = self._apihelper.list_episodes(category='docu', season='allseasons', programtype='oneoff')
        self._kodi.show_listing(episode_items, category=30044, sort=sort, ascending=ascending, content=content)

    def show_tvshow_menu(self, use_favorites=False):
        ''' The VRT NU add-on 'A-Z' listing menu '''
        # My favorites menus may need more up-to-date favorites
        self._favorites.refresh(ttl=5 * 60 if use_favorites else 60 * 60)
        self._resumepoints.refresh(ttl=5 * 60 if use_favorites else 60 * 60)
        tvshow_items = self._apihelper.list_tvshows(use_favorites=use_favorites)
        self._kodi.show_listing(tvshow_items, category=30012, sort='label', content='tvshows')

    def show_category_menu(self, category=None):
        ''' The VRT NU add-on 'Categories' listing menu '''
        if category:
            self._favorites.refresh(ttl=60 * 60)
            self._resumepoints.refresh(ttl=60 * 60)
            tvshow_items = self._apihelper.list_tvshows(category=category)
            from data import CATEGORIES
            category_msgctxt = find_entry(CATEGORIES, 'id', category).get('msgctxt')
            self._kodi.show_listing(tvshow_items, category=category_msgctxt, sort='label', content='tvshows')
        else:
            category_items = self._apihelper.list_categories()
            self._kodi.show_listing(category_items, category=30014, sort='unsorted', content='files')  # Categories

    def show_channels_menu(self, channel=None):
        ''' The VRT NU add-on 'Channels' listing menu '''
        if channel:
            from tvguide import TVGuide
            self._favorites.refresh(ttl=60 * 60)
            self._resumepoints.refresh(ttl=60 * 60)
            channel_items = self._apihelper.list_channels(channels=[channel])  # Live TV
            channel_items.extend(TVGuide(self._kodi).get_channel_items(channel=channel))  # TV guide
            channel_items.extend(self._apihelper.list_youtube(channels=[channel]))  # YouTube
            channel_items.extend(self._apihelper.list_tvshows(channel=channel))  # TV shows
            from data import CHANNELS
            channel_name = find_entry(CHANNELS, 'name', channel).get('label')
            self._kodi.show_listing(channel_items, category=channel_name, sort='unsorted', content='tvshows')  # Channel
        else:
            channel_items = self._apihelper.list_channels(live=False)
            self._kodi.show_listing(channel_items, category=30016, cache=False)

    def show_featured_menu(self, feature=None):
        ''' The VRT NU add-on 'Featured content' listing menu '''
        if feature:
            self._favorites.refresh(ttl=60 * 60)
            self._resumepoints.refresh(ttl=60 * 60)
            tvshow_items = self._apihelper.list_tvshows(feature=feature)
            from data import FEATURED
            feature_msgctxt = find_entry(FEATURED, 'id', feature).get('msgctxt')
            self._kodi.show_listing(tvshow_items, category=feature_msgctxt, sort='label', content='tvshows')
        else:
            featured_items = self._apihelper.list_featured()
            self._kodi.show_listing(featured_items, category=30024, sort='label', content='files')

    def show_livetv_menu(self):
        ''' The VRT NU add-on 'Live TV' listing menu '''
        channel_items = self._apihelper.list_channels()
        self._kodi.show_listing(channel_items, category=30018, cache=False)

    def show_episodes_menu(self, program, season=None):
        ''' The VRT NU add-on episodes listing menu '''
        self._favorites.refresh(ttl=60 * 60)
        self._resumepoints.refresh(ttl=60 * 60)
        episode_items, sort, ascending, content = self._apihelper.list_episodes(program=program, season=season)
        # FIXME: Translate program in Program Title
        self._kodi.show_listing(episode_items, category=program.title(), sort=sort, ascending=ascending, content=content)

    def show_recent_menu(self, page=0, use_favorites=False):
        ''' The VRT NU add-on 'Most recent' and 'My most recent' listing menu '''
        from statichelper import realpage

        # My favorites menus may need more up-to-date favorites
        self._favorites.refresh(ttl=5 * 60 if use_favorites else 60 * 60)
        self._resumepoints.refresh(ttl=5 * 60 if use_favorites else 60 * 60)
        page = realpage(page)
        episode_items, sort, ascending, content = self._apihelper.list_episodes(page=page, use_favorites=use_favorites, variety='recent')

        # Add 'More...' entry at the end
        if len(episode_items) == 50:
            if use_favorites:
                recent = 'favorites_recent'
            else:
                recent = 'recent'
            episode_items.append(TitleItem(
                title=self._kodi.localize(30300),
                path=self._kodi.url_for(recent, page=page + 1),
                art_dict=dict(thumb='DefaultRecentlyAddedEpisodes.png'),
                info_dict=dict(),
            ))

        self._kodi.show_listing(episode_items, category=30020, sort=sort, ascending=ascending, content=content, cache=False)

    def show_offline_menu(self, page=0, use_favorites=False):
        ''' The VRT NU add-on 'Soon offline' and 'My soon offline' listing menu '''
        from statichelper import realpage

        # My favorites menus may need more up-to-date favorites
        self._favorites.refresh(ttl=5 * 60 if use_favorites else 60 * 60)
        self._resumepoints.refresh(ttl=5 * 60 if use_favorites else 60 * 60)
        page = realpage(page)
        episode_items, sort, ascending, content = self._apihelper.list_episodes(page=page, use_favorites=use_favorites, variety='offline')

        # Add 'More...' entry at the end
        if len(episode_items) == 50:
            if use_favorites:
                offline = 'favorites_offline'
            else:
                offline = 'offline'
            episode_items.append(TitleItem(
                title=self._kodi.localize(30300),
                path=self._kodi.url_for(offline, page=page + 1),
                art_dict=dict(thumb='DefaultYear.png'),
                info_dict=dict(),
            ))

        self._kodi.show_listing(episode_items, category=30022, sort=sort, ascending=ascending, content=content, cache=False)

    def show_watchlater_menu(self, page=0):
        ''' The VRT NU add-on 'My watch later' listing menu '''
        from statichelper import realpage

        # My watch later menu may need more up-to-date favorites
        self._favorites.refresh(ttl=5 * 60)
        self._resumepoints.refresh(ttl=5 * 60)
        page = realpage(page)
        episode_items, sort, ascending, content = self._apihelper.list_episodes(page=page, variety='watchlater')
        self._kodi.show_listing(episode_items, category=30050, sort=sort, ascending=ascending, content=content, cache=False)

    def show_continue_menu(self, page=0):
        ''' The VRT NU add-on 'Continue waching' listing menu '''
        from statichelper import realpage

        # Continue watching menu may need more up-to-date favorites
        self._favorites.refresh(ttl=5 * 60)
        self._resumepoints.refresh(ttl=5 * 60)
        page = realpage(page)
        episode_items, sort, ascending, content = self._apihelper.list_episodes(page=page, variety='continue')
        self._kodi.show_listing(episode_items, category=30052, sort=sort, ascending=ascending, content=content, cache=False)

    def play_latest_episode(self, program):
        ''' A hidden feature in the VRT NU add-on to play the latest episode of a program '''
        video = self._apihelper.get_latest_episode(program)
        if not video:
            self._kodi.log_error('Play latest episode failed, program {program}', program=program)
            self._kodi.show_ok_dialog(message=self._kodi.localize(30954))
            self._kodi.end_of_directory()
            return
        self.play(video)

    def play_episode_by_air_date(self, channel, start_date, end_date):
        ''' Play an episode of a program given the channel and the air date in iso format (2019-07-06T19:35:00) '''
        video = self._apihelper.get_episode_by_air_date(channel, start_date, end_date)
        if video and video.get('errorlabel'):
            self._kodi.show_ok_dialog(message=self._kodi.localize(30986, title=video.get('errorlabel')))
            self._kodi.end_of_directory()
            return
        if not video:
            self._kodi.log_error('Play episode by air date failed, channel {channel}, start_date {start}', channel=channel, start=start_date)
            self._kodi.show_ok_dialog(message=self._kodi.localize(30954))
            self._kodi.end_of_directory()
            return
        self.play(video)

    def play_whatson(self, whatson_id):
        ''' Play a video by whatson_id '''
        video = self._apihelper.get_single_episode(whatson_id)
        if not video:
            self._kodi.log_error('Play by whatson_id {id} failed', id=whatson_id)
            self._kodi.show_ok_dialog(message=self._kodi.localize(30954))
            self._kodi.end_of_directory()
            return
        self.play(video)

    def play(self, video):
        ''' A wrapper for playing video items '''
        from tokenresolver import TokenResolver
        from streamservice import StreamService
        _tokenresolver = TokenResolver(self._kodi)
        _streamservice = StreamService(self._kodi, _tokenresolver)
        stream = _streamservice.get_stream(video)
        if stream is None:
            return
        self._kodi.play(stream, video.get('listitem'))
        if self._resumepoints.is_activated():
            from playerinfo import PlayerInfo
            # Get info from player
            playerinfo = PlayerInfo(info=lambda info: self.handle_info(info, video))
            playerinfo.run()

    def handle_info(self, info, video):
        ''' Handle information from PlayerInfo class '''
        self._kodi.log(2, 'Got VRT NU Player info: {info}', info=str(info))

        # Push resume position
        if info.get('position'):
            self.push_position(info, video)

        # Push up next episode info
        if info.get('episode'):
            self.push_upnext(info)

    def push_position(self, info, video):
        ''' Push player position to VRT NU resumepoints API '''
        # Get uuid, title and url from api based on video.get('publication_id') or video.get('video_url')
        if video.get('publication_id'):
            episode = self._apihelper.get_episodes(video_id=video.get('video_id'), variety='single')[0]
        elif video.get('video_url'):
            episode = self._apihelper.get_episodes(video_url=video_to_api_url(video.get('video_url')), variety='single')[0]
        uuid = self._resumepoints.assetpath_to_uuid(episode.get('assetPath'))
        title = episode.get('program')
        url = url_to_episode(episode.get('url', ''))

        # Push resumepoint to VRT NU
        self._resumepoints.update(uuid=uuid, title=title, url=url, watch_later=None, position=info.get('position'), total=info.get('total'))
        self._kodi.container_refresh()

    def push_upnext(self, info):
        ''' Push episode info to Up Next service add-on'''
        if self._kodi.has_addon('service.upnext') and self._kodi.get_setting('useupnext', 'true') == 'true' and info.get('program'):
            next_info = self._apihelper.get_upnext(info)
            if next_info:
                from binascii import hexlify
                import json
                data = [to_unicode(hexlify(json.dumps(next_info).encode()))]
                sender = '%s.SIGNAL' % self._kodi.addon_id()
                self._kodi.notify(sender=sender, message='upnext_data', data=data)
