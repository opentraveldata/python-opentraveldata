#!/usr/bin/env python

import os, json
from opentraveldata import CSVWriter, OpenTravelData

if __name__ == '__main__':
    """
    >>> a = 2
    """
    
    csv_test_filepath = '/tmp/optd-test.csv'
    csvwriter = CSVWriter (csv_test_filepath, '^')
    array = ['Test', 'of', 'OpenTravelData', 'OPTD']
    csvwriter.write (array)
    csvwriter.close()

    os.path.isfile (csv_test_filepath)

    

