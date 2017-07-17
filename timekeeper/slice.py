from datetime import datetime

class Slice(object):
    """
    A period of time with a start and an end
    """
    DT_FMT = "%Y-%m-%d %H:%M"
    
    def __init__(self, start, end, category, description):
        self._start = start
        self._end = end
        self._category = category
        self._description = description

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def category(self):
        return self._category

    @property
    def description(self):
        return self._description

    def __repr__(self):
        s = self._start.strftime(self._DT_FMT)
        s += ", "
        s += self._end.strftime(self._DT_FMT)
        s += ", "
        s += self._category
        s += ", "
        s += self._description

        return s
