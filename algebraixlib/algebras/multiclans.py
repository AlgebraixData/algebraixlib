r"""This module contains the :term:`algebra of multiclans` and related functionality.

A :term:`multiclan` is also a :term:`multiset` (of :term:`relation`\s), and inherits all operations
of the :term:`algebra of multisets`. These are provided in :mod:`~.algebras.multisets`.
"""

# $Id: multiclans.py 22702 2015-07-28 20:20:56Z jaustell $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-28 15:20:56 -0500 (Tue, 28 Jul 2015) $
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
import functools as _functools

import algebraixlib.algebras.relations as _relations
import algebraixlib.algebras.sets as _sets
import algebraixlib.mathobjects as _mo
import algebraixlib.extension as _extension
import algebraixlib.structure as _structure
from algebraixlib.undef import make_or_raise_undef as _make_or_raise_undef


# --------------------------------------------------------------------------------------------------

class Algebra:
    """Provide the operations and relations that are members of the :term:`algebra of multiclans`.

    This class contains only static member functions. Its main purpose is to provide a namespace for
    and highlight the operations and relations that belong to the algebra of multiclans. All member
    functions are also available at the enclosing module scope.
    """
    # ----------------------------------------------------------------------------------------------
    # Unary algebra operations.

    @staticmethod
    def transpose(multiclan: 'P(P(M x M) x N)', _checked=True) -> 'P(P(M x M) x N)':
        """Return a multiclan where all relations have their left and right components swapped.

        :return: The :term:`unary multi-extension` of :term:`transposition` from the
            :term:`algebra of relations` to the :term:`algebra of multiclans`, applied to
            ``multiclan``, or `Undef()` if ``multiclan`` is not a :term:`multiclan`.
        """
        if _checked:
            if not is_member(multiclan):
                return _make_or_raise_undef()
        else:
            assert is_member(multiclan)
        return _extension.unary_multi_extend(multiclan, _functools.partial(
            _relations.transpose, _checked=False), _checked=False)

    # ----------------------------------------------------------------------------------------------
    # Binary algebra operations.

    @staticmethod
    def compose(multiclan1: 'P(P(M x M) x N)', multiclan2: 'P(P(M x M) x N)',
                _checked=True) -> 'P(P(M x M) x N)':
        r"""Return the composition of ``multiclan1`` with ``multiclan2``.

        :return: The :term:`binary multi-extension` of :term:`composition` from the
            :term:`algebra of relations` to the :term:`algebra of multiclans`, applied to
            ``multiclan1`` and ``multiclan2``, or `Undef()` if ``multiclan1`` or ``multiclan2``
            are not :term:`multiclan`\s.
        """
        if _checked:
            if not is_member(multiclan1):
                return _make_or_raise_undef()
            if not is_member(multiclan2):
                return _make_or_raise_undef()
        else:
            assert is_member(multiclan1)
            assert is_member(multiclan2)
        return _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _relations.compose, _checked=False), _checked=False)

    @staticmethod
    def cross_union(multiclan1: 'P(P(M x M) x N)', multiclan2: 'P(P(M x M) x N)',
                    _checked=True) -> 'P(P(M x M) x N)':
        r"""Return the :term:`cross-union` of ``multiclan1`` and ``multiclan2``.

        :return: The :term:`binary multi-extension` of :term:`union` from the
            :term:`algebra of relations` (which inherits it from the :term:`algebra of sets`)
            to the :term:`algebra of multiclans` applied to ``multiclan1`` and ``multiclan2``,
            or `Undef()` if ``multiclan1`` or ``multiclan2`` are not :term:`multiclan`\s.
        """
        if _checked:
            if not is_member(multiclan1):
                return _make_or_raise_undef()
            if not is_member(multiclan2):
                return _make_or_raise_undef()
        else:
            assert is_member(multiclan1)
            assert is_member(multiclan2)
        return _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _sets.union, _checked=False), _checked=False)

    @staticmethod
    def cross_functional_union(multiclan1: 'P(P(M x M) x N)', multiclan2: 'P(P(M x M) x N)',
                               _checked=True) -> 'P(P(M x M) x N)':
        r"""Return the :term:`cross-functional union` of ``multiclan1`` and ``multiclan2``.

        :return: The :term:`binary multi-extension` of the :term:`functional union` from the
            :term:`algebra of relations` to the :term:`algebra of multiclans`, applied to
            ``multiclan1`` and ``multiclan2``, or `Undef()` if ``multiclan1`` or ``multiclan2`` are
            not :term:`multiclan`\s.
        """
        if _checked:
            if not is_member(multiclan1):
                return _make_or_raise_undef()
            if not is_member(multiclan2):
                return _make_or_raise_undef()
        else:
            assert is_member(multiclan1)
            assert is_member(multiclan2)
        return _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _relations.functional_union, _checked=False), _checked=False)

    @staticmethod
    def cross_right_functional_union(
            multiclan1: 'P(P(M x M) x N)', multiclan2: 'P(P(M x M) x N)',
            _checked=True) -> 'P(P(M x M) x N)':
        r"""Return the :term:`cross-right-functional union` of ``multiclan1`` and ``multiclan2``.

        :return: The :term:`binary multi-extension` of the :term:`right-functional union` from the
            :term:`algebra of relations` to the :term:`algebra of multiclans`, applied to
            ``multiclan1`` and ``multiclan2``, or `Undef()` if ``multiclan1`` or ``multiclan2`` are
            not :term:`multiclan`\s.
        """
        if _checked:
            if not is_member(multiclan1):
                return _make_or_raise_undef()
            if not is_member(multiclan2):
                return _make_or_raise_undef()
        else:
            assert is_member(multiclan1)
            assert is_member(multiclan2)
        return _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _relations.right_functional_union, _checked=False), _checked=False)

    @staticmethod
    def cross_intersect(multiclan1: 'P(P(M x M) x N)', multiclan2: 'PP(M x M)',
                        _checked=True) -> 'PP(M x M)':
        r"""Return the :term:`cross-intersection` of ``multiclan1`` and ``multiclan2``.

        :return: The :term:`binary multi-extension` of :term:`intersection` from the :term:`algebra
            of relations` (which inherits it from the :term:`algebra of sets`) to the :term:`algebra
            of multiclans` applied to ``multiclan1`` and ``multiclan2``, or `Undef()` if
            ``multiclan1`` or ``multiclan2`` are not :term:`multiclan`\s.
        """
        if _checked:
            if not is_member(multiclan1):
                return _make_or_raise_undef()
            if not is_member(multiclan2):
                return _make_or_raise_undef()
        else:
            assert is_member(multiclan1)
            assert is_member(multiclan2)
        return _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _sets.intersect, _checked=False), _checked=False)

    @staticmethod
    def substrict(multiclan1: 'P(P(M x M) x N)', multiclan2: 'P(P(M x M) x N)',
                  _checked=True) -> 'P(P(M x M) x N)':
        r"""Return the substriction of ``multiclan1`` and ``multiclan2``.

        The :term:`substriction` of two :term:`multiclan`\s is a multiclan that contains all
        :term:`relation`\s from ``multiclan1`` that are a :term:`submultiset` of a relation from
        ``multiclan2``.

        :return: The :term:`binary multi-extension` of :term:`substriction` from the :term:`algebra
            of relations` (which inherits it from the :term:`algebra of sets`) to the :term:`algebra
            of multiclans` applied to ``multiclan1`` and ``multiclan2``, or `Undef()` if
            ``multiclan1`` or ``multiclan2`` are not :term:`multiclan`\s.
        """
        if _checked:
            if not is_member(multiclan1):
                return _make_or_raise_undef()
            if not is_member(multiclan2):
                return _make_or_raise_undef()
        else:
            assert is_member(multiclan1)
            assert is_member(multiclan2)
        return _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _sets.substrict, _checked=False), _checked=False)

    @staticmethod
    def superstrict(multiclan1: 'P(P(M x M) x N)', multiclan2: 'P(P(M x M) x N)',
                    _checked=True) -> 'P(P(M x M) x N)':
        r"""Return the superstriction of ``multiclan1`` and ``multiclan2``.

        The :term:`superstriction` of two :term:`multiclan`\s is a multiclan that contains all
        :term:`relation`\s from ``multiclan1`` that are a :term:`supermultiset` of a relation from
        ``multiclan2``.

        :return: The :term:`binary multi-extension` of :term:`superstriction` from the
            :term:`algebra of relations` (which inherits it from the :term:`algebra of sets`) to the
            :term:`algebra of multiclans` applied to ``multiclan1`` and ``multiclan2``, or `Undef()`
            if ``multiclan1`` or ``multiclan2`` are not :term:`multiclan`\s.
        """
        if _checked:
            if not is_member(multiclan1):
                return _make_or_raise_undef()
            if not is_member(multiclan2):
                return _make_or_raise_undef()
        else:
            assert is_member(multiclan1)
            assert is_member(multiclan2)
        return _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _sets.superstrict, _checked=False), _checked=False)


