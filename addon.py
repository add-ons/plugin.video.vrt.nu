import sys
import xbmcgui
import xbmcplugin
from urllib2 import urlopen
from bs4 import BeautifulSoup

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'movies')
#http://stackoverflow.com/questions/37616797/correct-way-to-implement-multi-folder-menus
response = urlopen('https://www.vrt.be/vrtnu/a-z/')
soup = BeautifulSoup(response)
for tile in soup.find_all(class_="tile"):
	rawThumbnail = thumbnailImage=tile.find("img")['srcset'].split('1x,')[0]
	thumbnail =  rawThumbnail.replace("//", "https://")
	li = xbmcgui.ListItem(tile.find(class_="tile__title").contents[0])
	li.setArt({'thumb':thumbnail})
	xbmcplugin.addDirectoryItem(handle=addon_handle, url='test', listitem=li, true)

xbmcplugin.endOfDirectory(addon_handle)




