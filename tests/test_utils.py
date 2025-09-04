# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Tests for StaticHelper functionality"""

import unittest
import utils


class TestUtils(unittest.TestCase):
    """TestCase class"""

    def test_capitalize(self):
        """Test capitalizing string"""
        self.assertEqual('Foo bar', utils.capitalize('foo bar'))
        self.assertEqual('Foo bar', utils.capitalize('Foo bar'))
        self.assertEqual('FoO bAr', utils.capitalize('foO bAr'))
        self.assertEqual('FOO BAR', utils.capitalize('FOO BAR'))

    def test_strip_newlines(self):
        """Test strip_newlines"""
        self.assertEqual('foo bar', utils.strip_newlines(' \n\n  foo bar \n \n '))
        self.assertEqual('foo bar  baz', utils.strip_newlines(' \n\n  foo bar\n  baz \n \n '))

    # FIXME: Add more examples related to <p>, <br> and &nbsp; later
    def test_html_to_kodi(self):
        """Test html_to_kodi"""
        self.assertEqual('foo [I]bar[/I] baz', utils.html_to_kodi('foo <i>bar</i> baz'))
        self.assertEqual('foo [B]bar[/B] baz', utils.html_to_kodi('foo <b>bar</b> baz'))
        self.assertEqual('foo [B][COLOR={highlighted}]bar[/COLOR][/B] baz', utils.html_to_kodi('foo <em>bar</em> baz'))
        self.assertEqual('blah\n- foo\n- bar\n\nbaz', utils.html_to_kodi('blah<ul><li>foo</li><li>bar</li></ul>baz'))

    def test_reformat_url(self):
        """Test reformatting URLs (terzake)"""
        short_url = '/vrtmax/a-z/terzake/2019/terzake-d20191017/'
        medium_url = '//www.vrt.be/vrtmax/a-z/terzake/2019/terzake-d20191017/'
        long_url = 'https://www.vrt.be/vrtmax/a-z/terzake/2019/terzake-d20191017/'

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

    def test_url_to_program(self):
        """Test converting URL to program (buck)"""
        program = 'buck'
        short_url = '/vrtnu/a-z/buck/1/buck-s1a32/'
        short_max_url = '/vrtmax/a-z/buck/1/buck-s1a32/'
        medium_url = '//www.vrt.be/vrtnu/a-z/buck/1/buck-s1a32/'
        long_url = 'https://www.vrt.be/vrtnu/a-z/buck/1/buck-s1a32/'
        short_relevant_url = '/vrtnu/a-z/buck.relevant/'
        short_max_relevant_url = '/vrtmax/a-z/buck.relevant/'

        self.assertEqual(program, utils.url_to_program(long_url))
        self.assertEqual(program, utils.url_to_program(medium_url))
        self.assertEqual(program, utils.url_to_program(short_url))
        self.assertEqual(program, utils.url_to_program(short_max_url))
        self.assertEqual(program, utils.url_to_program(short_relevant_url))
        self.assertEqual(program, utils.url_to_program(short_max_relevant_url))

    def test_url_to_episode(self):
        """Test converting URL to episode (buck)"""
        long_url = 'https://www.vrt.be/vrtnu/a-z/buck/1/buck-s1a32/'
        episode = '/vrtnu/a-z/buck/1/buck-s1a32/'
        self.assertEqual(episode, utils.url_to_episode(long_url))

        medium_url = '//www.vrt.be/vrtnu/a-z/buck/1/buck-s1a32/'
        episode = '/vrtnu/a-z/buck/1/buck-s1a32/'
        self.assertEqual(episode, utils.url_to_episode(medium_url))

        short_url = '/vrtnu/a-z/buck/1/buck-s1a32/'
        self.assertEqual(short_url, utils.url_to_episode(short_url))

        short_url = '/vrtmax/a-z/buck/1/buck-s1a32/'
        self.assertEqual(short_url, utils.url_to_episode(short_url))

        self.assertEqual(None, utils.url_to_episode('foobar'))

    def test_video_to_api_url(self):
        """Test convert video to api URL (de-ideale-wereld)"""
        video = 'https://www.vrt.be/vrtnu/a-z/winteruur/1/winteruur-s1a61/'
        api_url = '//www.vrt.be/vrtnu/a-z/winteruur/1/winteruur-s1a61/'
        self.assertEqual(api_url, utils.video_to_api_url(video))

        video = 'https://www.vrt.be/vrtnu/a-z/winteruur/1/winteruur-s1a61'
        api_url = '//www.vrt.be/vrtnu/a-z/winteruur/1/winteruur-s1a61/'
        self.assertEqual(api_url, utils.video_to_api_url(video))

    def test_play_url_to_id(self):
        """Test converting play_url to play_id"""
        url = 'plugin://plugin.video.vrt.nu/play/id/vid-5b12c0f6-b8fe-426f-a600-557f501f3be9/pbs-pub-7e2764cf-a8c0-4e78-9cbc-46d39381c237'
        play_id = {'video_id': 'vid-5b12c0f6-b8fe-426f-a600-557f501f3be9'}
        self.assertEqual(play_id, utils.play_url_to_id(url))

        url = 'plugin://plugin.video.vrt.nu/play/upnext/vid-271d7238-b7f2-4a3c-b3c7-17a5110be71a'
        play_id = {'video_id': 'vid-271d7238-b7f2-4a3c-b3c7-17a5110be71a'}
        self.assertEqual(play_id, utils.play_url_to_id(url))

        url = 'plugin://plugin.video.vrt.nu/play/url/https://www.vrt.be/vrtmax/kanalen/canvas/'
        play_id = {'video_url': '//www.vrt.be/vrtmax/kanalen/canvas/'}
        self.assertEqual(play_id, utils.play_url_to_id(url))

    def test_shorten_link(self):
        """Test shortening links"""
        permalink = 'vrtmax.be/p.LR90GkqOD'
        medium_url = '//www.vrt.be/vrtmax/p.LR90GkqOD'
        long_url = 'https://www.vrt.be/vrtmax/p.LR90GkqOD'

        self.assertEqual(permalink, utils.shorten_link(long_url))
        self.assertEqual(permalink, utils.shorten_link(medium_url))
        self.assertEqual(None, utils.shorten_link(None))

    def test_add_https_proto(self):
        """Test add_https_proto"""
        self.assertEqual('https://www.vrt.be/foo.bar.baz', utils.add_https_proto('/foo.bar.baz'))
        self.assertEqual('https://foo.bar.baz', utils.add_https_proto('//foo.bar.baz'))
        self.assertEqual('https://foo.bar.baz', utils.add_https_proto('https://foo.bar.baz'))
        self.assertEqual('foo.bar.baz', utils.add_https_proto('foo.bar.baz'))

    def test_realpage(self):
        """Test converting input to page"""
        self.assertEqual(1, utils.realpage('foo'))
        self.assertEqual(1, utils.realpage('-1'))
        self.assertEqual(1, utils.realpage('0'))
        self.assertEqual(2, utils.realpage(2))
        self.assertEqual(3, utils.realpage('3'))

    def test_find_entry(self):
        """Test find_entry"""
        haystack = [
            {'foo': 'foo', 'bar': 'bar', 'baz': 'baz'},
            {'foo': 'bar', 'bar': 'baz', 'baz': 'foo'},
            {'foo': 'baz', 'bar': 'foo', 'baz': 'bar'},
        ]

        needle = utils.find_entry(haystack, 'foo', 'baz')
        self.assertEqual(needle, {'foo': 'baz', 'bar': 'foo', 'baz': 'bar'})

        needle = utils.find_entry(haystack, 'bar', 'baz', None)
        self.assertEqual(needle, {'foo': 'bar', 'bar': 'baz', 'baz': 'foo'})

        needle = utils.find_entry(haystack, 'foo', 'blah', None)
        self.assertEqual(needle, None)

        needle = utils.find_entry(haystack, 'foo', 'blah', {'foo': 'f', 'bar': 'r', 'baz': 'z'})
        self.assertEqual(needle, {'foo': 'f', 'bar': 'r', 'baz': 'z'})

    def test_youtube_to_plugin_url(self):
        """youtube_to_plugin_url"""
        self.assertEqual('plugin://plugin.video.youtube/foo/bar/', utils.youtube_to_plugin_url('https://www.youtube.com/foo/bar'))
        self.assertEqual('plugin://plugin.video.youtube/foo/bar/baz/', utils.youtube_to_plugin_url('https://www.youtube.com/foo/bar/baz/'))


if __name__ == '__main__':
    unittest.main()
