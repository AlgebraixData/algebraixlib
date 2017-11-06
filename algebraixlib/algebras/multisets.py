"""This module contains the :term:`algebra of multisets` and related functionality."""

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

import algebraixlib.algebras.sets as _sets
import algebraixlib.mathobjects as _mo
import algebraixlib.structure as _structure
import algebraixlib.undef as _undef

from ..cache_status import CacheStatus


# --------------------------------------------------------------------------------------------------

class Algebra:
    """Provide the operations and relations that are members of the :term:`algebra of multisets`.

    This class contains only static member functions. Its main purpose is to provide a namespace for
    and highlight the operations and relations that belong to the algebra of multisets. All member
    functions are also available at the enclosing module scope.
    """
    # ----------------------------------------------------------------------------------------------
    # Binary algebra operations.

    @staticmethod
    def union(multiset1: 'P( M x N )', multiset2: 'P( M x N )', _checked=True) -> 'P( M x N )':
        """Return the multiset union of ``multiset1`` with ``multiset2``.

        :return: The :term:`multiset union` of ``multiset1`` and ``multiset2`` or `Undef()` if
            ``multiset1`` or ``multiset2`` are not instances of :class:`~.Multiset`.
        """
        # pylint: disable=too-many-branches
        if _checked:
            if not is_member(multiset1):
                return _undef.make_or_raise_undef2(multiset1)
            if not is_member(multiset2):
                return _undef.make_or_raise_undef2(multiset2)
        else:
            assert is_member_or_undef(multiset1)
            assert is_member_or_undef(multiset2)
            if multiset1 is _undef.Undef() or multiset2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        values = multiset1.data | multiset2.data
        result = _mo.Multiset(values, direct_load=True)
        if not result.is_empty:
            # Multiclan flags:
            if multiset1.cached_is_multiclan and multiset2.cached_is_multiclan:
                result.cache_multiclan(CacheStatus.IS)
                if multiset1.cached_is_absolute and multiset2.cached_is_absolute:
                    result.cache_absolute(CacheStatus.IS)
                elif multiset1.cached_is_not_absolute or multiset2.cached_is_not_absolute:
                    result.cache_absolute(CacheStatus.IS_NOT)
                if multiset1.cached_is_functional and multiset2.cached_is_functional:
                    result.cache_functional(CacheStatus.IS)
                elif multiset1.cached_is_not_functional or multiset2.cached_is_not_functional:
                    result.cache_functional(CacheStatus.IS_NOT)
                if multiset1.cached_is_right_functional and multiset2.cached_is_right_functional:
                    result.cache_right_functional(CacheStatus.IS)
                elif multiset1.cached_is_not_right_functional \
                        or multiset2.cached_is_not_right_functional:
                    result.cache_right_functional(CacheStatus.IS_NOT)
                if multiset1.cached_is_not_regular or multiset1.cached_is_not_regular:
                    result.cache_regular(CacheStatus.IS_NOT)
                if multiset1.cached_is_not_right_regular or multiset1.cached_is_not_right_regular:
                    result.cache_right_regular(CacheStatus.IS_NOT)
            elif multiset1.cached_is_not_multiclan or multiset2.cached_is_not_multiclan:
                result.cache_multiclan(CacheStatus.IS_NOT)
        return result

    @staticmethod
    def intersect(multiset1: 'P( M x N )', multiset2: 'P( M x N )', _checked=True) -> 'P( M x N )':
        """Return the multiset intersection of ``multiset1`` with ``multiset2``.

        :return: The :term:`multiset intersection` of ``multiset1`` and ``multiset2`` or `Undef()`
            if ``multiset1`` or ``multiset2`` are not instances of :class:`~.Multiset`.
        """
        if _checked:
            if not is_member(multiset1):
                return _undef.make_or_raise_undef2(multiset1)
            if not is_member(multiset2):
                return _undef.make_or_raise_undef2(multiset2)
        else:
            assert is_member_or_undef(multiset1)
            assert is_member_or_undef(multiset2)
            if multiset1 is _undef.Undef() or multiset2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        values = multiset1.data & multiset2.data
        result = _mo.Multiset(values)
        if not result.is_empty:
            # Multiclan flags:
            if multiset1.cached_is_multiclan or multiset2.cached_is_multiclan:
                result.cache_multiclan(CacheStatus.IS)
                if multiset1.cached_is_absolute or multiset2.cached_is_absolute:
                    result.cache_absolute(CacheStatus.IS)
                if multiset1.cached_is_functional or multiset2.cached_is_functional:
                    result.cache_functional(CacheStatus.IS)
                if multiset1.cached_is_right_functional or multiset2.cached_is_right_functional:
                    result.cache_right_functional(CacheStatus.IS)
                if multiset1.cached_is_regular or multiset2.cached_is_regular:
                    result.cache_regular(CacheStatus.IS)
                if multiset1.cached_is_right_regular or multiset2.cached_is_right_regular:
                    result.cache_right_regular(CacheStatus.IS)
        return result

    @staticmethod
    def minus(multiset1: 'P( M x N )', multiset2: 'P( M x N )', _checked=True) -> 'P( M x N )':
        """Return the multiset difference of ``multiset1`` and ``multiset2``.

        :return: The :term:`multiset difference` of ``multiset1`` and ``multiset2`` or `Undef()`
            if ``multiset1`` or ``multiset2`` are not instances of :class:`~.Multiset`.
        """
        if _checked:
            if not is_member(multiset1):
                return _undef.make_or_raise_undef2(multiset1)
            if not is_member(multiset2):
                return _undef.make_or_raise_undef2(multiset2)
        else:
            assert is_member_or_undef(multiset1)
            assert is_member_or_undef(multiset2)
            if multiset1 is _undef.Undef() or multiset2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        values = multiset1.data - multiset2.data
        result = _mo.Multiset(values)
        if not result.is_empty:
            # Multiclan flags:
            if multiset1.cached_is_multiclan:
                result.cache_multiclan(CacheStatus.IS)
                if multiset1.cached_is_absolute:
                    result.cache_absolute(CacheStatus.IS)
                if multiset1.cached_is_functional:
                    result.cache_functional(CacheStatus.IS)
                if multiset1.cached_is_right_functional:
                    result.cache_right_functional(CacheStatus.IS)
                if multiset1.cached_is_regular:
                    result.cache_regular(CacheStatus.IS)
                if multiset1.cached_is_right_regular:
                    result.cache_right_regular(CacheStatus.IS)
        return result

    @staticmethod
    def add(multiset1: 'P( M x N )', multiset2: 'P( M x N )', _checked=True) -> 'P( M x N )':
        """Return the multiset addition of ``multiset1`` and ``multiset2``.

        :return: The :term:`multiset addition` of ``multiset1`` and ``multiset2`` or `Undef()` if
            ``multiset1`` or ``multiset2`` are not instances of :class:`~.Multiset`.
        """
        # pylint: disable=too-many-branches
        if _checked:
            if not is_member(multiset1):
                return _undef.make_or_raise_undef2(multiset1)
            if not is_member(multiset2):
                return _undef.make_or_raise_undef2(multiset2)
        else:
            assert is_member_or_undef(multiset1)
            assert is_member_or_undef(multiset2)
            if multiset1 is _undef.Undef() or multiset2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        values = multiset1.data + multiset2.data
        result = _mo.Multiset(values, direct_load=True)
        if not result.is_empty:
            # Multiclan flags:
            if multiset1.cached_is_multiclan and multiset2.cached_is_multiclan:
                result.cache_multiclan(CacheStatus.IS)
                if multiset1.cached_is_absolute and multiset2.cached_is_absolute:
                    result.cache_absolute(CacheStatus.IS)
                elif multiset1.cached_is_not_absolute or multiset2.cached_is_not_absolute:
                    result.cache_absolute(CacheStatus.IS_NOT)
                if multiset1.cached_is_functional and multiset2.cached_is_functional:
                    result.cache_functional(CacheStatus.IS)
                elif multiset1.cached_is_not_functional or multiset2.cached_is_not_functional:
                    result.cache_functional(CacheStatus.IS_NOT)
                if multiset1.cached_is_right_functional and multiset2.cached_is_right_functional:
                    result.cache_right_functional(CacheStatus.IS)
                elif multiset1.cached_is_not_right_functional \
                        or multiset2.cached_is_not_right_functional:
                    result.cache_right_functional(CacheStatus.IS_NOT)
                if multiset1.cached_is_not_regular or multiset1.cached_is_not_regular:
                    result.cache_regular(CacheStatus.IS_NOT)
                if multiset1.cached_is_not_right_regular or multiset1.cached_is_not_right_regular:
                    result.cache_right_regular(CacheStatus.IS_NOT)
            elif multiset1.cached_is_not_multiclan or multiset2.cached_is_not_multiclan:
                result.cache_multiclan(CacheStatus.IS_NOT)
        return result

    @staticmethod
    def substrict(multiset1: 'P( M x N )', multiset2: 'P( M x N )', _checked=True) -> 'P( M x N )':
        """Return ``multiset1`` if ``multiset1`` is a subset of ``multiset2`` or `Undef()` if not.

        :return: The :term:`substriction` of ``multiset1`` and ``multiset2`` (may return `Undef()`).
            Also return `Undef()` if ``multiset1`` or ``multiset2`` are not instances of
            :class:`~.Multiset`.
        """
        if _checked:
            if not is_member(multiset1):
                return _undef.make_or_raise_undef2(multiset1)
            if not is_member(multiset2):
                return _undef.make_or_raise_undef2(multiset2)
        else:
            assert is_member_or_undef(multiset1)
            assert is_member_or_undef(multiset2)
            if multiset1 is _undef.Undef() or multiset2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        if not is_subset_of(multiset1, multiset2, _checked=False):
            return _undef.make_or_raise_undef(2)
        if not multiset1.is_empty:
            # Multiclan flags:
            if multiset1.cached_is_multiclan:
                if multiset2.cached_is_absolute:
                    multiset1.cache_absolute(CacheStatus.IS)
                if multiset2.cached_is_functional:
                    multiset1.cache_functional(CacheStatus.IS)
                if multiset2.cached_is_right_functional:
                    multiset1.cache_right_functional(CacheStatus.IS)
                if multiset2.cached_is_regular:
                    multiset1.cache_regular(CacheStatus.IS)
                if multiset2.cached_is_right_regular:
                    multiset1.cache_right_regular(CacheStatus.IS)
        return multiset1

    @staticmethod
    def superstrict(multiset1: 'P( M x N )', multiset2: 'P( M X N )',
                    _checked=True) -> 'P( M X N )':
        """Return ``multiset1`` if ``multiset1`` is a superset of ``multiset2`` or `Undef()` if not.

        :return: The :term:`superstriction` of ``multiset1`` and ``multiset2`` (may return
            `Undef()`). Also return `Undef()` if ``multiset1`` or ``multiset2`` are not instances
            of :class:`~.Multiset`.
        """
        if _checked:
            if not is_member(multiset1):
                return _undef.make_or_raise_undef2(multiset1)
            if not is_member(multiset2):
                return _undef.make_or_raise_undef2(multiset2)
        else:
            assert is_member_or_undef(multiset1)
            assert is_member_or_undef(multiset2)
            if multiset1 is _undef.Undef() or multiset2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        if not is_superset_of(multiset1, multiset2, _checked=False):
            return _undef.make_or_raise_undef(2)
        if not multiset1.is_empty:
            # Multiclan flags:
            if multiset1.cached_is_clan:
                if multiset2.cached_is_not_absolute:
                    multiset1.cache_absolute(CacheStatus.IS_NOT)
                if multiset2.cached_is_not_functional:
                    multiset1.cache_functional(CacheStatus.IS_NOT)
                if multiset2.cached_is_not_right_functional:
                    multiset1.cache_right_functional(CacheStatus.IS_NOT)
                if multiset2.cached_is_not_regular:
                    multiset1.cache_regular(CacheStatus.IS_NOT)
                if multiset2.cached_is_not_right_regular:
                    multiset1.cache_right_regular(CacheStatus.IS_NOT)
        return multiset1

    # ----------------------------------------------------------------------------------------------
    # Algebra relations.

    @staticmethod
    def is_subset_of(multiset1: 'P( M x N )', multiset2: 'P( M x N )', _checked=True) -> bool:
        """Return whether ``multiset1`` is a submultiset of ``multiset2``.

        :return: ``True`` if ``multiset1`` is a :term:`submultiset` of ``multiset2``, ``False`` if
            not. Return `Undef()` if ``multiset1`` or ``multiset2`` are not instances of
            :class:`~.Multiset`.
        """
        if _checked:
            if not is_member(multiset1):
                return _undef.make_or_raise_undef2(multiset1)
            if not is_member(multiset2):
                return _undef.make_or_raise_undef2(multiset2)
        else:
            assert is_member_or_undef(multiset1)
            assert is_member_or_undef(multiset2)
            if multiset1 is _undef.Undef() or multiset2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        for key in multiset1.data.keys():
            if not multiset1.data[key] <= multiset2.data[key]:
                return False
        return True

    @staticmethod
    def is_superset_of(multiset1: 'P( M x N )', multiset2: 'P( M x N )', _checked=True) -> bool:
        """Return whether ``multiset1`` is a supermultiset of ``multiset2``.

        :return: ``True`` if ``multiset1`` is a :term:`supermultiset` of ``multiset2``, ``False``
            if not. Return `Undef()` if ``multiset1`` or ``multiset2`` are not instances of
            :class:`~.Multiset`.
        """
        if _checked:
            if not is_member(multiset1):
                return _undef.make_or_raise_undef2(multiset1)
            if not is_member(multiset2):
                return _undef.make_or_raise_undef2(multiset2)
        else:
            assert is_member_or_undef(multiset1)
            assert is_member_or_undef(multiset2)
            if multiset1 is _undef.Undef() or multiset2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        for key in multiset2.data.keys():
            if not multiset1.data[key] >= multiset2.data[key]:
                return False
        return True


