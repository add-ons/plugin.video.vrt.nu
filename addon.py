import sys
import xbmcgui
import xbmcplugin
import requests
import urlparse
from urllib2 import urlopen
from bs4 import BeautifulSoup

_url = sys.argv[0]
_handle = int(sys.argv[1])



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

    headers = {'Content-Type': 'application/json', 'Referer': 'https://www.vrt.be/vrtnu/'}
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
    # Get video categories
    titles = get_titles()
    # Create a list for our items.
    listing = []
    # Iterate through categories
    for title in titles:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=title)
        # Create a URL for the plugin recursive callback.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = '{0}?action=listing&title={1}'.format(_url, title)
        # Add our item to the listing as a 3-element tuple.
        listing.append((url, list_item, True))
    # Add our listing to Kodi.
    # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
    # instead of adding one by ove via addDirectoryItem.
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)
	
	
def list_videos():
	li = xbmcgui.ListItem('title')
	xbmcplugin.addDirectoryItem(_handle, listitem=li)
	xbmcplugin.endOfDirectory(_handle)
	
	
def router(paramstring):
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = parse_qs(urlparse(paramstring).query)
    # Check the parameters passed to the plugin
    if params:
        if params['action'][0] == 'listing':
            # Display the list of videos in a provided category.
            list_videos()
        elif params['action'][0] == 'play':
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
#response = urlopen('https://www.vrt.be/vrtnu/a-z/')
#soup = BeautifulSoup(response)
#for tile in soup.find_all(class_="tile"):
	#rawThumbnail = thumbnailImage=tile.find("img")['srcset'].split('1x,')[0]
	#thumbnail =  rawThumbnail.replace("//", "https://")
	#li = xbmcgui.ListItem(tile.find(class_="tile__title").contents[0])
	#li.setArt({'thumb':thumbnail})
	#xbmcplugin.addDirectoryItem(handle=_handle, url='http://vod.stream.vrt.be/mediazone_vrt/_definst_/smil:vid/2017/01/28/vid-dis-51dd6b3d-b659-4491-8677-c84bf8ed8018-2/video.smil/chunklist_w873303264_b2096000_slnl.m3u8', listitem=li)

#xbmcplugin.endOfDirectory(_handle)




