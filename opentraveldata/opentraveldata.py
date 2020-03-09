#
# https://github.com/opentraveldata/python-opentraveldata/tree/master/opentraveldata
#

import getopt, os, sys, re, csv, datetime, shutil, urllib.request

# OPTD maintains three lists of POR (points of reference)
# - optd_por_public.csv is the light version,
#   with slightly over 20,000 records (10 MB non compressed).
#   It corresponds to all the POR having a IATA code (e.g., AMS, BER, LON, PAR)
# - optd_por_public_all.csv is the full version,
#   with slightly over 123,000 records (42 MB non compressed).
#   It corresponds to all the POR having at least a code, be it IATA
#   and/or UN/LOCODE (e.g., DEHAM, CNSHA, NLRTM). The list therefore
#   includes the light version.
# - optd_por_unlc.csv is the list of UN/LOCODE assigned POR,
#   with slightly over 100,000 records (5 MB non compressed).
#   That list, in the contrast to the other two above,
#   comes with a very limited set of fields.
#
optd_url_base = 'https://github.com/opentraveldata/opentraveldata/blob/master'
optd_por_iata_rel_path = 'opentraveldata/optd_por_public.csv'
optd_por_all_rel_path = 'opentraveldata/optd_por_public_all.csv'
optd_por_unlc_rel_path = 'opentraveldata/optd_por_unlc.csv'


class Error (Exception):
   """
   Base class for other OpenTravelData (OPTD) exceptions
   """
   pass

class OPTDLocalFileError (Error):
   """
   Raised when there is an issue with the local OenTravelData (OPTD) file
   """
   pass

class OPTDDownloadFileError (Error):
   """
   Raised when there is an issue wile downloading OenTravelData (OPTD) file
   """
   pass    

class OPTDPORDictConsistencyError (Error):
   """
   Raised when the (IATA and UN/LOCODE) POR dictionaries are not consistent
   """
   pass

class OPTDIATACodeError (Error):
   """
   Raised when there is the IATA code is not known from OenTravelData (OPTD)
   """
   pass

class OPTDLocationTypeError (Error):
   """
   Raised when there is an issue with the location type
   """
   pass

