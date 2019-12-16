# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Tests for StaticHelper functionality"""

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import utils


class TestStaticHelper(unittest.TestCase):
    """TestCase class"""

    def test_url_to_episode(self):
        """Test converting URL to episode"""
        long_url = 'https://www.vrt.be/vrtnu/a-z/buck/1/buck-s1a32/'
        episode = '/vrtnu/a-z/buck/1/buck-s1a32/'
        self.assertEqual(episode, utils.url_to_episode(long_url))

        medium_url = '//www.vrt.be/vrtnu/a-z/buck/1/buck-s1a32/'
        episode = '/vrtnu/a-z/buck/1/buck-s1a32/'
        self.assertEqual(episode, utils.url_to_episode(medium_url))

        self.assertEqual(None, utils.url_to_episode('foobar'))

    def test_url_to_program(self):
        """Test converting URL to program"""
        program = 'buck'
        short_url = '/vrtnu/a-z/buck/1/buck-s1a32/'
        medium_url = '//www.vrt.be/vrtnu/a-z/buck/1/buck-s1a32/'
        long_url = 'https://www.vrt.be/vrtnu/a-z/buck/1/buck-s1a32/'
        short_relevant_url = '/vrtnu/a-z/buck.relevant/'

        self.assertEqual(program, utils.url_to_program(long_url))
        self.assertEqual(program, utils.url_to_program(medium_url))
        self.assertEqual(program, utils.url_to_program(short_url))
        self.assertEqual(program, utils.url_to_program(short_relevant_url))

    def test_program_to_url(self):
        """Test converting program to URL"""
        program = 'de-campus-cup'
        short_url = '/vrtnu/a-z/de-campus-cup/'
        medium_url = '//www.vrt.be/vrtnu/a-z/de-campus-cup/'
        long_url = 'https://www.vrt.be/vrtnu/a-z/de-campus-cup/'

        self.assertEqual(short_url, utils.program_to_url(program, 'short'))
        self.assertEqual(medium_url, utils.program_to_url(program, 'medium'))
        self.assertEqual(long_url, utils.program_to_url(program, 'long'))

    def test_video_to_api_url(self):
        """Test convert video to api URL"""
        video = 'https://www.vrt.be/vrtnu/a-z/de-ideale-wereld/2019-nj/de-ideale-wereld-d20191010/'
        api_url = '//www.vrt.be/vrtnu/a-z/de-ideale-wereld/2019-nj/de-ideale-wereld-d20191010/'
        self.assertEqual(api_url, utils.video_to_api_url(video))

        video = 'https://www.vrt.be/vrtnu/a-z/de-ideale-wereld/2019-nj/de-ideale-wereld-d20191010'
        api_url = '//www.vrt.be/vrtnu/a-z/de-ideale-wereld/2019-nj/de-ideale-wereld-d20191010/'
        self.assertEqual(api_url, utils.video_to_api_url(video))

    def test_play_url_to_id(self):
        """Test converting play_url to play_id"""
        url = 'plugin://plugin.video.vrt.nu/play/id/vid-5b12c0f6-b8fe-426f-a600-557f501f3be9/pbs-pub-7e2764cf-a8c0-4e78-9cbc-46d39381c237'
        play_id = dict(video_id='vid-5b12c0f6-b8fe-426f-a600-557f501f3be9')
        self.assertEqual(play_id, utils.play_url_to_id(url))

        url = 'plugin://plugin.video.vrt.nu/play/upnext/vid-271d7238-b7f2-4a3c-b3c7-17a5110be71a'
        play_id = dict(video_id='vid-271d7238-b7f2-4a3c-b3c7-17a5110be71a')
        self.assertEqual(play_id, utils.play_url_to_id(url))

        url = 'plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtnu/kanalen/canvas/'
        play_id = dict(video_url='//www.vrt.be/vrtnu/kanalen/canvas/')
        self.assertEqual(play_id, utils.play_url_to_id(url))

    def test_reformat_url(self):
        """Test reformatting URLs"""
        short_url = '/vrtnu/a-z/terzake/2019/terzake-d20191017/'
        medium_url = '//www.vrt.be/vrtnu/a-z/terzake/2019/terzake-d20191017/'
        long_url = 'https://www.vrt.be/vrtnu/a-z/terzake/2019/terzake-d20191017/'

        self.assertEqual(long_url, utils.reformat_url(short_url, 'long'))
        self.assertEqual(long_url, utils.reformat_url(medium_url, 'long'))
        self.assertEqual(long_url, utils.reformat_url(long_url, 'long'))

        self.assertEqual(medium_url, utils.reformat_url(short_url, 'medium'))
        self.assertEqual(medium_url, utils.reformat_url(medium_url, 'medium'))
        self.assertEqual(medium_url, utils.reformat_url(long_url, 'medium'))

        self.assertEqual(short_url, utils.reformat_url(short_url, 'short'))
        self.assertEqual(short_url, utils.reformat_url(medium_url, 'short'))
        self.assertEqual(short_url, utils.reformat_url(long_url, 'short'))

        self.assertEqual(long_url, utils.reformat_url(long_url + '#foo', 'long'))
        self.assertEqual(medium_url, utils.reformat_url(long_url + '#foo', 'medium'))
        self.assertEqual(short_url, utils.reformat_url(long_url + '#foo', 'short'))

    def test_shorten_link(self):
        """Test shortening links"""
        permalink = 'vrtnu.be/p.LR90GkqOD'
        medium_url = '//www.vrt.be/vrtnu/p.LR90GkqOD'
        long_url = 'https://www.vrt.be/vrtnu/p.LR90GkqOD'

        self.assertEqual(permalink, utils.shorten_link(long_url))
        self.assertEqual(permalink, utils.shorten_link(medium_url))
        self.assertEqual(None, utils.shorten_link(None))

    def test_realpage(self):
        """Test converting input to page"""
        self.assertEqual(1, utils.realpage('foo'))
        self.assertEqual(1, utils.realpage('-1'))
        self.assertEqual(1, utils.realpage('0'))
        self.assertEqual(2, utils.realpage(2))
        self.assertEqual(3, utils.realpage('3'))

    def test_capitalize(self):
        """Test capitalizing string"""
        self.assertEqual('Foo bar', utils.capitalize('foo bar'))
        self.assertEqual('Foo bar', utils.capitalize('Foo bar'))
        self.assertEqual('FoO bAr', utils.capitalize('foO bAr'))
        self.assertEqual('FOO BAR', utils.capitalize('FOO BAR'))


if __name__ == '__main__':
    unittest.main()
