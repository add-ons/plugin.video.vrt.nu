# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, unicode_literals
import re


# pylint: disable=unused-import
try:
    from html import unescape
except ImportError:
    from HTMLParser import HTMLParser

    def unescape(s):
        return HTMLParser().unescape(s)


def convert_html_to_kodilabel(text):
    rep = {"<i>": "[I]", "</i>": "[/I]"}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], text)


def strip_newlines(text):
    return text.replace('\n', '').strip()


def add_https_method(url):
    if url.startswith('//'):
        return 'https:' + url
    return url


def distinct(sequence):
    seen = set()
    for s in sequence:
        if s not in seen:
            seen.add(s)
            yield s
