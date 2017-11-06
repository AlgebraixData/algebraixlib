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

Working with Our IPython Notebooks
==================================

Some of our examples are provided as `IPython Notebook`_\s. (The file extension is .ipynb.) They
require an IPython Notebook server to run, and in some cases they also need the accompanying data
files.

While GitHub renders IPython notebooks, it does so with limitations (see
`Rendering Notebooks on GitHub`_). One of these limitations is that LaTeX math notation is not
rendered correctly. We use this feature quite a bit in our notebooks, so looking at them in GitHub
is not very useful. Because of this, we provide here two other options.

.. _IPython Notebook: http://ipython.org/ipython-doc/3/notebook/notebook.html
.. _Rendering Notebooks on GitHub: http://blog.jupyter.org/2015/05/07/rendering-notebooks-on-github/


Static Renderings of our Notebooks
----------------------------------

We use `nbviewer`_ to create *static* images of our notebooks that are properly rendered. (While
nbviewer code powers the rendering of IPython notebooks on GitHub, the code running at the nbviewer
site does not have the same limitations as the one running on GitHub.) nbviewer includes a file
browser, so you can simply go to the top-level directory and select the notebooks from there,
or you can use the direct links provided here.

-   `examples (directory)`_: The top-level directory of our IPython notebook examples and tutorials.

    -   `Hello World`_: A basic introduction into our API and math concepts.
    -   `Hello Multisets`_: A similarly basic introduction into multisets.
    -   `Hello XML`_: An introduction into the representation of hierarchical data.
    -   `TPC-H Query 5 (directory)`_: The directory with the TPC-H Query 5 example notebooks:

        -   `1-Introduction`_, `2-Tables`_, `3-Graphs`_, `4-Hierarchies`_, `5-Query`_

.. _nbviewer: http://nbviewer.ipython.org/
.. _examples (directory): http://nbviewer.ipython.org/github/AlgebraixData/algebraixlib/blob/master/examples/
.. _Hello World: http://nbviewer.ipython.org/github/AlgebraixData/algebraixlib/blob/master/examples/Hello_World.ipynb
.. _Hello Multisets: http://nbviewer.ipython.org/github/AlgebraixData/algebraixlib/blob/master/examples/Hello_Multisets.ipynb
.. _Hello XML: http://nbviewer.ipython.org/github/AlgebraixData/algebraixlib/blob/master/examples/Hello_XML.ipynb
.. _TPC-H Query 5 (directory): http://nbviewer.ipython.org/github/AlgebraixData/algebraixlib/blob/master/examples/TPC-H_Query5/
.. _1-Introduction: http://nbviewer.ipython.org/github/AlgebraixData/algebraixlib/blob/master/examples/TPC-H_Query5/1-Introduction.ipynb
.. _2-Tables: http://nbviewer.ipython.org/github/AlgebraixData/algebraixlib/blob/master/examples/TPC-H_Query5/2-Tables.ipynb
.. _3-Graphs: http://nbviewer.ipython.org/github/AlgebraixData/algebraixlib/blob/master/examples/TPC-H_Query5/3-Graphs.ipynb
.. _4-Hierarchies: http://nbviewer.ipython.org/github/AlgebraixData/algebraixlib/blob/master/examples/TPC-H_Query5/4-Hierarchies.ipynb
.. _5-Query: http://nbviewer.ipython.org/github/AlgebraixData/algebraixlib/blob/master/examples/TPC-H_Query5/5-Query.ipynb


Installing IPython Notebook Locally
-----------------------------------

If you want to interact with the notebooks, you need to run them on an `IPython Notebook`_
server. Installing it is simple::

> pip install ipython[notebook]

You also need to install our library::

> pip install algebraixlib

After this, you simply run the notebook server (typically from within the 'examples' directory in
a local copy of the code), like this::

> ipython notebook

Or like this if your Python "Scripts" directory is not on your path (``<PythonInstallDir>`` is your
Python installation directory)::

> <PythonInstallDir>/Scripts/ipython notebook

This will open a web page that is essentially a file browser into the 'examples' directory. From
there you can open the notebooks and interact with them.


Obtain a Local Copy of the Examples
-----------------------------------

A local copy of the example code can be obtained in a number of ways:

-   Download the `master.zip`_ file from GitHub (see also the button "Download ZIP" on the
    repository home page and expand the "examples" directory contained in it.
-   Run the command ``svn export https://github.com/AlgebraixData/algebraixlib/trunk/examples``
    or one of the other possibilities described in the StackOverflow article
    `Download a single folder or directory from a GitHub repo`_.

.. _master.zip: https://github.com/AlgebraixData/algebraixlib/archive/master.zip
.. _repository home page: https://github.com/AlgebraixData/algebraixlib
.. _Download a single folder or directory from a GitHub repo: http://stackoverflow.com/questions/7106012/download-a-single-folder-or-directory-from-a-github-repo
