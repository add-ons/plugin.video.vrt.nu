from abc import ABCMeta, abstractmethod
import requests
import urllib
import json
import os
import datetime
import time
import _strptime
from resources.lib.helperobjects import helperobjects

class StreamService:
    __metaclass__ = ABCMeta

    _BASE_MEDIA_SERVICE_URL = 'https://media-services-public.vrt.be/vualto-video-aggregator-web/rest/external/v1'
    _TOKEN_URL = _BASE_MEDIA_SERVICE_URL + '/tokens'
    _API_KEY = '3_qhEcPa5JGFROVwu5SWKqJ4mVOIkwlFNMSKwzPDAh8QZOtHqu6L4nD5Q7lk0eXOOG'

    @abstractmethod
    def __init__(self, kodi_wrapper):
        self._kodi_wrapper = kodi_wrapper
        self._settingsdir()

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
