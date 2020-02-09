OpenTravelData (OPTD) Data Wrapper - Python Bindings
====================================================

[![Docker Repository on Quay](https://quay.io/repository/opentraveldata/quality-assurance/status "Docker Repository on Quay")](https://quay.io/repository/opentraveldata/quality-assurance)

Python wrapper around OpenTravelData (OPTD) data sets, for instance
to be used by Python software needing to access OPTD data.

# References
* OpenTravelData (OPTD):
  + Source code on GitHub: https://opentraveldata/opentraveldata
  + Docker Cloud repository: https://cloud.docker.com/u/opentraveldata/repository/docker/opentraveldata/quality-assurance
  + This Python-wrapper Git repository: https://github.com/opentraveldata/python-opentraveldata
* OPTD data archive:
  + POR (Points of Reference)): https://www2.transport-search.org/data/optd/por/
* OPTD Quality Assurance (QA):
  + Sourcce code on GitHub: https://github.com/opentraveldata/quality-assurance

## Python
* [How-to install Python virtual environment with `pyenv` and `pipenv`](https://github.com/machine-learning-helpers/induction-python/tree/master/installation/virtual-env)
* [How to package modules for Python](https://packaging.python.org/tutorials/packaging-projects/)
* PyPi - Deployment with Travis CI
  + [PyPi Travis CI provider](https://github.com/travis-ci/dpl#pypi)
  + [dpl v2](https://blog.travis-ci.com/2019-08-27-deployment-tooling-dpl-v2-preview-release)
  + [dpl v1](https://docs.travis-ci.com/user/deployment/pypi/)

# Installation - configuration

## Python
* Reference: How-to install Python virtual environment with `pyenv`
  and `pipenv`:
  https://github.com/machine-learning-helpers/induction-python/tree/master/installation/virtual-env

* Install Pyenv, Python 3.8.1, `pip` and `pipenv`:
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
user@laptop$ pyenv install 3.81 && pyenv global 3.8.1 && pip install -U pip pipenv && pyenv global system
```

* Clone the Git repository and install the Python virtual environment
  (with `pipenv`):
```bash
user@laptop$ mkdir -p ~/dev/geo && \
  git clone https://github.com/opentraveldata/python-opentraveldata.git ~/dev/geo/python-opentraveldata
user@laptop$ cd ~/dev/geo/python-opentraveldata
user@laptop$ pipenv --rm && pipenv install && pipenv install --dev
user@laptop$ python --version
Python 3.8.1
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
creating opentraveldata-0.0.1
...
creating dist
Creating tar archive
removing 'opentraveldata-0.0.1' (and everything under it)
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
adding 'opentraveldata-0.0.1.dist-info/METADATA'
adding 'opentraveldata-0.0.1.dist-info/WHEEL'
adding 'opentraveldata-0.0.1.dist-info/top_level.txt'
adding 'opentraveldata-0.0.1.dist-info/RECORD'
removing build/bdist.macosx-10.15-x86_64/wheel

user@laptop$ ls -lFh dist/
total 32
total 32
-rw-r--r--  1 user  staff 6.6K Feb  9 18:53 opentraveldata-0.0.1-py3-none-any.whl
-rw-r--r--  1 user  staff 7.9K Feb  9 18:53 opentraveldata-0.0.1.tar.gz
```

* Upload/release the Python packages onto the
  [PyPi test repository](https://test.pypi.org):
```bash
user@laptop$ PYPIURL="https://test.pypi.org"
user@laptop$ pipenv run twine upload -u __token__ --repository-url ${PYPIURL}/legacy/ dist/*
Uploading distributions to https://test.pypi.org/legacy/
Uploading opentraveldata-0.0.1-py3-none-any.whl
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 15.7k/15.7k [00:02<00:00, 7.43kB/s]
Uploading opentraveldata-0.0.1.tar.gz
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 16.3k/16.3k [00:01<00:00, 15.1kB/s]

View at: https://test.pypi.org/project/opentraveldata/0.0.1/
```

* Upload/release the Python packages onto the
  [PyPi repository](https://pypi.org):
```bash
user@laptop$ PYPIURL="https://pypi.org"
user@laptop$ pipenv run keyring set ${PYPIURL}/ __token__
Password for '__token__' in '${PYPIURL}/':
user@laptop$ pipenv run twine upload -u __token__ --non-interactive dist/*
Uploading distributions to https://pypi.org/
Uploading opentraveldata-0.0.1-py3-none-any.whl
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 18.2k/18.2k [00:03<00:00, 5.99kB/s]
Uploading opentraveldata-0.0.1.tar.gz
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 19.0k/19.0k [00:01<00:00, 10.9kB/s]

View at: https://pypi.org/project/opentraveldata/0.0.1/
```

# Test the Python module
* Launch the test:
```bash
$ pipenv run python test_optd.py 
```


