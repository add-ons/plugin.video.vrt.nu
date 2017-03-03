import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests
from urlparse import parse_qsl
from urlparse import  urljoin
from urllib2 import urlopen
from bs4 import BeautifulSoup
from resources.lib.urltostreamservice import urltostreamservice
from resources.lib.helperobjects import helperobjects


class VRTPlayer:
    _VRT_LIVESTREAM_URL = "http://live.stream.vrt.be/vrt_video1_live/smil:vrt_video1_live.smil/playlist.m3u8"
    _VRT_BASE = "https://www.vrt.be/"
    _VRTNU_BASE_URL = urljoin(_VRT_BASE, "/vrtnu/")
    _addon_ = xbmcaddon.Addon()
    _addonname_ = _addon_.getAddonInfo('name')

    def __init__(self): pass

    def __get_title_items(self):
        return {helperobjects.TitleItem(self._addon_.getLocalizedString(32091), '{0}?action=listingaz', False),
                helperobjects.TitleItem(self._addon_.getLocalizedString(32092), self._VRT_LIVESTREAM_URL, True)}

    def __list_categories(self):
        listing = []
        for title_item in self.__get_title_items():
            list_item = xbmcgui.ListItem(label=title_item.title)
            url = title_item.url.format(_url, title_item.title)
            list_item.setProperty('IsPlayable', str(title_item.is_playable))
            listing.append((url, list_item, not title_item.is_playable))
        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(_handle)

    def __list_videos_az(self):
        joined_url = urljoin(self._VRTNU_BASE_URL, "./a-z/")
        response = urlopen(joined_url)
        soup = BeautifulSoup(response, "html.parser")
        listing = []
        for tile in soup.find_all(class_="tile"):
            link_to_video = tile["href"]
            li = self.__get_item(tile, "false")
            url = '{0}?action=getepisodes&video={1}'.format(_url, link_to_video)
            listing.append((url, li, True))

        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(_handle)

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

    def __get_video_episodes(self, path):
        url = urljoin(self._VRT_BASE, path)
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
                    url = '{0}?action=play&video={1}'.format(_url, link_to_video)
                    listing.append((url, li, False))
        else:
            vrt_video = soup.find(class_="vrtvideo")
            thumbnail = self.__format_image_url(vrt_video)
            li = xbmcgui.ListItem(soup.find(class_="content__title").text)
            li.setProperty('IsPlayable', 'true')
            li.setArt({'thumb': thumbnail})
            url = '{0}?action=play&video={1}'.format(_url, path)
            listing.append((url, li, False))

        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(_handle)

    def __play_video(self, path):
        stream_service = urltostreamservice.UrlToStreamService(self._VRT_BASE, self._VRTNU_BASE_URL, self._addon_)
        stream = stream_service.get_stream_from_url(path)
        if stream is not None:
            play_item = xbmcgui.ListItem(path=stream)
            xbmcplugin.setResolvedUrl(_handle, True, listitem= play_item)

    def router(self, params_string):
        params = dict(parse_qsl(params_string))
        if params:
            if params['action'] == 'listingaz':
                self.__list_videos_az()
            elif params['action'] == 'getepisodes':
                self.__get_video_episodes(params['video'])
            elif params['action'] == 'play':
                self.__play_video(params['video'])
        else:
            self.__list_categories()


_url = sys.argv[0]
_handle = int(sys.argv[1])
_VRTPlayer = VRTPlayer()

if __name__ == '__main__':
    _VRTPlayer.router(sys.argv[2][1:])

