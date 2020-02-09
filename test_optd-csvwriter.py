#!/usr/bin/env python

import os, json
import pytest
from opentraveldata import CSVWriter, OpenTravelData

def test_csvwriter_writing():
    """
    >>> a = 2
    """
    
    csv_test_filepath = '/tmp/optd-test.csv'
    csvwriter = CSVWriter (csv_test_filepath, '^')
    array = ['Test', 'of', 'OpenTravelData', 'OPTD']
    csvwriter.write (array)
    csvwriter.close()

    doesFileExist = os.path.isfile (csv_test_filepath)
    assert doesFileExist, f"Error in writing {csv_test_filepath}"

