# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
''' All functionality that requires Kodi imports '''

from __future__ import absolute_import, division, unicode_literals
from sys import version_info

try:  # Python 3
    from urllib.error import HTTPError
    from urllib.parse import unquote
    from urllib.request import urlopen, Request
except ImportError:  # Python 2
    from urllib2 import HTTPError, unquote, urlopen, Request

from kodiutils import (container_refresh, delete, exists, get_cache_path, get_setting, listdir,
                       localize, log, log_error, mkdirs, notification, ok_dialog, open_file, stat_file)
from statichelper import to_unicode


def human_delta(seconds):
    ''' Return a human-readable representation of the TTL '''
    from math import floor
    days = int(floor(seconds / (24 * 60 * 60)))
    seconds = seconds % (24 * 60 * 60)
    hours = int(floor(seconds / (60 * 60)))
    seconds = seconds % (60 * 60)
    if days:
        return '%d day%s and %d hour%s' % (days, 's' if days != 1 else '', hours, 's' if hours != 1 else '')
    minutes = int(floor(seconds / 60))
    seconds = seconds % 60
    if hours:
        return '%d hour%s and %d minute%s' % (hours, 's' if hours != 1 else '', minutes, 's' if minutes != 1 else '')
    if minutes:
        return '%d minute%s and %d second%s' % (minutes, 's' if minutes != 1 else '', seconds, 's' if seconds != 1 else '')
    return '%d second%s' % (seconds, 's' if seconds != 1 else '')


def get_cache(path, ttl=None):  # pylint: disable=redefined-outer-name
    ''' Get the content from cache, if it's still fresh '''
    if get_setting('usehttpcaching', 'true') == 'false':
        return None

    fullpath = get_cache_path() + path
    if not exists(fullpath):
        return None

    from time import localtime, mktime
    mtime = stat_file(fullpath).st_mtime()
    now = mktime(localtime())
    if ttl and now >= mtime + ttl:
        return None

    if ttl is None:
        log(3, "Cache '{path}' is forced from cache.", path=path)
    else:
        log(3, "Cache '{path}' is fresh, expires in {time}.", path=path, time=human_delta(mtime + ttl - now))
    from json import load
    with open_file(fullpath, 'r') as fdesc:
        try:
            return load(fdesc)
        except (TypeError, ValueError) as exc:  # No JSON object could be decoded
            fdesc.seek(0, 0)
            log_error('{exc}\nDATA: {data}', exc=exc, data=fdesc.read())
            return None


def update_cache(path, data):
    ''' Update the cache, if necessary '''
    if get_setting('usehttpcaching', 'true') == 'false':
        return

    from hashlib import md5
    from json import dump, dumps
    fullpath = get_cache_path() + path
    if exists(fullpath):
        with open_file(fullpath) as fdesc:
            cachefile = fdesc.read().encode('utf-8')
        md5_cache = md5(cachefile)
    else:
        md5_cache = 0
        # Create cache directory if missing
        if not exists(get_cache_path()):
            mkdirs(get_cache_path())

    # Avoid writes if possible (i.e. SD cards)
    if md5_cache != md5(dumps(data).encode('utf-8')):
        log(3, "Write cache '{path}'.", path=path)
        with open_file(fullpath, 'w') as fdesc:
            # dump(data, fdesc, encoding='utf-8')
            dump(data, fdesc)
    else:
        # Update timestamp
        from os import utime
        log(3, "Cache '{path}' has not changed, updating mtime only.", path=path)
        utime(path)


def ttl(kind='direct'):
    ''' Return the HTTP cache ttl in seconds based on kind of relation '''
    if kind == 'direct':
        return int(get_setting('httpcachettldirect', 5)) * 60
    if kind == 'indirect':
        return int(get_setting('httpcachettlindirect', 60)) * 60
    return 5 * 60


def get_url_json(url, cache=None, headers=None, data=None):
    ''' Return HTTP data '''
    if headers is None:
        headers = dict()
    from json import load, loads
    log(2, 'URL get: {url}', url=unquote(url))
    req = Request(url, headers=headers)
    if data is not None:
        req.data = data
    try:
        if (3, 0, 0) <= version_info <= (3, 5, 9):  # the JSON object must be str, not 'bytes'
            json_data = loads(to_unicode(urlopen(req).read()))
        else:
            json_data = load(urlopen(req))
    except ValueError as exc:  # No JSON object could be decoded
        log_error('JSON Error: {exc}', exc=exc)
        return []
    except HTTPError as exc:
        if hasattr(req, 'selector'):  # Python 3.4+
            url_length = len(req.selector)
        else:  # Python 2.7
            url_length = len(req.get_selector())
        if exc.code == 413 and url_length > 8192:
            ok_dialog(heading='HTTP Error 413', message=localize(30967))
            log_error('HTTP Error 413: Exceeded maximum url length: '
                      'VRT Search API url has a length of {length} characters.', length=url_length)
            return []
        if exc.code == 400 and 7600 <= url_length <= 8192:
            ok_dialog(heading='HTTP Error 400', message=localize(30967))
            log_error('HTTP Error 400: Probably exceeded maximum url length: '
                      'VRT Search API url has a length of {length} characters.', length=url_length)
            return []
        raise
    else:
        if cache:
            update_cache(cache, json_data)
    return json_data


def get_cached_url_json(url, cache, headers=None, ttl=None):  # pylint: disable=redefined-outer-name
    ''' Return data from cache, if any, else make an HTTP request '''
    # Get api data from cache if it is fresh
    json_data = get_cache(cache, ttl=ttl)
    if json_data is not None:
        return json_data
    return get_url_json(url, cache=cache, headers=headers)


def refresh_caches(cache_file=None):
    ''' Invalidate the needed caches and refresh container '''
    files = ['favorites.json', 'oneoff.json', 'resume_points.json']
    if cache_file and cache_file not in files:
        files.append(cache_file)
    invalidate_caches(*files)
    container_refresh()
    notification(message=localize(30981))


def invalidate_caches(*caches):
    ''' Invalidate multiple cache files '''
    import fnmatch
    _, files = listdir(get_cache_path())
    # Invalidate caches related to menu list refreshes
    removes = set()
    for expr in caches:
        removes.update(fnmatch.filter(files, expr))
    for filename in removes:
        delete(get_cache_path() + filename)