# For convenience, make the members of class Algebra (they are all static functions) available at
# the module level.

# pylint: disable=invalid-name

#: Convenience redirection to `Algebra.union`.
union = Algebra.union
#: Convenience redirection to `Algebra.intersect`.
intersect = Algebra.intersect
#: Convenience redirection to `Algebra.minus`.
minus = Algebra.minus
#: Convenience redirection to `Algebra.add`.
add = Algebra.add
#: Convenience redirection to `Algebra.substrict`.
substrict = Algebra.substrict
#: Convenience redirection to `Algebra.superstrict`.
superstrict = Algebra.superstrict
#: Convenience redirection to `Algebra.is_subset_of`.
is_subset_of = Algebra.is_subset_of
#: Convenience redirection to `Algebra.is_superset_of`.
is_superset_of = Algebra.is_superset_of

# pylint: enable=invalid-name


# --------------------------------------------------------------------------------------------------
# Metadata functions.
def get_name() -> str:
    """Return the name and :term:`ground set` of this :term:`algebra` in string form."""
    return 'Multisets(M): {ground_set}'.format(ground_set=str(get_ground_set()))


def get_ground_set() -> _structure.Structure:
    """Return the :term:`ground set` of this :term:`algebra`."""
    return _structure.PowerSet(_structure.CartesianProduct(_structure.GenesisSetM(),
                                                           _structure.GenesisSetN()))


