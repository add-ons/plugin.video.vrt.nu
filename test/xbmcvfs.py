# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function, unicode_literals
import os


def File(path, flags='r'):
    return open(path, flags)


def Stat(path):
    class stat:
        def __init__(self, path):
            self._stat = os.stat(path)

        def st_mtime(self):
            return self._stat.st_mtime

    return stat(path)


def delete(path):
    try:
        os.remove(path)
    except OSError:
        pass


def exists(path):
    return os.path.exists(path)


def listdir(path):
    files = []
    dirs = []
    for f in os.listdir(path):
        if os.path.isfile(f):
            files.append(f)
        if os.path.isdir(f):
            dirs.append(f)
    return dirs, files


def mkdir(path):
    return os.mkdir(path)


def mkdirs(path):
    return os.makedirs(path)
