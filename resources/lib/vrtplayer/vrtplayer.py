import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests
import re
import  time
from urlparse import parse_qsl
from urlparse import urljoin
from urllib import  urlencode
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from resources.lib.vrtplayer import urltostreamservice
from resources.lib.helperobjects import helperobjects


class VRTPlayer:

    _VRT_BASE = "https://www.vrt.be/"
    _VRTNU_BASE_URL = urljoin(_VRT_BASE, "/vrtnu/")
    _addon_ = xbmcaddon.Addon()
    _addonname_ = _addon_.getAddonInfo('name')

    def __init__(self, handle, url, session):
        self._handle = handle
        self._url = url
        self._session = session

    @staticmethod
    def __format_image_url(element):
        raw_thumbnail = element.find("img")['srcset'].split('1x,')[0]
        return raw_thumbnail.replace("//", "https://")

    @staticmethod
    def __set_plot(li, description):
        li.setInfo('video', {'plot': description.strip()})
        return li

    def list_categories(self, list_items):
        listing = []
        for title_item in list_items:
            list_item = xbmcgui.ListItem(label=title_item.title)
            url = self._url + '?' + urlencode(title_item.url_dictionary)
            list_item.setProperty('IsPlayable', str(title_item.is_playable))
            list_item.setArt({'thumb': title_item.logo})
            listing.append((url, list_item, not title_item.is_playable))
        xbmcplugin.addDirectoryItems(self._handle, listing, len(listing))
        xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(self._handle)

    @staticmethod
    def __get_AZ_description(tile):
        description = ""
        description_item = tile.find(class_="tile__description")
        if description_item is not None:
            p_item = description_item.find("p")
            if p_item is not None:
                description = p_item.text
        return description

    def list_videos_az(self):
        joined_url = urljoin(self._VRTNU_BASE_URL, "./a-z/")
        response = requests.get(joined_url)
        tiles = SoupStrainer('a', {"class": "tile"})
        soup = BeautifulSoup(response.content, "html.parser", parse_only=tiles)
        listing = []
        for tile in soup.find_all(class_="tile"):
            link_to_video = tile["href"]
            description = self.__get_AZ_description(tile)
            li = self.__get_item(tile, "false")
            li.setInfo('video', {'plot': description.strip()})
            url = '{0}?action=getepisodes&video={1}'.format(self._url, link_to_video)
            listing.append((url, li, True))

        xbmcplugin.addDirectoryItems(self._handle, listing, len(listing))
        xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(self._handle,)

    def __get_item(self, element, is_playable):
        thumbnail = self.__format_image_url(element)
        found_element = element.find(class_="tile__title")
        li = None
        if found_element is not None:
            li = xbmcgui.ListItem(found_element.contents[0]
                                  .replace("\n", "").strip())
            li.setProperty('IsPlayable', is_playable)
            li.setArt({'thumb': thumbnail})
        return li

    @staticmethod
    def __get_episode_description(soup):
        description = ""
        description_item = soup.find(class_="content__shortdescription")
        if description_item is not None:
            description = description_item.text
        return description

    @staticmethod
    def __get_episode_duration(soup):
        duration = None
        duration_item = soup.find(class_="content__duration")
        if duration_item is not None:
            minutes = re.findall("\d+", duration_item.text)
            if len(minutes) != 0:
                duration = VRTPlayer.__minutes_string_to_seconds_int(minutes[0])
        return duration

    def get_video_episodes(self, path):
        url = urljoin(self._VRT_BASE, path)
        #xbmc.log(url, xbmc.LOGWARNING)
        # go to url.relevant gets redirected and go on with this url
        relevant_path = requests.get(url)
        response = requests.get(relevant_path.url)
        soup = BeautifulSoup(response.content, "html.parser")
        listing = []
        episodes = soup.find_all(class_="tile")
        if len(episodes) != 0:
            listing.extend(self.get_multiple_videos(soup))
        else:
            li, url = self.get_single_video(relevant_path.url, soup)
            listing.append((url, li, False))

        xbmcplugin.addDirectoryItems(self._handle, listing, len(listing))
        xbmcplugin.endOfDirectory(self._handle)

    def get_multiple_videos(self, soup):
        items = []
        episode_list = soup.find("div", {"id": "episodelist__slider"})

        for tile in episode_list.find_all(class_="tile"):
            li = self.__get_item(tile, "true")
            if li is not None:
                link_to_video = tile["href"]
                duration = self.__get_multiple_episodes_duration(tile)
                video_dictionary = dict()
                self.__add_duration_to_video(video_dictionary, duration)
                li.setInfo('video', video_dictionary)
                url = '{0}?action=play&video={1}'.format(self._url, link_to_video)
                items.append((url, li, False))
        return items

    @staticmethod
    def __add_duration_to_video(dictionary, duration):
        if duration is not None:
            dictionary["duration"] = duration
        return duration

    @staticmethod
    def __add_plot_to_video(dictionary, plot):
        if plot is not None:
            dictionary["plot"] = plot.strip()
        return plot

    @staticmethod
    def __get_multiple_episodes_duration(tile):
        seconds = None
        minutes_element = tile.find("abbr", {"title": "minuten"})
        if minutes_element is not None and minutes_element.parent is not None:
            minutes = minutes_element.parent.next_element
            seconds = VRTPlayer.__minutes_string_to_seconds_int(minutes)
        return seconds

    @staticmethod
    def __minutes_string_to_seconds_int(minutes):
        try:
            return int(minutes) * 60
        except ValueError:
            return None

    def get_single_video(self, path, soup):
        vrt_video = soup.find(class_="vrtvideo")
        thumbnail = self.__format_image_url(vrt_video)
        description = self.__get_episode_description(soup)
        li = xbmcgui.ListItem(soup.find(class_="content__title").text)
        li.setProperty('IsPlayable', 'true')
        video_dictionary = dict()
        self.__add_duration_to_video(video_dictionary, self.__get_episode_duration(soup))
        self.__add_plot_to_video(video_dictionary, description)
        li.setInfo('video', video_dictionary)
        li.setArt({'thumb': thumbnail})
        url = '{0}?action=play&video={1}'.format(self._url, path)
        return li, url

    def play_video(self, path):
        stream_service = urltostreamservice.UrlToStreamService(self._VRT_BASE,
                                                               self._VRTNU_BASE_URL,
                                                               self._addon_,
                                                               self._session)
        stream = stream_service.get_stream_from_url(path)
        if stream is not None:
            play_item = xbmcgui.ListItem(path=stream.stream_url)
            play_item.setMimeType('video/mp4')
            if stream.subtitle_url is not None:
                play_item.setSubtitles([stream.subtitle_url])
            xbmcplugin.setResolvedUrl(self._handle, True, listitem=play_item)

    def play_livestream(self, path):
        play_item = xbmcgui.ListItem(path=path)
        xbmcplugin.setResolvedUrl(self._handle, True, listitem=play_item)