# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=invalid-name,missing-docstring

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import statichelper


class TestStaticHelper(unittest.TestCase):

    def test_url_to_episode(self):
        long_url = 'https://www.vrt.be/vrtnu/a-z/buck/1/buck-s1a32/'
        episode = '/vrtnu/a-z/buck/1/buck-s1a32/'
        self.assertEqual(episode, statichelper.url_to_episode(long_url))

        medium_url = '//www.vrt.be/vrtnu/a-z/buck/1/buck-s1a32/'
        episode = '/vrtnu/a-z/buck/1/buck-s1a32/'
        self.assertEqual(episode, statichelper.url_to_episode(medium_url))

        self.assertEqual(None, statichelper.url_to_episode('foobar'))

    def test_url_to_program(self):
        long_url = 'https://www.vrt.be/vrtnu/a-z/buck/1/buck-s1a32/'
        program = 'buck'
        self.assertEqual(program, statichelper.url_to_program(long_url))

        medium_url = '//www.vrt.be/vrtnu/a-z/buck/1/buck-s1a32/'
        program = 'buck'
        self.assertEqual(program, statichelper.url_to_program(medium_url))

        short_url = '/vrtnu/a-z/buck/1/buck-s1a32/'
        program = 'buck'
        self.assertEqual(program, statichelper.url_to_program(short_url))

        short_url = '/vrtnu/a-z/buck.relevant/'
        program = 'buck'
        self.assertEqual(program, statichelper.url_to_program(short_url))

    def test_program_to_url(self):
        program = 'de-campus-cup'
        short_url = '/vrtnu/a-z/de-campus-cup/'
        medium_url = '//www.vrt.be/vrtnu/a-z/de-campus-cup/'
        long_url = 'https://www.vrt.be/vrtnu/a-z/de-campus-cup/'

        self.assertEqual(short_url, statichelper.program_to_url(program, 'short'))
        self.assertEqual(medium_url, statichelper.program_to_url(program, 'medium'))
        self.assertEqual(long_url, statichelper.program_to_url(program, 'long'))

    def test_video_to_api_url(self):
        video = 'https://www.vrt.be/vrtnu/a-z/de-ideale-wereld/2019-nj/de-ideale-wereld-d20191010/'
        api_url = '//www.vrt.be/vrtnu/a-z/de-ideale-wereld/2019-nj/de-ideale-wereld-d20191010/'
        self.assertEqual(api_url, statichelper.video_to_api_url(video))

        video = 'https://www.vrt.be/vrtnu/a-z/de-ideale-wereld/2019-nj/de-ideale-wereld-d20191010'
        api_url = '//www.vrt.be/vrtnu/a-z/de-ideale-wereld/2019-nj/de-ideale-wereld-d20191010/'
        self.assertEqual(api_url, statichelper.video_to_api_url(video))

    def test_play_url_to_id(self):
        url = 'plugin://plugin.video.vrt.nu/play/id/vid-5b12c0f6-b8fe-426f-a600-557f501f3be9/pbs-pub-7e2764cf-a8c0-4e78-9cbc-46d39381c237'
        play_id = dict(video_id='vid-5b12c0f6-b8fe-426f-a600-557f501f3be9')
        self.assertEqual(play_id, statichelper.play_url_to_id(url))

        url = 'plugin://plugin.video.vrt.nu/play/whatson/705308178527'
        play_id = dict(whatson_id='705308178527')
        self.assertEqual(play_id, statichelper.play_url_to_id(url))

        url = 'plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtnu/kanalen/canvas/'
        play_id = dict(video_url='//www.vrt.be/vrtnu/kanalen/canvas/')
        self.assertEqual(play_id, statichelper.play_url_to_id(url))

    def test_reformat_url(self):
        short_url = '/vrtnu/a-z/terzake/2019/terzake-d20191017/'
        medium_url = '//www.vrt.be/vrtnu/a-z/terzake/2019/terzake-d20191017/'
        long_url = 'https://www.vrt.be/vrtnu/a-z/terzake/2019/terzake-d20191017/'

        self.assertEqual(long_url, statichelper.reformat_url(short_url, 'long'))
        self.assertEqual(long_url, statichelper.reformat_url(medium_url, 'long'))
        self.assertEqual(long_url, statichelper.reformat_url(long_url, 'long'))

        self.assertEqual(medium_url, statichelper.reformat_url(short_url, 'medium'))
        self.assertEqual(medium_url, statichelper.reformat_url(medium_url, 'medium'))
        self.assertEqual(medium_url, statichelper.reformat_url(long_url, 'medium'))

        self.assertEqual(short_url, statichelper.reformat_url(short_url, 'short'))
        self.assertEqual(short_url, statichelper.reformat_url(medium_url, 'short'))
        self.assertEqual(short_url, statichelper.reformat_url(long_url, 'short'))

        self.assertEqual(long_url, statichelper.reformat_url(long_url + '#foo', 'long'))
        self.assertEqual(medium_url, statichelper.reformat_url(long_url + '#foo', 'medium'))
        self.assertEqual(short_url, statichelper.reformat_url(long_url + '#foo', 'short'))

    def test_shorten_link(self):
        self.assertEqual(None, statichelper.shorten_link(None))

        long_url = 'https://www.vrt.be/vrtnu/p.LR90GkqOD'
        self.assertEqual('vrtnu.be/p.LR90GkqOD', statichelper.shorten_link(long_url))

        medium_url = '//www.vrt.be/vrtnu/p.LR90GkqOD'
        self.assertEqual('vrtnu.be/p.LR90GkqOD', statichelper.shorten_link(medium_url))

    def test_realpage(self):
        self.assertEqual(1, statichelper.realpage('foo'))
        self.assertEqual(1, statichelper.realpage('-1'))
        self.assertEqual(1, statichelper.realpage('0'))
        self.assertEqual(2, statichelper.realpage(2))
        self.assertEqual(3, statichelper.realpage('3'))

    def test_capitalize(self):
        self.assertEqual('Foo bar', statichelper.capitalize('foo bar'))
        self.assertEqual('Foo bar', statichelper.capitalize('Foo bar'))
        self.assertEqual('FoO bAr', statichelper.capitalize('foO bAr'))
        self.assertEqual('FOO BAR', statichelper.capitalize('FOO BAR'))


if __name__ == '__main__':
    unittest.main()
