r"""This package contains modules that represent :term:`algebra`\s and their operations.

The algebra modules contain a class ``Algebra`` that contains the operations that are formally part
of the given algebra (that is, they are closed within that algebra). For convenience, these
functions are also exposed at the module level. (We collect them in the ``Algebra`` class mainly
for documentation purposes.)

Besides the mathematical operations of a given algebra (in ``Algebra``), we also provide the
following types of functions that are related to the algebra, but are not members of it:

-   Functions that return metadata. For example, all our algebras contain an ``is_member``
    function that returns ``True`` if the argument is a member of the given algebra's :term:`ground
    set`. This function is not mathematically an operation of the algebra.
-   Other functions that are mathematically related, but have arguments or return results that are
    not members of the ground set. For example, the :func:`~.relations.get_lefts` function of the
    :term:`algebra of relations` returns a result that is not an element of the algebra's ground
    set.

The algebras that are provided are:

-   :mod:`~.sets`: The :term:`algebra of sets`.
-   :mod:`~.couplets`: The :term:`algebra of couplets`.
-   :mod:`~.relations`: The :term:`algebra of relations`. (A :term:`relation` is a :term:`set` of
    :term:`couplet`\s).
-   :mod:`~.clans`: The :term:`algebra of clans`. (A :term:`clan` is a :term:`set` of
    :term:`relation`\s; that is, a :term:`set` of :term:`set`\s of :term:`couplet`\s).
-   :mod:`~.multisets`: The :term:`algebra of multisets`.
-   :mod:`~.multiclans`: The :term:`algebra of multiclans`. (A :term:`multiclan` is a
    :term:`multiset` of :term:`relation`\s; that is, a :term:`multiset` of :term:`set`\s of
    :term:`couplet`\s).

Additional modules:

-   :mod:`~.properties`: Functions that return the value of a property for a given `MathObject`.
    They redirect to the appropriate algebra.
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
