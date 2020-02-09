#
# https://github.com/opentraveldata/python-opentraveldata/tree/master/opentraveldata
#

import csv

class CSVWriter():
    """Utility class to write to CSV files one line at a time"""
    filepath = None
    delimiter = '^'
    fp = None
    writer = None

    def __init__ (self, filepath = None, delimiter = '^'):
        self.filepath = filepath
        self.delimiter = delimiter
        self.fp = open (self.filepath, 'w', encoding = 'utf8', newline = '')
        self.writer = csv.writer (self.fp, delimiter = self.delimiter,
                                  quotechar = '"', quoting = csv.QUOTE_MINIMAL,
                                  lineterminator = '\n')

    def close (self):
        self.fp.close()

    def write (self, elems):
        self.writer.writerow(elems)

    def size (self):
        return os.path.getsize(self.filename)

    def fname (self):
        return self.filename


    
