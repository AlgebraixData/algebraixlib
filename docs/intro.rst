.. Algebraix Technology Core Library documentation.
   $Id: intro.rst 22797 2015-08-13 16:57:29Z mhaque $
   Copyright Algebraix Data Corporation 2015 - $Date: 2015-08-13 16:57:29 -0400 (Thu, 13 Aug 2015) $

A Beginner's Introduction to Data Algebra
=========================================

The purpose of this section is to provide a brief introduction to data algebra.  In particular,
we would like to motivate the various definitions and terms in a way that is not daunting to
beginners, and shows the usefulness of the data algebra framework.  Note that this introduction
will make use of set notation, of which there is a short primer at :ref:`sets` if needed.

We will do this by taking a dataset and analyze it using data algebra.  Consider the following
table of information:

.. list-table::  Sightings
   :widths: 5 10 10 10 5 10 10 10
   :header-rows: 1
   :stub-columns: 1

   * - year
     - providedScientificName
     - ITISscientificName
     - ITIScommonName
     - ITIStsn
     - validAcceptedITIStsn
     - decimalLatitude
     - decimalLongitude
   * - 1970
     - Micrurus tener Baird & Girard, 1853
     - Micrurus tener
     - Texas Coralsnake
     - 683040
     - 683040
     - 30.43099976
     - -98.05999756
   * - 2008
     - Masticophis taeniatus Hallowell, 1852
     - Masticophis taeniatus
     - Culebra-chirriadora adornada;Striped Whipsnake
     - 174240
     - 174240
     - 30.43399048
     - -97.96090698
   * - 1951
     - Kinosternon flavescens Agassiz, 1857
     - Kinosternon flavescens
     - Tortuga-pecho quebrado amarilla;Yellow Mud Turtle
     - 173766
     - 173766
     - 30.43678093
     - -97.66889191
   * - 1951
     - Acris crepitans Baird, 1854
     - Acris crepitans
     - Northern Cricket Frog;Rana-grillo norte
     - 173520
     - 173520
     - 30.43678093
     - -97.66889191
   * - 2011
     - Parus bicolor Linnaeus, 1766
     - Baeolophus bicolor
     - Carbonero cresta negra;Tufted Titmouse
     - 178738
     - 554138
     - 30.4736805
     - -97.96916962

