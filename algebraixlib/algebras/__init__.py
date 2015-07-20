r"""This package contains modules that represent :term:`algebra`\s and their operations.

To the mathematical operations of a given algebra, we also add:

-   Functions that return metadata. (For example, all our algebras contain an ``is_member``
    function that returns ``True`` if the argument is a member of the given algebra's :term:`ground
    set`. This function is not mathematically an operation of the algebra.)
-   Other functions that are mathematically related, but have arguments or return results that are
    not members of the ground set. (For example, the :func:`~.relations.get_lefts` function of the
    :term:`algebra of relations` returns a result that is not an element of the algebra's ground
    set.)

The algebras based on :term:`set`\s that are provided are:

-   :mod:`~.sets`: The :term:`algebra of sets`.
-   :mod:`~.couplets`: The :term:`algebra of couplets`.
-   :mod:`~.relations`: The :term:`algebra of relations`.
-   :mod:`~.clans`: The :term:`algebra of clans`.

The algebras based on :term:`multiset`\s that are provided are:

-   :mod:`~.multisets`: The :term:`algebra of multisets`.
-   :mod:`~.multiclans`: The :term:`algebra of multiclans`.
"""

# $Id: __init__.py 22614 2015-07-15 18:14:53Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-15 13:14:53 -0500 (Wed, 15 Jul 2015) $
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