def get_absolute_ground_set() -> _structure.Structure:
    """Return the :term:`absolute ground set` of this :term:`algebra`."""
    return _structure.PowerSet(_structure.CartesianProduct(_structure.GenesisSetA(),
                                                           _structure.GenesisSetN()))


def is_member(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is a member of the :term:`ground set` of this :term:`algebra`.

     :return: ``True`` if ``obj`` is a :term:`multiset` (an instance of :class:`~.Multiset`),
        ``False`` if not.
     """
    return obj.is_multiset


def is_member_or_undef(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is either a member of the :term:`ground set` of this :term:`algebra`
        or :class:`~.Undef`.

     :return: ``True`` if ``obj`` is either a :term:`relation` or :class:`~.Undef`,
        ``False`` if not.
    """
    return obj is _undef.Undef() or is_member(obj)


def is_absolute_member(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is a member of the :term:`absolute ground set` of this algebra.

    :type obj: _mo.MathObject|_mo.Multiset
    :return: ``True`` if ``obj`` is an :term:`absolute multiset`, ``False`` if not.
    """
    import algebraixlib.algebras.multiclans as _multiclans

    if not obj.is_multiset:
        # If known to not be a multiset, it's also not an absolute multiset. No further checking or
        # caching.
        return False
    # From this point on, `obj` is known to be a multiset.
    if obj.cached_absolute == CacheStatus.UNKNOWN:
        # In order to find out whether this is an absolute multiset, we need to know whether `obj`
        # is a multiclan (also a multiset). If it is one, it is not an absolute multiset -- but
        # we also don't know whether it is an absolute multiclan. So we return `False` but don't
        # cache anything. (But we have now cached that it is a multiclan.)
        if _multiclans.is_member(obj):
            return False
        is_absolute_multiset = all(elem.is_atom for elem in obj.data)
        obj.cache_absolute(CacheStatus.from_bool(is_absolute_multiset))
    # In order to determine whether this is an absolute multiset, we need to also examine whether
    # this is a multiclan (also a multisets). Absolute multiclans are not absolute multisets.
    return obj.cached_is_absolute and not obj.cached_is_multiclan


# --------------------------------------------------------------------------------------------------
# Related operations, not formally part of the algebra.

def demultify(multiset: 'P( M x N )', _checked=True) -> 'P( M )':
    """Return a :term:`set` based on ``multiset`` that contains all elements without multiples."""
    if _checked:
        if not is_member(multiset):
            return _undef.make_or_raise_undef2(multiset)
    else:
        assert is_member_or_undef(multiset)
        if multiset is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    result = _mo.Set(multiset.data.keys(), direct_load=True)
    if not result.is_empty:
        result.cache_clan(multiset.cached_multiclan)
        if multiset.cached_is_multiclan:
            result.cache_absolute(multiset.cached_absolute)
            result.cache_functional(multiset.cached_functional)
            result.cache_right_functional(multiset.cached_right_functional)
            result.cache_reflexive(multiset.cached_reflexive)
            result.cache_symmetric(multiset.cached_symmetric)
            result.cache_transitive(multiset.cached_transitive)
            result.cache_regular(multiset.cached_regular)
            result.cache_right_regular(multiset.cached_right_regular)
        # We don't yet have a concept of multirelations (multisets of couplets). Because of this,
        # a multiset that is converted into a set may be a relation without us being able to know
        # this here. Because of this, the only flags we can propagate are multiclan flags.
    return result


def big_union(set_of_multisets: 'PP( M x N )', _checked=True) -> 'P( M x N )':
    """Return the set_of_multisets union of all members of ``set_of_multisets``.

    :return: The :term:`multiset union` of all members of ``set_of_multisets`` or `Undef()` if
        ``set_of_multisets`` is not a :class:`~.Set` or any of its members are not instances of
        :class:`~.Multiset`.
    """
    if _checked:
        if not isinstance(set_of_multisets, _mo.Set):
            return _undef.make_or_raise_undef2(set_of_multisets)
        for element in set_of_multisets:
            if not is_member(element):
                return _undef.make_or_raise_undef2(element)
    else:
        assert _sets.is_member_or_undef(set_of_multisets)
        if set_of_multisets is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    return _sets.chain_binary_operation(
        set_of_multisets, _functools.partial(union, _checked=False), is_member)


def big_intersect(set_of_multisets: 'PP( M x N )', _checked=True) -> 'P( M x N )':
    """Return the multiset intersection of all members of ``multiset``.

    :return: The :term:`multiset intersection` of all members of ``set_of_multisets`` or `Undef()`
        if ``set_of_multisets`` is not a :class:`~.Set` or any of its members are not instances of
        :class:`~.Multiset`.
    """
    if _checked:
        if not isinstance(set_of_multisets, _mo.Set):
            return _undef.make_or_raise_undef2(set_of_multisets)
        for element in set_of_multisets:
            if not is_member(element):
                return _undef.make_or_raise_undef2(element)
    else:
        assert _sets.is_member_or_undef(set_of_multisets)
        if set_of_multisets is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    return _sets.chain_binary_operation(
        set_of_multisets, _functools.partial(intersect, _checked=False), is_member)


def single(mset: _mo.Multiset):
    """Return the single element of ``mset``.

    :return: Return the single element of ``mset``, or `Undef()` if ``mset`` has not exactly one
        element with a multiplicity of 1 or is not a :term:`multiset` (that is, an instance of
        :class:`~.Multiset`).
    """
    if not is_member(mset):
        return _undef.make_or_raise_undef2(mset)
    if mset.cardinality == 1:
        single_elem = next(iter(mset.data))
        if mset.data[single_elem] == 1:
            return single_elem
    return _undef.make_or_raise_undef(2)


def some(mset: _mo.Multiset):
    """Return 'some' element of ``mset``. Use with caution - may be non-deterministic.

    :return: Some element of ``mset``, or `Undef()` if ``mset`` is empty or is not a
        :term:`multiset` (that is, an instance of :class:`~.Multiset`).

    .. note:: This function should only be used in contexts where the way the return value will be
        utilized by the calling function is invariant of the particular element returned; the
        element of ``mset`` that is returned is non-deterministic.

        This function is only intended to be used in (mostly implementation) scenarios where it
        does not matter which element of ``mset`` is retrieved, because the expressions that
        consume that value will be invariant with respect to the exact element of ``mset`` that is
        returned.
    """
    if not is_member(mset):
        return _undef.make_or_raise_undef(2)
    if mset.cardinality == 0:
        return _undef.make_or_raise_undef(2)
    return next(iter(mset))