class OpenTravelData():
    """
    Utility class to write to CSV files one line at a time.

    >>> import opentraveldata

    >>> myOPTD = opentraveldata.OpenTravelData()

    >>> myOPTD
    OpenTravelData:
	Local IATA/ICAO POR file: /tmp/opentraveldata/optd_por_public_all.csv
	Local UN/LOCODE POR file: /tmp/opentraveldata/optd_por_unlc.csv

    >>> myOPTD.localIATAPORFilepath()
    '/tmp/opentraveldata/optd_por_public_all.csv'

    >>> myOPTD.localUNLCPORFilepath()
    '/tmp/opentraveldata/optd_por_unlc.csv'

    >>> myOPTD.iataPORFileURL()
    'https://github.com/opentraveldata/opentraveldata/blob/master/opentraveldata/optd_por_public_all.csv?raw=true'

    >>> myOPTD.unlcPORFileURL()
    'https://github.com/opentraveldata/opentraveldata/blob/master/opentraveldata/optd_por_unlc.csv?raw=true'

    >>> myOPTD.downloadFilesIfNeeded()

    >>> myOPTD.fileSizes()
    (43897966, 4863565)

    >>> myOPTD.extractIATAPORFileHeader()
    'iata_code^icao_code^faa_code^is_geonames^geoname_id^envelope_id^name^asciiname^latitude^longitude^fclass^fcode^page_rank^date_from^date_until^comment^country_code^cc2^country_name^continent_name^adm1_code^adm1_name_utf^adm1_name_ascii^adm2_code^adm2_name_utf^adm2_name_ascii^adm3_code^adm4_code^population^elevation^gtopo30^timezone^gmt_offset^dst_offset^raw_offset^moddate^city_code_list^city_name_list^city_detail_list^tvl_por_list^iso31662^location_type^wiki_link^alt_name_section^wac^wac_name^ccy_code^unlc_list^uic_list^geoname_lat^geoname_lon'

    >>> myOPTD.extractUNLCPORFileHeader()
    'unlocode^latitude^longitude^geonames_id^iso31662_code^iso31662_name^feat_class^feat_code'

    >>> myOPTD.displayFilesHead (3)
    Header of the '/tmp/opentraveldata/optd_por_public_all.csv' file
    iata_code,icao_code,faa_code,is_geonames,geoname_id,envelope_id,name,asciiname,latitude,longitude,fclass,fcode,page_rank,date_from,date_until,comment,country_code,cc2,country_name,continent_name,adm1_code,adm1_name_utf,adm1_name_ascii,adm2_code,adm2_name_utf,adm2_name_ascii,adm3_code,adm4_code,population,elevation,gtopo30,timezone,gmt_offset,dst_offset,raw_offset,moddate,city_code_list,city_name_list,city_detail_list,tvl_por_list,iso31662,location_type,wiki_link,alt_name_section,wac,wac_name,ccy_code,unlc_list,uic_list,geoname_lat,geoname_lon
    ,,,Y,11085,,Bīsheh Kolā,Bisheh Kola,36.18604,53.16789,P,PPL,,,,,IR,,Iran,Asia,35,Māzandarān,Mazandaran,,,,,,0,,1168,Asia/Tehran,3.5,4.5,3.5,2012-01-16,,,,,,C,,fa|بيشه كلا|=fa|Bīsheh Kolā|,632,Iran,IRR,IRBSM|,,,
    ,,,Y,14645,,Kūch Be Masjed-e Soleymān,Kuch Be Masjed-e Soleyman,31.56667,49.53333,P,PPL,,,,,IR,,Iran,Asia,15,Khuzestan,Khuzestan,,,,,,0,,424,Asia/Tehran,3.5,4.5,3.5,2012-01-16,,,,,,C,,fa|Kūch Be Masjed-e Soleymān|,632,Iran,IRR,IRQMJ|,,,
    Header of the '/tmp/opentraveldata/optd_por_unlc.csv' file
    unlocode,latitude,longitude,geonames_id,iso31662_code,iso31662_name,feat_class,feat_code
    ADALV,42.50779,1.52109,3041563,,,P,PPLC
    ADALV,42.51124,1.53358,7730819,,,S,AIRH

    >>> myOPTD.extractPORSubsetFromOPTD()

    >>> import pprint as pp

    >>> pp.pprint (myOPTD.getServingPORList ('IEV'))
    {'original': {'adm1_code': '12',
              'adm1_name_utf': 'Kyiv City',
              'country_code': 'UA',
              'country_name': 'Ukraine',
              'envelope_id': '',
              'geoname_id': 703448,
              'iata_code': 'IEV',
              'location_type': 'C',
              'name': 'Kyiv'},
    'tvl_list': [{'adm1_code': '12',
               'adm1_name_utf': 'Kyiv City',
               'country_code': 'UA',
               'country_name': 'Ukraine',
               'envelope_id': '',
               'geoname_id': 6300960,
               'iata_code': 'IEV',
               'location_type': 'A',
               'name': 'Kyiv Zhuliany International Airport'},
              {'adm1_code': '13',
               'adm1_name_utf': 'Kyiv',
               'country_code': 'UA',
               'country_name': 'Ukraine',
               'envelope_id': '',
               'geoname_id': 6300952,
               'iata_code': 'KBP',
               'location_type': 'A',
               'name': 'Kyiv Boryspil International Airport'},
              {'adm1_code': '13',
               'adm1_name_utf': 'Kyiv',
               'country_code': 'UA',
               'country_name': 'Ukraine',
               'envelope_id': '',
               'geoname_id': 8260936,
               'iata_code': 'QOF',
               'location_type': 'B',
               'name': 'Darnytsia Bus Station'},
              {'adm1_code': '',
               'adm1_name_utf': '',
               'country_code': 'UA',
               'country_name': 'Ukraine',
               'envelope_id': '',
               'geoname_id': 0,
               'iata_code': 'QOH',
               'location_type': 'B',
               'name': 'Kiev UA Hotel Rus'}]}
    
    >>> pp.pprint (myOPTD.getServingPORList ('BAK'))
    {'original': {'adm1_code': '09',
              'adm1_name_utf': 'Baki',
              'country_code': 'AZ',
              'country_name': 'Azerbaijan',
              'envelope_id': '',
              'geoname_id': 587084,
              'iata_code': 'BAK',
              'location_type': 'C',
              'name': 'Baku'},
    'tvl_list': [{'adm1_code': '09',
               'adm1_name_utf': 'Baki',
               'country_code': 'AZ',
               'country_name': 'Azerbaijan',
               'envelope_id': '',
               'geoname_id': 6300924,
               'iata_code': 'GYD',
               'location_type': 'A',
               'name': 'Heydar Aliyev International Airport'},
              {'adm1_code': '09',
               'adm1_name_utf': 'Baki',
               'country_code': 'AZ',
               'country_name': 'Azerbaijan',
               'envelope_id': '',
               'geoname_id': 8521639,
               'iata_code': 'ZXT',
               'location_type': 'A',
               'name': 'Zabrat Airport'}]}

    """
    verbose = False
    local_dir = None
    geo_por_dict = None
    #
    local_iata_por_filename = None
    local_iata_por_filepath = None
    iata_por_file_url = None
    iata_por_dict = None
    #
    local_unlc_por_filename = None
    local_unlc_por_filepath = None
    unlc_por_file_url = None
    unlc_por_dict = None

    def __init__ (self, local_dir = '/tmp/opentraveldata', verbose = False):
       # Vebosity
        self.verbose = verbose

        # Remote URL/file-path for IATA POR
        self.iata_por_file_url = \
           f"{optd_url_base}/{optd_por_all_rel_path}?raw=true"

        # Remote URL/file-path for UN/LOCODE POR
        self.unlc_por_file_url = \
           f"{optd_url_base}/{optd_por_unlc_rel_path}?raw=true"

        # Local copy/file-path, directory and file pointer
        self.local_dir = local_dir

        # For IATA POR
        self.local_iata_por_filename = os.path.basename (optd_por_all_rel_path)
        self.local_iata_por_filepath = \
           f"{self.local_dir}/{self.local_iata_por_filename}"

        # For UN/LOCODE POR
        self.local_unlc_por_filename = os.path.basename (optd_por_unlc_rel_path)
        self.local_unlc_por_filepath = \
           f"{self.local_dir}/{self.local_unlc_por_filename}"

        # Create the local directory if not already existing
        try:
           os.makedirs (self.local_dir, exist_ok = True)
        except:
           err_msg = "[OpenTravelData::init] Error while creating " \
              f"{self.local_dir} directory locally"
           raise OPTDLocalFileError (err_msg)            
         
    def __repr__ (self):
       repr_msg = "OpenTravelData:\n" \
          f"\tLocal IATA/ICAO POR file: {self.local_iata_por_filepath}\n" \
          f"\tLocal UN/LOCODE POR file: {self.local_unlc_por_filepath}"
       return repr_msg
     
    def iataPORFileURL (self):
        return self.iata_por_file_url

    def unlcPORFileURL (self):
        return self.unlc_por_file_url

    def localIATAPORFilepath (self):
        return self.local_iata_por_filepath

    def localUNLCPORFilepath (self):
        return self.local_unlc_por_filepath

    def doLocalFilesExist (self):
       do_files_exist = os.path.isfile (self.local_iata_por_filepath) and \
          os.path.isfile (self.local_unlc_por_filepath)
       return do_files_exist

    def fileSizes (self):
        iata_por_file_size = os.path.getsize (self.local_iata_por_filepath)
        unlc_por_file_size = os.path.getsize (self.local_unlc_por_filepath)
        if self.verbose:
           print ("[Opentraveldata::fileSizes] Sizes - " \
                  f"{self.local_iata_por_filepath}: {iata_por_file_size} ; " \
                  f"{self.local_unlc_por_filepath}: {unlc_por_file_size}")
        return (iata_por_file_size, unlc_por_file_size)

    def deleteLocalFiles (self):
        do_files_exist = self.doLocalFilesExist()
        if do_files_exist:
            if self.verbose:
               print ("[Opentraveldata::deleteLocalFiles] Deleting " \
                      f"{self.local_iata_por_filepath} and  " \
                      f"{self.local_unlc_por_filepath}...")
               os.remove (self.local_iata_por_filepath)
               os.remove (self.local_unlc_por_filepath)

            if verbose:
               print ("[Opentraveldata::deleteLocalFiles] " \
                      f"{self.local_iata_por_filepath} and  " \
                      f"{self.local_unlc_por_filepath} have been deleted")
               
        # Sanity check
        do_files_exist = self.doLocalFilesExist()
        if do_files_exist:
            err_msg = "[OpenTravelData::deleteLocalFiles] The " \
               f"{self.local_iata_por_filepath} and/or  " \
               f"{self.local_unlc_por_filepath} files cannot be deleted"
            raise OPTDLocalFileError (err_msg)
         #
        return

    def downloadIATAPORFile (self):
        """
        Download the IATA POR file from the OpenTravelData (OPTD) GitHub
        repository.
        """
        if self.verbose:
           print ("[OpenTravelData::downloadIATAPORFile] Downloading " \
                  f"{self.local_iata_por_filepath} from " \
                  f"{self.iata_por_file_url}...")

        try:
            with urllib.request.urlopen (self.iata_por_file_url) as response, \
                 open (self.local_iata_por_filepath, 'wb') as out_file:
               shutil.copyfileobj (response, out_file)
        except:
            err_msg = "[OpenTravelData::init] Error while downloading " \
              f"{self.iata_por_file_url} as {self.local_iata_por_filepath}"
            raise OPTDDownloadFileError (err_msg)
         
        if self.verbose:
           file_size = os.path.getsize (self.local_iata_por_filepath)
           print ("[Opentraveldata::downloadIATAPORFile] ... done. " \
                  f"{self.local_iata_por_filepath} - Size: {file_size}")
        return
     
    def downloadUNLCPORFile (self):
        """
        Download the UN/LOCODE POR file from the OpenTravelData (OPTD) GitHub
        repository.
        """
        if self.verbose:
           print ("[OpenTravelData::downloadUNLCPORFile] Downloading " \
                  f"{self.local_unlc_por_filepath} from " \
                  f"{self.unlc_por_file_url}...")

        try:
           with urllib.request.urlopen (self.unlc_por_file_url) as response, \
                open (self.local_unlc_por_filepath, 'wb') as out_file:
              shutil.copyfileobj (response, out_file)
        except:
            err_msg = "[OpenTravelData::init] Error while downloading " \
               f"{self.unlc_por_file_url} as {self.local_unlc_por_filepath}"
            raise OPTDDownloadFileError (err_msg)
         
        if self.verbose:
           file_size = os.path.getsize (self.local_unlc_por_filepath)
           print ("[Opentraveldata::downloadIATAPORFile] ... done. " \
                  f"{self.local_unlc_por_filepath} - Size: {file_size}")
        return
     
    def downloadFilesIfNeeded (self):
        """
        Download the IATA and UN/LOCODE POR files from the
        OpenTravelData (OPTD) GitHub repository, if those files have not
        already been downloaded before and stored locally, and/or if the
        locally stored version of those files is too old.

        As there is no good automatic check for deprecation of those files,
        it is nevertheless advised to call the deleteLocalFiles() method
        from times to times to force the downloading of newer versions.
        """

        # Check whether the OPTD data file has already been downloaded
        do_files_exist = self.doLocalFilesExist()
        if not do_files_exist:
           self.downloadUNLCPORFile()
           self.downloadIATAPORFile()
           
        iata_por_file_size, unlc_por_file_size = self.fileSizes()
        mtime = os.path.getmtime (self.local_iata_por_filepath)
        file_time = datetime.datetime.fromtimestamp (mtime)
        if self.verbose:
           print ("[Opentraveldata::downloadFilesIfNeeded] " \
                  f"{self.local_iata_por_filepath} - Size: " \
                  f"{iata_por_file_size} - " \
                  f"{self.local_unlc_por_filepath} - Size: " \
                  f"{unlc_por_file_size} - " \
                  f"Time-stamp: {file_time}. If those files are too old, " \
                  "you can delete them, e.g. by calling the " \
                  "deleteLocalFiles() method and call again this method " \
                  "(downloadFilesIfNeeded())")
           
        #
        return

    def displayFilesHead (self, lines = 10):
        """
        Display the first 10 lines of the POR files.
        """

        # Download the OPTD data files if needed
        self.downloadFilesIfNeeded()        

        # IATA POR file
        print (f"Header of the '{self.local_iata_por_filepath}' file")
        #
        with open (self.local_iata_por_filepath, newline='') as csvfile:
            file_reader = csv.reader (csvfile, delimiter='^')
            for i in range (lines):
               print (','.join(file_reader.__next__()))

        # UN/LOCODE POR file
        print (f"Header of the '{self.local_unlc_por_filepath}' file")
        #
        with open (self.local_unlc_por_filepath, newline='') as csvfile:
            file_reader = csv.reader (csvfile, delimiter='^')
            for i in range (lines):
               print (','.join(file_reader.__next__()))

        #
        return

    def extractIATAPORFileHeader (self):
        """
        Extract the header of the IATA POR file.
        """

        # Download the OPTD data files if needed
        self.downloadFilesIfNeeded()        
        
        # IATA POR
        header_line_iata_por = ''
        with open (self.local_iata_por_filepath) as tmpfile:
           header_line_iata_por = tmpfile.readline().strip()
           
        #
        return header_line_iata_por

    def extractUNLCPORFileHeader (self):
        """
        Extract the header of the UN/LOCODE POR file.
        """

        # Download the OPTD data files if needed
        self.downloadFilesIfNeeded()        
        
        # UN/LOCODE POR
        header_line_unlc_por = ''
        with open (self.local_unlc_por_filepath) as tmpfile:
           header_line_unlc_por = tmpfile.readline().strip()
           
        #
        return header_line_unlc_por

    def extractPORSubsetFromOPTD (self):
        """
        Extract a few details from the OpenTravelData (OPTD)
        POR (points of reference)
        """

        # If the dictionaries have already been initialized, just move on,
        # no need to re-initialize it
        if not self.iata_por_dict:
           # Sanity check: either both POR dictionaries should have been
           # initialized, or none. But one dictionary cannot have been
           # initialized, while the other was not
            err_msg = "[OpenTravelData::extractPORSubsetFromOPTD] " \
               "Consistency error with the two POR dictionaries"
            assert not self.unlc_por_dict, err_msg
            assert not self.geo_por_dict, err_msg
            
            #
            self.iata_por_dict = dict()
            self.unlc_por_dict = dict()
            self.geo_por_dict = dict()
        else:
            return

        # Download the OPTD data files if needed
        self.downloadFilesIfNeeded()        

        # Reporting
        if self.verbose:
           print ("[OpenTravelData::extractPORSubsetFromOPTD] Extracting " \
                  f"POR dictionaries from {self.local_iata_por_filepath} " \
                  f"and {self.local_unlc_por_filepath}...")
           
        # OPTD-maintained list of POR
        with open (self.local_iata_por_filepath, newline='') as csvfile:
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

                # UN/LOCODE POR dictionary
                # There may be several POR (points of reference)
                # with the same UN/LOCODE code. The Geonames ID
                # then allows to differentiate them
                for unlc in unlc_list:
                    if not unlc in self.unlc_por_dict:
                       self.unlc_por_dict[unlc] = dict()

                    self.unlc_por_dict[unlc][optd_geo_id] = optd_por_rec
                    
                # Geonames POR dictionary
                # There is a single POR (point of reference)
                # for a specific Geonames ID.
                if not optd_geo_id in self.geo_por_dict:
                   self.geo_por_dict[optd_geo_id] = optd_por_rec
                   
                # IATA POR dictionary
                # Only the POR with a IATA code are interesting
                # from this stage onwards
                if optd_por_code == '':
                    continue
                 
                # There may be several POR (points of reference)
                # with the same IATA code. The location type (e.g.,
                # 'C' for city, 'A' for airrport) then allows
                # to differentiate them
                if not optd_por_code in self.iata_por_dict:
                   self.iata_por_dict[optd_por_code] = dict()

                self.iata_por_dict[optd_por_code][optd_loc_type] = optd_por_rec

        #
        return

    def isAirport (self, loc_type = None):
        """
        That method states whether the lcation type corresponds
        to an airport
        """
        is_airport = re.search ("A", loc_type)
        return is_airport
     
    def isHeliport (self, loc_type = None):
        """
        That method states whether the lcation type corresponds
        to an heliport
        """
        is_heliport = re.search ("H", loc_type)
        return is_heliport
     
    def isPort (self, loc_type = None):
        """
        That method states whether the lcation type corresponds
        to a maritime/river port
        """
        is_port = re.search ("P", loc_type)
        return is_port
     
    def isRailwayStation (self, loc_type = None):
        """
        That method states whether the lcation type corresponds
        to a railway station
        """
        is_railway_station = re.search ("R", loc_type)
        return is_railway_station
     
    def isBusStation (self, loc_type = None):
        """
        That method states whether the lcation type corresponds
        to a bus station
        """
        is_bus_station = re.search ("B", loc_type)
        return is_bus_station
     
    def isOffline (self, loc_type = None):
        """
        That method states whether the lcation type corresponds
        to an offline point
        """
        is_offpoint = re.search ("O", loc_type)
        return is_offpoint
     
    def isTransportRelated (self, loc_type = None):
        """
        That method states whether the lcation type corresponds
        to a serving POR wrt travel or transport
        """
        is_tvl = self.isAirport (loc_type) or self.isHeliport (loc_type) \
           or self.isPort (loc_type) or self.isRailwayStation (loc_type) \
           or self.isBusStation (loc_type) or self.isOffline (loc_type)
        return is_tvl
     
    def isCity (self, loc_type = None):
        """
        That method states whether the lcation type corresponds
        to a city
        """
        is_city = re.search ("C", loc_type) or re.search ("O", loc_type)
        return is_city

    def getPORByGeoID (self, por_geo_id):
        """
        Retrieve the POR (point of reference) corresponding to a specific
        Geonames ID.
        The POR may be browsed online through:
        https://geonames.org/<geonames-id>
        """
        optd_por_rec = None
       
        # If the dictionary is still empty, initialize it
        if not self.geo_por_dict:
           self.extractPORSubsetFromOPTD()

        #
        if por_geo_id in self.geo_por_dict:
           optd_por_rec = self.geo_por_dict[por_geo_id]
        else:
            if self.verbose:
               print ("[OpenTravelData::getPORByGeoID] Error - A POR with " \
                      f"{por_geo_id} as Geonames ID cannot be found in OPTD")

        return optd_por_rec

    def isPORRecInTvlList (self, tvl_list, tvl_sht_rec):
        is_in_list = False

        for tvl_rec in tvl_list:
            if tvl_rec == tvl_sht_rec:
               is_in_list = True
               return is_in_list
             
        return is_in_list
     
    def getServingPORList (self, por_code = 'FRA',
                           only_when_city_code_differs = True):
        """
        Derive the list of travel-/transport-related POR (point of reference)
        IATA codes for a given city IATA code.

        Not implemented yet -- Just an idea
        only_when_city_code_differs: whether or not that method should return
        the travel-/transport-related POR only when the city IATA code
        differs from the IATA codes of those serving POR.
        For instance:
        - When that parameter is set to True,
          getServingPORList('IEV') will return {'IEV'} only
        - When that parameter is set to True,
          getServingPORList('IEV') will return {'IEV', 'KBP'}
        And getServingPORList('CHI') will always return
          {'DPA', 'MDW', 'ORD', 'PWK', 'RFD'}
        """
       
        # If the dictionary is still empty, initialize it
        if not self.iata_por_dict:
           self.extractPORSubsetFromOPTD()

        # Initialize the return structure (list)
        original_por_rec = {'iata_code': por_code, 'location_type': None,
                            'geoname_id': None, 'envelope_id': None,
                            'name': None,
                            'country_code': None, 'country_name': None,
                            'adm1_code': None, 'adm1_name_utf': None}
        tvl_list = []
        srv_dict = {'original': original_por_rec, 'tvl_list': tvl_list}

        # Retrieve the OPTD POR corresponding to the given POR IATA code
        if not por_code in self.iata_por_dict:
           err_msg = f"[OpenTravelData::getAirportList] The {por_code} " \
              "IATA code does not seem to be valid in OPTD"
           raise OPTDIATACodeError (err_msg)

        optd_por_rec_dict = self.iata_por_dict[por_code]
        have_city_details_been_set = False
        for optd_loc_type, optd_por_rec in optd_por_rec_dict.items():
           # Retrieve the details of the POR
           geo_id = optd_por_rec['geoname_id']
           geo_id = int (geo_id)
           env_id = optd_por_rec['envelope_id']
           por_name = optd_por_rec['name']
           ctry_code = optd_por_rec['country_code']
           ctry_name = optd_por_rec['country_name']
           adm1_code = optd_por_rec['adm1_code']
           adm1_name_utf = optd_por_rec['adm1_name_utf']
           
           # If the POR is transport-related, add it to the target list
           # (tvl_list), if not already there.
           is_transport_related = self.isTransportRelated (optd_loc_type)
           if is_transport_related:
              tvl_sht_rec = {'iata_code': por_code,
                             'location_type': optd_loc_type,
                             'geoname_id': geo_id,
                             'envelope_id': env_id,
                             'name': por_name,
                             'country_code': ctry_code,
                             'country_name': ctry_name,
                             'adm1_code': adm1_code,
                             'adm1_name_utf': adm1_name_utf}
              
              # Add to the list only if not already there
              if not self.isPORRecInTvlList (tvl_list, tvl_sht_rec):
                 tvl_list.append (tvl_sht_rec)

              # If the details for a city have not already been set,
              # update the original POR details (as it may not be a city,
              # like for instance CDG, LHR or ORD)
              if not have_city_details_been_set:
                 original_por_rec['location_type'] = optd_loc_type
                 original_por_rec['geoname_id'] = geo_id
                 original_por_rec['envelope_id'] = env_id
                 original_por_rec['name'] = por_name
                 original_por_rec['country_code'] = ctry_code
                 original_por_rec['country_name'] = ctry_name
                 original_por_rec['adm1_code'] = adm1_code
                 original_por_rec['adm1_name_utf'] = adm1_name_utf
                 
           # When the POR is a city (e.g., BAK, IEV), the list
           # of airports, among the list of serving
           # travel-/transport-related points, have to be retrieved.
           # Note that non-airport POR (e.g., railway stations, ports)
           # may also serve a given city.
           is_city = re.search ("C", optd_loc_type)

           # When the POR is not city (and can no longer be a
           # transport-/travel-related serving POR, or an offline point,
           # as those cases have been handled above), there is no
           # travel-/transport-related serving POR, by definition.
           if not is_city: continue

           # The update of the details for the (city) POR has to be done once.
           # Example of multiple city POR having the same IATA code: RDU
           if have_city_details_been_set: continue
           
           # Record that the details for the city POR will have been set (once
           # the following code will be executed)
           have_city_details_been_set = True
           original_por_rec['location_type'] = optd_loc_type
           original_por_rec['geoname_id'] = geo_id
           original_por_rec['envelope_id'] = env_id
           original_por_rec['name'] = por_name
           original_por_rec['country_code'] = ctry_code
           original_por_rec['country_name'] = ctry_name
           original_por_rec['adm1_code'] = adm1_code
           original_por_rec['adm1_name_utf'] = adm1_name_utf
           
           # Derive the serving travel-/transport-related points
           tvl_por_list = optd_por_rec['tvl_por_list']
           
           for tvl_por_code in tvl_por_list:
              if not tvl_por_code in self.iata_por_dict:
                 err_msg = "[OpenTravelData::getAirportList] The " \
                    f"{tvl_por_code} IATA code (transport-related), " \
                    f"serving {por_code} (city), does not seem " \
                    "to be valid in OPTD"
                 raise OPTDIATACodeError (err_msg)

              # Browse the various location types for that IATA code
              tvl_por_rec_dict = self.iata_por_dict[tvl_por_code]
              for tvl_loc_type, tvl_por_rec in tvl_por_rec_dict.items():
                 # From the full POR record, retrieve the Geonames ID
                 is_transport_related = self.isTransportRelated (tvl_loc_type)
                 if is_transport_related:
                    # Retrieve the Geonames ID and the envelope ID
                    geo_id = tvl_por_rec['geoname_id']
                    geo_id = int (geo_id)
                    env_id = tvl_por_rec['envelope_id']
                    por_name = tvl_por_rec['name']
                    ctry_code = tvl_por_rec['country_code']
                    ctry_name = tvl_por_rec['country_name']
                    adm1_code = tvl_por_rec['adm1_code']
                    adm1_name_utf = tvl_por_rec['adm1_name_utf']

                    # Insert into the target list (tvl_list)
                    # only if not already present there
                    # As dictionaries are not hashables,
                    # a direct comparison cannot be made
                    tvl_sht_rec = {'iata_code': tvl_por_code,
                                   'location_type': tvl_loc_type,
                                   'geoname_id': geo_id,
                                   'envelope_id': env_id,
                                   'name': por_name,
                                   'country_code': ctry_code,
                                   'country_name': ctry_name,
                                   'adm1_code': adm1_code,
                                   'adm1_name_utf': adm1_name_utf}

                    # Add to the list only if not already there
                    if not self.isPORRecInTvlList (tvl_list, tvl_sht_rec):
                       tvl_list.append (tvl_sht_rec)

        #
        return srv_dict

