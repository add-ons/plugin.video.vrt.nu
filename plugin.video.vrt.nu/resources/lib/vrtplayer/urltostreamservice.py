# -*- coding: utf-8 -*-
import requests
from urlparse import urljoin
import datetime
import time
import _strptime
import json
import re
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from resources.lib.helperobjects import helperobjects, streamurls, apidata

class UrlToStreamService:

    _API_KEY = '3_qhEcPa5JGFROVwu5SWKqJ4mVOIkwlFNMSKwzPDAh8QZOtHqu6L4nD5Q7lk0eXOOG'
    _VUPLAY_API_URL = 'https://api.vuplay.co.uk'
    _LOGIN_URL = 'https://accounts.vrt.be/accounts.login'
    _TOKEN_GATEWAY_URL = 'https://token.vrt.be'

    def __init__(self, vrt_base, vrtnu_base_url, kodi_wrapper):
        self._kodi_wrapper = kodi_wrapper
        self._vrt_base = vrt_base
        self._vrtnu_base_url = vrtnu_base_url
        self._create_settings_dir()
        self._can_play_drm = self._kodi_wrapper.has_widevine_installed()
        self._license_url = self._get_license_url()

    def _get_license_url(self):
        return requests.get(self._VUPLAY_API_URL).json()['drm_providers']['widevine']['la_url']

    def _create_settings_dir(self):
        settingsdir = self._kodi_wrapper.get_userdata_path()
        if not self._kodi_wrapper.check_if_path_exists(settingsdir):
            self._kodi_wrapper.make_dir(settingsdir)

    def _get_new_playertoken(self, path, token_url, headers):
        playertoken = requests.post(token_url, headers=headers).json()
        json.dump(playertoken, open(path,'w'))
        return playertoken['vrtPlayerToken']

    def _get_cached_token(self, path, token_url=None, xvrttoken=None):
        token = json.loads(open(path, 'r').read())
        now = datetime.datetime.utcnow()
        exp = datetime.datetime(*(time.strptime(token['expirationDate'], '%Y-%m-%dT%H:%M:%S.%fZ')[0:6]))
        if exp > now:
            self._kodi_wrapper.log_notice(path)
            return token[token.keys()[0]]
        else:
            self._kodi_wrapper.delete_path(path)
            if path.split('/')[-1] == 'XVRTToken':
                return self._get_xvrttoken()
            elif path.split('/')[-1] == 'roaming_XVRTToken':
                 return self._get_xvrttoken('roaming_XVRTToken')
            else:
                return self._get_playertoken(token_url, xvrttoken)

    def _get_playertoken(self, token_url, xvrttoken=None):
        #on demand cache
        tokenfile = self._kodi_wrapper.get_userdata_path() + 'ondemand_vrtPlayerToken'
        if self._kodi_wrapper.check_if_path_exists(tokenfile):
            playertoken = self._get_cached_token(tokenfile, token_url, xvrttoken)
            return playertoken
        #live cache
        elif xvrttoken is None:
            tokenfile = self._kodi_wrapper.get_userdata_path() + 'live_vrtPlayerToken'
            if self._kodi_wrapper.check_if_path_exists(tokenfile):
                playertoken = self._get_cached_token(tokenfile, token_url, xvrttoken)
                return playertoken
            #renew live 
            else:
                headers = {'Content-Type': 'application/json'}
                return self._get_new_playertoken(tokenfile, token_url, headers)
        #renew on demand
        else:
            cookie_value = 'X-VRT-Token=' + xvrttoken
            headers = {'Content-Type': 'application/json', 'Cookie' : cookie_value}
            return self._get_new_playertoken(tokenfile, token_url, headers)

    def _get_roaming_xvrttoken(self, login_cookie, xvrttoken):
        url = 'https://token.vrt.be/vrtnuinitloginEU?destination=https://www.vrt.be/vrtnu/'
        cookie_value = 'X-VRT-Token=' + xvrttoken['X-VRT-Token']
        headers = {'Cookie' : cookie_value}
        r = requests.get(url, headers=headers, allow_redirects=False)
        url = r.headers.get('Location')
        r = requests.get(url, headers=headers, allow_redirects=False)
        url = r.headers.get('Location')
        headers = {'Cookie': login_cookie }
        roaming_xvrttoken = None
        if url is not None:
            cookie_jar = requests.get(url, headers=headers).cookies
            if 'X-VRT-Token' in cookie_jar:
                xvrttoken_cookie = cookie_jar._cookies['.vrt.be']['/']['X-VRT-Token']
                roaming_xvrttoken = { xvrttoken_cookie.name : xvrttoken_cookie.value, 'expirationDate' : datetime.datetime.fromtimestamp(xvrttoken_cookie.expires).strftime('%Y-%m-%dT%H:%M:%S.%fZ')}
            return roaming_xvrttoken
        
    def _get_new_xvrttoken(self, path):
        cred = helperobjects.Credentials(self._kodi_wrapper)
        if not cred.are_filled_in():
            self._kodi_wrapper.open_settings()
            cred.reload()
        data = {'loginID': cred.username, 'password': cred.password, 'sessionExpiration': '-1', 'APIKey': self._API_KEY, 'targetEnv': 'jssdk'}
        logon_json = requests.post(self._LOGIN_URL, data).json()
        if logon_json['errorCode'] == 0:
            session = logon_json['sessionInfo']
            login_token = logon_json['sessionInfo']['login_token']
            login_cookie = ''.join(('glt_', self._API_KEY, '=', login_token))
            payload = {'uid': logon_json['UID'], 'uidsig': logon_json['UIDSignature'], 'ts': logon_json['signatureTimestamp'], 'email': cred.username}
            headers = {'Content-Type': 'application/json', 'Cookie': login_cookie}
            cookie_jar = requests.post(self._TOKEN_GATEWAY_URL, headers=headers, json=payload).cookies
            if 'X-VRT-Token' in cookie_jar:
                xvrttoken_cookie = cookie_jar._cookies['.vrt.be']['/']['X-VRT-Token']
                xvrttoken = { xvrttoken_cookie.name : xvrttoken_cookie.value, 'expirationDate' : datetime.datetime.fromtimestamp(xvrttoken_cookie.expires).strftime('%Y-%m-%dT%H:%M:%S.%fZ')}
                if 'roaming_XVRTToken' in path:
                    roaming_xvrttoken = self._get_roaming_xvrttoken(login_cookie, xvrttoken)
                    if roaming_xvrttoken is not None:
                        json.dump(roaming_xvrttoken, open(path,'w'))
                        roaming_xvrttoken = roaming_xvrttoken['X-VRT-Token']
                    return roaming_xvrttoken
                else:
                    json.dump(xvrttoken, open(path,'w'))
                    return xvrttoken['X-VRT-Token']
            else:
                return self._get_new_xvrttoken(path)
        else:
            title = self._kodi_wrapper.get_localized_string(32051)
            message = self._kodi_wrapper.get_localized_string(32052)
            self._kodi_wrapper.show_ok_dialog(title, message)

    def _get_xvrttoken(self, tokenfile=None):
        tokenfile = self._kodi_wrapper.get_userdata_path() + (tokenfile or 'XVRTToken')
        if self._kodi_wrapper.check_if_path_exists(tokenfile):
            xvrttoken = self._get_cached_token(tokenfile)
            return xvrttoken
        else:
            return self._get_new_xvrttoken(tokenfile)

    def _get_license_key(self, key_url, key_type='R', key_headers=None, key_value=None):
            """ Generates a propery license key value

            # A{SSM} -> not implemented
            # R{SSM} -> raw format
            # B{SSM} -> base64 format
            # D{SSM} -> decimal format

            The generic format for a LicenseKey is:
            |<url>|<headers>|<key with placeholders|

            The Widevine Decryption Key Identifier (KID) can be inserted via the placeholder {KID}

            @type key_url: str
            @param key_url: the URL where the license key can be obtained

            @type key_type: str
            @param key_type: the key type (A, R, B or D)

            @type key_headers: dict
            @param key_headers: A dictionary that contains the HTTP headers to pass

            @type key_value: str
            @param key_value: i
            @return:
            """

            header = ''
            if key_headers:
                for k, v in list(key_headers.items()):
                    header = ''.join((header, '&', k, '=', requests.utils.quote(v)))

            if key_type in ('A', 'R', 'B'):
                key_value = ''.join((key_type,'{SSM}'))
            elif key_type == 'D':
                if 'D{SSM}' not in key_value:
                    raise ValueError('Missing D{SSM} placeholder')
                key_value = requests.utils.quote(key_value)

            return ''.join((key_url, '|', header.strip('&'), '|', key_value, '|'))

    def _get_api_data(self, video_url):
        video_url = urljoin(self._vrt_base, video_url)
        html_page = requests.get(video_url).text
        strainer = SoupStrainer('div', {'class': 'cq-dd-vrtvideo'})
        soup = BeautifulSoup(html_page, 'html.parser', parse_only=strainer)
        video_data = soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['vrtvideo']).attrs

        #store required data attributes
        client = video_data['data-client']
        media_api_url = video_data['data-mediaapiurl']
        if 'data-videoid' in video_data.keys():
            video_id = video_data['data-videoid']
            xvrttoken = self._get_xvrttoken()
        else:
            xvrttoken = None
            video_id = video_data['data-livestream']
        publication_id = ''
        if 'data-publicationid' in video_data.keys():
            publication_id = video_data['data-publicationid'] + requests.utils.quote('$')
        return apidata.ApiData(client, media_api_url, video_id, publication_id, xvrttoken)

    def _get_video_json(self, client, media_api_url, video_id, publication_id, xvrttoken):
        token_url = media_api_url + '/tokens'
        playertoken = self._get_playertoken(token_url, xvrttoken)

        #construct api_url and get video json
        api_url = ''.join((media_api_url, '/videos/', publication_id, video_id, '?vrtPlayerToken=', playertoken, '&client=', client))
        video_json = requests.get(api_url).json()
            
        return video_json

    def _handle_error(self, video_json):
        self._kodi_wrapper.log_error(video_json['message'])
        message = self._kodi_wrapper.get_localized_string(32054)
        self._kodi_wrapper.show_ok_dialog('', message)

    def get_stream_from_url(self, video_url, retry = False, api_data = None):
        vudrm_token = None
        api_data = api_data or self._get_api_data(video_url)
        video_json = self._get_video_json(api_data.client, api_data.media_api_url, api_data.video_id, api_data.publication_id, api_data.xvrttoken)

        if 'drm' in video_json:
            vudrm_token = video_json['drm']
            target_urls = video_json['targetUrls']
            stream_dict = dict(list(map(lambda x: (x['type'] , x['url']), target_urls)))
            return self._select_stream(stream_dict, vudrm_token)

        elif video_json['code'] == 'INVALID_LOCATION' or video_json['code'] == 'INCOMPLETE_ROAMING_CONFIG':
            self._kodi_wrapper.log_notice(video_json['message'])
            roaming_xvrttoken = self._get_xvrttoken('roaming_XVRTToken')
            if not retry and roaming_xvrttoken is not None:
                if video_json['code'] == 'INCOMPLETE_ROAMING_CONFIG':
                    #delete cached ondemand_vrtPlayerToken
                    self._kodi_wrapper.delete_path(self._kodi_wrapper.get_userdata_path() + 'ondemand_vrtPlayerToken')
                #update api_data with roaming_xvrttoken
                api_data.xvrttoken = roaming_xvrttoken
                return self.get_stream_from_url(video_url, True, api_data)
            else:
                message = self._kodi_wrapper.get_localized_string(32053)
                self._kodi_wrapper.show_ok_dialog('', message)
        else:
            self._handle_error(video_json)


    def _try_get_drm_stream(self, stream_dict, vudrm_token):
        encryption_json = '{{"token":"{0}","drm_info":[D{{SSM}}],"kid":"{{KID}}"}}'.format(vudrm_token)
        license_key = self._get_license_key(key_url=self._license_url, key_type='D', key_value=encryption_json, key_headers={'Content-Type': 'text/plain;charset=UTF-8'})
        return streamurls.StreamURLS(stream_dict['mpeg_dash'], license_key=license_key)
        
    def _select_stream(self, stream_dict, vudrm_token):
        if vudrm_token and self._can_play_drm and self._kodi_wrapper.get_setting('usedrm') == 'true':
            return self._try_get_drm_stream(stream_dict, vudrm_token)
        elif vudrm_token:
            return streamurls.StreamURLS(*self._select_hls_substreams(stream_dict['hls_aes']))
        else:
            return streamurls.StreamURLS(stream_dict['mpeg_dash']) #non drm stream

    #speed up hls selection, workaround for slower kodi selection
    def _select_hls_substreams(self, master_hls_url):
        base_url = master_hls_url.split('.m3u8')[0]
        m3u8 = requests.get(master_hls_url).text
        stream_regex = re.compile(r'#EXT-X-STREAM-INF:[\w\-=,\.\"]+[\r\n]{1}([\w\-=]+\.m3u8)[\r\n]{2}')
        direct_stream_url = None
        direct_subtitle_url = None
        match_stream = re.search(stream_regex, m3u8)
        if match_stream:
            direct_stream_url = base_url + match_stream.group(1)
        if self._kodi_wrapper.get_setting('showsubtitles') == 'true':
            subtitle_regex = re.compile(r'#EXT-X-MEDIA:TYPE=SUBTITLES[\w\-=,\.\"\/]+URI=\"([\w\-=]+)\.m3u8\"')
            match_sub = re.search(subtitle_regex, m3u8)
            if match_sub and '/live/' not in master_hls_url:
                direct_subtitle_url = ''.join((base_url, match_sub.group(1), '.webvtt'))
        return direct_stream_url, direct_subtitle_url
