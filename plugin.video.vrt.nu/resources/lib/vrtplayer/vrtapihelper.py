import requests
from resources.lib.vrtplayer import statichelper, metadatacreator, actions
from resources.lib.helperobjects import helperobjects
from bs4 import BeautifulSoup
import time

class VRTApiHelper:
    
    _API_URL = 'https://search.vrt.be/search?size=150&facets[programUrl]=//www.vrt.be'

    def get_video_items(self, relevant_url):
        joined_url = self._API_URL + relevant_url.replace(".relevant" ,"")
        response = (requests.get(joined_url)).json()
        result_list = response['results']
        title_items = list(map(lambda x: self.__map_to_title_item(x), result_list))
        return title_items

    def __map_to_title_item(self, result):
        metadata_creator = metadatacreator.MetadataCreator()
        json_broadcast_date = result['broadcastDate']
        description = None
        if json_broadcast_date != -1 :
            epoch_in_seconds = result['broadcastDate']/1000
            metadata_creator.datetime = time.localtime(epoch_in_seconds)
            description = metadata_creator.datetime_as_short_date
        metadata_creator.duration = result['duration']
        metadata_creator.plot = BeautifulSoup(result['description'], 'html.parser').text 
        description = description +  " "  + result['shortDescription']
        
        thumb = statichelper.replace_double_slashes_with_https(result['videoThumbnailUrl'])
        #shortdescription as title just like vrt nu does
        return helperobjects.TitleItem(description, {'action': actions.PLAY, 'video': result['url']}, True, thumb, metadata_creator.get_video_dictionary())
        


