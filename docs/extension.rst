.. Algebraix Technology Core Library documentation.
   $Id$
   Copyright Algebraix Data Corporation 2015 - $Date$

   This file is part of algebraixlib <http://github.com/AlgebraixData/algebraixlib>.

   algebraixlib is free software: you can redistribute it and/or modify it under the terms of
   version 3 of the GNU Lesser General Public License as published by the Free Software Foundation.

   algebraixlib is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
   even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public License along with algebraixlib.
   If not, see <http://www.gnu.org/licenses/>.

.. _extension:

Extension
=========

**Definition**

Given a set, or algebra :math:`S`, we say that :math:`T` is an **extension** of :math:`S`, or
**extends** :math:`S`, if one or more of the following holds:

-   :math:`S \subseteq T` and :math:`T` has operations that :math:`S` does not.
-   :math:`S \subset T` and any operation :math:`op` on :math:`S` can be obtained from an
    operation :math:`OP` on :math:`T` by restricting :math:`OP` to elements only in :math:`S`.

For the purposes of data algebra, we will deal almost exclusively with :term:`algebra`\s of
:term:`set`\s and their extensions.  Mathematically an algebra can be extended in many different
ways.  Below are some general examples, as well as some specific to data algebra.

Examples of extensions
----------------------

Basic examples
``````````````

-   Any set :math:`S` with no pre-defined operations on it extends to its set algebra:
    :math:`\bigg[P(S), \big \{ [ \cup, \varnothing ] , [ \cap, M ] \big\} , \big\{\ '\
    \big\} , \big\{ \subset \big\} \bigg]`.

-   Let :math:`\mathbb{Z}` represent the set of integers, and :math:`\mathbb{Q}` represent
    the set of rational numbers.  The set :math:`\mathbb{Z}` has a natural algebra under addition,
    and multiplication, and negation with signature:
    :math:`\bigg[ \mathbb{Z}, \big \{[+,0],[\cdot ,1]\}, \big \{-\}, \bigg]`.
    This algebra naturally extends to an algebra on the rational numbers with signature:
    :math:`\bigg[ \mathbb{Q}, \big \{[+,0],[\cdot ,1]\}, \big \{-\}, \bigg]`.

Examples from data algebra
``````````````````````````

-   The :term:`algebra of couplets` on a set :math:`M` with signature
    :math:`\bigg[ M \times M , \big\{\ \circ\ \big\} , \big\{ \leftrightarrow \big\} \bigg]`
    extends to the :term:`algebra of relations`
    :math:`\bigg[P(M \times M),\big\{[ \circ, D_M ] \big\} , \big\{ \leftrightarrow \big\}\bigg]`,
    where :math:`\circ` is :term:`composition`, :math:`\leftrightarrow` is :term:`transposition`,
    and :math:`D_M` is the :term:`diagonal` of :math:`M`.

-   The :term:`power set` of a power set has an algebra given by the :term:`algebra of sets`.
    Hence, if :math:`U` is a set, we have an algebra with signature
    :math:`\bigg[ P^{2}(U),[\cup ,\varnothing ],[\mathbb{\cap },P(U)],\subset ,\prime \bigg]`.
    This algebra extends to the algebra
    :math:`\bigg[ P^{2}(U),[\cup ,\varnothing ],[\mathbb{\cap },P(U)],
    [\blacktriangledown ,\{\varnothing\}],[\mathbb{\blacktriangle },\{U\}],\subset ,\prime \bigg]`,
    where :math:`\blacktriangledown` is the :term:`cross-intersection` and :math:`\blacktriangle`
    is the :term:`cross-union`, which are :term:`binary extension`\s of :term:`intersection` and
    :term:`union` resprectively from :math:`P(U)` to :math:`P^{2}(U)`.  This is how we extend the
    :term:`algebra of relations` to the :term:`algebra of clans`.

