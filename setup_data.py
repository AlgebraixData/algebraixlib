"""Provide the data for the ``setup()`` call in setup.py.

This is separate here so that other places in our build system that need the algebraixlib data
can get it from here without actually running setup.py.
"""

# Copyright Algebraix Data Corporation 2015 - 2017
#
# Confidential and proprietary. For internal use only.
# --------------------------------------------------------------------------------------------------
from setuptools import find_packages

# RELEASE: This is the only place where the algebraixlib version is defined. Other places that
# need the version import this module and get it from here.
version = '1.4'


# Import readme as long description that is used by PyPI as the home page for the library's package.
with open('README.rst') as file:
    long_description = file.read()

# Define the keyword arguments that are sent to setup().
setup_data = {
    'name': 'algebraixlib',
    'version': version,
    'description': 'A data algebra library',
    'long_description': long_description,
    'author': 'Algebraix Data Corporation',
    'author_email': 'algebraixlib@algebraixdata.com',
    'maintainer': 'Algebraix Data Corporation',
    'maintainer_email': 'algebraixlib@algebraixdata.com',
    'url': 'https://github.com/AlgebraixData/algebraixlib',
    'license': 'http://www.gnu.org/licenses/lgpl-3.0-standalone.html',
    'platforms': [
        'any'
    ],
    'classifiers': [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    'packages': find_packages(exclude='test'),
    'install_requires': [
        'rdflib>=4.2'
    ],
    'keywords': 'data algebra set theory',
}
