# -*- coding: UTF-8 -*-

# GNU General Public License v2.0 (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

''' This is <describe here> '''

from __future__ import absolute_import, division, print_function, unicode_literals


def replace_newlines_and_strip(text):
    return text.replace('\n', '').strip()


def replace_double_slashes_with_https(url):
    return url.replace('//', 'https://')


def distinct(sequence):
    seen = set()
    for s in sequence:
        if s not in seen:
            seen.add(s)
            yield s
