#!/usr/bin/python

import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'cloud-insight'
DESCRIPTION = 'Simplifies the tracking of docker container versions,' \
              ' health and other important information across various platforms.'
URL = 'https://github.com/noahjohnhay/cloud-insight'
EMAIL = "noahjohnhay@gmail.com"
AUTHOR = 'Noah Hay'

here = os.path.abspath(os.path.dirname(__file__))

REQUIRED = [
    'boto3',
    'colorlog',
    'cement==2.10.12',
    'plotly',
    'PrettyTable'
]

setup(
    name=NAME,
    version='1.0.0',
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    entry_points={
         'console_scripts': ['cloud-insight=cloud_insight.cli:main'],
     },
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
