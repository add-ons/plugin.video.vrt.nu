# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function, unicode_literals
from contextlib import contextmanager
import os
import polib

PO = polib.pofile('resources/language/resource.language.en_gb/strings.po')
SETTINGS = dict(
    username='qsdfdsq',
    password='qsdfqsdfds',
    log_level='Verbose',
    showpermalink='true',
    showsubtitles='true',
    usedrm='false',
    usefavorites='false',
)


def get_localized_string(msgctxt):
    for entry in PO:
        if entry.msgctxt == '#%s' % msgctxt:
            return entry.msgstr
    return 'vrttest'


def get_setting(key):
    return SETTINGS[key]


def log_notice(msg, level='Info'):
    print('%s: %s' % (level, msg))


@contextmanager
def open_file(path, flags='r'):
    f = open(path, flags)
    yield f
    f.close()


def stat_file(path):
    class stat:
        def __init__(self, path):
            self._stat = os.stat(path)

        def st_mtime(self):
            return self._stat.st_mtime

    return stat(path)
