# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Implementation of IPTVManager class"""

from __future__ import absolute_import, division, unicode_literals
from kodiutils import log
from data import CHANNELS


class IPTVManager:
    """Interface to IPTV Manager"""

    def send_data(self, host, port, data):
        """Send data to IPTV Manager"""
        import json
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        try:
            sock.send(json.dumps(data))
        finally:
            # Close our connection
            sock.close()

    def channels(self, port):
        """Return JSON-M3U formatted information to IPTV Manager"""
        streams = []
        for channel in CHANNELS:
            if not channel.get('live_stream_id'):
                continue
            streams.append(dict(
                id='{name}.be'.format(**channel),
                name=channel.get('label'),
                logo=channel.get('epg_logo'),
                stream='plugin://plugin.video.vrt.nu/play/id/{live_stream_id}'.format(**channel),
                group='VRT',
                radio=False,
            ))
        log(2, 'Sending channels to IPTV Manager on port {port}', port=port)
        self.send_data('localhost', port, dict(version=1, streams=streams))

    def epg(self, port):
        """Return JSONTV formatted information to IPTV Manager"""
        log(2, 'Sending EPG to IPTV Manager on port {port}', port=port)
        self.send_data('localhost', port, dict(version=1, epg=dict()))
