#!/usr/bin/env python

"""Install algebraixlib or builds its installation package."""

<<<<<<< HEAD
# $Id: setup.py 22842 2015-08-21 17:48:54Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-08-21 12:48:54 -0500 (Fri, 21 Aug 2015) $
=======
# $Id: setup.py 22690 2015-07-27 20:23:37Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-27 15:23:37 -0500 (Mon, 27 Jul 2015) $
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
#
# This file is part of algebraixlib <http://github.com/AlgebraixData/algebraixlib>.
#
# algebraixlib is free software: you can redistribute it and/or modify it under the terms of version
# 3 of the GNU Lesser General Public License as published by the Free Software Foundation.
#
# algebraixlib is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with algebraixlib.
# If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------
from sys import version_info, exit
from setuptools import setup

# Check python version
python_version = str(version_info[0]) + '.' + str(version_info[1]) + '.' + str(version_info[2])
if version_info < (3, 0):
    exit('The current Python Version is ' + python_version + '. '
         + 'This library requires Python Version 3. Exiting.')
elif version_info < (3, 4):
    print('Warning: The current Python Version is ' + python_version + '. '
          + 'This library has been tested with Python Version 3.4.3. Use at your own risk.')
elif version_info < (3, 4, 3):
    print('Note: The current Python Version is ' + python_version + '. '
          + 'This library has been tested with Python Version 3.4.3.')

# Import readme as long description that is used by PyPI as the home page for the library's package.
with open('README.rst') as file:
    long_description = file.read()

setup(
    name="algebraixlib",
<<<<<<< HEAD
    version="1.2",
=======
    version="1.1",
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
    description="A data algebra library",
    long_description=long_description,
    author="Algebraix Data Corporation",
    author_email="algebraixlib@algebraixdata.com",
    maintainer="Algebraix Data Corporation",
    maintainer_email="algebraixlib@algebraixdata.com",
    url="https://github.com/AlgebraixData/algebraixlib",
    license="http://www.gnu.org/licenses/lgpl-3.0-standalone.html",
    platforms=["any"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        'Intended Audience :: Developers',
<<<<<<< HEAD
=======
        'Intended Audience :: Developers',
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=[
        'algebraixlib',
        'algebraixlib/algebras',
        'algebraixlib/io',
        'algebraixlib/mathobjects',
        'algebraixlib/util',
    ],
    install_requires=['rdflib>=4.2'],
    keywords='data algebra set theory',
)
