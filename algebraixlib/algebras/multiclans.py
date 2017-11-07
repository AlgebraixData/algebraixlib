r"""This module contains the :term:`algebra of multiclans` and related functionality.

A :term:`multiclan` is also a :term:`multiset` (of :term:`relation`\s), and inherits all operations
of the :term:`algebra of multisets`. These are provided in :mod:`~.algebras.multisets`.
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
import functools as _functools

import algebraixlib.algebras.multisets as _multisets
import algebraixlib.algebras.relations as _relations
import algebraixlib.algebras.sets as _sets
import algebraixlib.mathobjects as _mo
import algebraixlib.extension as _extension
import algebraixlib.structure as _structure
import algebraixlib.undef as _undef

from ..cache_status import CacheStatus


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
                return _undef.make_or_raise_undef2(multiclan)
        else:
            assert is_member_or_undef(multiclan)
            if multiclan is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.unary_multi_extend(multiclan, _functools.partial(
            _relations.transpose, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_multiclan(CacheStatus.IS)
            result.cache_absolute(multiclan.cached_absolute)
            result.cache_functional(multiclan.cached_right_functional)
            result.cache_right_functional(multiclan.cached_functional)
            result.cache_reflexive(multiclan.cached_reflexive)
            result.cache_symmetric(multiclan.cached_symmetric)
            result.cache_transitive(multiclan.cached_transitive)
            result.cache_regular(multiclan.cached_right_regular)
            result.cache_right_regular(multiclan.cached_regular)
        return result

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
                return _undef.make_or_raise_undef2(multiclan1)
            if not is_member(multiclan2):
                return _undef.make_or_raise_undef2(multiclan2)
        else:
            assert is_member_or_undef(multiclan1)
            assert is_member_or_undef(multiclan2)
            if multiclan1 is _undef.Undef() or multiclan2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _relations.compose, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_multiclan(CacheStatus.IS)
            if multiclan1.cached_is_absolute and multiclan2.cached_is_absolute:
                result.cache_absolute(CacheStatus.IS)
            if multiclan1.cached_is_functional and multiclan2.cached_is_functional:
                result.cache_functional(CacheStatus.IS)
            if multiclan1.cached_is_right_functional and multiclan2.cached_is_right_functional:
                result.cache_right_functional(CacheStatus.IS)
        return result

    @staticmethod
    def cross_union(mclan1: 'P(P(M x M) x N)', mclan2: 'P(P(M x M) x N)',
                    _checked=True) -> 'P(P(M x M) x N)':
        r"""Return the :term:`cross-union` of ``mclan1`` and ``mclan2``.

        :return: The :term:`binary multi-extension` of :term:`union` from the
            :term:`algebra of relations` (which inherits it from the :term:`algebra of sets`)
            to the :term:`algebra of multiclans` applied to ``mclan1`` and ``mclan2``,
            or `Undef()` if ``mclan1`` or ``mclan2`` are not :term:`multiclan`\s.
        """
        if _checked:
            if not is_member(mclan1):
                return _undef.make_or_raise_undef2(mclan1)
            if not is_member(mclan2):
                return _undef.make_or_raise_undef2(mclan2)
        else:
            assert is_member_or_undef(mclan1)
            assert is_member_or_undef(mclan2)
            if mclan1 is _undef.Undef() or mclan2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.binary_multi_extend(mclan1, mclan2, _functools.partial(
            _sets.union, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_multiclan(CacheStatus.IS)
            if mclan1.cached_is_not_functional or mclan2.cached_is_not_functional:
                result.cache_functional(CacheStatus.IS_NOT)
            if mclan1.cached_is_not_right_functional or mclan2.cached_is_not_right_functional:
                result.cache_right_functional(CacheStatus.IS_NOT)
        return result

    @staticmethod
    def cross_functional_union(mclan1: 'P(P(M x M) x N)', mclan2: 'P(P(M x M) x N)',
                               _checked=True) -> 'P(P(M x M) x N)':
        r"""Return the :term:`cross-functional union` of ``mclan1`` and ``mclan2``.

        :return: The :term:`binary multi-extension` of the :term:`functional union` from the
            :term:`algebra of relations` to the :term:`algebra of multiclans`, applied to
            ``mclan1`` and ``mclan2``, or `Undef()` if ``mclan1`` or ``mclan2`` are
            not :term:`multiclan`\s.
        """
        if _checked:
            if not is_member(mclan1):
                return _undef.make_or_raise_undef2(mclan1)
            if not is_member(mclan2):
                return _undef.make_or_raise_undef2(mclan2)
        else:
            assert is_member_or_undef(mclan1)
            assert is_member_or_undef(mclan2)
            if mclan1 is _undef.Undef() or mclan2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.binary_multi_extend(mclan1, mclan2, _functools.partial(
            _relations.functional_union, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_multiclan(CacheStatus.IS)
            result.cache_functional(CacheStatus.IS)
            if mclan1.cached_is_not_right_functional or mclan2.cached_is_not_right_functional:
                result.cache_right_functional(CacheStatus.IS_NOT)
        return result

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
                return _undef.make_or_raise_undef2(multiclan1)
            if not is_member(multiclan2):
                return _undef.make_or_raise_undef2(multiclan2)
        else:
            assert is_member_or_undef(multiclan1)
            assert is_member_or_undef(multiclan2)
            if multiclan1 is _undef.Undef() or multiclan2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _relations.right_functional_union, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_multiclan(CacheStatus.IS)
            result.cache_right_functional(CacheStatus.IS)
            if multiclan1.cached_is_not_functional or multiclan2.cached_is_not_functional:
                result.cache_functional(CacheStatus.IS_NOT)
        return result

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
                return _undef.make_or_raise_undef2(multiclan1)
            if not is_member(multiclan2):
                return _undef.make_or_raise_undef2(multiclan2)
        else:
            assert is_member_or_undef(multiclan1)
            assert is_member_or_undef(multiclan2)
            if multiclan1 is _undef.Undef() or multiclan2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _sets.intersect, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_multiclan(CacheStatus.IS)
            if multiclan1.cached_is_functional or multiclan2.cached_is_functional:
                result.cache_functional(CacheStatus.IS)
            if multiclan1.cached_is_right_functional or multiclan2.cached_is_right_functional:
                result.cache_right_functional(CacheStatus.IS)
        return result

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
                return _undef.make_or_raise_undef2(multiclan1)
            if not is_member(multiclan2):
                return _undef.make_or_raise_undef2(multiclan2)
        else:
            assert is_member_or_undef(multiclan1)
            assert is_member_or_undef(multiclan2)
            if multiclan1 is _undef.Undef() or multiclan2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _sets.substrict, _checked=False), _checked=False)
        for elem, multi in result.data.items():
            result.data[elem] = multiclan1.data[elem]
        if not result.is_empty:
            result.cache_multiclan(CacheStatus.IS)
            if multiclan1.cached_is_functional or multiclan2.cached_is_functional:
                result.cache_functional(CacheStatus.IS)
            if multiclan1.cached_is_right_functional or multiclan2.cached_is_right_functional:
                result.cache_right_functional(CacheStatus.IS)
            if multiclan1.cached_is_reflexive:
                result.cache_reflexive(CacheStatus.IS)
            if multiclan1.cached_is_symmetric:
                result.cache_symmetric(CacheStatus.IS)
            if multiclan1.cached_is_transitive:
                result.cache_transitive(CacheStatus.IS)
            if multiclan1.cached_is_regular:
                result.cache_regular(CacheStatus.IS)
            if multiclan1.cached_is_right_regular:
                result.cache_right_regular(CacheStatus.IS)
        return result

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
                return _undef.make_or_raise_undef2(multiclan1)
            if not is_member(multiclan2):
                return _undef.make_or_raise_undef2(multiclan2)
        else:
            assert is_member_or_undef(multiclan1)
            assert is_member_or_undef(multiclan2)
            if multiclan1 is _undef.Undef() or multiclan2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _sets.superstrict, _checked=False), _checked=False)
        for elem, multi in result.data.items():
            result.data[elem] = multiclan2.data[elem]
        if not result.is_empty:
            result.cache_multiclan(CacheStatus.IS)
            if multiclan1.cached_is_functional:
                result.cache_functional(CacheStatus.IS)
            if multiclan1.cached_is_right_functional:
                result.cache_right_functional(CacheStatus.IS)
            if multiclan1.cached_is_reflexive:
                result.cache_reflexive(CacheStatus.IS)
            if multiclan1.cached_is_symmetric:
                result.cache_symmetric(CacheStatus.IS)
            if multiclan1.cached_is_transitive:
                result.cache_transitive(CacheStatus.IS)
            if multiclan1.cached_is_regular:
                result.cache_regular(CacheStatus.IS)
            if multiclan1.cached_is_right_regular:
                result.cache_right_regular(CacheStatus.IS)
        return result


# For convenience, make the members of class Algebra (they are all static functions) available at
# the module level.

# pylint: disable=invalid-name

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

# pylint: enable=invalid-name


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

     :return: ``True`` if ``obj`` is a :term:`multiclan`, ``False`` if not.

    .. note:: This function may call :meth:`~.MathObject.get_ground_set` on ``obj``. The result of
        this operation is cached.
    """
    if obj.cached_multiclan == CacheStatus.UNKNOWN:
        is_multiclan = obj.get_ground_set().is_subset(get_ground_set())
        obj.cache_multiclan(CacheStatus.from_bool(is_multiclan))
    return obj.cached_is_multiclan


