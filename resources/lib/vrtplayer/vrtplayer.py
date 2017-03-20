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
from urllib2 import urlopen
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

    def __init__(self, handle, url):
        self._handle = handle
        self._url = url

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

    def list_videos_az(self):
        joined_url = urljoin(self._VRTNU_BASE_URL, "./a-z/")
        response = urlopen(joined_url)
        tiles = SoupStrainer('a', {"class": "tile"})
        soup = BeautifulSoup(response, "html.parser", parse_only=tiles)
        listing = []
        for tile in soup.find_all(class_="tile"):
            link_to_video = tile["href"]
            info = tile.find(class_="tile__description").find("p").text
            li = self.__get_item(tile, "false")
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
    def __format_image_url(element):
        raw_thumbnail = element.find("img")['srcset'].split('1x,')[0]
        return raw_thumbnail.replace("//", "https://")

    def get_video_episodes(self, path):
        url = urljoin(self._VRT_BASE, path)
        #xbmc.log(url, xbmc.LOGWARNING)
        s = requests.session()
        # go to url.relevant gets redirected and go on with this url
        response = urlopen(s.get(url).url)
        soup = BeautifulSoup(response, "html.parser")
        listing = []
        episodes = soup.find_all(class_="tile")
        if len(episodes) != 0:
            for tile in soup.find_all(class_="tile"):
                li = self.__get_item(tile, "true")
                if li is not None:
                    link_to_video = tile["href"]
                    url = '{0}?action=play&video={1}'.format(self._url, link_to_video)
                    listing.append((url, li, False))
        else:
            vrt_video = soup.find(class_="vrtvideo")
            thumbnail = self.__format_image_url(vrt_video)
            li = xbmcgui.ListItem(soup.find(class_="content__title").text)
            li.setProperty('IsPlayable', 'true')
            li.setArt({'thumb': thumbnail})
            url = '{0}?action=play&video={1}'.format(self._url, path)
            listing.append((url, li, False))

        xbmcplugin.addDirectoryItems(self._handle, listing, len(listing))
        xbmcplugin.endOfDirectory(self._handle)

    def play_video(self, path):
        stream_service = urltostreamservice.UrlToStreamService(self._VRT_BASE, self._VRTNU_BASE_URL, self._addon_)
        stream = stream_service.get_stream_from_url(path)
        if stream is not None:
            play_item = xbmcgui.ListItem(path=stream.stream_url)
            if stream.subtitle_url is not None:
                play_item.setSubtitles([stream.subtitle_url])
            xbmcplugin.setResolvedUrl(self._handle, True, listitem=play_item)

    def play_livestream(self, path):
        play_item = xbmcgui.ListItem(path=path)
        xbmcplugin.setResolvedUrl(self._handle, True, listitem=play_item)