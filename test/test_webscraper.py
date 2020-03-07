# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for WebScraper functionality"""

# pylint: disable=invalid-name

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from data import CATEGORIES
from webscraper import get_categories, get_video_attributes, valid_categories


class TestWebScraper(unittest.TestCase):
    """TestCase class"""

    def test_get_categories(self):
        """Test to ensure our hardcoded categories conforms to scraped categories"""
        # Remove thumbnails from scraped categories first
        categories_scraped = [dict(id=c['id'], name=c['name']) for c in get_categories()]
        categories_stored = [dict(id=c['id'], name=c['name']) for c in CATEGORIES]
        self.assertTrue(valid_categories(categories_scraped))
        self.assertTrue(valid_categories(categories_stored))
        self.assertEqual(categories_scraped, categories_stored)

    def test_get_video_attributes(self):
        """Test getting video attributes"""
        vrtnu_urls = [
            'https://www.vrt.be/vrtnu/a-z/girls-talk/2/girls-talk-s2-mannen-kunnen-beter-drinken/',
            'https://www.vrt.be/vrtnu/a-z/de-ideale-wereld/2019-nj/de-ideale-wereld-d20191219/',
            'https://www.vrt.be/vrtnu/livestream/#epgchannel=O8',  # Eén
            'https://www.vrt.be/vrtnu/livestream/#epgchannel=1H',  # Canvas
            'https://www.vrt.be/vrtnu/livestream/#epgchannel=O9'  # Ketnet
        ]
        for vrtnu_url in vrtnu_urls:
            video_attrs = get_video_attributes(vrtnu_url)
            self.assertTrue(isinstance(video_attrs, dict))
            self.assertTrue(any(key in video_attrs for key in ['livestream', 'videoid']))

    def test_get_video_attributes_bad_urls(self):
        """Test getting video attributes using bad urls"""
        bad_urls = [
            'https://www.vrt.be/vrtnu/a-z/de-ideale-wereld/2019-nj/de-ideale-wereld-d20191218/',
            'https://www.vrt.be/vrtnu/kanalen/studio-brussel/',
            'https://vtm.be/vtmgo'
        ]
        for bad_url in bad_urls:
            video_attrs = get_video_attributes(bad_url)
            self.assertEqual(None, video_attrs)


if __name__ == '__main__':
    unittest.main()
