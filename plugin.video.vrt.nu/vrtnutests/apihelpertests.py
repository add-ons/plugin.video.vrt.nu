import unittest
from resources.lib.vrtplayer import vrtapihelper

class ApiHelperTests(unittest.TestCase):

    def test_get_api_data(self):
        api_helper = vrtapihelper.VRTApiHelper()
        title_items = api_helper.get_video_items('/vrtnu/a-z/animal-babies.relevant/')
        self.assertEqual(3, len(title_items))
        