-   An algebra of sets can also be extended to an :term:`algebra of multisets`.    In particular we
    can simply take :term:`binary multi-extension`\s of all of the binary operations, and replace
    :term:`subset` with :term:`submultiset`.  We can also include :term:`multiset addition`, but we
    will have to take out :term:`complement`, as there is not multiset equivalent of that.
    Therefore, the algebra

    .. math:: \bigg[
        P(M) ,
        \big\{
            [ \cup, \varnothing ] ,
            [ \cap, M ]
        \big\} ,
        \big\{\ '\ \big\} ,
        \big\{ \subset \big\}
        \bigg]

    extends to

    .. math::  \bigg[\dot{P}(M), [\cup,\varnothing], [+,\varnothing],\cap,\subset \bigg].

-   Similar to the previous example an :term:`algebra of clans` can extend to an
    :term:`algebra of multiclans`, by taking binary multi-extensions of all the operations.  Hence,
    an algebra of clans with signature:

        .. math::
            \bigg[ P^{2}(M \times M),[\cup ,\varnothing ],[\mathbb{\cap },P(M \times M)],
            [\blacktriangledown ,\{\varnothing\}],[\mathbb{\blacktriangle },\{M \times M\}],
            \vartriangleleft, \vartriangleright, \blacktriangleleft, \blacktriangleright, \subset , \prime
            \bigg]

    can be extended to an algebra of multiclans with signature

        .. math::
            \bigg[ \dot{P}(P(M \times M)),[\cup ,\varnothing ],[+,\varnothing],\mathbb{\cap },
            [\blacktriangledown ,\{\varnothing\}],[\mathbb{\blacktriangle },\{M \times M\}],
            \vartriangleleft, \vartriangleright, \blacktriangleleft, \blacktriangleright, \subset
            \bigg].

An example of adding set operations to an algebra with no given set structure
`````````````````````````````````````````````````````````````````````````````

-   Let us take the algebra of integers with signature
    :math:`\bigg[ \mathbb{Z}, \big \{[+,0],[\cdot ,1]\}, \big \{-\}, \bigg]` as in an earlier
    example.  Since :math:`\mathbb{Z}` is a set, it also posesses the set algebra
    :math:`\bigg[P(\mathbb{Z}), \big \{ [ \cup, \varnothing ] , [ \cap, M ] \big\} , \big\{\ '\
    \big\} , \big\{ \subset \big\} \bigg]`.  We can extend
    :math:`\bigg[ \mathbb{Z}, \big \{[+,0],[\cdot ,1]\}, \big \{-\}, \bigg]` to the set algebra
    by defining addition, multiplication, and negation on subsets of :math:`\mathbb{Z}` as follows:
    Given subsets :math:`A,B\subset\mathbb{Z}`

    .. math::
        \begin{align*}
            A + B &:= \{c \in \mathbb{Z} : c = a + b
                \text{ for some }a \in A \text{ and for some } b \in B\} \\
            A \cdot B &:= \{c \in \mathbb{Z} : c = a \cdot b
                \text{ for some } a \in A \text{ and for some } b \in B\} \\
            -A &:= \{c \in \mathbb{Z} : c = -a
                \text{ for some } a \in A\}
        \end{align*}

    In words, the above equations say that over the integers:

    -   The sum of sets is the set of sums.
    -   The product of sets the set of products.
    -   The negative of a set is the set of negatives.

    So for example if :math:`A=\{3,-5,9\}` and :math:`B=\{4,12\}`, then

    .. math::
        \begin{eqnarray*}
            \{3,-5,9\}+\{4,12\} &=&\left\{
                \begin{array}{c}
                    3+4,3+12, \\
                    -5+4,-5+12, \\
                    9+4,9+12%
                \end{array}%
                \right\} \\
                &=&\left\{
                \begin{array}{c}
                    7,15, \\
                    -1,7, \\
                    13,21%
                \end{array}%
                \right\} \\
                &=&\{7,15,-1,13,21\}.
        \end{eqnarray*}

    and,

    .. math::
        \begin{eqnarray*}
        \{3,-5,9\}\cdot \{4,12\} &=&\left\{
        \begin{array}{c}
            3\cdot 4,3\cdot 12, \\
            -5\cdot 4,-5\cdot 12, \\
            9\cdot 4,9\cdot 12%
        \end{array}%
        \right\} \\
        &=&\left\{
        \begin{array}{c}
            12,36, \\
            -20,-60, \\
            36,108%
        \end{array}%
        \right\} \\
        &=&\{12,36,-20,-60,36,108\}.
        \end{eqnarray*}

    and

    .. math:: -A=-\{3,-5,9\}=\{-3,5,-9\}

    In conclusion, this shows that the algebra
    :math:`\bigg[ \mathbb{Z}, \big \{[+,0],[\cdot ,1]\}, \big \{-\}, \bigg]` extends to the algebra

    .. math::
        \begin{equation*}
            \bigg[ P(\mathbb{Z}),\{[\cup ,\varnothing ],[\mathbb{\cap },%
            \mathbb{Z}],[+,\{0\}],[\cdot ,\{1\}]\},\{-,^{\prime }\},\{\subset \}\bigg] ,
        \end{equation*}
