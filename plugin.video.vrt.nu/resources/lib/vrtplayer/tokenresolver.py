from resources.lib.helperobjects import helperobjects
import requests
import json
import datetime
import time

class TokenResolver:

    _API_KEY = '3_qhEcPa5JGFROVwu5SWKqJ4mVOIkwlFNMSKwzPDAh8QZOtHqu6L4nD5Q7lk0eXOOG'
    _LOGIN_URL = 'https://accounts.vrt.be/accounts.login'
    _TOKEN_GATEWAY_URL = 'https://token.vrt.be'

    def __init__(self, kodi_wrapper):
        self._kodi_wrapper = kodi_wrapper

    def get_playertoken(self, token_url, xvrttoken):
        tokenfile = self._kodi_wrapper.get_userdata_path() + 'ondemand_vrtPlayerToken'
        token = None
        if self._kodi_wrapper.check_if_path_exists(tokenfile):
            token = self._get_cached_token(tokenfile, token_url, xvrttoken)

        if token == None:
            cookie_value = 'X-VRT-Token=' + xvrttoken
            headers = {'Content-Type': 'application/json', 'Cookie' : cookie_value}
            token = self._get_new_playertoken(tokenfile, token_url, headers)
        return token

    def get_live_playertoken(self, token_url):
        tokenfile = self._kodi_wrapper.get_userdata_path() + 'live_vrtPlayerToken'
        token = None
        if self._kodi_wrapper.check_if_path_exists(tokenfile):
            token = self._get_cached_token(tokenfile, token_url, xvrttoken)
         
        if token == None:
            headers = {'Content-Type': 'application/json'}
            token = self._get_new_playertoken(tokenfile, token_url, headers)
        return token

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
            

    def get_xvrttoken(self, tokenfile=None):
        tokenfile = self._kodi_wrapper.get_userdata_path() + (tokenfile or 'XVRTToken')
        if self._kodi_wrapper.check_if_path_exists(tokenfile):
            xvrttoken = self._get_cached_token(tokenfile)
            return xvrttoken
        else:
            return self._get_new_xvrttoken(tokenfile)

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