Table Sightings is taken from BISON (Biodiversity Information Serving Our Nation) [#BISON]_, a
publicly available dataset from the US Geological Survey, and consists of animal sightings in
Travis County, TX.

Couplets: The Basic Pieces of Data
----------------------------------

Every data entry, or datum, is represented in data algebra using :term:`couplet`\s.  The idea being
any piece of data consists of two pieces of information.  For example in table Sightings 2011 refers
to a year, and 30.7436805 is a decimalLatitude.  In data algebra notation we write these as

.. math:: year{\mapsto}2011

and

.. math:: decimalLatitude{\mapsto}30.7436805

The object before the arrow is called the :term:`left component`, and the object after the arrow is
called the :term:`right component`.  For example the couplet :math:`year{\mapsto}2011` has left
component :math:`year` and right right component :math:`2011`.

Relations: Sets of Couplets
---------------------------

Each row of Sightings is a :term:`set` of couplets, which we call a :term:`relation`.  For example,
the first row of Sightings, let us denote it by :math:`R_1`, is the relation

.. math::
    \begin{align*}
    R_1 =\ & \{ \\
        & year{\mapsto}1970,  \\
        & providedScientificName{\mapsto}Micrurus\ tener\ Baird\ \&\ Girard,\ 1853, \\
        & ITISscientificName{\mapsto}Micrurus\ tener, \\
        & ITIScommonName{\mapsto}Texas\ Coralsnake, \\
        & ITIStsn{\mapsto}683040,                 \\
        & validAcceptedITIStsn{\mapsto}683040,    \\
        & decimalLatitude{\mapsto}30.43099976,    \\
        & decimalLongitude{\mapsto}-98.05999756 \\
    & \}
    \end{align*}

While there are other ways of forming relations from the table, for our purposes we will use rows
to form relations.  One reason we will do this is that each row relation is in fact a
:term:`function` in this case.  It is often the case that row relations are :term:`functional`.

Getting Data from a Relation
````````````````````````````

One of our primary methods of extracting information from a dataset is :term:`composition`.  Let
us say we want to know the :math:`ITIScommonName` of the first row of Sightings.  What we can do
is compose :math:`R_1` with the relation

.. math:: \{ ITIScommonName{\mapsto}ITIScommonName \}

Just like function composition, the output of the first relation becomes the input for the next
relation.  In this case, our first relation has only one output, or right component, which
corresponds to only one input, or left component, in :math:`R_1`, hence

.. math:: R_1 \circ \{ ITIScommonName{\mapsto}ITIScommonName \} =
            \{ITIScommonName{\mapsto}Texas\ Coralsnake\}

which tells us that :math:`ITIScommonName` for the first row is :math:`Texas\ Coralsnake`.  (Note
that, just like with functions, compositions are evaluated from right to left.  In particular,
given relation composition :math:`r_2 \circ r_1` we would apply :math:`r_1` first, and then
:math:`r_2`.)

Clans: Sets of Relations
------------------------

A set of relations is called a :term:`clan`.  In particular, any table can be divided up into a
set of row relations, which means any table can be represented by a clan.  We will refer to the
table Sightings as a clan whose relations are the row relations.  Once again, we can use
composition to extract data out of our clan.

Getting Data from a Clan
````````````````````````

For example, if we want the :term:`projection` (in terms of relational algebra) of Sightings over
:math:`ITISscientificName` and :math:`ITIScommonName`, we can form the relation

.. math:: D =   \{  ITISscientificName{\mapsto}ITISscientificName,
                    ITIScommonName{\mapsto}ITIScommonName
                \}

Let us use :math:`\mathbb{S}` to denote the Sightings clan.  If we use :math:`R_k` to denote the
:math:`k`\th row of Sightings, then

.. math:: \mathbb{S} = \{ R_1, R_2, R_3, R_4, R_5 \}

Note that

.. math:: \mathbb{S} \circ D = \{ R_1 \circ D, R_2 \circ D, R_3 \circ D, R_4 \circ D,
                                    R_5 \circ D \}

and :math:`R_k \circ D` will give you the :math:`ITISscientificName` and :math:`ITIScommonName`
in the :math:`k`\th row of Sightings.  In particular we have

.. math::
    \mathbb{S} \circ D =\
        & \{ \\
            & \{ ITISscientificName{\mapsto}Micrurus\ tener,
                ITIScommonName{\mapsto}Texas\ Coralsnake \} \\
            & \{ ITISscientificName{\mapsto}Masticophis\ taeniatus,
                ITIScommonName{\mapsto}Culebra-chirriadora\ adornada;Striped\ Whipsnake \} \\
            & \{ ITISscientificName{\mapsto}Kinosternon\ flavescens,
                ITIScommonName{\mapsto}Tortuga-pecho\ quebrado\ amarilla;Yellow\ Mud\ Turtle \} \\
            & \{ ITISscientificName{\mapsto}Acris\ crepitans,
                ITIScommonName{\mapsto}Northern\ Cricket\ Frog;Rana-grillo\ norte \} \\
            & \{ ITISscientificName{\mapsto}Baeolophus\ bicolor,
                ITIScommonName{\mapsto}Carbonero\ cresta\ negra;Tufted\ Titmouse \} \\
        & \}

which is the projection of Sightings onto :math:`ITISscientificName` and :math:`ITIScommonName` as
we wanted.


.. [#BISON] BISON can be accessed at http://bison.usgs.ornl.gov  To obtain the data in the table,
    on the map click on Texas, then on Travis county, and one can then download all of the
    wildlife sightings recorded for Travis county.  The above table is only a small subset of
    the many sightings in Travis county.