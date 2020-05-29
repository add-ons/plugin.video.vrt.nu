# -*- coding: utf-8 -*-
"""Check VRT NU app"""
from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime, timedelta
import json
import re

try:  # Python 3
    from urllib.request import urlopen, Request
except ImportError:  # Python 2
    from urllib2 import urlopen, Request


class NewVersionException(Exception):
    """Is thrown when a new VRT NU app is released."""

    def __init__(self, message):
        self.message = message
        super(NewVersionException, self).__init__(self.message)


def google_play_info():
    """Get info for VRT NU app from Google Play"""
    app_id = 'be.vrt.vrtnu'
    url = 'https://play.google.com/store/apps/details?id={}'.format(app_id)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}
    req = Request(url, headers=headers)
    response = urlopen(req)
    regex = re.compile(r'AF_initDataCallback\(([\s\S]*?return[\s\S]*?)\);<\/')
    match = re.findall(regex, response.read().decode('utf-8'))
    key_regex = re.compile(r'key: \'ds:(.*?)\',')
    value_regex = re.compile(r'return ([\s\S]*?)}}')
    for prop in match:
        key = re.search(key_regex, prop).group(1)
        info = json.loads(re.search(value_regex, prop).group(1))
        if key == '5':
            changelog = info[0][12][6][1]
            published = info[0][12][8][0]
        elif key == '8':
            version = info[1]
    return dict(version=version, changelog=changelog, published=published)


def run():
    """Check VRT NU app"""
    import dateutil.tz
    info = google_play_info()
    published = datetime.fromtimestamp(info.get('published'), dateutil.tz.UTC)
    published_string = published.astimezone(dateutil.tz.gettz('Europe/Brussels')).strftime('%A %e %B %Y at %H:%M')
    if published > datetime.now(dateutil.tz.UTC) - timedelta(hours=1):
        message = 'VRT NU for Android is updated to version {} released on {}\nChangelog:\n {}'.format(
            info.get('version'), published_string, info.get('changelog'))
        raise NewVersionException(message)
    message = 'Everything quiet here, VRT NU for Android is still at version {} released on {}'.format(info.get('version'), published_string)
    print(message)


if __name__ == '__main__':
    run()
