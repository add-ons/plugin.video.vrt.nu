# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""This module collects and prepares stream info for Kodi Player."""

from __future__ import absolute_import, division, unicode_literals

try:  # Python 3
    from urllib.error import HTTPError
    from urllib.parse import quote
except ImportError:  # Python 2
    from urllib2 import quote, HTTPError

from helperobjects import ApiData, StreamURLS
from kodiutils import (addon_profile, can_play_drm, container_reload, exists, end_of_directory, generate_expiration_date, get_cache,
                       get_max_bandwidth, get_setting_bool, get_url_json, has_inputstream_adaptive, invalidate_caches, kodi_version_major,
                       localize, log, log_error, mkdir, ok_dialog, open_settings, open_url, supports_drm, to_unicode, update_cache)


class StreamService:
    """Collect and prepare stream info for Kodi Player"""

    _VUALTO_API_URL = 'https://media-services-public.vrt.be/media-aggregator/v2'
    _CLIENT = 'vrtnu-web@PROD'
    _VUALTO_LICENSE_URL = 'https://widevine-proxy.drm.technology/proxy'
    _UPLYNK_LICENSE_URL = 'https://content.uplynk.com/wv'
    _INVALID_LOCATION = 'INVALID_LOCATION'
    _INCOMPLETE_ROAMING_CONFIG = 'INCOMPLETE_ROAMING_CONFIG'
    _BELGIUM_ONLY = ('CONTENT_AVAILABLE_ONLY_IN_BE', 'CONTENT_AVAILABLE_ONLY_FOR_BE_RESIDENTS')
    _GEOBLOCK_ERROR_CODES = (_INCOMPLETE_ROAMING_CONFIG, _INVALID_LOCATION) + _BELGIUM_ONLY

    def __init__(self, _tokenresolver):
        """Initialize Stream Service class"""
        self._tokenresolver = _tokenresolver
        self._create_settings_dir()
        self._can_play_drm = can_play_drm()

    @staticmethod
    def _create_settings_dir():
        """Create settings directory"""
        settingsdir = addon_profile()
        if not exists(settingsdir):
            mkdir(settingsdir)

    def _get_api_data(self, video):
        """Create api data object from video dictionary"""
        api_data = None
        video_url = video.get('video_url')
        video_id = video.get('video_id')
        publication_id = video.get('publication_id')
        # Prepare api_data for on demand streams by video_id and publication_id
        if video_id and publication_id:
            api_data = ApiData(self._CLIENT, self._VUALTO_API_URL, video_id, publication_id + quote('$'), False)
        # Prepare api_data for livestreams by video_id, e.g. vualto_strubru, vualto_mnm, ketnet_jr
        elif video_id and not video_url:
            api_data = ApiData(self._CLIENT, self._VUALTO_API_URL, video_id, '', True)
        elif video_url:
            from api import get_stream_id_data
            data_json = get_stream_id_data(video_url)
            episode_data = data_json.get('data').get('page')
            stream_id = ''
            is_live_stream = False
            if episode_data and episode_data.get('episode'):
                stream_id = episode_data.get('episode').get('watchAction').get('streamId')
            elif episode_data and episode_data.get('player'):
                stream_id = episode_data.get('player').get('watchAction').get('streamId')
                is_live_stream = True
            api_data = ApiData(self._CLIENT, self._VUALTO_API_URL, stream_id, '', is_live_stream)
        return api_data

    def _get_stream_json(self, api_data, roaming=False):
        """Get JSON with stream details from VRT API"""
        if not api_data:
            return None

        # Try cache for livestreams
        if api_data.is_live_stream and not roaming:
            filename = api_data.video_id + '.json'
            data = get_cache(filename)
            if data:
                return data

        if api_data.is_live_stream:
            playertoken = self._tokenresolver.get_token('vrtPlayerToken', 'live', roaming=roaming)
        else:
            playertoken = self._tokenresolver.get_token('vrtPlayerToken', 'ondemand', roaming=roaming)

        # Construct api_url and get video json
        if not playertoken:
            return None
        api_url = api_data.media_api_url + '/media-items/' + api_data.publication_id + \
            api_data.video_id + '?vrtPlayerToken=' + playertoken + '&client=' + api_data.client

        stream_json = get_url_json(url=api_url)

        # Update livestream cache if we have a livestream
        if stream_json and api_data.is_live_stream:
            from json import dumps
            # Warning: Currently, the drmExpired key in the stream_json cannot be used because it provides a wrong 6 hour ttl for the VUDRM tokens.
            # After investigation these tokens seem to have an expiration time of only two hours, so we set the expirationDate value accordingly.
            stream_json.update(expirationDate=generate_expiration_date(hours=2))
            cache_file = api_data.video_id + '.json'
            update_cache(cache_file, dumps(stream_json))
        return stream_json

    @staticmethod
    def _fix_virtualsubclip(manifest_url, duration):
        """VRT MAX already offers some programs (mostly current affairs programs) as video on demand from the moment the live broadcast has started.
           To do so, VRT MAX adds start (and stop) timestamps to the livestream url to indicate the beginning (and the end) of a program.
           So Unified Origin streaming platform knows it should return a time bounded manifest file, this is called a Live-to-VOD stream or virtual subclip:
           https://docs.unified-streaming.com/documentation/vod/player-urls.html#virtual-subclips
           e.g. https://live-cf-vrt.akamaized.net/groupc/live/8edf3bdf-7db3-41c3-a318-72cb7f82de66/live.isml/.mpd?t=2020-07-20T11:07:00

           Right after a program is completely broadcasted, the stop timestamp is usually missing and should be added to the manifest_url.
        """
        if any(param in manifest_url for param in ('?t=', '&t=')):
            try:  # Python 3
                from urllib.parse import parse_qs, urlsplit
            except ImportError:  # Python 2
                from urlparse import parse_qs, urlsplit
            import re

            # Detect single start timestamp
            begin = parse_qs(urlsplit(manifest_url).query).get('t')[0]
            rgx = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$')
            is_single_start_timestamp = bool(re.match(rgx, begin))
            if begin and is_single_start_timestamp:
                from datetime import datetime, timedelta
                import dateutil.parser
                begin_time = dateutil.parser.parse(begin)
                # Calculate end_time with a safety margin
                end_time = begin_time + duration + timedelta(seconds=10)
                # Add stop timestamp if a program is broadcasted completely
                now = datetime.utcnow()
                if end_time < now:
                    manifest_url += '-' + end_time.strftime('%Y-%m-%dT%H:%M:%S')
        return manifest_url

    def get_stream(self, video, roaming=False, api_data=None):
        """Main streamservice function"""
        if not api_data:
            api_data = self._get_api_data(video)

        stream_json = self._get_stream_json(api_data, roaming)

        if not stream_json:

            # Roaming token failed
            if roaming:
                message = localize(30964)  # Geoblock error: Cannot be played, need Belgian phone number validation
                return self._handle_stream_api_error(message)
            # X-VRT-Token failed
            message = localize(30963)  # You need a VRT MAX account to play this stream.
            return self._handle_stream_api_error(message)

        if 'targetUrls' in stream_json:

            # DRM support for ketnet junior/uplynk streaming service
            uplynk = 'uplynk.com' in stream_json.get('targetUrls')[0].get('url')

            vudrm_token = stream_json.get('drm')
            drm_stream = (vudrm_token or uplynk)

            # Select streaming protocol
            if not drm_stream and has_inputstream_adaptive():
                protocol = 'mpeg_dash'
            elif drm_stream and self._can_play_drm:
                protocol = 'mpeg_dash'
            elif vudrm_token:
                protocol = 'hls_aes'
            else:
                protocol = 'hls'

            # Get stream manifest url
            manifest_url = next((stream.get('url') for stream in stream_json.get('targetUrls') if stream.get('type') == protocol), None)

            # Failed to get compatible manifest url, ask user to toggle "Use Widevine DRM"
            if manifest_url is None:
                available_protocols = [stream.get('type') for stream in stream_json.get('targetUrls')]
                if protocol not in available_protocols:
                    error_json = {'message': '%s is not available for this stream, please try toggling the "Use Widevine DRM" setting' % protocol}
                    message = localize(30989)  # Failed to load a compatible stream
                    return self._handle_stream_api_error(message, error_json)
            else:

                # External virtual subclip, live-to-VOD from past 24 hours archived livestream (airdate feature)
                if video.get('start_date') and video.get('end_date'):
                    if '?' in manifest_url:
                        manifest_parts = manifest_url.split('?')
                        uri = manifest_parts[0]
                        querystring = '&' + manifest_parts[1]
                    else:
                        uri = manifest_url
                        querystring = ''
                    manifest_url = '{}?t={}-{}{}'.format(uri, video.get('start_date'), video.get('end_date'), querystring)

                # Fix virtual subclip
                from datetime import timedelta
                duration = timedelta(milliseconds=stream_json.get('duration', 0))
                manifest_url = self._fix_virtualsubclip(manifest_url, duration)

                # Prepare stream for Kodi player
                if protocol == 'mpeg_dash' and drm_stream:
                    log(2, 'Protocol: mpeg_dash drm')
                    if vudrm_token:
                        stream = StreamURLS(
                            manifest_url,
                            license_url=self._VUALTO_LICENSE_URL,
                            license_headers={'X-VUDRM-TOKEN': vudrm_token},
                            use_inputstream_adaptive=True
                        )
                    else:
                        stream = StreamURLS(
                            manifest_url,
                            license_url=self._UPLYNK_LICENSE_URL,
                            license_headers={},
                            use_inputstream_adaptive=True
                        )
                elif protocol == 'mpeg_dash':
                    log(2, 'Protocol: mpeg_dash')
                    stream = StreamURLS(manifest_url, use_inputstream_adaptive=True)
                else:
                    log(2, 'Protocol: {protocol}', protocol=protocol)
                    # Fix 720p quality for HLS livestreams
                    manifest_url = manifest_url.replace('.m3u8?', '.m3u8?hd&') if '.m3u8?' in manifest_url else manifest_url + '?hd'
                    # Play HLS directly in Kodi Player on Kodi 17
                    if kodi_version_major() < 18 or not has_inputstream_adaptive():
                        stream = self._select_hls_substreams(manifest_url, protocol)
                    else:
                        stream = StreamURLS(manifest_url, use_inputstream_adaptive=True)
                return stream

        # VRT Geoblock: failed to get stream, now try again with roaming enabled
        if stream_json.get('code') in self._GEOBLOCK_ERROR_CODES:
            log_error('VRT Geoblock: {msg}', msg=stream_json)
            if not roaming:
                return self.get_stream(video, roaming=True, api_data=api_data)

            if stream_json.get('code') == self._INVALID_LOCATION:
                message = localize(30965)  # Geoblock error: Blocked on your geographical location based on your IP address
                return self._handle_stream_api_error(message, stream_json)

            if stream_json.get('code') in self._BELGIUM_ONLY:
                message = localize(30973)  # Geoblock error: This program can only be played from EU
                return self._handle_stream_api_error(message, stream_json)

            message = localize(30964)  # Geoblock error: Cannot be played, need Belgian phone number validation
            return self._handle_stream_api_error(message, stream_json)
        if stream_json.get('code') == 'VIDEO_NOT_FOUND':
            # Refresh listing
            invalidate_caches('*.json')
            container_reload()
            message = localize(30987)  # No stream found
            return self._handle_stream_api_error(message, stream_json)
        if stream_json.get('code') == 'ERROR_AGE_RESTRICTED':
            message = localize(30990)  # Cannot be played, VRT MAX account not allowed to access 12+ content
            return self._handle_stream_api_error(message, stream_json)

        # Failed to get stream, handle error
        message = localize(30954)  # Whoops something went wrong
        return self._handle_stream_api_error(message, stream_json)

    @staticmethod
    def _handle_stream_api_error(message, video_json=None):
        """Show localized stream api error messages in Kodi GUI"""
        if video_json:
            log_error(video_json)
        ok_dialog(message=message)
        end_of_directory()

    @staticmethod
    def _handle_bad_stream_error(protocol, code=None, reason=None):
        """Show a localized error message in Kodi GUI for a failing VRT MAX stream based on protocol: hls, hls_aes, mpeg_dash)
            message: VRT MAX stream <stream_type> problem, try again with (InputStream Adaptive) (and) (DRM) enabled/disabled:
                30959=and DRM, 30960=disabled, 30961=enabled
       """
        # HLS AES DRM failed
        if protocol == 'hls_aes' and not supports_drm():
            message = localize(30962, protocol=protocol.upper(), version=kodi_version_major())
        elif protocol == 'hls_aes' and not has_inputstream_adaptive() and not get_setting_bool('usedrm', default=True):
            message = localize(30958, protocol=protocol.upper(), component=localize(30959), state=localize(30961))
        elif protocol == 'hls_aes' and has_inputstream_adaptive():
            message = localize(30958, protocol=protocol.upper(), component='Widevine DRM', state=localize(30961))
        elif protocol == 'hls_aes' and get_setting_bool('usedrm', default=True):
            message = localize(30958, protocol=protocol.upper(), component='InputStream Adaptive', state=localize(30961))
        else:
            message = localize(30958, protocol=protocol.upper(), component='InputStream Adaptive', state=localize(30960))
        heading = 'HTTP Error {code}: {reason}'.format(code=code, reason=reason) if code and reason else None
        log_error('Unable to play stream. {error}', error=heading)
        ok_dialog(heading=heading, message=message)
        end_of_directory()

    def _select_hls_substreams(self, master_hls_url, protocol):
        """Select HLS substreams to speed up Kodi player start, workaround for slower Kodi selection"""
        hls_variant_url = None
        subtitle_url = None
        hls_audio_id = None
        hls_subtitle_id = None
        hls_base_url = master_hls_url.split('.m3u8')[0]
        try:
            response = open_url(master_hls_url, raise_errors=[415])
        except HTTPError as exc:
            self._handle_bad_stream_error(protocol, exc.code, exc.reason)
            return None
        if response is None:
            return None
        hls_playlist = to_unicode(response.read())
        max_bandwidth = get_max_bandwidth()
        stream_bandwidth = None

        # Get hls variant url based on max_bandwidth setting
        import re
        hls_variant_regex = re.compile(r'#EXT-X-STREAM-INF:[\w\-.,=\"]*?BANDWIDTH=(?P<BANDWIDTH>\d+),'
                                       r'[\w\-.,=\"]+\d,(?:AUDIO=\"(?P<AUDIO>[\w\-]+)\",)?(?:SUBTITLES=\"'
                                       r'(?P<SUBTITLES>\w+)\",)?[\w\-.,=\"]+?[\r\n](?P<URI>[\w:\/\-.=?&]+)')
        # reverse sort by bandwidth
        for match in sorted(re.finditer(hls_variant_regex, hls_playlist), key=lambda m: int(m.group('BANDWIDTH')), reverse=True):
            stream_bandwidth = int(match.group('BANDWIDTH')) // 1000
            if max_bandwidth == 0 or stream_bandwidth < max_bandwidth:
                if match.group('URI').startswith('http'):
                    hls_variant_url = match.group('URI')
                else:
                    hls_variant_url = hls_base_url + match.group('URI')
                hls_audio_id = match.group('AUDIO')
                hls_subtitle_id = match.group('SUBTITLES')
                break

        if stream_bandwidth > max_bandwidth and not hls_variant_url:
            message = localize(30957, max=max_bandwidth, min=stream_bandwidth)
            ok_dialog(message=message)
            open_settings()
            return self._select_hls_substreams(master_hls_url, protocol)

        # Get audio url
        if hls_audio_id:
            audio_regex = re.compile(r'#EXT-X-MEDIA:TYPE=AUDIO[\w\-=,\.\"\/]+?GROUP-ID=\"' + hls_audio_id + ''
                                     r'\"[\w\-=,\.\"\/]+?URI=\"(?P<AUDIO_URI>[\w\-=]+)\.m3u8\"')
            match_audio = re.search(audio_regex, hls_playlist)
            if match_audio:
                hls_variant_url = hls_base_url + match_audio.group('AUDIO_URI') + '-' + hls_variant_url.split('-')[-1]

        # Get subtitle url, works only for on demand streams
        if get_setting_bool('showsubtitles', default=True) and '/live/' not in master_hls_url and hls_subtitle_id:
            subtitle_regex = re.compile(r'#EXT-X-MEDIA:TYPE=SUBTITLES[\w\-=,\.\"\/]+?GROUP-ID=\"' + hls_subtitle_id + ''
                                        r'\"[\w\-= ,;\.\"\/]+URI=\"(?P<SUBTITLE_URI>[\w\-=]+)\.m3u8\"')
            match_subtitle = re.search(subtitle_regex, hls_playlist)
            if match_subtitle:
                subtitle_url = hls_base_url + match_subtitle.group('SUBTITLE_URI') + '.webvtt'

        return StreamURLS(hls_variant_url, subtitle_url)
