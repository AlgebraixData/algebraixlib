.. Algebraix Technology Core Library documentation.
   $Id: algebras.rst 22614 2015-07-15 18:14:53Z gfiedler $
   Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-15 13:14:53 -0500 (Wed, 15 Jul 2015) $

   This file is part of algebraixlib <http://github.com/AlgebraixData/algebraixlib>.

   algebraixlib is free software: you can redistribute it and/or modify it under the terms of
   version 3 of the GNU Lesser General Public License as published by the Free Software Foundation.

   algebraixlib is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
   even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public License along with algebraixlib.
   If not, see <http://www.gnu.org/licenses/>.

.. _algebras:

Algebras
========
**Definition**

In mathematics (`abstract algebra`_), an **algebra** (also referred to as an `algebraic structure`_
consists of a set (called the :term:`ground set`, which is the set that contains the elements
to which the algebra applies) with one or more operations (`finitary operation`_) on the set
such as:

        -   A :term:`set` of :term:`binary operation`\s (each with an optional
            :term:`identity element`).
        -   A :term:`set` of :term:`unary operation`\s.
        -   A :term:`set` of :term:`relation`\s defined on the ground set.

The ground set combined with the set of operations and identity elements together is called
the **signature** of the algebra.

**Some types of algebras**:

-   A **semigroup** is a non-empty set :math:`X` together with a binary operation :math:`\ast`
    which is associative.
-   A **monoid** is a semigroup :math:`X` with an identity element :math:`e` under :math:`\ast`.
    We call :math:`e` and **identity element** if:
    :math:`\begin{equation*}
    x\ast e=e\ast x\text{ for all }x\in X.
    \end{equation*}`
-   A **group** is a monoid where every element has an **inverse** under :math:`\ast`, namely,
    for each :math:`x\in X` there exists a :math:`y\in X` such that :math:`x\ast y=e=y\ast x`.
-   A **Boolean algebra** consists of a non-empty set :math:`B` together with two binary
    operations we will call :math:`\oplus` and :math:`\odot`, a unary operation :math:`^{*}`, and
    two distinguished elements :math:`\mathbf{0}` and :math:`\mathbf{1}` (*these are not, in
    general, the integers 0 and 1*) such that:

    1.  :math:`\oplus` and :math:`\odot` are each commutative and associative, and each
        distributes over the other.

    2.   For each :math:`x\in B`

        .. math:: \begin{equation*}
            \begin{array}{lll}
                x\oplus \mathbf{0}=x & \text{     } & x\odot \mathbf{0}=\mathbf{0} \\
                x\oplus \mathbf{1}=\mathbf{1} & \text{     } & x\odot \mathbf{1}=x \\
                x\oplus x\text{*}=\mathbf{1} & \text{     } & x\odot x\text{*}=\mathbf{0}%
            \end{array}%
            .
            \end{equation*}

    3.   For all :math:`x,y\in B`

        .. math:: \begin{equation*}
            \begin{array}{lll}
                x\odot (x\oplus y)=x & \text{     } & x\oplus (x\odot y)=x%
            \end{array}%
            .
            \end{equation*}

.. _algebraofsets:

Algebra of Sets
---------------

**Definition**:

The **algebra of sets** is an :term:`algebra` with the signature

.. math:: \bigg[
        P(M) ,
        \big\{
            [ \cup, \varnothing ] ,
            [ \cap, M ]
        \big\} ,
        \big\{\ '\ \big\} ,
        \big\{ \subset \big\}
    \bigg]

Its ground set is the :term:`power set` of |set M|. The :term:`binary operation`\s are
:term:`union` (:math:`\cup`, with the identity element :math:`\varnothing`, the empty set)
and :term:`intersection` (:math:`\cap`, with the identity element :math:`M`), the one
:term:`unary operation` is the :term:`complement` (:math:`'`) and the one relation is the
:term:`subset` relation.

Other binary operations (that can be derived from the basic operations and relations)
include :term:`difference`, :term:`substriction` and :term:`superstriction`; other
relations include the :term:`superset` relation.

**Remark and useful fact**: The algebra of any non-empty set is always a Boolean algebra.
This means that in particular the algebra on |set M| is a Boolean algebra.  It also
true that any Boolean algebra with a finite ground set :math:`B` is the algebra of some set.

**Other useful operations on sets**:

-   The :term:`difference` of two sets.
-   The :term:`symmetric difference` of two sets.

This gives us two alternative algebras of sets where we use difference and symmetric
difference:

    .. math:: \bigg[ P(M),[-],[\bigtriangleup ],\subset ,^{\prime }\bigg]

and an :term:`extension`

    .. math:: \bigg[
            P(M),
            [\cup ,\varnothing ],
            [\cap ,M],[-],
            [\bigtriangleup ],\subset ,^{\prime }
        \bigg].



**Identities concerning difference and symmetric difference**:  Given subsets :math:`S,T` and
:math:`U` of |set M|:

    1. :math:`S-T=S\cap T^{\prime }`.
    2. :math:`S-S=\varnothing`.
    3. :math:`S-\varnothing =S`.
    4. :math:`\varnothing -S=\varnothing`.
    5. :math:`S-M=\varnothing`.
    6. :math:`M-S=S^{\prime }`.
    7. :math:`S\bigtriangleup T=T\bigtriangleup S`. (:math:`\bigtriangleup` is *commutative*.)
    8. :math:`S\bigtriangleup (T\bigtriangleup U)=(S\bigtriangleup T)\bigtriangleup U`. (:math:`\bigtriangleup` is *associative*.)
    9. :math:`S\bigtriangleup S=\varnothing`.
    10. :math:`S\bigtriangleup \varnothing =S`.
    11. :math:`S\bigtriangleup M=M-S=S^{\prime }`.

Algebra of Multisets
--------------------

.. _multiset:

Multiset
````````

**Definition**

A **multiset** is a set that allows multiple instances of any given element.  We define it as a
function from |set M| to the nonnegative integers, or from a given :term:`subset` of
|set M| to the positive integers.  In particular, we call :math:`\dot{S}` a multiset of :math:`M`
if for any :math:`x\in M` we have :math:`\dot{S}(x)` is a nonnegative integer that we call the
**multiplicity** of :math:`x`.

**Example**

Let :math:`M=\{a,b,c\}` and :math:`\dot{S}` represent the multiset :math:`\{a,a,a,b,b\}`, then
we have :math:`\dot{S}(a)=3`, :math:`\dot{S}(b)=2`, and :math:`\dot{S}(c)=0`.  In this case
:math:`a` has multiplicity 3, and :math:`b` has multiplicity 2.

.. _algebraofmultisets:

Multiset Algebra
````````````````
**Definition**

Let :math:`\dot{P}(M)` represent the set of all multisets of :math:`M`.  Using the definitions of
:term:`union`, :term:`addition`, :term:`intersection`, and :term:`subset` as applied to multisets
we have an algebra on multisets with the following signature:

.. math::  \bigg[\dot{P}(M), [\cup,\varnothing], [+,\varnothing],\cap,\subset \bigg].

.. _algebraofcouplets:

Algebra of Couplets
-------------------

The **algebra of couplets** is an :term:`algebra` with the signature

    .. math:: \bigg[
                M \times M ,
                \big\{\ \circ\ \big\} ,
                \big\{ \leftrightarrow \big\}
            \bigg]

Its ground set is the :term:`Cartesian product` of |set M| with itself. The only
:term:`binary operation` is :term:`composition` (:math:`\circ`, without identity element)
and the only :term:`unary operation` is the :term:`transposition` (:math:`\leftrightarrow`).

.. _algebraofrelns:

Algebra of Relations
--------------------

**Definition**

The **algebra of relations** is the :term:`algebra` of :term:`set`\s of :term:`couplet`\s;
its signature is

    .. math:: \bigg[
                P(M \times M) ,
                \big\{
                    [ \circ, D_M ]
                \big\} ,
                \big\{ \leftrightarrow \big\}
            \bigg]

Its ground set is the :term:`power set` of the :term:`Cartesian product` of |set M| with
itself. The only :term:`binary operation` is :term:`composition` (:math:`\circ`, with the
identity element :math:`D_M`, which is the :term:`diagonal` on |set M|) and the only
:term:`unary operation` is the :term:`transposition` (:math:`\leftrightarrow`).

The :term:`binary operation`\s :term:`union` and :term:`intersection`, the :term:`unary
operation` :term:`complement` and the :term:`subset` relation are implicitly present,
inherited from the :term:`algebra of sets` (since the algebra of relations is also an
algebra of sets).

Other operations and relations (that can be derived from the basic operations and relations)
include the binary operations :term:`difference`, :term:`substriction`, :term:`superstriction`,
:term:`left-functional union` and :term:`right-functional union` and the :term:`superset`
relation.

.. _algebraofclans:

Algebra of Clans
----------------

**Definition**

The **algebra of clans** is the :term:`algebra` of :term:`set`\s of :term:`relation`\s, which
is sets of sets :term:`couplet`\s. Its ground set is therefore the second :term:`power set` of the
:term:`Cartesian product` of |set M| with itself.  As a result of being a second power set, the
operations of :term:`cross-union` and :term:`cross-intersection` can be applied, in addition to
the operations on an :term:`algebra of sets`. Moreover, the operations :term:`transposition` and
:term:`composition` from the :term:`algebra of relations` extend in a natural way to the
algebra of clans.  We also include :term:`substriction`, :term:`superstriction`, and
:term:`cross-superstriction`.  As a result, it has the following signature:

.. math::
    \bigg[ P^{2}(M \times M),[\cup ,\varnothing ],[\mathbb{\cap },P(M \times M)],
    [\blacktriangledown ,\{\varnothing\}],[\mathbb{\blacktriangle },\{M \times M\}],
    \triangleleft, \triangleright, \blacktriangleright, \subset , \prime \bigg].

Note that included in the operations of union and cross-union are the special
:term:`left-functional` and :term:`right-functional` cases of
:term:`left-functional cross-union` and :term:`right-functional cross-union`.

.. _algebraofmultclan:

Algebra of Multiclans
---------------------

**Definition**

The **algebra of multiclans** is an algebra that generalizes the :term:`algebra of clans`.  Since
we use :math:`P(M \times M)` to denote the set of couplets, a :term:`multiset` of relations is a
multiset of sets of couplets, so we will use :math:`\dot{P}(P(M \times M))` to denote the multiset
of relations.  Combining the multiset algebra with the clan algebra we have

.. math::
    \bigg[ \dot{P}(P(M \times M)),[\cup ,\varnothing ],[+,\varnothing],\mathbb{\cap },
    [\blacktriangledown ,\{\varnothing\}],[\mathbb{\blacktriangle },\{M \times M\}],
    \triangleleft, \triangleright, \blacktriangleright, \subset , \prime \bigg].

As in the case of clans, the operations of :term:`left-functional cross-union` and
:term:`right-functional cross-union` are implied.

.. |set M| replace:: :term:`set M` (:math:`M`)

.. _abstract algebra:
    http://en.wikipedia.org/wiki/Abstract_algebra
.. _algebraic structure:
    http://en.wikipedia.org/wiki/Algebraic_structure
.. _finitary operation:
    https://en.wikipedia.org/wiki/Finitary

