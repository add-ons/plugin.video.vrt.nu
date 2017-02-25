import sys
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests
import urlparse
from urlparse import parse_qsl
from urllib2 import urlopen
from bs4 import BeautifulSoup

_url = sys.argv[0]
_handle = int(sys.argv[1])

_VRT_BASE = "https://www.vrt.be/"
_VRTNU_BASE_URL = _VRT_BASE + "vrtnu/"
_addon_ = xbmcaddon.Addon()
_addonname_ = _addon_.getAddonInfo('name')


def get_stream_from_url(url, login_id, password):
    API_Key = "3_qhEcPa5JGFROVwu5SWKqJ4mVOIkwlFNMSKwzPDAh8QZOtHqu6L4nD5Q7lk0eXOOG"
    BASE_GET_STREAM_URL_PATH = "https://mediazone.vrt.be/api/v1/vrtvideo/assets/"
    url = urlparse.urljoin(_VRT_BASE, url)
    s = requests.session()
    # go to url.relevant gets redirected and go on with this url
    url = s.get(url).url
    r = s.post("https://accounts.eu1.gigya.com/accounts.login",
               {'loginID': login_id, 'password': password, 'APIKey': API_Key})

    logon_json = r.json()
    if logon_json['errorCode'] == 0:
        uid = logon_json['UID']
        sig = logon_json['UIDSignature']
        ts = logon_json['signatureTimestamp']

        headers = {'Content-Type': 'application/json', 'Referer': _VRTNU_BASE_URL}
        data = '{"uid": "%s", ' \
               '"uidsig": "%s", ' \
               '"ts": "%s", ' \
               '"email": "%s"}' % (uid, sig, ts, login_id)

        response = s.post("https://token.vrt.be", data=data, headers=headers)
        securevideo_url = "{0}.securevideo.json".format(cut_slash_if_present(url))
        securevideo_response = s.get(securevideo_url, cookies=response.cookies)
        json = securevideo_response.json()

        mzid = list(json
                    .values())[0]['mzid']
        final_url = urlparse.urljoin(BASE_GET_STREAM_URL_PATH,
                                     mzid)

        stream_response = s.get(final_url)
        return get_hls(stream_response.json()['targetUrls'])
    else:
        xbmcgui.Dialog().ok(_addonname_, _addon_.getLocalizedString(32051), _addon_.getLocalizedString(32052))



def get_hls(dictionary):
    for item in dictionary:
        if item['type'] == 'HLS':
            return item['url']


def cut_slash_if_present(url):
    if url.endswith('/'):
        return url[:-1]
    else:
        return url


def get_titles():
    return {'A-Z'}


def list_categories():
    titles = get_titles()
    listing = []
    for title in titles:
        list_item = xbmcgui.ListItem(label=title)
        url = '{0}?action=listing&title={1}'.format(_url, title)
        listing.append((url, list_item, True))

    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def list_videos():
    joined_url = urlparse.urljoin(_VRTNU_BASE_URL, "a-z/")
    response = urlopen(joined_url)
    soup = BeautifulSoup(response, "html.parser")
    listing = []
    for tile in soup.find_all(class_="tile"):
        link_to_video = tile["href"]
        get_item(tile, "false")
        url = '{0}?action=getepisodes&video={1}'.format(_url, link_to_video)
        listing.append((url, li, False))

    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)


def get_item(element, is_playable):
    rawThumbnail = element.find("img")['srcset'].split('1x,')[0]
    thumbnail = rawThumbnail.replace("//", "https://")
    li = xbmcgui.ListItem(tile.find(class_="tile__title").contents[0])
    li.setProperty('IsPlayable', is_playable)
    li.setArt({'thumb': thumbnail})
    return li



def get_video_episodes(path):
    url = urlparse.urljoin(_VRT_BASE, url)
    s = requests.session()
    # go to url.relevant gets redirected and go on with this url
    response = urlopen(s.get(url).url)
    soup = BeautifulSoup(response, "html.parser")
    listing = []
    episodes = soup.find_all(class_="vrtlist__item")
    if(len(episodes) != 0):
        for tile in soup.find_all(class_="vrtlist__item"):
            get_item(tile, "true")
            url = '{0}?action=getepisodes&video={1}'.format(_url, link_to_video)
            listing.append((url, li, False))

    #username = _addon_.getSetting("username")
    #password = _addon_.getSetting("password")
    #if username is None or password is None or username == "" or password == "":
    #    _addon_.openSettings()
    #else:
    #    stream = get_stream_from_url(path, username, password)
    #    if stream is not None:
    #        play_item = xbmcgui.ListItem(path=stream)
    #        xbmcplugin.setResolvedUrl(_handle, True, listitem= play_item)#


def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'listing':
            list_videos()
        elif params['action'] == 'getepisodes':
            get_video_episodes(params['video'])
    else:
        list_categories()


if __name__ == '__main__':
    router(sys.argv[2][1:])





