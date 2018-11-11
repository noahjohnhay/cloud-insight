#!/usr/bin/python

import os
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='cloud-insight',
    version='1.0.0',
    description='',
    author='Noah Hay',
    author_email='noahjohnhay@gmail.com',
    url='https://github.com/noahjohnhay/cloud-insight',
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': ['cloud-insight=cloud_insight.cli:main'],
     },
    install_requires=[
        'boto3',
        'colorlog',
        'cement==2.10.12',
        'plotly==2.7.0',
        'PrettyTable',
        'urllib3<=1.23',
        'botocore',
        'flask-cors',
        'flask'
    ],
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
