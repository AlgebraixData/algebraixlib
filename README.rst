.. Algebraix Technology Core Library documentation.
   Copyright Algebraix Data Corporation 2015 - 2017

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

:orphan:

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

#.  Make sure you have the required versions of Python and Jupyter Notebook installed (see
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
*   Post questions about algebraixlib on `Stack Overflow`_ using the tag `[algebraixlib]`_.
*   Post questions about the mathematics of data algebra on `math.stackexchange`_ using the tag
    `[data-algebra]`_.
*   Contact us by `email`_.

See also our `GitHub project page`_. In addition, there is a `book`_ about data algebra.


Detailed Instructions
=====================

Requirements
------------

*   `Python`_: Tested with 3.6.1. Likely to run with Python 3.6.x and later. It may run with earlier
    Python 3 versions, but you may run into issues. Does not run with any version of Python before
    Python 3.

    *   For installing and using multiple versions of Python on the same machine, see
        `Official multiple python versions on the same machine? (Stack Overflow)`_,
        `How to install both Python 2.x and Python 3.x in Windows 7 (Stack Overflow)`_ and
        `A Python Launcher For Windows (Python Insider)`_.

*   `Jupyter Notebook`_: Tested with Jupyter 5.2 (used in the Jupyter notebook tutorials and
    examples).

    *   See `Jupyter Installation`_ for instructions how to install the Jupyter notebook
        (``pip install jupyter``).
    *   If you don't want Jupyter in your system environment, you can install it into a virtual
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

To execute the unit tests, download the file `runtests.py`_ and the directory `test`_ into any
location on your system, then run `runtests.py`_::

> mkdir algebraixlib-test
> cd algebraixlib-test
> svn export https://github.com/AlgebraixData/algebraixlib/trunk/runtests.py
> svn export https://github.com/AlgebraixData/algebraixlib/trunk/test
> python runtests.py

Documentation Build
-------------------

The documentation build requires the following libraries be installed:

*   `Sphinx`_ (1.3.2 or later)

To run a documentation build, you need a local working copy of our complete `GitHub`_ repository.
Then run `build.py`_ in the directory `docs`_::

> mkdir algebraixlib
> cd algebraixlib
> svn export https://github.com/AlgebraixData/algebraixlib/trunk
> cd trunk/docs
> python build.py


Legalese
========

Copyright
---------

Copyright(c) 2017 Algebraix Data Corporation.

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

.. _[algebraixlib]:
    http://stackoverflow.com/questions/tagged/algebraixlib
.. _A Beginner's Introduction to Data Algebra:
    http://algebraixlib.readthedocs.org/en/latest/intro.html
.. _A Python Launcher For Windows (Python Insider):
    http://blog.python.org/2011/07/python-launcher-for-windows_11.html
.. _book:
    https://algebraixdata.com/resources/the-algebra-of-data/
.. _build.py:
    https://github.com/AlgebraixData/algebraixlib/blob/master/docs/build.py
.. _coverage:
    https://pypi.python.org/pypi/coverage
.. _Creation of virtual environments:
    https://docs.python.org/3/library/venv.html
.. _[data-algebra]:
    http://math.stackexchange.com/questions/tagged/data-algebra
.. _docs:
    https://github.com/AlgebraixData/algebraixlib/tree/master/docs
.. _Examples:
    https://github.com/AlgebraixData/algebraixlib/tree/master/examples
.. _Free Software Foundation:
    http://www.fsf.org/
.. _How to install both Python 2.x and Python 3.x in Windows 7 (Stack Overflow):
    http://stackoverflow.com/questions/3809314/how-to-install-both-python-2-x-and-python-3-x-in-windows-7
.. _email:
    mailto:algebraixlib@algebraixdata.com
.. _GitHub:
    http://github.com/AlgebraixData/algebraixlib
.. _GitHub project page:
    http://algebraixdata.github.io/algebraixlib/
.. _GNU Licenses:
    http://www.gnu.org/licenses/
.. _Hello_World.ipynb:
    https://github.com/AlgebraixData/algebraixlib/blob/master/examples/Hello_World.ipynb
.. _Jupyter Installation:
    http://jupyter.readthedocs.org/en/latest/install.html
.. _Jupyter Notebook:
    https://jupyter.org/
.. _math.stackexchange:
    http://math.stackexchange.com/
.. _nbviewer:
    http://nbviewer.ipython.org/
.. _nose:
    https://pypi.python.org/pypi/nose/
.. _Official multiple python versions on the same machine? (Stack Overflow):
    http://stackoverflow.com/questions/2547554/official-multiple-python-versions-on-the-same-machine
.. _PyPI:
    http://pypi.python.org/pypi/algebraixlib
.. _Python:
    http://python.org
.. _Read the Docs:
    http://algebraixlib.rtfd.org/
.. _runtests.py:
    https://github.com/AlgebraixData/algebraixlib/blob/master/runtests.py
.. _Sphinx:
    https://pypi.python.org/pypi/Sphinx
.. _Stack Overflow:
    http://stackoverflow.com/
.. _test:
    https://github.com/AlgebraixData/algebraixlib/tree/master/test
.. _Version 3 of the GNU Lesser General Public License:
    http://www.gnu.org/licenses/lgpl-3.0-standalone.html

.. |logo| image:: https://raw.githubusercontent.com/AlgebraixData/algebraixlib/gh-pages/ALGBX-Logo-Color-150DPI.png
.. _logo: http://www.algebraixdata.com/technology/#algebraix-library
