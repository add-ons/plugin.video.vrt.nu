# -*- coding: utf-8 -*-

# GNU General Public License v2.0 (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

import time


class MetadataCreator:

    def __init__(self):
        self._title = None
        self._tvshowtitle = None
        self._duration = None
        self._plot = None
        self._plotoutline = None
        self._datetime = None
        self._season = None
        self._episode = None
        self._year = None
        self._mediatype = None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def tvshowtitle(self):
        return self._tvshowtitle

    @tvshowtitle.setter
    def tvshowtitle(self, value):
        self._tvshowtitle = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def plot(self):
        return self._plot

    @plot.setter
    def plot(self, value):
        self._plot = value.strip()

    @property
    def plotoutline(self):
        return self._plotoutline

    @plotoutline.setter
    def plotoutline(self, value):
        self._plotoutline = value.strip()

    @property
    def datetime(self):
        return self._datetime

    @datetime.setter
    def datetime(self, value):
        self._datetime = value

    @property
    def season(self):
        return self._season

    @season.setter
    def season(self, value):
        self._season = value

    @property
    def episode(self):
        return self._episode

    @episode.setter
    def episode(self, value):
        self._episode = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def mediatype(self):
        return self._mediatype

    @mediatype.setter
    def mediatype(self, value):
        self._mediatype = value

    def get_video_dictionary(self):
        video_dictionary = dict()

        if self.tvshowtitle is not None:
            video_dictionary['tvshowtitle'] = self.tvshowtitle

        if self.plot is not None:
            video_dictionary['plot'] = self.plot

        if self.plotoutline is not None:
            video_dictionary['plotoutline'] = self.plotoutline

        if self.duration is not None:
            video_dictionary['duration'] = self.duration

        if self.datetime is not None:
            video_dictionary['date'] = time.strftime('%d.%m.%Y', self.datetime)

        if self.season is not None:
            video_dictionary['season'] = self.season

        if self.episode is not None:
            video_dictionary['episode'] = self.episode

        if self.year is not None:
            video_dictionary['year'] = self.year

        if self.mediatype is not None:
            video_dictionary['mediatype'] = self.mediatype

        return video_dictionary