def is_member_or_undef(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is either a member of the :term:`ground set` of this :term:`algebra`
        or :class:`~.Undef`.

     :return: ``True`` if ``obj`` is either a :term:`relation` or :class:`~.Undef`,
        ``False`` if not.
    """
    return obj is _undef.Undef() or is_member(obj)


def is_absolute_member(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is a member of the :term:`absolute ground set` of this algebra.

     :return: ``True`` if ``obj`` is an :term:`absolute clan`, ``False`` if not.

    .. note:: This function may call :meth:`~.MathObject.get_ground_set` on ``obj``. The result
        of this operation is cached.
    """
    if obj.cached_is_not_multiclan:
        # If known to not be a multiclan, it's also not an absolute multiclan. No further caching.
        return False
    # The `or` clause in this `if` statement is a safety thing. It should never hit.
    if obj.cached_absolute == CacheStatus.UNKNOWN \
            or obj.cached_multiclan == CacheStatus.UNKNOWN:
        # The 'absolute' state has not yet been cached. Determine whether obj is an absolute
        # multiclan.
        is_absolute_mclan = obj.get_ground_set().is_subset(get_absolute_ground_set())
        if obj.cached_multiclan == CacheStatus.UNKNOWN:
            if is_absolute_mclan:
                # If it is an absolute multiclan, it is also a multiclan.
                obj.cache_multiclan(CacheStatus.IS)
            else:
                # If it is not an absolute multiclan, it may still be a multiclan.
                is_mclan = is_member(obj)
                if not is_mclan:
                    # If it is neither an absolute multiclan nor a multiclan, exit. (That it is
                    # not a multiclan has already been cached in is_member().)
                    return False
        # At this point, cached_multiclan == IS. Cache whether this is an absolute multiclan.
        assert obj.cached_is_multiclan
        obj.cache_absolute(CacheStatus.from_bool(is_absolute_mclan))
    # At this point, cached_multiclan == IS. Return whether it is an absolute multiclan.
    return obj.cached_is_absolute


# --------------------------------------------------------------------------------------------------
# Related operations, not formally part of the algebra.

def get_lefts(mclan: 'P(P(M x M) x N)', _checked=True) -> 'P( M )':
    r"""Return the set of the left components of all couplets in all relations in ``mclan``.

    :return: The :term:`union` of the :term:`left set`\s of all :term:`relation`\s in ``mclan`` or
        `Undef()` if ``mclan`` is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef2(mclan)
    else:
        assert is_member_or_undef(mclan)
        if mclan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if mclan.is_empty:
        # The left set of an empty set is the empty set
        return mclan
    clan_itr = iter(mclan)
    left_set = _relations.get_lefts(next(clan_itr), _checked=False)
    for rel in clan_itr:
        left_set = _sets.union(
            _relations.get_lefts(rel, _checked=False), left_set, _checked=False)
    if not left_set.is_empty:
        if mclan.cached_is_absolute:
            left_set.cache_absolute(CacheStatus.IS)
    return left_set


def get_rights(mclan: 'P(P(M x M) x N)', _checked=True) -> 'P( M )':
    r"""Return the set of the right components of all couplets in all relations in ``mclan``.

    :return: The :term:`union` of the :term:`right set`\s of all :term:`relation`\s in ``mclan`` or
        `Undef()` if ``mclan`` is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef2(mclan)
    else:
        assert is_member_or_undef(mclan)
        if mclan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if mclan.is_empty:
        # The right set of an empty set is the empty set
        return mclan
    clan_itr = iter(mclan)
    right_set = _relations.get_rights(next(clan_itr), _checked=False)
    for rel in clan_itr:
        right_set = _sets.union(
            _relations.get_rights(rel, _checked=False), right_set, _checked=False)
    if not right_set.is_empty:
        if mclan.cached_is_absolute:
            right_set.cache_absolute(CacheStatus.IS)
    return right_set


def get_rights_for_left(mclan: 'P(P(M x M) x N)', left: '( M )', _checked=True) -> 'P(M x N)':
    """Return the multiset of the right components of all couplets in the multiclan ``mclan``
    associated with the left component ``left``.

    :return: The :term:`right multiset` of the :term:`multiclan` ``mclan`` associated with the
        :term:`left component` ``left`` or `Undef()` if ``mclan`` is not a multiclan.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef2(mclan)
        if left is _undef.Undef():
            return _mo.Set()
        left = _mo.auto_convert(left)
    else:
        assert is_member_or_undef(mclan)
        assert _mo.is_mathobject_or_undef(left)
        if mclan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
        if left is _undef.Undef():
            return _mo.Set()
    clan_itr = iter(mclan)
    rights = _sets.multify(_relations.get_rights_for_left(next(clan_itr), left, _checked=False))
    for rel in clan_itr:
        rights = _multisets.add(
            _sets.multify(_relations.get_rights_for_left(rel, left, _checked=False)),
            rights, _checked=False)
    if not rights.is_empty:
        if mclan.cached_is_absolute:
            rights.cache_absolute(CacheStatus.IS)
    return rights


def is_functional(mclan, _checked=True) -> bool:
    """Return whether ``mclan`` is functional.

    :return: ``True`` if every :term:`relation` in ``mclan`` is :term:`functional` (is a
        :term:`function`), ``False`` if not, or `Undef()` if ``mclan`` is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef2(mclan)
    else:
        assert is_member_or_undef(mclan)
        if mclan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if mclan.cached_functional == CacheStatus.UNKNOWN:
        # The empty set is already handled in Set().__init__ via flags initialization.
        functional = all(_relations.is_functional(rel, _checked=False) for rel in mclan.data)
        mclan.cache_functional(CacheStatus.from_bool(functional))
    return mclan.cached_is_functional


def is_right_functional(mclan, _checked=True) -> bool:
    """Return whether ``mclan`` is right-functional.

    :return: ``True`` if every :term:`relation` in ``mclan`` is :term:`right-functional`, ``False``
        if not, or `Undef()` if ``mclan`` is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef2(mclan)
    else:
        assert is_member_or_undef(mclan)
        if mclan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if mclan.cached_right_functional == CacheStatus.UNKNOWN:
        # The empty set is already handled in Set().__init__ via flags initialization.
        right_functional = all(
            _relations.is_right_functional(rel, _checked=False) for rel in mclan.data)
        mclan.cache_right_functional(CacheStatus.from_bool(right_functional))
    return mclan.cached_is_right_functional


def is_regular(mclan, _checked=True) -> bool:
    """Return whether ``mclan`` is (left-)regular.

    :return: ``True`` if ``mclan`` is :term:`regular`, ``False`` if not, or `Undef()` if ``mclan``
        is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef2(mclan)
    else:
        assert is_member_or_undef(mclan)
        if mclan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if mclan.cached_regular == CacheStatus.UNKNOWN:
        # The empty set is already handled in Set().__init__ via flags initialization.
        if mclan.cached_is_not_functional:
            mclan.cache_regular(CacheStatus.IS_NOT)
            return False
        itr = iter(mclan.data)
        rel = next(itr)
        if not _relations.is_functional(rel):
            mclan.cache_regular(CacheStatus.IS_NOT)
            return False
        left_set = rel.get_left_set()
        regular = all(
            _relations.is_functional(rel) and left_set == rel.get_left_set() for rel in itr)
        mclan.cache_regular(CacheStatus.from_bool(regular))
    return mclan.cached_is_regular


def is_right_regular(mclan, _checked=True) -> bool:
    """Return whether ``mclan`` is right-regular.

    :return: ``True`` if ``mclan`` is :term:`right-regular`, ``False`` if not, or `Undef()` if
        ``mclan`` is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef2(mclan)
    else:
        assert is_member_or_undef(mclan)
        if mclan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if mclan.cached_right_regular == CacheStatus.UNKNOWN:
        # The empty set is already handled in Set().__init__ via flags initialization.
        if mclan.cached_is_not_right_functional:
            mclan.cache_right_regular(CacheStatus.IS_NOT)
            return False
        itr = iter(mclan.data)
        rel = next(itr)
        if not _relations.is_right_functional(rel):
            mclan.cache_right_regular(CacheStatus.IS_NOT)
            return False
        right_set = rel.get_right_set()
        right_regular = all(
            _relations.is_right_functional(rel) and right_set == rel.get_right_set() for rel in itr)
        mclan.cache_regular(CacheStatus.from_bool(right_regular))
    return mclan.cached_is_regular


def is_reflexive(mclan, _checked=True) -> bool:
    """Return whether ``mclan`` is reflexive.

    :return: ``True`` if ``mclan`` is :term:`reflexive`, ``False`` if it is not, or `Undef()` if
        ``mclan`` is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef2(mclan)
    else:
        assert is_member_or_undef(mclan)
        if mclan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if mclan.cached_reflexive == CacheStatus.UNKNOWN:
        reflexive = all(_relations.is_reflexive(rel, _checked=False) for rel in mclan.data)
        mclan.cache_reflexive(CacheStatus.from_bool(reflexive))
    return mclan.cached_reflexive == CacheStatus.IS


def is_symmetric(mclan, _checked=True) -> bool:
    """Return whether ``mclan`` is symmetric.

    :return: ``True`` if ``mclan`` is :term:`symmetric`, ``False`` if it is not, or `Undef()` if
        ``mclan`` is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef2(mclan)
    else:
        assert is_member_or_undef(mclan)
        if mclan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if mclan.cached_symmetric == CacheStatus.UNKNOWN:
        symmetric = all(_relations.is_symmetric(rel, _checked=False) for rel in mclan.data)
        mclan.cache_symmetric(CacheStatus.from_bool(symmetric))
    return mclan.cached_symmetric == CacheStatus.IS


def is_transitive(mclan, _checked=True) -> bool:
    """Return whether ``mclan`` is transitive.

    :return: ``True`` if ``mclan`` is :term:`transitive`, ``False`` if it is not, or `Undef()` if
        ``mclan`` is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef2(mclan)
    else:
        assert is_member_or_undef(mclan)
        if mclan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if mclan.cached_transitive == CacheStatus.UNKNOWN:
        transitive = all(_relations.is_transitive(rel, _checked=False) for rel in mclan.data)
        mclan.cache_transitive(CacheStatus.from_bool(transitive))
    return mclan.cached_transitive == CacheStatus.IS


def project(mclan: 'P(P(M x M) x N)', *lefts) -> 'P(P(M x M) x N)':
    r"""Return a multiclan that contains only the couplets with lefts from ``mclan`` that match
    ``lefts``.

    :param mclan: The source data. Must be a :term:`multiclan`.
    :param lefts: The names of the :term:`left component`\s to match. (If you want to pass in an
        iterable, you need to prefix it with an asterisk ``*``.)
    :return: The :term:`projection` of ``mclan`` (a multiclan that contains only :term:`couplet`\s
        with left components as indicated by ``lefts``), or `Undef()` if ``mclan`` is not a
        multiclan.
    """
    if not is_member(mclan):
        return _undef.make_or_raise_undef2(mclan)
    mclan = compose(mclan, diag(*lefts))
    return mclan


def _to_listgen_check_args(mclan: 'P(P(M x M) x N)', offset: '( A )', limit: '( A )',
        _checked: bool=True) -> ():
    """Check the arguments of `multiclan_to_listgen` and `order_slice_to_listgen`. Return a tuple
    with the clean values of ``offset`` and ``limit`` or `Undef()` if there was a problem.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef2(mclan)
        if isinstance(offset, _mo.Atom) and isinstance(offset.value, int):
            pass
        elif isinstance(offset, int):
            offset = _mo.Atom(limit)
        elif offset is _undef.Undef():
            return _undef.make_or_raise_undef(2)
        else:
            return _undef.make_or_raise_undef()
        if isinstance(limit, _mo.Atom) \
                and (isinstance(limit.value, int) or limit.value == float('inf')):
            pass
        elif isinstance(limit, int) or limit == float('inf'):
            limit = _mo.Atom(limit)
        elif limit is _undef.Undef():
            return _undef.make_or_raise_undef(2)
        else:
            return _undef.make_or_raise_undef()
    else:
        if mclan is _undef.Undef() or offset is _undef.Undef() or limit is _undef.Undef():
            return _undef.make_or_raise_undef(2)
        assert is_member(mclan)
        assert offset.is_atom and isinstance(offset.value, int)
        assert limit.is_atom and (isinstance(limit.value, int) or limit.value == float('inf'))
    return offset, limit


def _to_listgen_slice(counter_list: [()], offset, limit):
    """Slice ``counter_list`` according to ``offset`` and ``limit`` considering the multiplicities
    in the second elements of the 2-tuples in ``counter_list``. Return a list or a list generator.
    """
    start_offset = offset.value
    end_offset = limit.value + start_offset
    if start_offset == 0 and end_offset >= float('inf'):
        # Effectively no offset and limit. Return sorted list as-is.
        return counter_list

    # Find the list indices of the first and last tuple (representing a relation and a multiplicity)
    # and the resulting multiplicities in these first and last tuples (which may be different from
    # their original multiplicities).
    start_index = first_multiple = None
    end_index = last_multiple = None
    start_offset_next_tuple = 0
    for index, counter_entry in enumerate(counter_list):
        # Calculate the starting offset of the next tuple (by adding the multiplicity of the
        # current tuple).
        start_offset_next_tuple += counter_entry[1]
        if start_index is None and start_offset < start_offset_next_tuple:
            start_index = index
            first_multiple = start_offset_next_tuple - start_offset
            assert first_multiple <= counter_list[start_index][1]
        if start_index is not None and end_offset <= start_offset_next_tuple:
            end_index = index
            last_multiple = counter_list[end_index][1] - (start_offset_next_tuple - end_offset)
            assert counter_list[end_index][1] > (start_offset_next_tuple - end_offset)
            break
    if start_index is None:
        # No start_index found: start_offset is bigger than all existing offsets. Nothing selected.
        assert end_index is None
        return []
    if end_index is None:
        # No end_index found: end_offset is bigger than all existing offsets. Put end_index beyond
        # list bounds.
        end_index = len(counter_list)

    # If needed, adjust the multiplicities of the first and last tuple in the selected range.
    if start_index < len(counter_list) and counter_list[start_index][1] != first_multiple:
        counter_list[start_index] = (counter_list[start_index][0], first_multiple)
    if end_index < len(counter_list) and counter_list[end_index][1] != last_multiple:
        counter_list[end_index] = (counter_list[end_index][0], last_multiple)

    # Create and return a generator expression to avoid another copy of the data.
    limited_list_iter = (counter_tuple for counter_tuple in counter_list[start_index:end_index + 1])
    return limited_list_iter


def multiclan_to_listgen(mclan: 'P(P(M x M) x N)', offset: '( A )', limit: '( A )',
        _checked: bool=True) -> [()]:
    r"""Return a generator expression for a list of tuples that contains the relations with indices
    ``offset <= index < offset + limit``. Note that because of the lack of order the result is
    not deterministic when using ``offset`` or ``limit``. (See also `order_slice_to_listgen`.)
    Each tuple contains a relation and its multiplicity.

    :param mclan: The source data. Must be a :term:`multiclan`.
    :param offset: An :term:`atom` with an integer value that indicates the index of the first
        relation (after sorting the multiclan) in the result. Set to ``Atom(0)`` if you want to
        start with the first relation of the sorted multiclan.
    :param limit: An atom with an integer value that indicates how many relations should be in
        the resulting multiclan. When ``limit`` is ``float('inf')``, all relations are returned.
    """
    checked_args = _to_listgen_check_args(mclan, offset, limit, _checked)
    if checked_args is _undef.Undef():
        return _undef.Undef()
    offset, limit = checked_args

    if mclan.cardinality == 0:
        return []

    counter_list = list(mclan.data.items())
    return _to_listgen_slice(counter_list, offset, limit)


def order_slice_to_listgen(mclan: 'P(P(M x M) x N)', less_than_f,
        offset: '( A )', limit: '( A )', _checked: bool=True) -> [()]:
    r"""Return a generator expression for a list of tuples that contains the relations with indices
    ``offset <= index < offset + limit``, after having been ordered according to ``order``. Each
    tuple contains a relation and its multiplicity.

    :param mclan: The source data. Must be a :term:`multiclan`.
    :param less_than_f: A function that accepts two :term:`relation`\s as arguments and returns
        ``True`` if the first one is less than the second one.
    :param offset: An :term:`atom` with an integer value that indicates the index of the first
        relation (after sorting the multiclan) in the result. Set to ``Atom(0)`` if you want to
        start with the first relation of the sorted multiclan.
    :param limit: An atom with an integer value that indicates how many relations should be in
        the resulting multiclan. When ``limit`` is ``float('inf')``, all relations are returned.

    .. note:: Eventually we may add a `MathObject` representation for sequences ('ordered sets').
        Until we do, we can't split the application of offset and limit from the ordering/sorting.
    """
    checked_args = _to_listgen_check_args(mclan, offset, limit, _checked)
    if checked_args is _undef.Undef():
        return _undef.Undef()
    offset, limit = checked_args

    if mclan.cardinality == 0:
        return []

    counter_list = list(mclan.data.items())

    class Key:
        def __init__(self, relation, less_than):
            self._rel = relation
            self._lt = less_than

        def __lt__(self, other) -> bool:
            assert isinstance(other, Key)
            result = self._lt(self._rel, other._rel)
            return result.value

    def make_key(multiset_tuple) -> Key:
        result = Key(relation=multiset_tuple[0], less_than=less_than_f)
        return result

    counter_list.sort(key=make_key)
    return _to_listgen_slice(counter_list, offset, limit)


def order_slice(mclan: 'P(P(M x M) x N)', less_than_f,
        offset: '( A )', limit: '( A )', _checked: bool=True) -> 'P(P(M x M) x N)':
    r"""Return a multiclan that contains the relations with indices ``offset <= index < offset +
    limit``, after having been ordered according to ``order``.

    :param mclan: The source data. Must be a :term:`multiclan`.
    :param less_than_f: A function that accepts two :term:`relation`\s as arguments and returns
        ``True`` if the first one is less than the second one.
    :param offset: An :term:`atom` with an integer value that indicates the index of the first
        relation (after sorting the multiclan) in the result. Set to ``Atom(0)`` if you want to
        start with the first relation of the sorted multiclan.
    :param limit: An atom with an integer value that indicates how many relations should be in
        the resulting multiclan. When ``limit`` is ``float('inf')``, all relations are returned.
    """
    tuple_list_generator = order_slice_to_listgen(mclan, less_than_f, offset, limit, _checked)
    if tuple_list_generator is _undef.Undef():
        return _undef.Undef()
    mclan = _mo.Multiset({rel: mult for (rel, mult) in tuple_list_generator}, direct_load=True)
    return mclan


def from_dict(dict1: dict) -> 'P(P(M x M) x N)':
    r"""Return a :term:`multiclan` with a single :term:`relation` where the :term:`couplet`\s are the
    elements of ``dict1``."""
    rel = _relations.from_dict(dict1)
    mclan = _mo.Multiset(rel, direct_load=True)
    mclan.cache_multiclan(CacheStatus.IS)
    mclan.cache_functional(CacheStatus.IS)
    mclan.cache_regular(CacheStatus.IS)
    return mclan


def diag(*args, _checked=True) -> 'P(P(M x M) x N)':
    """Return a multiclan diagonal of the arguments.

    :param args: Pass in the elements from which the :term:`clan diagonal` is formed. (If you want
        to pass in an iterable, you need to prefix it with an asterisk ``*``.)
    """
    rels = _relations.diag(*args, _checked=_checked)
    if rels is _undef.Undef():
        return _undef.make_or_raise_undef(2)
    clan = _mo.Multiset(rels, direct_load=True)
    clan.cache_multiclan(CacheStatus.IS)
    clan.cache_functional(CacheStatus.IS).cache_right_functional(CacheStatus.IS)
    clan.cache_reflexive(CacheStatus.IS).cache_symmetric(CacheStatus.IS)
    clan.cache_regular(CacheStatus.IS).cache_right_regular(CacheStatus.IS)
    return clan


def defined_at(mclan: 'P(P(M x M) x N)', left: '( M )', _checked=True):
    r"""Return the :term:`relation`\s of ``mclan`` that are defined for ``left``."""
    if not is_member(mclan):
        return _undef.make_or_raise_undef(2)
    if left is _undef.Undef():
        return _undef.make_or_raise_undef(2)
    result = _extension.unary_multi_extend(
        mclan, _functools.partial(_relations.defined_at, left=left, _checked=_checked),
        _checked=_checked)
    if result is _undef.Undef() or not result:
        return _undef.make_or_raise_undef2(result)
    result.cache_multiclan(CacheStatus.IS)
    if not result.is_empty:
        if mclan.cached_is_functional:
            result.cache_functional(CacheStatus.IS)
        if mclan.cached_is_right_functional:
            result.cache_right_functional(CacheStatus.IS)
        if mclan.cached_is_regular:
            result.cache_regular(CacheStatus.IS)
        if mclan.cached_is_right_regular:
            result.cache_right_regular(CacheStatus.IS)
    return result
