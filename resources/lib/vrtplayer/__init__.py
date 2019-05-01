# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, unicode_literals

# Fallback list of categories so we don't depend on web scraping only
CATEGORIES = [
    dict(name='Audiodescriptie', id='met-audiodescriptie'),
    dict(name='Cultuur', id='cultuur'),
    dict(name='Docu', id='docu'),
    dict(name='Entertainment', id='entertainment'),
    dict(name='Films', id='films'),
    dict(name='Human interest', id='human-interest'),
    dict(name='Humor', id='humor'),
    dict(name='Kinderen', id='voor-kinderen'),
    dict(name='Koken', id='koken'),
    dict(name='Lifestyle', id='lifestyle'),
    dict(name='Muziek', id='muziek'),
    dict(name='Nieuws en actua', id='nieuws-en-actua'),
    dict(name='Series', id='series'),
    dict(name='Sport', id='sport'),
    dict(name='Talkshows', id='talkshows'),
    dict(name='Vlaamse Gebarentaal', id='met-gebarentaal'),
    dict(name='Wetenschap en natuur', id='wetenschap-en-natuur'),
]

CHANNELS = {
    'een': dict(
        id='O8',
        type='tv',
        name='Eén',
        studio='Een',
        live_stream='https://www.vrt.be/vrtnu/kanalen/een/',
        live_stream_id='vualto_een',
    ),
    'canvas': dict(
        id='1H',
        type='tv',
        name='Canvas',
        studio='Canvas',
        live_stream='https://www.vrt.be/vrtnu/kanalen/canvas/',
        live_stream_id='vualto_canvas',
    ),
    'ketnet': dict(
        id='O9',
        type='tv',
        name='Ketnet',
        studio='Ketnet',
        live_stream='https://www.vrt.be/vrtnu/kanalen/ketnet/',
        live_stream_id='vualto_ketnet',
    ),
    'ketnet-jr': dict(
        id='1H',
        type='tv',
        name='Ketnet Junior',
        studio='Ketnet Junior',
    ),
    'sporza': dict(
        id='12',
        type='radio+tv',
        name='Sporza',
        studio='Sporza',
        live_stream_id='vualto_sporza',
    ),
    'vrtnxt': dict(
        id='',
        type='tv',
        name='VRT NXT',
        studio='VRT NXT',
    ),
    'radio1': dict(
        id='11',
        type='radio',
        name='Radio 1',
        studio='Radio 1',
    ),
    'radio2': dict(
        id='24',
        type='radio',
        name='Radio 2',
        studio='Radio 2',
    ),
    'klara': dict(
        id='31',
        type='radio',
        name='Klara',
        studio='Klara',
    ),
    'stubru': dict(
        id='41',
        type='radio+tv',
        name='Studio Brussel',
        studio='Studio Brussel',
        # live_stream='https://stubru.be/live',
        live_stream_id='vualto_stubru',
    ),
    'mnm': dict(
        id='55',
        type='radio+tv',
        name='MNM',
        studio='MNM',
        # live_stream='https://mnm.be/kijk/live',
        live_stream_id='vualto_mnm',
    ),
    'vrtnws': dict(
        id='13',
        type='radio+tv',
        name='VRT NWS',
        studio='VRT NWS',
        live_stream_id='vualto_nieuws',
        # live_stream_id='vualto_journaal',
    ),
}
