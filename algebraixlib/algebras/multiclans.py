r"""This module contains the :term:`algebra of multiclans` and related functionality.

A :term:`multiclan` is also a :term:`multiset` (of :term:`relation`\s), and inherits all operations
of the :term:`algebra of multisets`. These are provided in :mod:`~.algebras.multisets`.
"""

# $Id: multiclans.py 22804 2015-08-14 17:43:32Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-08-14 12:43:32 -0500 (Fri, 14 Aug 2015) $
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
import algebraixlib.undef as _undef


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
                return _undef.make_or_raise_undef()
        else:
            assert is_member(multiclan)
        result = _extension.unary_multi_extend(multiclan, _functools.partial(
            _relations.transpose, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_multiclan(_mo.CacheStatus.IS)
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
                return _undef.make_or_raise_undef()
            if not is_member(multiclan2):
                return _undef.make_or_raise_undef()
        else:
            assert is_member(multiclan1)
            assert is_member(multiclan2)
        result = _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _relations.compose, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_multiclan(_mo.CacheStatus.IS)
            if multiclan1.cached_is_absolute and multiclan2.cached_is_absolute:
                result.cache_absolute(_mo.CacheStatus.IS)
            if multiclan1.cached_is_functional and multiclan2.cached_is_functional:
                result.cache_functional(_mo.CacheStatus.IS)
            if multiclan1.cached_is_right_functional and multiclan2.cached_is_right_functional:
                result.cache_right_functional(_mo.CacheStatus.IS)
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
                return _undef.make_or_raise_undef()
            if not is_member(mclan2):
                return _undef.make_or_raise_undef()
        else:
            assert is_member(mclan1)
            assert is_member(mclan2)
        result = _extension.binary_multi_extend(mclan1, mclan2, _functools.partial(
            _sets.union, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_multiclan(_mo.CacheStatus.IS)
            if mclan1.cached_is_not_functional or mclan2.cached_is_not_functional:
                result.cache_functional(_mo.CacheStatus.IS_NOT)
            if mclan1.cached_is_not_right_functional or mclan2.cached_is_not_right_functional:
                result.cache_right_functional(_mo.CacheStatus.IS_NOT)
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
                return _undef.make_or_raise_undef()
            if not is_member(mclan2):
                return _undef.make_or_raise_undef()
        else:
            assert is_member(mclan1)
            assert is_member(mclan2)
        result = _extension.binary_multi_extend(mclan1, mclan2, _functools.partial(
            _relations.functional_union, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_multiclan(_mo.CacheStatus.IS)
            result.cache_functional(_mo.CacheStatus.IS)
            if mclan1.cached_is_not_right_functional or mclan2.cached_is_not_right_functional:
                result.cache_right_functional(_mo.CacheStatus.IS_NOT)
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
                return _undef.make_or_raise_undef()
            if not is_member(multiclan2):
                return _undef.make_or_raise_undef()
        else:
            assert is_member(multiclan1)
            assert is_member(multiclan2)
        result = _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _relations.right_functional_union, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_multiclan(_mo.CacheStatus.IS)
            result.cache_right_functional(_mo.CacheStatus.IS)
            if multiclan1.cached_is_not_functional or multiclan2.cached_is_not_functional:
                result.cache_functional(_mo.CacheStatus.IS_NOT)
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
                return _undef.make_or_raise_undef()
            if not is_member(multiclan2):
                return _undef.make_or_raise_undef()
        else:
            assert is_member(multiclan1)
            assert is_member(multiclan2)
        result = _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _sets.intersect, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_multiclan(_mo.CacheStatus.IS)
            if multiclan1.cached_is_functional or multiclan2.cached_is_functional:
                result.cache_functional(_mo.CacheStatus.IS)
            if multiclan1.cached_is_right_functional or multiclan2.cached_is_right_functional:
                result.cache_right_functional(_mo.CacheStatus.IS)
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
                return _undef.make_or_raise_undef()
            if not is_member(multiclan2):
                return _undef.make_or_raise_undef()
        else:
            assert is_member(multiclan1)
            assert is_member(multiclan2)
        result = _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _sets.substrict, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_multiclan(_mo.CacheStatus.IS)
            if multiclan1.cached_is_functional or multiclan2.cached_is_functional:
                result.cache_functional(_mo.CacheStatus.IS)
            if multiclan1.cached_is_right_functional or multiclan2.cached_is_right_functional:
                result.cache_right_functional(_mo.CacheStatus.IS)
            if multiclan1.cached_is_reflexive:
                result.cache_reflexive(_mo.CacheStatus.IS)
            if multiclan1.cached_is_symmetric:
                result.cache_symmetric(_mo.CacheStatus.IS)
            if multiclan1.cached_is_transitive:
                result.cache_transitive(_mo.CacheStatus.IS)
            if multiclan1.cached_is_regular:
                result.cache_regular(_mo.CacheStatus.IS)
            if multiclan1.cached_is_right_regular:
                result.cache_right_regular(_mo.CacheStatus.IS)
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
                return _undef.make_or_raise_undef()
            if not is_member(multiclan2):
                return _undef.make_or_raise_undef()
        else:
            assert is_member(multiclan1)
            assert is_member(multiclan2)
        result = _extension.binary_multi_extend(multiclan1, multiclan2, _functools.partial(
            _sets.superstrict, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_multiclan(_mo.CacheStatus.IS)
            if multiclan1.cached_is_functional:
                result.cache_functional(_mo.CacheStatus.IS)
            if multiclan1.cached_is_right_functional:
                result.cache_right_functional(_mo.CacheStatus.IS)
            if multiclan1.cached_is_reflexive:
                result.cache_reflexive(_mo.CacheStatus.IS)
            if multiclan1.cached_is_symmetric:
                result.cache_symmetric(_mo.CacheStatus.IS)
            if multiclan1.cached_is_transitive:
                result.cache_transitive(_mo.CacheStatus.IS)
            if multiclan1.cached_is_regular:
                result.cache_regular(_mo.CacheStatus.IS)
            if multiclan1.cached_is_right_regular:
                result.cache_right_regular(_mo.CacheStatus.IS)
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
    if obj.cached_multiclan == _mo.CacheStatus.UNKNOWN:
        is_multiclan = obj.get_ground_set().is_subset(get_ground_set())
        obj.cache_multiclan(_mo.CacheStatus.from_bool(is_multiclan))
    return obj.cached_is_multiclan


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
    if obj.cached_absolute == _mo.CacheStatus.UNKNOWN \
            or obj.cached_multiclan == _mo.CacheStatus.UNKNOWN:
        # The 'absolute' state has not yet been cached. Determine whether obj is an absolute
        # multiclan.
        is_absolute_mclan = obj.get_ground_set().is_subset(get_absolute_ground_set())
        if obj.cached_multiclan == _mo.CacheStatus.UNKNOWN:
            if is_absolute_mclan:
                # If it is an absolute multiclan, it is also a multiclan.
                obj.cache_multiclan(_mo.CacheStatus.IS)
            else:
                # If it is not an absolute multiclan, it may still be a multiclan.
                is_mclan = is_member(obj)
                if not is_mclan:
                    # If it is neither an absolute multiclan nor a multiclan, exit. (That it is
                    # not a multiclan has already been cached in is_member().)
                    return False
        # At this point, cached_multiclan == IS. Cache whether this is an absolute multiclan.
        assert obj.cached_is_multiclan
        obj.cache_absolute(_mo.CacheStatus.from_bool(is_absolute_mclan))
    # At this point, cached_multiclan == IS. Return whether it is an absolute multiclan.
    return obj.cached_is_absolute


# --------------------------------------------------------------------------------------------------
# Related operations, not formally part of the algebra.

def get_lefts(mclan: 'PP(M x M)', _checked=True) -> 'P( M )':
    r"""Return the set of the left components of all couplets in all relations in ``mclan``.

    :return: The :term:`union` of the :term:`left set`\s of all :term:`relation`\s in ``mclan`` or
        `Undef()` if ``mclan`` is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef()
    else:
        assert is_member(mclan)
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
            left_set.cache_absolute(_mo.CacheStatus.IS)
    return left_set


def is_functional(mclan, _checked=True) -> bool:
    """Return whether ``mclan`` is functional.

    :return: ``True`` if every :term:`relation` in ``mclan`` is :term:`functional` (is a
        :term:`function`), ``False`` if not, or `Undef()` if ``mclan`` is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef()
    else:
        assert is_member(mclan)

    if mclan.cached_functional == _mo.CacheStatus.UNKNOWN:
        # The empty set is already handled in Set().__init__ via flags initialization.
        functional = all(_relations.is_functional(rel, _checked=False) for rel in mclan.data)
        mclan.cache_functional(_mo.CacheStatus.from_bool(functional))
    return mclan.cached_is_functional


def is_right_functional(mclan, _checked=True) -> bool:
    """Return whether ``mclan`` is right-functional.

    :return: ``True`` if every :term:`relation` in ``mclan`` is :term:`right-functional`, ``False``
        if not, or `Undef()` if ``mclan`` is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef()
    else:
        assert is_member(mclan)

    if mclan.cached_right_functional == _mo.CacheStatus.UNKNOWN:
        # The empty set is already handled in Set().__init__ via flags initialization.
        right_functional = all(
            _relations.is_right_functional(rel, _checked=False) for rel in mclan.data)
        mclan.cache_right_functional(_mo.CacheStatus.from_bool(right_functional))
    return mclan.cached_is_right_functional


def is_regular(mclan, _checked=True) -> bool:
    """Return whether ``mclan`` is (left-)regular.

    :return: ``True`` if ``mclan`` is :term:`regular`, ``False`` if not, or `Undef()` if ``mclan``
        is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef()
    else:
        assert is_member(mclan)

    if mclan.cached_regular == _mo.CacheStatus.UNKNOWN:
        # The empty set is already handled in Set().__init__ via flags initialization.
        if mclan.cached_is_not_functional:
            mclan.cache_regular(_mo.CacheStatus.IS_NOT)
            return False
        itr = iter(mclan.data)
        rel = next(itr)
        if not _relations.is_functional(rel):
            mclan.cache_regular(_mo.CacheStatus.IS_NOT)
            return False
        left_set = rel.get_left_set()
        regular = all(
            _relations.is_functional(rel) and left_set == rel.get_left_set() for rel in itr)
        mclan.cache_regular(_mo.CacheStatus.from_bool(regular))
    return mclan.cached_is_regular


def is_right_regular(mclan, _checked=True) -> bool:
    """Return whether ``mclan`` is right-regular.

    :return: ``True`` if ``mclan`` is :term:`right-regular`, ``False`` if not, or `Undef()` if
        ``mclan`` is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef()
    else:
        assert is_member(mclan)

    if mclan.cached_right_regular == _mo.CacheStatus.UNKNOWN:
        # The empty set is already handled in Set().__init__ via flags initialization.
        if mclan.cached_is_not_right_functional:
            mclan.cache_right_regular(_mo.CacheStatus.IS_NOT)
            return False
        itr = iter(mclan.data)
        rel = next(itr)
        if not _relations.is_right_functional(rel):
            mclan.cache_right_regular(_mo.CacheStatus.IS_NOT)
            return False
        right_set = rel.get_right_set()
        right_regular = all(
            _relations.is_right_functional(rel) and right_set == rel.get_right_set() for rel in itr)
        mclan.cache_regular(_mo.CacheStatus.from_bool(right_regular))
    return mclan.cached_is_regular


def is_reflexive(mclan, _checked=True) -> bool:
    """Return whether ``mclan`` is reflexive.

    :return: ``True`` if ``mclan`` is :term:`reflexive`, ``False`` if it is not, or `Undef()` if
        ``mclan`` is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef()
    else:
        assert is_member(mclan)
    if mclan.cached_reflexive == _mo.CacheStatus.UNKNOWN:
        reflexive = all(_relations.is_reflexive(rel, _checked=False) for rel in mclan.data)
        mclan.cache_reflexive(_mo.CacheStatus.from_bool(reflexive))
    return mclan.cached_reflexive == _mo.CacheStatus.IS


def is_symmetric(mclan, _checked=True) -> bool:
    """Return whether ``mclan`` is symmetric.

    :return: ``True`` if ``mclan`` is :term:`symmetric`, ``False`` if it is not, or `Undef()` if
        ``mclan`` is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef()
    else:
        assert is_member(mclan)
    if mclan.cached_symmetric == _mo.CacheStatus.UNKNOWN:
        symmetric = all(_relations.is_symmetric(rel, _checked=False) for rel in mclan.data)
        mclan.cache_symmetric(_mo.CacheStatus.from_bool(symmetric))
    return mclan.cached_symmetric == _mo.CacheStatus.IS


def is_transitive(mclan, _checked=True) -> bool:
    """Return whether ``mclan`` is transitive.

    :return: ``True`` if ``mclan`` is :term:`transitive`, ``False`` if it is not, or `Undef()` if
        ``mclan`` is not a :term:`multiclan`.
    """
    if _checked:
        if not is_member(mclan):
            return _undef.make_or_raise_undef()
    else:
        assert is_member(mclan)
    if mclan.cached_transitive == _mo.CacheStatus.UNKNOWN:
        transitive = all(_relations.is_transitive(rel, _checked=False) for rel in mclan.data)
        mclan.cache_transitive(_mo.CacheStatus.from_bool(transitive))
    return mclan.cached_transitive == _mo.CacheStatus.IS
