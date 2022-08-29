# -*- coding: utf-8 -*-
"""Check VRT MAX app"""
from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime, timedelta
import json
import re
import requests


class NewVersionException(Exception):
    """Is thrown when a new VRT MAX app is released."""

    def __init__(self, message):
        self.message = message
        super(NewVersionException, self).__init__(self.message)


def google_play_info():
    """Get info for VRT MAX app from Google Play"""
    app_id = 'be.vrt.vrtnu'
    url = 'https://play.google.com/store/apps/details?id={}'.format(app_id)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'}
    req = requests.get(url, headers=headers)

    if req.status_code != 200:
        raise Exception('HTTP request failed with %s' % req.status_code)

    regex = re.compile(r'<script[\s\S]*?AF_initDataCallback\(([\s\S]*?\));<\/script>')
    match = re.findall(regex, req.text)
    key_regex = re.compile(r'key: \'ds:(.*?)\',')
    value_regex = re.compile(r'data:([\s\S]*?), sideChannel: {}}\)')
    version = None
    changelog = None
    published = None
    for prop in match:
        key = re.search(key_regex, prop)
        value = re.search(value_regex, prop)
        if key and value:
            key = key.group(1)
            info = json.loads(value.group(1))
            if key == '4':
                changelog = info[1][2][144][1][1]
                published = info[1][2][145][0][0]
            elif key == '8':
                version = info[1]

    if version is None or published is None:
        print("HTTP request returned: %s" % req.text)
        print("ERROR: Could not find 'version' or 'published' from %s" % json.dumps(match, indent=2))
        raise Exception("Could not find 'version' or 'published'")

    return dict(version=version, changelog=changelog, published=published)


def run():
    """Check VRT MAX app"""
    import dateutil.tz
    import dateutil.parser
    info = google_play_info()
    published = dateutil.parser.parse(info.get('published') + ' 22:00:00 UTC', tzinfos={'UTC': dateutil.tz.UTC})
    published_string = published.astimezone(dateutil.tz.gettz('Europe/Brussels')).strftime('%A %e %B %Y at %H:%M')
    if published > datetime.now(dateutil.tz.UTC) - timedelta(minutes=90):
        message = 'VRT MAX for Android is updated to version {} released on {}\nChangelog:\n {}'.format(
            info.get('version'), published_string, info.get('changelog'))
        raise NewVersionException(message)
    message = 'Everything quiet here, VRT MAX for Android is still at version {} released on {}'.format(info.get('version'), published_string)
    print(message)


if __name__ == '__main__':
    run()
