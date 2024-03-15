#!/usr/bin/env python

from __future__ import absolute_import

from setuptools import find_packages, setup

import pywebdav

long_desc = open("README.rst").read()

setup(name='m9s-PyWebDAV3',
    description='WebDAV library for Python3',
    long_description=long_desc,
    author=pywebdav.__author__,
    author_email=pywebdav.__email__,
    maintainer='MBSolutions',
    maintainer_email='info@m9s.biz',
    project_urls={
            "Bug Tracker": 'https://support.m9s.biz/',
            "Source Code": 'https://gitlab.com/m9s/webdav.git',
            },
    platforms=['Unix', 'Windows'],
    license=pywebdav.__license__,
    version=pywebdav.__version__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
    keywords=[
        'webdav',
        'Tryton',
        'GNUHealth',
        'server',
        'dav',
        'standalone',
        'library',
        'gpl',
        'http',
        'rfc2518',
        'rfc 2518'
        ],
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        'console_scripts': ['davserver = pywebdav.server.server:run']
    },
    tests_require=['pytest'],
    )
