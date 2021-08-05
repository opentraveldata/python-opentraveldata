OpenTravelData (OPTD) Data Wrapper - Python Bindings
====================================================

[![Docker Repository on Quay](https://quay.io/repository/opentraveldata/quality-assurance/status "Docker Repository on Quay")](https://quay.io/repository/opentraveldata/quality-assurance)

Python wrapper around OpenTravelData (OPTD) data sets, for instance
to be used by Python software needing to access OPTD data.

# References
* PyPi artifacts: https://pypi.org/project/opentraveldata/
* OpenTravelData (OPTD):
  + Source code on GitHub: https://github.com/opentraveldata/opentraveldata
  + Docker Cloud repository: https://cloud.docker.com/u/opentraveldata/repository/docker/opentraveldata/quality-assurance
  + This Python-wrapper Git repository: https://github.com/opentraveldata/python-opentraveldata
* OPTD data archive:
  + POR (Points of Reference)): https://www2.transport-search.org/data/optd/por/
  + CI/CD deliveries: https://www2.transport-search.org/data/optd/cicd/
* OPTD Quality Assurance (QA):
  + Sourcce code on GitHub: https://github.com/opentraveldata/quality-assurance
  + Quality Assurance (QA) reports: https://www2.transport-search.org/data/optd/qa/

## Python
* [How-to install Python virtual environment with `pyenv` and `pipenv`](https://github.com/machine-learning-helpers/induction-python/tree/master/installation/virtual-env)
* [How to package modules for Python](https://packaging.python.org/tutorials/packaging-projects/)
* PyPi - Deployment with Travis CI
  + [PyPi Travis CI provider](https://github.com/travis-ci/dpl#pypi)
  + [dpl v2](https://blog.travis-ci.com/2019-08-27-deployment-tooling-dpl-v2-preview-release)
  + [dpl v1](https://docs.travis-ci.com/user/deployment/pypi/)

# Usage

* Launch a Python interpreter:
```bash
$ python
```
```python
>>> 
```

* Import the `opentraveldata` library:
```python
>>> import opentraveldata
```

* Specify a variable, say `myOPTD`, as a handle on the OPTD library
  + With the default local directory for the data files,
    that is `/tmp/opentraveldata`
```python
>>> myOPTD = opentraveldata.OpenTravelData()
```
  +  If you do not have access rights for writing into that directory,
     initialize the `OpenTravelData` object with a directory on which
	 you have writing access rights:
```python
>>> myOPTD = opentraveldata.OpenTravelData(local_dir='/directory-on-which-you-have-writing-access-rights')
```

* Display some information about the `OpenTravelData` object:
```python
>>> myOPTD
OpenTravelData:
  Local IATA/ICAO POR file: /tmp/opentraveldata/optd_por_public_all.csv
  Local UN/LOCODE POR file: /tmp/opentraveldata/optd_por_unlc.csv
```

* Display the expected location of the data files
  + For the main (IATA/ICAO) POR (points of reference) data file:
```python
>>> myOPTD.localIATAPORFilepath()
'/tmp/opentraveldata/optd_por_public_all.csv'
```
  + For the UN/LOCODE POR (points of reference) data file:
```python
>>> myOPTD.localUNLCPORFilepath()
'/tmp/opentraveldata/optd_por_unlc.csv'
```

* Display the source URL of the data files
  + For the main (IATA/ICAO) POR (points of reference) data file:
```python
>>> myOPTD.iataPORFileURL()
'https://github.com/opentraveldata/opentraveldata/blob/master/opentraveldata/optd_por_public_all.csv?raw=true'
```
  + For the UN/LOCODE POR (points of reference) data file:
```python
>>> myOPTD.unlcPORFileURL()
'https://github.com/opentraveldata/opentraveldata/blob/master/opentraveldata/optd_por_unlc.csv?raw=true'
```

* Download the latest data files (to be done once in a while; it takes
  a few seconds, depending on the network bandwidth):
```python
>>> myOPTD.downloadFilesIfNeeded()
```

* Trigger an exception if the data files have not been properly downloaded:
```python
>>> myOPTD.assumeFilesExist()
```

* Check that the data files have been properly downloaded, and that their
  sizes are as expected (40 to 50 MB for the IATA/ICAO data file and 4 to 5 MB
  for the UN/LOCODE data file):
```python
>>> myOPTD.validateFileSizes()
True
```

* Display the sizes of the data files
  + In Bytes:
```python
>>> myOPTD.fileSizes()
(44432069, 4956451)
```
  + In MB:
```python
>>> myOPTD.humanFileSizes()
('42.37 MB', '4.73 MB')
```

* Display the headers of the data files
  + IATA/ICAO data file:
```python
>>> myOPTD.extractIATAPORFileHeader()
'iata_code^icao_code^faa_code^is_geonames^geoname_id^envelope_id^name^asciiname^latitude^longitude^fclass^fcode^page_rank^date_from^date_until^comment^country_code^cc2^country_name^continent_name^adm1_code^adm1_name_utf^adm1_name_ascii^adm2_code^adm2_name_utf^adm2_name_ascii^adm3_code^adm4_code^population^elevation^gtopo30^timezone^gmt_offset^dst_offset^raw_offset^moddate^city_code_list^city_name_list^city_detail_list^tvl_por_list^iso31662^location_type^wiki_link^alt_name_section^wac^wac_name^ccy_code^unlc_list^uic_list^geoname_lat^geoname_lon'
```
  + UN/LOCODE data file:
```python
>>> myOPTD.extractUNLCPORFileHeader()
'unlocode^latitude^longitude^geonames_id^iso31662_code^iso31662_name^feat_class^feat_code'
```

* Display the first few lines (here, 3 lines) of the data files:
```python
>>> myOPTD.displayFilesHead (3)
Header of the '/tmp/opentraveldata/optd_por_public_all.csv' file
iata_code,icao_code,faa_code,is_geonames,geoname_id,envelope_id,name,asciiname,latitude,longitude,fclass,fcode,page_rank,date_from,date_until,comment,country_code,cc2,country_name,continent_name,adm1_code,adm1_name_utf,adm1_name_ascii,adm2_code,adm2_name_utf,adm2_name_ascii,adm3_code,adm4_code,population,elevation,gtopo30,timezone,gmt_offset,dst_offset,raw_offset,moddate,city_code_list,city_name_list,city_detail_list,tvl_por_list,iso31662,location_type,wiki_link,alt_name_section,wac,wac_name,ccy_code,unlc_list,uic_list,geoname_lat,geoname_lon
,,,Y,11085,,Bīsheh Kolā,Bisheh Kola,36.18604,53.16789,P,PPL,,,,,IR,,Iran,Asia,35,Māzandarān,Mazandaran,,,,,,0,,1168,Asia/Tehran,3.5,4.5,3.5,2012-01-16,,,,,,C,,fa|بيشه كلا|=fa|Bīsheh Kolā|,632,Iran,IRR,IRBSM|,,,
,,,Y,14645,,Kūch Be Masjed-e Soleymān,Kuch Be Masjed-e Soleyman,31.56667,49.53333,P,PPL,,,,,IR,,Iran,Asia,15,Khuzestan,Khuzestan,,,,,,0,,424,Asia/Tehran,3.5,4.5,3.5,2012-01-16,,,,,,C,,fa|Kūch Be Masjed-e Soleymān|,632,Iran,IRR,IRQMJ|,,,
Header of the '/tmp/opentraveldata/optd_por_unlc.csv' file
unlocode,latitude,longitude,geonames_id,iso31662_code,iso31662_name,feat_class,feat_code
ADALV,42.50779,1.52109,3041563,,,P,PPLC
ADALV,42.51124,1.53358,7730819,,,S,AIRH
```

* Parse the data files and load their content into internal Python
  dictionaries:
```python
>>> myOPTD.extractPORSubsetFromOPTD()
```

* Retrieve the details for the `IEV` code:
```python
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
```

# Installation - configuration

## Python
* Reference: How-to install Python virtual environment with `pyenv`
  and `pipenv`:
  https://github.com/machine-learning-helpers/induction-python/tree/master/installation/virtual-env

* Install Pyenv, Python 3.9.6, `pip` and `pipenv`:
```bash
user@laptop$ if [ ! -d ${HOME}/.pyenv ]; then git clone https://github.com/pyenv/pyenv.git ${HOME}/.pyenv; else pushd ${HOME}/.pyenv && git pull && popd; fi
user@laptop$ cat >> ~/.bashrc << _EOF
# Python
# git clone https://github.com/pyenv/pyenv.git \${HOME}/.pyenv
export PATH="\${HOME}/.pyenv/shims:\${PATH}"
eval "\$(pyenv init -)"
eval "\$(pipenv --completion)"
 
_EOF
user@laptop$ . ~/.bashrc
user@laptop$ pyenv install 3.9.6 && pyenv global 3.9.6 && pip install -U pip pipenv && pyenv global
```

* Clone the Git repository and install the Python virtual environment
  (with `pipenv`):
```bash
user@laptop$ mkdir -p ~/dev/geo && \
  git clone https://github.com/opentraveldata/python-opentraveldata.git ~/dev/geo/python-opentraveldata
user@laptop$ cd ~/dev/geo/python-opentraveldata
user@laptop$ pipenv --rm && pipenv install && pipenv install --dev
user@laptop$ pipenv shell
(python-opentraveldata-BScCAakO)$ python --version
Python 3.9.6
(python-opentraveldata-BScCAakO)$ exit
```

## PyPi credentials for Travis deployment
* Encrypt the PyPi API token with the Travis command-line utility,
  which stores the encrypted `secret` token. As the project is managed
  by `travis-ci.com`, the `--com` option has to be added in the command-line:
```bash
user@laptop$ travis encrypt pypi-NotARealKey_Xo -add deploy.password --com
user@laptop$ git add .travis.yml
```

# Package and release the Python module
* Launch the `setup.py` script:
```bash
user@laptop$ rm -rf dist && mkdir dist
user@laptop$ pipenv run python setup.py sdist bdist_wheel
running sdist
running egg_info
creating opentraveldata.egg-info
...
running check
creating opentraveldata-0.0.9
...
creating dist
Creating tar archive
removing 'opentraveldata-0.0.9' (and everything under it)
running bdist_wheel
...
creating build
...
installing to build/bdist.macosx-10.15-x86_64/wheel
running install
running install_lib
...
running install_egg_info
adding 'opentraveldata/__init__.py'
adding 'opentraveldata/csvwriter.py'
adding 'opentraveldata/opentraveldata.py'
adding 'opentraveldata-0.0.9.dist-info/METADATA'
adding 'opentraveldata-0.0.9.dist-info/WHEEL'
adding 'opentraveldata-0.0.9.dist-info/top_level.txt'
adding 'opentraveldata-0.0.9.dist-info/RECORD'
removing build/bdist.macosx-11.1-x86_64/wheel

user@laptop$ ls -lFh dist/
total 136
-rw-r--r--  1 user  staff 14K Aug  5 18:52 opentraveldata-0.0.9-py3-none-any.whl
-rw-r--r--  1 user  staff 52K Aug  5 18:52 opentraveldata-0.0.9.tar.gz
```

* Upload/release the Python packages onto the
  [PyPi test repository](https://test.pypi.org):
```bash
user@laptop$ PYPIURL="https://test.pypi.org"
user@laptop$ pipenv run twine upload -u __token__ --repository-url ${PYPIURL}/legacy/ dist/*
Uploading distributions to https://test.pypi.org/legacy/
Uploading opentraveldata-0.0.9-py3-none-any.whl
100%|█████████████████████████████████████████████████████████████████████| 23.7k/23.7k [00:01<00:00, 13.5kB/s]
Uploading opentraveldata-0.0.9.tar.gz
100%|█████████████████████████████████████████████████████████████████████| 44.3k/44.3k [00:01<00:00, 41.2kB/s]

View at: https://test.pypi.org/project/opentraveldata/0.0.9/
```

* Upload/release the Python packages onto the
  [PyPi repository](https://pypi.org):
```bash
user@laptop$ PYPIURL="https://pypi.org"
user@laptop$ pipenv run keyring set ${PYPIURL}/ __token__
Password for '__token__' in '${PYPIURL}/':
user@laptop$ pipenv run twine upload -u __token__ --non-interactive dist/*
Uploading distributions to https://upload.pypi.org/legacy/
Uploading opentraveldata-0.0.9-py3-none-any.whl
100%|██████████████████████████████████████████████████████████████████████| 23.7k/23.7k [00:01<00:00, 15.2kB/s]
Uploading opentraveldata-0.0.9.tar.gz
100%|██████████████████████████████████████████████████████████████████████| 44.3k/44.3k [00:01<00:00, 44.7kB/s]

View at:
https://pypi.org/project/opentraveldata/0.0.9/
```

# Test the Python module

## Pytest
* Launch the test:
```bash
$ pipenv run pytest test_optd-csvwriter.py
======================= test session starts =============================
platform darwin -- Python 3.9.5, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: ~/dev/geo/python-opentraveldata
collected 3 items                                                     

test_optd-csvwriter.py .                                           [ 33%]
test_optd-serving-por.py ..                                        [100%]

=============================== 3 passed in 2.58s =======================
_________________________________ summary _____________________________
```

## Tox

```bash
$ pipenv run tox
.package recreate: ~/dev/geo/python-opentraveldata/.tox/.package
.package installdeps: setuptools >= 35.0.2, setuptools_scm >= 2.0.0, <3
py39 create: ~/dev/geo/python-opentraveldata/.tox/py39
py39 installdeps: pytest
py39 inst: ~/dev/geo/python-opentraveldata/.tox/.tmp/package/1/opentraveldata-0.0.9.tar.gz
py39 installed: attrs==19.3.0,certifi==2019.11.28,chardet==3.0.4,idna==2.9,more-itertools==8.2.0,opentraveldata==0.0.9,packaging==20.3,pluggy==0.13.1,py==1.8.1,pyparsing==2.4.6,pytest==5.3.5,python-dateutil==2.8.1,pytz==2019.3,requests==2.23.0,six==1.14.0,urllib3==1.25.8,wcwidth==0.1.8
py39 run-test-pre: PYTHONHASHSEED='3773488260'
py39 run-test: commands[0] | pytest
======================= test session starts =============================
platform darwin -- Python 3.9.5, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
cachedir: .tox/py39/.pytest_cache
rootdir: ~/dev/geo/python-opentraveldata
collected 3 items                                                     

test_optd-csvwriter.py .                                           [ 33%]
test_optd-serving-por.py ..                                        [100%]

=============================== 3 passed in 2.58s =======================
_________________________________ summary _____________________________
  py39: commands succeeded
  congratulations :)

```

