#!/usr/bin/env python

import os, json
import pyjq
import pytest
import opentraveldata

def test_download_feature():
    """
    Test the file download ability of OpenTravelData
    """
    
    myOPTD = opentraveldata.OpenTravelData()

    # Main OPTD POR file
    optd_por_filepath = myOPTD.localIATAPORFilepath()
    optd_por_fileurl = myOPTD.iataPORFileURL()

    # OPTD UN/LOCODE POR file
    optd_unlc_filepath = myOPTD.localUNLCPORFilepath()
    optd_unlc_fileurl = myOPTD.unlcPORFileURL() 

    # Download the OPTD POR files
    myOPTD.downloadFilesIfNeeded()
    
    # Retrieve the sizes of the downloaded files
    (optd_por_file_size, optd_unlc_file_size) = myOPTD.fileSizes()

    # Test the size of the OPTD main POR file
    optd_por_file_size_within_range = optd_por_file_size > 4e7 \
        and optd_por_file_size < 5e7
    assert optd_por_file_size_within_range, \
        f"The OPTD POR data file ({optd_por_filepath}, downloaded from " \
        f"{optd_por_fileurl}) has not the expected file size (around 40-50 MB)"

    # Test the size of the OPTD UN/LOCODE POR file
    optd_unlc_file_size_within_range = optd_unlc_file_size > 4e6 \
        and optd_unlc_file_size < 5e6
    assert optd_unlc_file_size_within_range, \
        f"The OPTD POR data file ({optd_unlc_filepath}, downloaded from " \
        f"{optd_unlc_fileurl}) has not the expected file size (around 4-5 MB)"

def test_serving_por_for_iev_city():
    """
    Test the OpenTravelData::getServingPORList() method
    """
    
    myOPTD = opentraveldata.OpenTravelData()

    # Retrieve the POR serving Kyiv (the city assigned IEV as IATA code)
    iev_serving_por_struct = myOPTD.getServingPORList ('IEV')

    # Check whether the retrieved structure is as expected
    is_iev_serving_por_struct_well_formed = \
        'original' in iev_serving_por_struct \
        and 'geoname_id' in iev_serving_por_struct['original'] \
        and 'tvl_list' in iev_serving_por_struct
    assert is_iev_serving_por_struct_well_formed, \
        "The structure returned by getServingPORList('IEV') does not contain " \
        "an 'original' dictionary and/or that latter does not contain " \
        "a 'geoname_id' field, and/or it does not contain a 'tvl_list' field. " \
        f"Retrieved structure: {iev_serving_por_struct}"

    # Geonames ID of (the city of) Kyiv
    iev_geo_id = iev_serving_por_struct['original']['geoname_id']
    assert iev_geo_id == 703448, \
        "The Geonames ID of the IEV city is expected to be 703448, but is not." \
        f" Actual Geoanmes ID: {iev_geo_id}. " \
        f"Retrieved structure: {iev_serving_por_struct}"

    # Extract the list of Geonames ID of the serving POR
    serving_por_list = pyjq.\
        all ('.tvl_list[] | .geoname_id', iev_serving_por_struct)
    does_geo_id_list_match = (serving_por_list == [6300960, 6300952, 8260936, 12156352])
    assert does_geo_id_list_match, \
        "The list of Geonames ID for the serving POR of the city of Kyiv " \
        "(assigned IEV as IATA code) is expected to be " \
        "[6300960, 6300952, 8260936, 12156352], but is not. Actual list: " \
        f"{serving_por_list}"

