class MetadataCreator:

    def __init__(self):
        self._duration = None
        self._plot = None
        self._date = None

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
    def date(self):
        return self._date

    @date.setter
    def date (self, value):
        self._date = value

    def get_video_dictionary(self):
        video_dictionary = dict()
        if self.plot is not None:
            video_dictionary["plot"] = self.plot
        if self.duration is not None:
            video_dictionary["duration"] = self.duration
        if self.date is not None:
            video_dictionary["date"] = self.date
        return video_dictionary
