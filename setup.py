# Copyright (C) 2015 Twitter, Inc.

import os
import sys
from setuptools import setup, find_packages

DESCRIPTION = 'A Twitter supported and maintained Ads API SDK for Python.'
LONG_DESCRIPTION = None
URL = 'http://twitterdev.github.io/twitter-python-ads-sdk/'
DOWNLOAD_URL = 'https://github.com/twitterdev/twitter-python-ads-sdk/tarball/master'


def get_version(version_tuple):
    if not isinstance(version_tuple[-1], int):
        return '.'.join(map(str, version_tuple[:-1])) + version_tuple[-1]
    return '.'.join(map(str, version_tuple))

init = os.path.join(os.path.dirname(__file__), 'twitter_ads', '__init__.py')
version_line = list(filter(lambda l: l.startswith('VERSION'), open(init)))[0]

VERSION = get_version(eval(version_line.split('=')[-1]))

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Internet',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

extra_opts = {
    'setup_requires': ['pytest-runner'],
    'tests_require': ['pytest', 'responses', 'mock']
}

if sys.version_info[0] != 3:
    extra_opts['setup_requires'].append('flake8<=2.6.2')

setup(
    name='twitter-ads',
    version=VERSION,
    author='Brandon Black, Jacob Petrie',
    author_email='bblack@twitter.com, jpetrie@twitter.com',
    url=URL,
    download_url=DOWNLOAD_URL,
    license='MIT',
    include_package_data=True,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    classifiers=CLASSIFIERS,
    scripts=['bin/twitter-ads'],
    install_requires=['pyyaml', 'requests-oauthlib', 'python-dateutil'],
    packages=find_packages(exclude=['docs', 'tests']),
    **extra_opts
)
