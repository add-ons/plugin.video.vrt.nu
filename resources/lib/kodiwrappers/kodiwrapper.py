import xbmc
import xbmcgui
import xbmcplugin
from urllib import urlencode

class KodiWrapper:

    def __init__(self, handle, url):
        self._handle = handle
        self._url = url

    def show_listing(self, list_items):
        listing = []
        for title_item in list_items:
            list_item = xbmcgui.ListItem(label=title_item.title)
            url = self._url + '?' + urlencode(title_item.url_dictionary)
            list_item.setProperty('IsPlayable', str(title_item.is_playable))
            list_item.setArt({'thumb': title_item.logo})
            list_item.setInfo('video', title_item.video_dictionary)
            listing.append((url, list_item, not title_item.is_playable))
        xbmcplugin.addDirectoryItems(self._handle, listing, len(listing))
        xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(self._handle)
