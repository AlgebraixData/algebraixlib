.. Algebraix Technology Core Library documentation.
   $Id: README.rst 22838 2015-08-20 21:49:14Z gfiedler $
   Copyright Algebraix Data Corporation 2015 - $Date: 2015-08-20 16:49:14 -0500 (Thu, 20 Aug 2015) $

   This file is part of algebraixlib <http://github.com/AlgebraixData/algebraixlib>.

   algebraixlib is free software: you can redistribute it and/or modify it under the terms of
   version 3 of the GNU Lesser General Public License as published by the Free Software Foundation.

   algebraixlib is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
   even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public License along with algebraixlib.
   If not, see <http://www.gnu.org/licenses/>.

   This file is not included via toctree. Mark it as orphan to suppress the warning that it isn't
   included in any toctree.

|logo|_

algebraixlib
============

What Is It?
-----------

``algebraixlib`` is a library that provides constructs and facilities to harness the fundamentals
of data algebra. Data algebra consists of mathematical constructs that can represent all data, no
matter how it is structured, and the operations on that data. With this, all the advantages of a
mathematically rigorous modeling can be unleashed. See also
`A Beginner's Introduction to Data Algebra`_.

Getting Started
---------------

#.  Make sure you have the right versions of Python and IPython Notebook installed (see
    `Requirements`_ below).
#.  Install the ``algebraixlib`` library (see `How to Install`_ below).
#.  Download the `examples`_ from our `GitHub`_ repository.
#.  Try the Hello_World.ipynb example first.

(Alternatively, you can also look at a static version of the notebooks in `nbviewer`_; see the
README file in our `examples`_ directory for direct links. For this you don't need to install or
download anything. You can also start with the simpler hello_world.py. However, you'll lose out
on some math and need to read up on it in our documentation at `Read the Docs`_. )

Documentation and Support
-------------------------

*   Find documentation at `Read the Docs`_.
*   Find the ``pip`` installer on `PyPI`_.
*   Find the source code, the bugtracker and contribute on `GitHub`_.
*   Find tutorials and example code in the `examples`_ directory on GitHub.
*   Post questions about algebraixlib on `Stack Overflow`_ using the tag [algebraixlib].
*   Post questions about the mathematics of data algebra on `math.stackexchange`_ using the tag
    [data-algebra].
*   Contact us at `email`_.

See also our `GitHub project page`_. In addition, there is a book forthcoming about data algebra.


Detailed Instructions
=====================

Requirements
------------

*   `Python`_: Tested with 3.4.3. Likely to run with Python 3.4.x. It may run with earlier Python 3
    versions, but you may run into issues. Does not run with any version of Python before Python 3.

    *   For installing and using multiple versions of Python on the same machine, see
        `Official multiple python versions on the same machine? (Stack Overflow)`_,
        `How to install both Python 2.x and Python 3.x in Windows 7 (Stack Overflow)`_ and
        `A Python Launcher For Windows (Python Insider)`_.

*   `IPython Notebook`_: Tested with IPython 3.2 (used in the IPython notebook tutorials and
    examples).

    *   See `IPython Installation`_ for instructions how to install the IPython notebook
        (``pip install "ipython[notebook]"``).
    *   If you don't want IPython in your system environment, you can install it into a virtual
        environment (see `Creation of virtual environments`_).

How to Install
--------------

If you already have Python installed and are familiar with installing packages, you can install
``algebraixlib`` with ``pip``::

> pip install algebraixlib

Additional user permissions may be necessary to complete the installation. In such a situation,
other options include installing the package for a single user (in the user's home directory)::

> pip install algebraixlib --user <username> 

or in a virtual environment (see `Creation of virtual environments`_).

You can also manually download ``algebraixlib`` from `GitHub`_ or `PyPI`_. To install from a
download, unpack it and run the following command from the top-level source directory (the
directory that contains the file setup.py)::

> python setup.py install

(The same considerations about permissions apply.)

Unit Tests
----------

The unit tests require the following libraries to be installed:

*   `nose`_
*   `coverage`_

To execute the unit tests, use the following command in the algebraixlib directory (it contains the
file runtests.py)::

> python runtests.py

Document Build
--------------
The document build requires the following libraries be installed:

*   `Sphinx`_ (1.3 or later)

To run a document build, use the following command in the algebraixlib/docs directory (it
contains the file build.py)::

> python build.py


Legalese
========

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
.. _Official multiple python versions on the same machine? (Stack Overflow):
    http://stackoverflow.com/questions/2547554/official-multiple-python-versions-on-the-same-machine
.. _How to install both Python 2.x and Python 3.x in Windows 7 (Stack Overflow):
    http://stackoverflow.com/questions/3809314/how-to-install-both-python-2-x-and-python-3-x-in-windows-7
.. _A Python Launcher For Windows (Python Insider):
    http://blog.python.org/2011/07/python-launcher-for-windows_11.html
.. _IPython Notebook:
    http://ipython.org/notebook.html
.. _IPython Installation:
    http://ipython.org/install.html
.. _nbviewer:
    http://nbviewer.ipython.org/
.. _email:
    mailto:algebraixlib@algebraixdata.com
.. _Read the Docs:
    http://algebraixlib.rtfd.org/
.. _A Beginner's Introduction to Data Algebra:
    http://algebraixlib.readthedocs.org/en/latest/intro.html
.. _Examples:
    https://github.com/AlgebraixData/algebraixlib/tree/master/examples
.. _Hello_World.ipynb:
    https://github.com/AlgebraixData/algebraixlib/blob/master/examples/Hello_World.ipynb
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

.. |logo| image:: https://raw.githubusercontent.com/AlgebraixData/algebraixlib/gh-pages/ALGBX-Logo-Color-150DPI.png
.. _logo: http://www.algebraixdata.com/technology/#algebraix-library
