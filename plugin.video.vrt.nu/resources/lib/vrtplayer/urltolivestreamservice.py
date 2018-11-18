import requests
from resources.lib.helperobjects import helperobjects
from resources.lib.vrtplayer import streamservice

class UrlToLivestreamService(streamservice.StreamService):

    def __init__(self, kodi_wrapper):
        super(UrlToLivestreamService, self).__init__(kodi_wrapper)

    _TOKEN_URL = "https://media-services-public.vrt.be/vualto-video-aggregator-web/rest/external/v1/tokens"

    def get_license_key(self, keyUrl, keyType="R", keyHeaders=None, keyValue=None):
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

            header = ""
            if keyHeaders:
                for k, v in list(keyHeaders.items()):
                    header = "{0}&{1}={2}".format(header, k, requests.utils.quote(v))

            if keyType in ("A", "R", "B"):
                keyValue = "{0}{{SSM}}".format(keyType)
            elif keyType == "D":
                if "D{SSM}" not in keyValue:
                    raise ValueError("Missing D{SSM} placeholder")
                keyValue = requests.utils.quote(keyValue)

            return "{0}|{1}|{2}|".format(keyUrl, header.strip("&"), keyValue)

    def get_stream_from_url(self, url):
        (token) = super(UrlToLivestreamService, self)._get_token_from_()

        stream_response = requests.get(url, {'vrtPlayerToken': token, 'client':'vrtvideo' }).json()
        target_urls = stream_response['targetUrls']
        stream_dict = {}
        for stream in target_urls:
            stream_dict[stream['type']] = stream['url']
        if self._kodi_wrapper.get_setting('usedrm') == 'true':
            vudrm_token = stream_response['drm']
            license_url = requests.get('https://api.vuplay.co.uk').json()['drm_providers']['widevine']['la_url']
            encryption_json = '{{"token":"{0}","drm_info":[D{{SSM}}],"kid":"{{KID}}"}}'.format(vudrm_token)
            license_key = self.get_license_key(keyUrl=license_url, keyType="D", keyValue=encryption_json, keyHeaders={"Content-Type": "text/plain;charset=UTF-8"})
            return stream_dict['mpeg_dash'], license_key
        else:
            return stream_dict['hls_aes'], None
