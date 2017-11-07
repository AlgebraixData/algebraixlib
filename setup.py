#!/usr/bin/env python

"""Install 'algebraixlib' or build its installation package."""

# Copyright Algebraix Data Corporation 2015-2017
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
from setup_data import setup_data  # Local import.


# Check python version. This doesn't run in a wheel install.
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


setup(**setup_data)
