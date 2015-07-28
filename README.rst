.. Algebraix Technology Core Library documentation.
   $Id: README.rst 22693 2015-07-28 15:15:37Z gfiedler $
   Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-28 10:15:37 -0500 (Tue, 28 Jul 2015) $

   This file is part of algebraixlib <http://github.com/AlgebraixData/algebraixlib>.

   algebraixlib is free software: you can redistribute it and/or modify it under the terms of
   version 3 of the GNU Lesser General Public License as published by the Free Software Foundation.

   algebraixlib is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
   even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public License along with algebraixlib.
   If not, see <http://www.gnu.org/licenses/>.

algebraixlib
============

What Is It?
-----------
``algebraixlib`` is a library that provides constructs and facilities to harness the fundamentals
of data algebra.

Requirements
------------
`Python`_  3.4.3 or later.
`IPython Notebook`_ 3.2 or later for the IPython notebook tutorials and examples.

How to Install
--------------
If you already have Python installed and are familiar with installing packages, you can get
``algebraixlib`` with ``pip``::

> pip install algebraixlib

Additional user permissions may be necessary to complete the installation. In such a situation
other options include installing the package to the home directory::

> pip install algebraixlib --user <username> 

or in a virtual environment, see `Creation of virtual environments`_.

You can also manually download ``algebraixlib`` from `GitHub`_ or `PyPI`_. To install from a
download, unpack it and run the following from the top-level source directory using the terminal::

> python setup.py install

Unit Tests
----------
The unit tests require the following libraries be installed:

*   `nose`_
*   `coverage`_

To execute the unit tests, from the console, in the algebraixlib directory, use the command::

> python runtests.py

Document Build
--------------
The document builds require the following libraries be installed:

*   `Sphinx`_ (1.3 or later)

To execute the document builds, from the console, in the algebraixlib/docs directory, use command::

> python build.py

Documentation and Support
-------------------------

*   Find documentation at `Read the Docs`_.
*   Find the library on `PyPI`_.
*   Find the library, the bugtracker and contribute on `GitHub`_.
*   Find tutorials and example code in the `examples`_ directory on GitHub.
*   Post questions about algebraixlib on `Stack Overflow`_ using the tag [algebraixlib].
*   Post questions about the mathematics of data algebra on `math.stackexchange`_ using the tag
    [data-algebra].
*   Contact us at `email`_.

See also our `GitHub project page`_. In addition, there is a book forthcoming about data algebra.

Copyright
---------
Copyright(c) 2015 Algebraix Data Corporation.

License
-------
``algebraixlib`` is free software: you can redistribute it and/or modify it under the terms of
`version 3 of the GNU Lesser General Public License`_ as published by the
`Free Software Foundation`_. A copy of the GNU Lesser General Public License is published along
with ``algebraixlib`` on `GitHub`_. Otherwise, see `GNU licenses`_.

Warranty
--------
``algebraixlib`` is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.


.. _Python:
    http://python.org
.. _IPython Notebook:
    http://ipython.org/notebook.html
.. _email:
    mailto:algebraixlib@algebraixdata.com
.. _Read the Docs:
    http://algebraixlib.rtfd.org/
.. _Examples:
    https://github.com/AlgebraixData/algebraixlib/tree/master/examples
.. _PyPI:
    http://pypi.python.org/pypi/algebraixlib
.. _nose:
    https://pypi.python.org/pypi/nose/
.. _coverage:
    https://pypi.python.org/pypi/coverage
.. _Sphinx:
    https://pypi.python.org/pypi/Sphinx
.. _GitHub:
    http://github.com/AlgebraixData/algebraixlib
.. _Stack Overflow:
    http://stackoverflow.com/
.. _math.stackexchange:
    http://math.stackexchange.com/
.. _GitHub project page:
    http://algebraixdata.github.io/algebraixlib/
.. _Version 3 of the GNU Lesser General Public License:
    http://www.gnu.org/licenses/lgpl-3.0-standalone.html
.. _GNU Licenses:
    http://www.gnu.org/licenses/
.. _Free Software Foundation:
    http://www.fsf.org/
.. _Creation of virtual environments:
    https://docs.python.org/3/library/venv.html