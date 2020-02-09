#
# https://github.com/opentraveldata/python-opentraveldata/tree/master/opentraveldata
#

import getopt, os, sys, re, csv, datetime

# OPTD-maintained list of POR
optd_url_base = 'https://github.com/opentraveldata/opentraveldata/blob/master'
'/opentraveldata/optd_por_public.csv?raw=true'
optd_por_public_url = 'https://github.com/opentraveldata/opentraveldata/blob/master/opentraveldata/optd_por_public.csv?raw=true'
optd_por_public_file = 'data/optd_por_public.csv'

class OpenTravelData():
    """Utility class to write to CSV files one line at a time"""
    rel_path = None
    local_filepath = None
    file_hdlr = None
    verbose = False

    def __init__ (self, rel_path = 'opentraveldata/optd_por_public.csv',
                  verbose = False):
        self.rel_path = rel_path
        self.verbose = verbose

    def close (self):
        self.file_hdlr.close()

    def size (self):
        return os.path.getsize(self.local_filepath)

    def local_filepath (self):
        return self.local_filepath

    def downloadFileIfNeeded (file_url, output_file, verbose_flag = False):
        """Download a file from the Web, only if newer on that latter."""

        # Check whether the output_file has already been downloaded
        file_exists = os.path.isfile (output_file)
        if file_exists:
            try:
                if os.stat (output_file).st_size > 0:
                    mtime = os.path.getmtime (output_file)
                    file_time = datetime.datetime.fromtimestamp (mtime)
                    if verbose_flag:
                        print (f"Time-stamp of '{output_file}': {file_time}")
                        print ("If that file is too old, you can delete it, " \
                               "and re-execute that script")
                else:
                    downloadFile (file_url, output_file, verbose_flag)
            except:
                downloadFile (file_url, output_file, verbose_flag)
        else:
            downloadFile (file_url, output_file, verbose_flag)
        return

    def displayFileHead (input_file):
        """Display the first 10 lines of the given file."""

        #
        print ("Header of the '" + input_file + "' file")
        #
        with open (input_file, newline='') as csvfile:
            file_reader = csv.reader (csvfile, delimiter='^')
            for i in range(10):
                print (','.join(file_reader.__next__()))

        #
        return

    def extractFileHeader (input_file):
        """Extract the header of the given file."""

        #
        header_line = ''
        with open (input_file) as tmpfile:
            header_line = tmpfile.readline().strip()
        
        #
        return header_line

    def extractPORSubsetFromOPTD (verboseFlag, optd_por_public_file):
        """Extract a few details from the OpenTravelData (OPTD)
        POR (points of reference)"""
    
        optd_por_dict = dict()

        # OPTD-maintained list of POR
        with open (optd_por_public_file, newline='') as csvfile:
            file_reader = csv.DictReader (csvfile, delimiter='^')
            for row in file_reader:
                optd_por_code = row['iata_code']
                optd_loc_type = row['location_type']
                optd_geo_id = row['geoname_id']
                optd_env_id = row['envelope_id']
                optd_coord_lat = row['latitude']
                optd_coord_lon = row['longitude']
                optd_por_name = row['name']
                optd_page_rank = row['page_rank']
                optd_ctry_code = row['country_code']
                optd_ctry_name = row['country_name']
                optd_adm1_code = row['adm1_code']
                optd_adm1_name = row['adm1_name_utf']
                city_code_list_str = row['city_code_list']
                city_code_list = city_code_list_str.split(',')
                tvl_por_list_str = row['tvl_por_list']
                tvl_por_list = tvl_por_list_str.split(',')
                unlc_list_str = row['unlc_list']
                unlc_list_tmp = unlc_list_str.split('|')
                unlc_list = unlc_list_tmp[:-1]

                if city_code_list:
                    # Derive whether that POR is a city
                    is_city = re.search ("C", optd_loc_type)

                optd_por_rec = {'iata_code': optd_por_code,
                                'location_type': optd_loc_type,
                                'geoname_id': optd_geo_id,
                                'envelope_id': optd_env_id,
                                'latitude': optd_coord_lat,
                                'longitude': optd_coord_lon,
                                'name': optd_por_name,
                                'page_rank': optd_page_rank,
                                'country_code': optd_ctry_code,
                                'country_name': optd_ctry_name,
                                'adm1_code': optd_adm1_code,
                                'adm1_name_utf': optd_adm1_name,
                                'city_code_list': city_code_list,
                                'tvl_por_list': tvl_por_list,
                                'unlc_list': unlc_list}
                # There may be several POR (points of reference)
                # with the same IATA code. The location type (e.g.,
                # 'C' for city, 'A' for airrport) then allows
                # to differentiate them
                if not optd_por_code in optd_por_dict:
                    optd_por_dict[optd_por_code] = dict()

                optd_por_dict[optd_por_code][optd_loc_type] = optd_por_rec
            
        #
        return optd_por_dict

    def getAirportList (verboseFlag, por_code, optd_por_dict):
        """Derive the list of airports for a given
        POR (point of reference)"""
        apt_list = []

        # Retrieve the OPTD POR corresponding to the given POR IATA code
        if not por_code in optd_por_dict:
            print (f"Error - The {por_code} IATA code does not seem " \
                   "to be valid in OPTD")
            return apt_list

        optd_por_rec_dict = optd_por_dict[por_code]
        for optd_loc_type, optd_por_rec in optd_por_rec_dict.items():
            # When that POR is already an airport or an offline point (also
            # considered as an airport, potentially), there is nothing else
            # to do at this stage
            is_offpoint = re.search ("O", optd_loc_type)
            is_airport = re.search ("A", optd_loc_type)
            if is_airport or is_offpoint:
                apt_list.append (por_code)
                return apt_list

            # When the POR is a city (e.g., BAK, IEV), the list
            # of airports, among the list of serving
            # travel-/transport-related points, have to be retrieved.
            # Note that non-airport POR (e.g., railway stations, ports)
            # may serve a given city.
            is_city = re.search ("C", optd_loc_type)

            # When the POR is not city (and can no longer be an airport
            # or an offline point, as those cases have been handled above),
            # there is no travel-/transport-related serving POR,
            # by definition.
            if not is_city: continue

            # Derive the serving travel-/transport-related points
            tvl_por_list = optd_por_rec['tvl_por_list']
        
            for tvl_por_code in tvl_por_list:
                if not tvl_por_code in optd_por_dict:
                    print (f"Error - The {tvl_por_code} IATA code (tvl), " \
                           f"serving {por_code} (city), does not seem " \
                           "to be valid in OPTD")
                    
                # As explained abovr, only the airports, from al
                # the POR serving the city, are considered.
                # The location type for airpots is usually 'A',
                # but may also be 'O' in some rare cases (if any).
                tvl_por_rec_dict = optd_por_dict[tvl_por_code]
                for tvl_loc_type, tvl_por_rec in tvl_por_rec_dict.items():
                    is_offpoint = re.search ("O", tvl_loc_type)
                    is_airport = re.search ("A", tvl_loc_type)
                    if is_airport or is_offpoint:
                        apt_list.append (tvl_por_code)

        #
        return apt_list