# For convenience, make the members of class Algebra (they are all static functions) available at
# the module level.

#: Convenience redirection to `Algebra.transpose`.
transpose = Algebra.transpose
#: Convenience redirection to `Algebra.compose`.
compose = Algebra.compose
#: Convenience redirection to `Algebra.cross_union`.
cross_union = Algebra.cross_union
#: Convenience redirection to `Algebra.cross_functional_union`.
cross_functional_union = Algebra.cross_functional_union
#: Convenience redirection to `Algebra.cross_right_functional_union`.
cross_right_functional_union = Algebra.cross_right_functional_union
#: Convenience redirection to `Algebra.cross_intersect`.
cross_intersect = Algebra.cross_intersect
#: Convenience redirection to `Algebra.substrict`.
substrict = Algebra.substrict
#: Convenience redirection to `Algebra.superstrict`.
superstrict = Algebra.superstrict


# --------------------------------------------------------------------------------------------------
# Metadata functions.

def get_name() -> str:
    """Return the name and :term:`ground set` of this :term:`algebra` in string form."""
    return 'Multiclans(M): {ground_set}'.format(ground_set=str(get_ground_set()))


def get_ground_set() -> _structure.Structure:
    """Return the :term:`ground set` of this :term:`algebra`."""
    return _structure.PowerSet(
        _structure.CartesianProduct(_relations.get_ground_set(), _structure.GenesisSetN()))


def get_absolute_ground_set() -> _structure.Structure:
    """Return the :term:`absolute ground set` of this :term:`algebra`."""
    return _structure.PowerSet(
        _structure.CartesianProduct(_relations.get_absolute_ground_set(), _structure.GenesisSetN()))


def is_member(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is a member of the :term:`ground set` of this :term:`algebra`.

    .. note:: This function calls :meth:`~.MathObject.get_ground_set` on ``obj``.
    """
    _mo.raise_if_not_mathobject(obj)
    if not obj.cached_is_multiclan and not obj.cached_is_not_multiclan:
        obj.cache_is_multiclan(obj.get_ground_set().is_subset(get_ground_set()))
    return obj.cached_is_multiclan


def is_absolute_member(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is a member of the :term:`absolute ground set` of this algebra.

     :return: ``True`` if ``obj`` is an :term:`absolute clan`, ``False`` if not.

    .. note:: This function calls :meth:`~.MathObject.get_ground_set` on ``obj``.
    """
    _mo.raise_if_not_mathobject(obj)
    return obj.get_ground_set().is_subset(get_absolute_ground_set())
