import sys
import xbmcgui
import xbmcplugin
import requests
import urlparse
from urlparse import parse_qsl
from urllib2 import urlopen
from bs4 import BeautifulSoup

_url = sys.argv[0]
_handle = int(sys.argv[1])

_VRT_BASE_URL = "https://www.vrt.be/vrtnu/"



def get_stream_from_url(url, login_id, password):
    API_Key = "3_qhEcPa5JGFROVwu5SWKqJ4mVOIkwlFNMSKwzPDAh8QZOtHqu6L4nD5Q7lk0eXOOG"
    BASE_GET_STREAM_URL_PATH ="https://mediazone.vrt.be/api/v1/vrtvideo/assets/"

    s = requests.session()
    r = s.post("https://accounts.eu1.gigya.com/accounts.login",
               {'loginID': login_id, 'password': password, 'APIKey': API_Key})

    logon_json = r.json()
    uid = logon_json['UID']
    sig = logon_json['UIDSignature']
    ts = logon_json['signatureTimestamp']

    headers = {'Content-Type': 'application/json', 'Referer': _VRT_BASE_URL}
    data = '{"uid": "%s", ' \
           '"uidsig": "%s", ' \
           '"ts": "%s", ' \
           '"email": "%s"}' % (uid, sig, ts, login_id)

    response = s.post("https://token.vrt.be", data=data, headers=headers)
    securevideo_url = "{0}.securevideo.json".format(cut_slash_if_present(url))
    securevideo_response = s.get(securevideo_url, cookies=response.cookies)

    mzid = list(securevideo_response
                .json()
                .values())[0]['mzid']
    final_url = urlparse.urljoin(BASE_GET_STREAM_URL_PATH,
                                     mzid)

    stream_response = s.get(final_url)
    return get_hls(stream_response.json()['targetUrls'])


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
	return{ 'A-Z'}
	

def list_categories():
    titles = get_titles()
    listing = []
    for title in titles:
        list_item = xbmcgui.ListItem(label=title)
        # Create a URL for the plugin recursive callback.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = '{0}?action=listing&title={1}'.format(_url, title)
        listing.append((url, list_item, True))
		
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)
	
	
def list_videos():
	joined_url = urlparse.urljoin(_VRT_BASE_URL, "a-z/")
	response = urlopen(joined_url)
	soup = BeautifulSoup(response)
	listing = []
	for tile in soup.find_all(class_="tile"):
		rawThumbnail = thumbnailImage=tile.find("img")['srcset'].split('1x,')[0]
		thumbnail =  rawThumbnail.replace("//", "https://")
		li = xbmcgui.ListItem(tile.find(class_="tile__title").contents[0])
		li.setArt({'thumb':thumbnail})
		url = '{0}?action=play&video={1}'.format(_url, 'video')
		listing.append((url, li, False))
		
	xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
	xbmcplugin.endOfDirectory(_handle)
	
	
def router(paramstring):
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos()
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            print("playvid")
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
	

#xbmcplugin.setContent(_handle, 'movies')
#ga naar https://www.vrt.be/vrtnu/a-z/bat-pat/1/bat-pat-s1a19-over-de-regenboog
#rename met https://www.vrt.be/vrtnu/a-z/bat-pat/1/bat-pat-s1a19-over-de-regenboog.securevideo.json
#pak basepath: https://mediazone.vrt.be/api/v1/vrtvideo/assets/
#geconcateneerd met mzid
 
#https://userbase.be/forum/viewtopic.php?f=23&t=46630&start=80
#http://stackoverflow.com/questions/37616797/correct-way-to-implement-multi-folder-menus





