import requests
import urlparse
import datetime
import time
import _strptime
import os
import json
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from resources.lib.helperobjects import helperobjects

class UrlToStreamService:

    _BASE_MEDIA_SERVICE_URL = 'https://media-services-public.vrt.be/vualto-video-aggregator-web/rest/external/v1'
    _TOKEN_URL = _BASE_MEDIA_SERVICE_URL + '/tokens'
    _API_KEY = '3_qhEcPa5JGFROVwu5SWKqJ4mVOIkwlFNMSKwzPDAh8QZOtHqu6L4nD5Q7lk0eXOOG'

    def __init__(self, vrt_base, vrtnu_base_url, kodi_wrapper):
        self._kodi_wrapper = kodi_wrapper
        self._settingsdir()
        self._vrt_base = vrt_base
        self._vrtnu_base_url = vrtnu_base_url
        self._STREAM_URL_PATH = self._BASE_MEDIA_SERVICE_URL + '/videos/{}%24{}?vrtPlayerToken={}'

    def _settingsdir(self):
        settingsdir = self._kodi_wrapper.get_userdata_path()
        if not os.path.exists(settingsdir):
            os.makedirs(settingsdir)

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
            os.remove(path)
            if 'XVRTToken' in path:
                return self._get_xvrttoken()
            else:
                return self._get_playertoken(xvrttoken)

    def _get_playertoken(self, xvrttoken=None):
        #on demand cache
        tokenfile = self._kodi_wrapper.get_userdata_path() + 'ondemand_vrtPlayerToken'
        if os.path.isfile(tokenfile):
            playertoken = self._get_cached_token(tokenfile, xvrttoken)
            return playertoken
        #live cache
        elif xvrttoken is None:
            tokenfile = self._kodi_wrapper.get_userdata_path() + 'live_vrtPlayerToken'
            if os.path.isfile(tokenfile):
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
        if os.path.isfile(tokenfile):
            xvrttoken = self._get_cached_token(tokenfile)
            return xvrttoken
        else:
            return self._get_new_xvrttoken(tokenfile)

    def get_license_key(self, keyUrl, keyType='R', keyHeaders=None, keyValue=None):
            """ Generates a propery license key value

            # A{SSM} -> not implemented
            # R{SSM} -> raw format
            # B{SSM} -> base64 format
            # D{SSM} -> decimal format

            The generic format for a LicenseKey is:
            |<url>|<headers>|<key with placeholders|

            The Widevine Decryption Key Identifier (KID) can be inserted via the placeholder {KID}

            @type keyUrl: str
            @param keyUrl: the URL where the license key can be obtained

            @type keyType: str
            @param keyType: the key type (A, R, B or D)

            @type keyHeaders: dict
            @param keyHeaders: A dictionary that contains the HTTP headers to pass

            @type keyValue: str
            @param keyValue: i
            @return:
            """

            header = ''
            if keyHeaders:
                for k, v in list(keyHeaders.items()):
                    header = '{0}&{1}={2}'.format(header, k, requests.utils.quote(v))

            if keyType in ('A', 'R', 'B'):
                keyValue = '{0}{{SSM}}'.format(keyType)
            elif keyType == 'D':
                if 'D{SSM}' not in keyValue:
                    raise ValueError('Missing D{SSM} placeholder')
                keyValue = requests.utils.quote(keyValue)

            return '{0}|{1}|{2}|'.format(keyUrl, header.strip('&'), keyValue)

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
            url = host + '/videos/' + pubId + videoId + '?vrtPlayerToken=' + token + '&client=' + clientId;
            videojson = requests.get(url).json() 
            try: 
                target_urls = videojson['targetUrls']
            except:
                self._kodi_wrapper.log(str(videojson))
            stream_dict = {}
            for stream in target_urls:
                stream_dict[stream['type']] = stream['url']
            vudrm_token = videojson['drm']
            if self._kodi_wrapper.get_setting('usedrm') == 'true' and vudrm_token is not None:
                license_url = requests.get('https://api.vuplay.co.uk').json()['drm_providers']['widevine']['la_url']
                encryption_json = '{{"token":"{0}","drm_info":[D{{SSM}}],"kid":"{{KID}}"}}'.format(vudrm_token)
                license_key = self.get_license_key(keyUrl=license_url, keyType='D', keyValue=encryption_json, keyHeaders={'Content-Type': 'text/plain;charset=UTF-8'})
                return stream_dict['mpeg_dash'], license_key
            elif vudrm_token is not None:
                return (stream_dict['hls_aes'], None)
            else:
                return (stream_dict['mpeg_dash'], None)
        else:
            return (None, None)

    @staticmethod
    def __get_hls(dictionary):
        hls_url = None
        hls_aes_url = None
        for item in dictionary:
            if item['type'] == 'hls_aes':
                hls_aes_url = item['url']
                break
            if item['type'] == 'hls':
                hls_url = item['url']
        return (hls_aes_url or hls_url).replace('remix.aka', 'remix-aka')

    @staticmethod
    def __get_subtitle(dictionary):
        for item in dictionary:
            if item['type'] == 'CLOSED':
                return item['url']

    @staticmethod
    def __cut_slash_if_present(url):
        if url.endswith('/'):
            return url[:-1]
        else:
            return url
