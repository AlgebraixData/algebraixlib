#!/usr/bin/env python

"""An executable script that builds the Data Algebra Library's installation package."""

# $Id: setup.py 22624 2015-07-15 21:35:12Z wholler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-15 16:35:12 -0500 (Wed, 15 Jul 2015) $
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
if version_info < (3, 4, 3):
    exit("This library requires Python 3.4.3 or newer!")

# Import readme as long description that is used by PyPI as the home page for the library's package.
with open('README.rst') as file:
    long_description = file.read()

setup(
    name="algebraixlib",
    version="1.0",
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
        'Intended Audience :: Developers',
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
