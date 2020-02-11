#
# https://github.com/opentraveldata/python-opentraveldata/tree/master/opentraveldata
#

import getopt, os, sys, re, csv, datetime, shutil, urllib.request

# OPTD-maintained list of POR
optd_url_base = 'https://github.com/opentraveldata/opentraveldata/blob/master'

class Error (Exception):
   """Base class for other OpenTravelData (OPTD) exceptions"""
   pass

class OPTDLocalFileError (Error):
   """Raised when there is an issue with the local OenTravelData (OPTD) file"""
   pass

class OPTDDownloadFileError (Error):
   """Raised when there is an issue wile downloading OenTravelData (OPTD) file"""
   pass    

class OPTDIATACodeError (Error):
   """Raised when there is the IATA code is not known from OenTravelData (OPTD)"""
   pass

class OpenTravelData():
    """
    Utility class to write to CSV files one line at a time.

    >>> import opentraveldata

    >>> myOPTD = opentraveldata.OpenTravelData()

    >>> str (myOPTD)
    'OpenTravelData - Local file: /tmp/opentraveldata/optd_por_public.csv'

    >>> myOPTD.localFilepath()
    '/tmp/opentraveldata/optd_por_public.csv'

    >>> myOPTD.fileURL()
    'https://github.com/opentraveldata/opentraveldata/blob/master/opentraveldata/optd_por_public.csv?raw=true'

    >>> myOPTD.downloadFileIfNeeded()

    >>> myOPTD.size()
    66404

    >>> myOPTD.extractFileHeader()
    'iata_code^icao_code^faa_code^is_geonames^geoname_id^envelope_id^name^asciiname^latitude^longitude^fclass^fcode^page_rank^date_from^date_until^comment^country_code^cc2^country_name^continent_name^adm1_code^adm1_name_utf^adm1_name_ascii^adm2_code^adm2_name_utf^adm2_name_ascii^adm3_code^adm4_code^population^elevation^gtopo30^timezone^gmt_offset^dst_offset^raw_offset^moddate^city_code_list^city_name_list^city_detail_list^tvl_por_list^iso31662^location_type^wiki_link^alt_name_section^wac^wac_name^ccy_code^unlc_list^uic_list'

    >>> myOPTD.displayFileHead (3)
    Header of the '/tmp/opentraveldata/optd_por_public.csv' file
    iata_code,icao_code,faa_code,is_geonames,geoname_id,envelope_id,name,asciiname,latitude,longitude,fclass,fcode,page_rank,date_from,date_until,comment,country_code,cc2,country_name,continent_name,adm1_code,adm1_name_utf,adm1_name_ascii,adm2_code,adm2_name_utf,adm2_name_ascii,adm3_code,adm4_code,population,elevation,gtopo30,timezone,gmt_offset,dst_offset,raw_offset,moddate,city_code_list,city_name_list,city_detail_list,tvl_por_list,iso31662,location_type,wiki_link,alt_name_section,wac,wac_name,ccy_code,unlc_list,uic_list
    AAA,NTGA,,Y,6947726,,Anaa Airport,Anaa Airport,-17.352606,-145.509956,S,AIRP,0.03172939118539184,,,,PF,,French Polynesia,Oceania,,,,,,,,,0,,8,Pacific/Tahiti,-10.0,-10.0,-10.0,2012-04-29,AAA,Anaa,AAA|4034700|Anaa|Anaa,,,A,https://en.wikipedia.org/wiki/Anaa_Airport,ru|Анаа|=wkdt|Q1430785|,823,French Polynesia,XPF,,
    AAA,,,Y,4034700,,Anaa,Anaa,-17.41667,-145.5,T,ATOL,0.03172939118539184,,,,PF,,French Polynesia,Oceania,00,,,,,,,,0,,-9999,Pacific/Tahiti,-10.0,-10.0,-10.0,2019-02-10,AAA,Anaa,AAA|4034700|Anaa|Anaa,AAA,,C,https://en.wikipedia.org/wiki/Anaa,|Anaa|=es|Isla de Todos Santos|=|Anau|=|Tapuhoe|=|Anhar|=en|Chain|=fr|La Chaîne|=en|Chain Island|=fr|La Conversión de San Pablo|=en|Anaa Atoll|=en|Anaa|s=ar|أنا|=gl|Atol Anaa|=hy|Անա|=mrj|Анаа|=ur|انآ|=ru|Анаа|=zh|阿納環礁|,823,French Polynesia,XPF,,

    >>> myOPTD.extractPORSubsetFromOPTD()

    >>> myOPTD.getAirportList ('IEV')
    ['IEV']

    >>> myOPTD.getAirportList ('BAK')
    ['GYD', 'ZXT']

    """
    data_rel_path = None
    file_url = None
    local_dirname = None
    local_filename = None
    local_filepath = None
    por_dict = None
    verbose = False

    def __init__ (self, data_rel_path = 'opentraveldata/optd_por_public.csv',
                  local_dir = '/tmp/opentraveldata', verbose = False):
        # Remote URL/file-path
        self.data_rel_path = data_rel_path
        self.file_url = f"{optd_url_base}/{self.data_rel_path}?raw=true"

        # Local copy/file-path, directory and file pointer
        self.local_dirname = local_dir
        self.local_filename = os.path.basename (data_rel_path)
        self.local_filepath = f"{self.local_dirname}/{self.local_filename}"

        # Vebosity
        self.verbose = verbose

        # Create the local directory if not already existing
        try:
            os.makedirs (self.local_dirname, exist_ok = True)
        except:
            err_msg = "[OpenTravelData::init] Error while creating " \
                f"{self.local_dirname} directory locally"
            raise OPTDLocalFileError (err_msg)            
        
    def __repr__ (self):
        repr_msg = f"OpenTravelData - Local file: {self.local_filepath}"
        return repr_msg
    
    def fileURL (self):
        return self.file_url

    def localFilepath (self):
        return self.local_filepath

    def size (self):
        return os.path.getsize (self.local_filepath)

    def downloadFile (self):
        """Download a file from the Web."""
        if self.verbose:
            print (f"[OpenTravelata::downloadFile] Downloading " \
                   "'{self.local_filepath}' from {self.file_url}...")

        try:
            with urllib.request.urlopen (self.file_url) \
                as response, open (self.local_filepath, 'wb') as out_file:
                shutil.copyfileobj (response, out_file)
        except:
            err_msg = "[OpenTravelData::init] Error while downloading " \
                f"{self.file_url} as {self.local_filepath}"
            raise OPTDDownloadFileError (err_msg)
            
            if self.verbose:
                print ("[Opentraveldata::downloadFile] ... done")
        return

    def downloadFileIfNeeded (self):
        """Download a file from the Web, only if newer on that latter."""

        # Check whether the OPTD data file has already been downloaded
        file_exists = os.path.isfile (self.local_filepath)
        if file_exists:
            try:
                if os.stat (self.local_filepath).st_size > 0:
                    mtime = os.path.getmtime (self.local_filepath)
                    file_time = datetime.datetime.fromtimestamp (mtime)
                    if self.verbose:
                        print ("[Opentraveldata::downloadFileIfNeeded] " \
                               f"Time-stamp of '{self.local_filepath}': " \
                               f"{file_time}. If that file is too old, " \
                               "you can delete it, and re-execute that task")
                else:
                    self.downloadFile()
            except:
                self.downloadFile()
        else:
            self.downloadFile()
        return

    def displayFileHead (self, lines = 10):
        """Display the first 10 lines of the given file."""

        #
        print (f"Header of the '{self.local_filepath}' file")
        #
        with open (self.local_filepath, newline='') as csvfile:
            file_reader = csv.reader (csvfile, delimiter='^')
            for i in range (lines):
                print (','.join(file_reader.__next__()))

        #
        return

    def extractFileHeader (self):
        """Extract the header of the given file."""

        #
        header_line = ''
        with open (self.local_filepath) as tmpfile:
            header_line = tmpfile.readline().strip()
        
        #
        return header_line

    def extractPORSubsetFromOPTD (self):
        """
        Extract a few details from the OpenTravelData (OPTD)
        POR (points of reference)
        """
    
        self.por_dict = dict()

        # OPTD-maintained list of POR
        with open (self.local_filepath, newline='') as csvfile:
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
                if not optd_por_code in self.por_dict:
                    self.por_dict[optd_por_code] = dict()

                self.por_dict[optd_por_code][optd_loc_type] = optd_por_rec
            
        #
        return

    def getAirportList (self, por_code = 'FRA',
                        only_when_city_code_differs = True):
        """
        Derive the list of travel-/transport-related POR (point of reference)
        IATA code for a given city IATA code.

        only_when_city_code_differs: whether or not that method should return
        the travel-/transport-related POR only when the city IATA code
        differs from the IATA codes of those serving POR.
        For instance:
        - When that parameter is set to True,
          getAirportList('IEV') will return ['IEV'] only
        - When that parameter is set to True,
          getAirportList('IEV') will return ['IEV', 'KBP']
        """
        apt_list = []

        # Retrieve the OPTD POR corresponding to the given POR IATA code
        if not por_code in self.por_dict:
            err_msg = f"[OpenTravelData::getAirportList] The {por_code} " \
                "IATA code does not seem to be valid in OPTD"
            raise OPTDIATACodeError (err_msg)

        optd_por_rec_dict = self.por_dict[por_code]
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
            # may also serve a given city.
            is_city = re.search ("C", optd_loc_type)

            # When the POR is not city (and can no longer be an airport
            # or an offline point, as those cases have been handled above),
            # there is no travel-/transport-related serving POR,
            # by definition.
            if not is_city: continue

            # Derive the serving travel-/transport-related points
            tvl_por_list = optd_por_rec['tvl_por_list']
        
            for tvl_por_code in tvl_por_list:
                if not tvl_por_code in self.por_dict:
                    err_msg = "[OpenTravelData::getAirportList] The " \
                        f"{tvl_por_code} IATA code (transport-related), " \
                        f"serving {por_code} (city), does not seem " \
                        "to be valid in OPTD"
                    raise OPTDIATACodeError (err_msg)
                    
                # As explained above, only the airports, from all
                # the POR serving the city, are considered.
                # The location type for airpots is usually 'A',
                # but may also be 'O' in some rare cases (if any).
                tvl_por_rec_dict = self.por_dict[tvl_por_code]
                for tvl_loc_type, tvl_por_rec in tvl_por_rec_dict.items():
                    is_offpoint = re.search ("O", tvl_loc_type)
                    is_airport = re.search ("A", tvl_loc_type)
                    if is_airport or is_offpoint:
                        apt_list.append (tvl_por_code)

        #
        return apt_list

