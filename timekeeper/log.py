from datetime import datetime
import sqlite3

from . import slice

class Log(object):
    """
    Represents a series of slices, forming a log of how time was spent
    """
    DT_FMT = "%Y-%m-%d %H:%M"
    _COL_WIDTH = 15
    
    def __init__(self, slices):
        self._slices = {}
        
        for s in slices:
            self._slices[s.start] = (s, False)

    @property
    def slices(self):
        sl = {}

        for k, v in self._slices.items():
            sl[k] = v[0]

        return sl

    def get_slice(self, dt):
        """
        Returns the slice at the specified time
        """
        return self._slices.get(dt)[0]

    def set_slice(self, s, saved=False):
        """
        Adds s to the log, overwriting any slice previously at that location
        """
        self._slices[s.start] = (s, saved)

    def __repr__(self):
        s = "Start            | End              | Category        | Description                   \n"
        s += "-----------------|------------------|-----------------|-------------------------------\n"

        for k, v in self._slices.items():
            start_str = v[0].start.strftime(self.DT_FMT)
            end_str = v[0].end.strftime(self.DT_FMT)

            if not v[1]:
                saved_notice = "(!)"
            else:
                saved_notice = ""

            s += saved_notice + start_str + " | " + end_str + " | " + v[0].category + " " * (self._COL_WIDTH - len(v[0].category)) + " | " + v[0].description + "\n"

        return s

    def save(self, db_path):
        """
        Saves the log to the specified database file by inserting each slice
        into the SQL table
        """
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS log (id INTEGER PRIMARY KEY AUTOINCREMENT, start DATETIME, end DATETIME, category VARCHAR, description TEXT)''')

        for k, v in self._slices.items():
            if v[1]:
                break
            
            start_str = v[0].start.strftime(self.DT_FMT)
            end_str = v[0].end.strftime(self.DT_FMT)

            data = (start_str, end_str, v[0].category, v[0].description)
            
            c.execute('''INSERT INTO log (start, end, category, description) VALUES (?, ?, ?, ?)''', data)
            conn.commit()

            v = (v[0], True)

        conn.close()

    def load(self, db_path):
        """
        Loads a log from the specified database file by inserting each slice
        into the log object from the SQL table
        """ 
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''SELECT * FROM log''')

        data = c.fetchall()

        for d in data:
            self.set_slice(slice.Slice(datetime.strptime(d[1], self.DT_FMT),
                           datetime.strptime(d[2], self.DT_FMT),
                           d[3], d[4]), True)

        conn.close()
