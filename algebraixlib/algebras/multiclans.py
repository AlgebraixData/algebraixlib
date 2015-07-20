"""This module contains the :term:`algebra of multiclans`."""

# $Id: multiclans.py 22614 2015-07-15 18:14:53Z gfiedler $
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
from functools import partial

import algebraixlib.algebras.relations as _relations
import algebraixlib.algebras.sets as _sets
import algebraixlib.mathobjects as _mo
import algebraixlib.extension as _extension
import algebraixlib.structure as _structure
from algebraixlib.undef import make_or_raise_undef as _make_or_raise_undef


class Algebra:
    """Provide the operations and relations that are members of the :term:`algebra of multiclans`.

    This class contains only static member functions. Its main purpose is to provide a namespace for
    and highlight the operations and relations that belong to the algebra of multiclans. All member
    functions are also available at the enclosing module scope.
    """
    # --------------------------------------------------------------------------------------------------
    # Unary algebra operations.

    @staticmethod
    def transpose(multiclan: 'P(P(M x M) x N)', _checked=True) -> 'P(P(M x M) x N)':
        """Return the :term:`transposition` of the :term:`multiclan` ``multiclan``.

        :return: The :term:`unary extension` of :term:`transposition` from the :term:`algebra of
            relations` to the :term:`algebra of multiclans`, applied to ``multiclan``, or `Undef()`
            if ``multiclan`` is not a :term:`multiclan`.
        """
        if _checked:
            if not is_member(multiclan):
                return _make_or_raise_undef()
        else:
            assert is_member(multiclan)
        return _extension.unary_multi_extend(multiclan, partial(
            _relations.transpose, _checked=False), _checked=False)

    # --------------------------------------------------------------------------------------------------
    # Binary algebra operations.

    @staticmethod
    def compose(multiclan1: 'P(P(M x M) x N)', multiclan2: 'P(P(M x M) x N)',
                _checked=True) -> 'P(P(M x M) x N)':
        r"""Return the :term:`composition` of ``multiclan1`` with ``multiclan2``.

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
        return _extension.binary_multi_extend(multiclan1, multiclan2, partial(
            _relations.compose, _checked=False), _checked=False)

    @staticmethod
    def cross_union(multiclan1: 'P(P(M x M) x N)', multiclan2: 'P(P(M x M) x N)',
                    _checked=True) -> 'P(P(M x M) x N)':
        r"""Return the :term:`cross-union` of ``multiclan1`` and ``multiclan2``.

        :return: The :term:`binary multi-extension` of :term:`union` from the
            :term:`algebra of relations` (which inherits it from the :term:`algebra of multisets`)
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
        return _extension.binary_multi_extend(multiclan1, multiclan2, partial(
            _sets.union, _checked=False), _checked=False)

    @staticmethod
    def functional_cross_union(multiclan1: 'P(P(M x M) x N)', multiclan2: 'P(P(M x M) x N)',
                               _checked=True) -> 'P(P(M x M) x N)':
        r"""Return the :term:`left-functional cross-union` of ``multiclan1`` and ``multiclan2``.

        :return: The :term:`binary multi-extension` of the :term:`left-functional union` from the
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
        return _extension.binary_multi_extend(multiclan1, multiclan2, partial(
            _relations.functional_union, _checked=False), _checked=False)

    @staticmethod
    def right_functional_cross_union(
            multiclan1: 'P(P(M x M) x N)', multiclan2: 'P(P(M x M) x N)',
            _checked=True) -> 'P(P(M x M) x N)':
        r"""Return the :term:`right-functional cross-union` of ``multiclan1`` and ``multiclan2``.

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
        return _extension.binary_multi_extend(multiclan1, multiclan2, partial(
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
        return _extension.binary_multi_extend(multiclan1, multiclan2, partial(
            _sets.intersect, _checked=False), _checked=False)

    @staticmethod
    def substrict(multiclan1: 'P(P(M x M) x N)', multiclan2: 'P(P(M x M) x N)',
                  _checked=True) -> 'P(P(M x M) x N)':
        r"""Return the :term:`binary extension` of :term:`substriction` of ``multiclan1`` and
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
        return _extension.binary_multi_extend(multiclan1, multiclan2, partial(
            _sets.substrict, _checked=False), _checked=False)

    @staticmethod
    def superstrict(multiclan1: 'P(P(M x M) x N)', multiclan2: 'P(P(M x M) x N)',
                    _checked=True) -> 'P(P(M x M) x N)':
        r"""Return the :term:`binary multi-extension` of :term:`superstriction` of ``multiclan1``
            and ``multiclan2``.

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
        return _extension.binary_multi_extend(multiclan1, multiclan2, partial(
            _sets.superstrict, _checked=False), _checked=False)

transpose = Algebra.transpose
compose = Algebra.compose
cross_union = Algebra.cross_union
functional_cross_union = Algebra.functional_cross_union
right_functional_cross_union = Algebra.right_functional_cross_union
cross_intersect = Algebra.cross_intersect
substrict = Algebra.substrict
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
    """Return ``True`` if ``obj`` is a member of the :term:`ground set` of this :term:`algebra`.

    .. note:: This function calls :meth:`~.MathObject.get_ground_set` on ``obj``.
    """
    _mo.raise_if_not_mathobject(obj)
    if not obj.cached_is_multiclan and not obj.cached_is_not_multiclan:
        obj.cache_is_multiclan(obj.get_ground_set().is_subset(get_ground_set()))
    return obj.cached_is_multiclan


def is_absolute_member(obj: _mo.MathObject) -> bool:
    """Return ``True`` if ``obj`` is a member of the :term:`absolute ground set` of this algebra.

     :return: ``True`` if ``obj`` is an :term:`absolute clan`.

    .. note:: This function calls :meth:`~.MathObject.get_ground_set` on ``obj``.
    """
    _mo.raise_if_not_mathobject(obj)
    return obj.get_ground_set().is_subset(get_absolute_ground_set())
