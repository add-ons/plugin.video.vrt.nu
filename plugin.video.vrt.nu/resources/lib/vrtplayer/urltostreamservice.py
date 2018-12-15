import requests
import urlparse
import datetime
import time
import _strptime
import json
import re
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from resources.lib.helperobjects import helperobjects

class UrlToStreamService:

    _BASE_MEDIA_SERVICE_URL = 'https://media-services-public.vrt.be/vualto-video-aggregator-web/rest/external/v1'
    _TOKEN_URL = _BASE_MEDIA_SERVICE_URL + '/tokens'
    _API_KEY = '3_qhEcPa5JGFROVwu5SWKqJ4mVOIkwlFNMSKwzPDAh8QZOtHqu6L4nD5Q7lk0eXOOG'
    _VUALTO_API_URL = 'https://api.vuplay.co.uk'

    def __init__(self, vrt_base, vrtnu_base_url, kodi_wrapper):
        self._kodi_wrapper = kodi_wrapper
        self._vrt_base = vrt_base
        self._vrtnu_base_url = vrtnu_base_url
        self._settingsdir()
        self._has_drm = self._check_drm()
        self._license_url = self._get_license_url()

    def _check_drm(self):
        return self._kodi_wrapper.check_inputstream_adaptive() and self._kodi_wrapper.check_widevine()

    def _get_license_url(self):
        return requests.get(self._VUALTO_API_URL).json()['drm_providers']['widevine']['la_url']

    def _settingsdir(self):
        settingsdir = self._kodi_wrapper.get_userdata_path()
        if not self._kodi_wrapper.check_path(settingsdir):
            self._kodi_wrapper.make_dir(settingsdir)
 
    def _get_token_from_(self):
        token = self._get_playertoken()
        return token

    def _get_sessiontoken_from_(self):
        xvrttoken = self._get_xvrttoken()
        if xvrttoken is not None:
            token = self._get_playertoken(xvrttoken)
        else:
            token = None
        return token

    def _get_new_playertoken(self, path, headers):
        playertoken = requests.post(self._TOKEN_URL, headers=headers).json()
        json.dump(playertoken, open(path,'w'))
        return playertoken['vrtPlayerToken']

    def _get_cached_token(self, path, xvrttoken=None):
        token = json.loads(open(path, 'r').read())
        now = datetime.datetime.utcnow()
        exp = datetime.datetime(*(time.strptime(token['expirationDate'], '%Y-%m-%dT%H:%M:%S.%fZ')[0:6]))
        if exp > now:
            return token[token.keys()[0]]
        else:
            self._kodi_wrapper.delete_path(path)
            if 'XVRTToken' in path:
                return self._get_xvrttoken()
            else:
                return self._get_playertoken(xvrttoken)

    def _get_playertoken(self, xvrttoken=None):
        #on demand cache
        tokenfile = self._kodi_wrapper.get_userdata_path() + 'ondemand_vrtPlayerToken'
        if self._kodi_wrapper.check_path(tokenfile):
            playertoken = self._get_cached_token(tokenfile, xvrttoken)
            return playertoken
        #live cache
        elif xvrttoken is None:
            tokenfile = self._kodi_wrapper.get_userdata_path() + 'live_vrtPlayerToken'
            if self._kodi_wrapper.check_path(tokenfile):
                playertoken = self._get_cached_token(tokenfile, xvrttoken)
                return playertoken
            #renew live 
            else:
                headers = {'Content-Type': 'application/json'}
                return self._get_new_playertoken(tokenfile, headers)
        #renew on demand
        else:
            cookiestring = 'X-VRT-Token=%s' % xvrttoken
            headers = {'Content-Type': 'application/json', 'Cookie' : cookiestring}
            return self._get_new_playertoken(tokenfile, headers)

    def _get_new_xvrttoken(self, path):
        cred = helperobjects.Credentials(self._kodi_wrapper)
        if not cred.are_filled_in():
            self._kodi_wrapper.open_settings()
            cred.reload()
        url = 'https://accounts.vrt.be/accounts.login'
        data = {'loginID' : cred.username, 'password' : cred.password, 'APIKey' : self._API_KEY, 'targetEnv' : 'jssdk'}
        r = requests.post(url, data)
        logon_json = r.json()
        if logon_json['errorCode'] == 0:
            uid = logon_json['UID']
            sig = logon_json['UIDSignature']
            ts = logon_json['signatureTimestamp']
            logintoken = logon_json['sessionInfo']['login_token']
            cookiestring = 'glt_%s=%s' % (self._API_KEY, logintoken)
            url = 'https://token.vrt.be/'
            data = '{"uid": "%s", "uidsig": "%s", "ts": "%s", "email": "%s"}' % (uid, sig, ts, cred.username)
            headers = {'Content-Type': 'application/json', 'Cookie' : cookiestring}
            r = requests.post(url, headers=headers, data=data)
            for cookie in r.cookies:
                if cookie.name == 'X-VRT-Token':
                    xvrttoken = { cookie.name : cookie.value, 'expirationDate' : datetime.datetime.fromtimestamp(cookie.expires).strftime('%Y-%m-%dT%H:%M:%S.%fZ')}
                    json.dump(xvrttoken, open(path,'w'))
                return xvrttoken['X-VRT-Token']
        else:
            title = self._kodi_wrapper.get_localized_string(32051)
            message = self._kodi_wrapper.get_localized_string(32052)
            self._kodi_wrapper.show_ok_dialog(title, message)

    def _get_xvrttoken(self):
        tokenfile = self._kodi_wrapper.get_userdata_path() + 'XVRTToken'
        if self._kodi_wrapper.check_path(tokenfile):
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
                    header = '{0}&{1}={2}'.format(header, k, requests.utils.quote(v))

            if key_type in ('A', 'R', 'B'):
                key_value = '{0}{{SSM}}'.format(key_type)
            elif key_type == 'D':
                if 'D{SSM}' not in key_value:
                    raise ValueError('Missing D{SSM} placeholder')
                key_value = requests.utils.quote(key_value)

            return '{0}|{1}|{2}|'.format(key_url, header.strip('&'), key_value)

    def get_stream_from_url(self, url):
        if 'vrtnu/kanalen' in url:
            token = self._get_token_from_()
        else:
            token = self._get_sessiontoken_from_()
        if token is not None:
            url = urlparse.urljoin(self._vrt_base, url)
            htmlpage = requests.get(url).text
            strainer = SoupStrainer('div', {'class': 'cq-dd-vrtvideo'})
            soup = BeautifulSoup(htmlpage, 'html.parser', parse_only=strainer)
            vrt_video = soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['vrtvideo'])
            video_data = {}
            for attr in vrt_video.attrs:
                if attr.startswith('data-'):
                    video_data[attr.split('data-')[1]] = vrt_video.attrs[attr]
            clientId = video_data['client']
            host = video_data['mediaapiurl']
            if 'videoid' in video_data.keys():
                videoId = video_data['videoid']
            else:
                videoId = video_data['livestream']
            if 'publicationid' in video_data.keys():
                pubId = video_data['publicationid'] + requests.utils.quote('$')
            else:
                pubId = ''
            url = host + '/videos/' + pubId + videoId + '?vrtPlayerToken=' + token + '&client=' + clientId
            videojson = requests.get(url).json() 
            try: 
                target_urls = videojson['targetUrls']
            except:
                self._kodi_wrapper.log(str(videojson))
            stream_dict = {}
            for stream in target_urls:
                stream_dict[stream['type']] = stream['url']
            vudrm_token = videojson['drm']
            return self._select_stream(stream_dict, vudrm_token)
        else:
            return None

    def _select_stream(self, stream_dict, vudrm_token):
        if self._has_drm and self._kodi_wrapper.get_setting('usedrm') == 'true' and vudrm_token is not None:
            encryption_json = '{{"token":"{0}","drm_info":[D{{SSM}}],"kid":"{{KID}}"}}'.format(vudrm_token)
            license_key = self._get_license_key(key_url=self._license_url, key_type='D', key_value=encryption_json, key_headers={'Content-Type': 'text/plain;charset=UTF-8'})
            return helperobjects.StreamURLS(stream_dict['mpeg_dash'], license_key=license_key)

        elif vudrm_token is not None:
            if self._kodi_wrapper.get_setting('showsubtitles') == 'true':
                subtitle_url = self._get_subtitle(stream_dict['hls_aes'])
            else:
                subtitle_url = None
            return helperobjects.StreamURLS(stream_dict['hls_aes'], subtitle_url=subtitle_url)

        else:
            if self._kodi_wrapper.check_inputstream_adaptive():
                return helperobjects.StreamURLS(stream_dict['mpeg_dash'])
            else:
                if self._kodi_wrapper.get_setting('showsubtitles') == 'true':
                    subtitle_url = self._get_subtitle(stream_dict['hls'])
                else:
                    subtitle_url = None
                return helperobjects.StreamURLS(stream_dict['hls'], subtitle_url=subtitle_url)

    def _get_subtitle(self, stream_url):
        r = requests.get(stream_url)
        subtitle_regex = re.compile(r'#EXT-X-MEDIA:TYPE=SUBTITLES,[a-zA-Z-,/\"=]+,URI=\"([a-zA-Z0-9-_=]+)\.m3u8\"')
        match = re.search(subtitle_regex, r.text)
        if match is not None and '/live/' not in stream_url:
            subtitle_url = match.group(1) + '.webvtt'
            return stream_url.split('.m3u8')[0] + subtitle_url
        else:
            return None
