
import os, setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='opentraveldata',
    version='0.0.8.post1',
    author='Denis Arnaud',
    author_email='denis.arnaud_pypi@m4x.org',
    description=('''Simple Python wrapper for OpenTravelata (OPTD)'''),
    license='MIT',
    keywords='api python optd opentraveldata package',
    url='https://github.com/opentraveldata/python-opentraveldata',
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'python-dateutil',
        'pytz'
    ],
)

