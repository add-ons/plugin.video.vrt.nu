# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, unicode_literals


class actions:
    LISTING_AZ_TVSHOWS = 'listingaztvshows'
    LISTING_CATEGORIES = 'listingcategories'
    LISTING_CATEGORY_TVSHOWS = 'listingcategorytvshows'
    LISTING_CHANNELS = 'listingchannels'
    LISTING_EPISODES = 'listingepisodes'
    LISTING_LIVE = 'listinglive'
    LISTING_RECENT = 'listingrecent'
    LISTING_TVGUIDE = 'listingtvguide'
    PLAY = 'play'


class TitleItem:

    def __init__(self, title, url, is_playable, art_dict=None, video_dict=None):
        self.title = title
        self.url = url
        self.is_playable = is_playable
        self.art_dict = art_dict
        self.video_dict = video_dict


class Credentials:

    def __init__(self, kodi_wrapper):
        self._kodi_wrapper = kodi_wrapper
        self._username = self._kodi_wrapper.get_setting('username')
        self._password = self._kodi_wrapper.get_setting('password')

    def are_filled_in(self):
        return not (self._username is None or self._password is None or self._username == '' or self._password == '')

    def reload(self):
        self._username = self._kodi_wrapper.get_setting('username')
        self._password = self._kodi_wrapper.get_setting('password')

    def reset(self):
        self._username = self._kodi_wrapper.set_setting('username', None)
        self._password = self._kodi_wrapper.set_setting('password', None)

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password


class ApiData:

    def __init__(self, client, media_api_url, video_id, publication_id, xvrttoken, is_live_stream):
        self._client = client
        self._media_api_url = media_api_url
        self._video_id = video_id
        self._publication_id = publication_id
        self._xvrttoken = xvrttoken
        self._is_live_stream = is_live_stream

    @property
    def client(self):
        return self._client

    @property
    def media_api_url(self):
        return self._media_api_url

    @property
    def video_id(self):
        return self._video_id

    @property
    def publication_id(self):
        return self._publication_id

    @property
    def xvrttoken(self):
        return self._xvrttoken

    @xvrttoken.setter
    def xvrttoken(self, value):
        self._xvrttoken = value

    @property
    def is_live_stream(self):
        return self._is_live_stream

    @is_live_stream.setter
    def is_live_stream(self, value):
        self._is_live_stream = value


class StreamURLS:

    def __init__(self, stream_url, subtitle_url=None, license_key=None, use_inputstream_adaptive=False):
        self._stream_url = stream_url
        self._subtitle_url = subtitle_url
        self._license_key = license_key
        self._use_inputstream_adaptive = use_inputstream_adaptive
        self._video_id = None

    @property
    def stream_url(self):
        return self._stream_url

    @property
    def subtitle_url(self):
        return self._subtitle_url

    @property
    def video_id(self):
        return self._video_id

    @property
    def license_key(self):
        return self._license_key

    @property
    def use_inputstream_adaptive(self):
        return self._use_inputstream_adaptive
