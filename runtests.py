#!/usr/bin/env python

"""Run all unit tests. 

This script requires the packages nose and coverage (available from PyPI, install using pip).
"""

# Copyright Algebraix Data Corporation 2015 - 2017
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
import inspect
import os.path as path
import sys

# noinspection PyPackageRequirements
import nose

# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # Check python version
    if sys.version_info < (3, 4, 3):
        sys.exit("This script requires Python 3.4.3 or newer!")

    filepath = inspect.getfile(inspect.currentframe())
    dirpath = path.dirname(filepath)

    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file} --where={dir}'.format(file=path.basename(filepath), dir=dirpath))

    arguments = [
        '-s', '--nocapture', '-v',  # Don't capture stdout (show it in the console).
        '--all-modules',  # Run tests in all modules (so that __main__ tests run).
        '--with-doctest',  # Include doctests.
        '--with-coverage',  # Include unit test coverage.
        '--cover-package=algebraixlib',  # Exclude 3rd party code from unit test coverage report.
        '--where=' + dirpath,  # Enable invocation from an external path.

        # --all-modules makes the following functions being run so we exclude them:
        '--exclude=create_test_object|get_test_file_(name|path)'
    ]
    nose.main(argv=arguments)
