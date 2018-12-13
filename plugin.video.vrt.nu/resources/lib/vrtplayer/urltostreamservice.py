import requests
import urlparse
import os
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from resources.lib.helperobjects import helperobjects
from resources.lib.vrtplayer import streamservice

class UrlToStreamService(streamservice.StreamService):

    def __init__(self, vrt_base, vrtnu_base_url, kodi_wrapper):
        super(UrlToStreamService, self).__init__(kodi_wrapper)
        self._vrt_base = vrt_base
        self._vrtnu_base_url = vrtnu_base_url
        self._STREAM_URL_PATH = super(UrlToStreamService, self)._BASE_MEDIA_SERVICE_URL + '/videos/{}%24{}?vrtPlayerToken={}'

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
            token = super(UrlToStreamService, self)._get_token_from_()
        else:
            token = super(UrlToStreamService, self)._get_sessiontoken_from_()
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
