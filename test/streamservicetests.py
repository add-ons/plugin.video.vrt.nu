# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=unused-variable

from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime, timedelta
import dateutil.tz
import mock
import unittest
from urllib2 import HTTPError

from resources.lib.vrtplayer import CHANNELS, streamservice, tokenresolver, vrtapihelper
from test import SETTINGS, get_setting, get_localized_string, log_notice

SETTINGS['use_drm'] = 'false'
now = datetime.now(dateutil.tz.tzlocal())
yesterday = now + timedelta(days=-1)


class StreamServiceTests(unittest.TestCase):

    _kodiwrapper = mock.MagicMock()
    _kodiwrapper.check_if_path_exists.return_value = False
    _kodiwrapper.check_inputstream_adaptive.return_value = True
    _kodiwrapper.get_localized_dateshort = mock.MagicMock(return_value='%d-%m-%Y')
    _kodiwrapper.get_localized_string = mock.MagicMock(side_effect=get_localized_string)
    _kodiwrapper.get_proxies = mock.MagicMock(return_value=dict())
    _kodiwrapper.get_setting = mock.MagicMock(side_effect=get_setting)
    _kodiwrapper.get_userdata_path.return_value = './userdata/'
    _kodiwrapper.log_notice = mock.MagicMock(side_effect=log_notice)
    _kodiwrapper.make_dir.return_value = None
    _apihelper = vrtapihelper.VRTApiHelper(_kodiwrapper)
    _tokenresolver = tokenresolver.TokenResolver(_kodiwrapper)
    _streamservice = streamservice.StreamService(_kodiwrapper, _tokenresolver)

    def test_get_ondemand_stream_from_invalid_url(self):
        video = dict(
            video_url='https://www.vrt.be/vrtnu/a-z/het-journaal/2017/het-journaal-het-journaal-laat-20170501/',
            video_id=None,
            publication_id=None,
        )
        try:
            stream = self._streamservice.get_stream(video)
            self.assertEqual(stream.stream_url, video['video_url'])
        except HTTPError:
            pass

    def test_get_ondemand_stream_from_url_gets_stream_does_not_crash(self):
        video = dict(
            # video_url='https://www.vrt.be/vrtnu/a-z/pano/2019/pano-s2019a6/',
            video_url=yesterday.strftime('https://www.vrt.be/vrtnu/a-z/het-journaal/2019/het-journaal-het-journaal-laat-%Y%m%d/'),
            video_id=None,
            publication_id=None,
        )
        stream = self._streamservice.get_stream(video)
        self.assertTrue(stream is not None)

    def test_get_live_stream_from_url_does_not_crash_returns_stream_and_licensekey(self):
        SETTINGS['use_drm'] = 'true'
        video = dict(
            video_url=CHANNELS[1]['live_stream'],
            video_id=None,
            publication_id=None,
        )
        stream = self._streamservice.get_stream(video)
        self.assertTrue(stream is not None)
        self.assertTrue(stream.license_key is not None)

    def test_get_live_stream_from_url_does_not_crash(self):
        video = dict(
            video_url=CHANNELS[1]['live_stream'],
            video_id=None,
            publication_id=None,
        )
        stream = self._streamservice.get_stream(video)
        self.assertTrue(stream is not None)

    def test_get_live_stream_from_id_does_not_crash(self):
        video = dict(
            video_url=None,
            video_id=CHANNELS[1]['live_stream_id'],
            publication_id=None,
        )
        stream = self._streamservice.get_stream(video)
        self.assertTrue(stream is not None)


if __name__ == '__main__':
    unittest.main()
