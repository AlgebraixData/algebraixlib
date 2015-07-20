.. Algebraix Technology Core Library documentation.
   $Id: set.rst 22614 2015-07-15 18:14:53Z gfiedler $
   Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-15 13:14:53 -0500 (Wed, 15 Jul 2015) $

   This file is part of algebraixlib <http://github.com/AlgebraixData/algebraixlib>.

   algebraixlib is free software: you can redistribute it and/or modify it under the terms of
   version 3 of the GNU Lesser General Public License as published by the Free Software Foundation.

   algebraixlib is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
   even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public License along with algebraixlib.
   If not, see <http://www.gnu.org/licenses/>.

This page is here to help review notation and terminology for those new to, or requiring a
refresher, of :term:`set`\s and set theory.

.. _sets:

Set Notation
============

Recall that a :term:`set` is a collection of distinct objects.  In any given set each object in
the set is called an **element** of the set.

For example, if :math:`S` represents a set, and :math:`a` is an element of set :math:`S`, we denote
this by writing

    .. math:: a \in S.

If :math:`a` *is not* an element of set :math:`S`, we write it as

    .. math:: a \not\in S.

We can more explicitly write out what the specific elements of a set are by using braces:
:math:`\{,\}`.  For example, if I wanted :math:`S` to be the set of integers between 2 and 6
inclusively, then I can write

    .. math:: S = \{2,3,4,5,6\}.

There is also the set with no elements at all in it, and it is called the **empty set**, and is
denoted by :math:`\emptyset`.  Other ways of denoting are by using :math:`\varnothing`, or even
:math:`\{\}`.

We also use colons to represent conditions on elements in a particular set.  This lets us build up
more complicated sets.  For example, if I use :math:`\mathbb{Z}` to represent the set of all
integers, then if I want :math:`T` to represent the set of all integers greater than five, I can
write it as

    .. math:: T = \{n \in \mathbb{Z} : n > 5\}.

Colons in combination with braces and :math:`\in` is called **set builder notation** and lets us
create very complicated sets.  Let's say I want to create the set of all irrational numbers, then
I can do this by starting with the sets of real numbers, rational numbers, and using set
builder notation:

Let :math:`\mathbb{R}` represent the set of real numbers, and :math:`\mathbb{Q}` the set of
rational numbers, then if we use :math:`X` to represent the set of irrational numbers, we can write
it as

    .. math:: X = \{ r \in \mathbb{R} : r \not\in \mathbb{Q} \}.

We can add even more conditions.  Let us use :math:`Y` to represent the set of negative rational
numbers, then we can write it as

    .. math:: Y = \{ r \in\mathbb{R} : r\not\in\mathbb{Q}\ \&\ r<0 \},

or alternatively by going back to :math:`X` and saying

    .. math:: Y = \{ x \in X : x<0 \}.

To help write conditions precisely without creating too much clutter, we will sometimes use symbols
to represent logical quantifiers such as :math:`\exists` to say "there exists" or :math:`\forall` to
represent "for all".  For example, if we wanted to say that a set :math:`S` was a subset of a set
:math:`T`, that is, eny element of :math:`S` is also an element of :math:`T`, we can write that as

    .. math:: \forall x, x \in S \implies x \in T.

See also `set notation`_ and `set (mathematics)`_ for more information.

.. _set (mathematics):
    https://en.wikipedia.org/wiki/Set_%28mathematics%29
.. _set notation:
    https://en.wikipedia.org/wiki/Set_notation