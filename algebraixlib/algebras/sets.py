"""This module contains the :term:`algebra of sets` and related functionality."""

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
import collections as _collections
import functools as _functools

import algebraixlib.mathobjects as _mo
import algebraixlib.structure as _structure
import algebraixlib.undef as _undef

from ..cache_status import CacheStatus


# --------------------------------------------------------------------------------------------------

class Algebra:
    """Provide the operations and relations that are members of the :term:`algebra of sets`.

    This class contains only static member functions. Its main purpose is to provide a namespace for
    and highlight the operations and relations that belong to the algebra of sets. All member
    functions are also available at the enclosing module level.
    """
    # ----------------------------------------------------------------------------------------------
    # Binary algebra operations.

    @staticmethod
    def union(set1: 'P( M )', set2: 'P( M )', _checked=True) -> 'P( M )':
        r"""Return the union of ``set1`` with ``set2``.

        :return: The :term:`binary union` of ``set1`` and ``set2`` or `Undef()` if ``set1`` or
            ``set2`` are not :term:`set`\s (that is, instances of :class:`~.Set`).
        """
        # pylint: disable=too-many-branches
        if _checked:
            if not is_member(set1):
                return _undef.make_or_raise_undef2(set1)
            if not is_member(set2):
                return _undef.make_or_raise_undef2(set2)
        else:
            assert is_member_or_undef(set1)
            assert is_member_or_undef(set2)
            if set1 is _undef.Undef() or set2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        values = set1.data.union(set2.data)
        result = _mo.Set(values, direct_load=True)
        if not result.is_empty:
            # Relation flags:
            if set1.cached_is_relation and set2.cached_is_relation:
                result.cache_relation(CacheStatus.IS)
                if set1.cached_is_absolute and set2.cached_is_absolute:
                    result.cache_absolute(CacheStatus.IS)
                elif set1.cached_is_not_absolute or set2.cached_is_not_absolute:
                    result.cache_absolute(CacheStatus.IS_NOT)
                if set1.cached_is_not_functional or set2.cached_is_not_functional:
                    result.cache_functional(CacheStatus.IS_NOT)
                if set1.cached_is_not_right_functional or set2.cached_is_not_right_functional:
                    result.cache_right_functional(CacheStatus.IS_NOT)
            elif set1.cached_is_not_relation or set2.cached_is_not_relation:
                result.cache_relation(CacheStatus.IS_NOT)
            # Clan flags:
            if set1.cached_is_clan and set2.cached_is_clan:
                result.cache_clan(CacheStatus.IS)
                if set1.cached_is_absolute and set2.cached_is_absolute:
                    result.cache_absolute(CacheStatus.IS)
                elif set1.cached_is_not_absolute or set2.cached_is_not_absolute:
                    result.cache_absolute(CacheStatus.IS_NOT)
                if set1.cached_is_functional and set2.cached_is_functional:
                    result.cache_functional(CacheStatus.IS)
                elif set1.cached_is_not_functional or set2.cached_is_not_functional:
                    result.cache_functional(CacheStatus.IS_NOT)
                if set1.cached_is_right_functional and set2.cached_is_right_functional:
                    result.cache_right_functional(CacheStatus.IS)
                elif set1.cached_is_not_right_functional or set2.cached_is_not_right_functional:
                    result.cache_right_functional(CacheStatus.IS_NOT)
                if set1.cached_is_not_regular or set2.cached_is_not_regular:
                    result.cache_regular(CacheStatus.IS_NOT)
                if set1.cached_is_not_right_regular or set2.cached_is_not_right_regular:
                    result.cache_right_regular(CacheStatus.IS_NOT)
            elif set1.cached_is_not_clan or set2.cached_is_not_clan:
                result.cache_clan(CacheStatus.IS_NOT)

            # Neither are clan and neither are rel
            if set1.cached_is_not_clan and set2.cached_is_not_clan\
                    and set1.cached_is_not_relation and set2.cached_is_not_relation:
                if set1.cached_is_absolute and set2.cached_is_absolute:
                    result.cache_absolute(CacheStatus.IS)
                elif set1.cached_is_not_absolute or set2.cached_is_not_absolute:
                    result.cache_absolute(CacheStatus.IS_NOT)

        return result

    @staticmethod
    def intersect(set1: 'P( M )', set2: 'P( M )', _checked=True) -> 'P( M )':
        r"""Return the intersection of ``set1`` with ``set2``.

        :return: The :term:`binary intersection` of ``set1`` and ``set2`` or `Undef()` if ``set1``
            or ``set2`` are not :term:`set`\s (that is, instances of :class:`~.Set`).
        """
        # pylint: disable=too-many-branches
        if _checked:
            if not is_member(set1):
                return _undef.make_or_raise_undef2(set1)
            if not is_member(set2):
                return _undef.make_or_raise_undef2(set2)
        else:
            assert is_member_or_undef(set1)
            assert is_member_or_undef(set2)
            if set1 is _undef.Undef() or set2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        values = set1.data.intersection(set2.data)
        result = _mo.Set(values, direct_load=True)
        if not result.is_empty:
            # Relation flags:
            if set1.cached_is_relation or set2.cached_is_relation:
                result.cache_relation(CacheStatus.IS)
                if set1.cached_is_absolute or set2.cached_is_absolute:
                    result.cache_absolute(CacheStatus.IS)
                if set1.cached_is_functional or set2.cached_is_functional:
                    result.cache_functional(CacheStatus.IS)
                if set1.cached_is_right_functional or set2.cached_is_right_functional:
                    result.cache_right_functional(CacheStatus.IS)
            # Clan flags:
            if set1.cached_is_clan or set2.cached_is_clan:
                result.cache_clan(CacheStatus.IS)
                if set1.cached_is_absolute or set2.cached_is_absolute:
                    result.cache_absolute(CacheStatus.IS)
                if set1.cached_is_functional or set2.cached_is_functional:
                    result.cache_functional(CacheStatus.IS)
                if set1.cached_is_right_functional or set2.cached_is_right_functional:
                    result.cache_right_functional(CacheStatus.IS)
                if set1.cached_is_regular or set2.cached_is_regular:
                    result.cache_regular(CacheStatus.IS)
                if set1.cached_is_right_regular or set2.cached_is_right_regular:
                    result.cache_right_regular(CacheStatus.IS)
        return result

    @staticmethod
    def minus(set1: 'P( M )', set2: 'P( M )', _checked=True) -> 'P( M )':
        r"""Return the set difference of ``set1`` and ``set2``.

        :return: The :term:`difference` of ``set1`` and ``set2`` or `Undef()` if ``set1`` or
            ``set2`` are not :term:`set`\s (that is, instances of :class:`~.Set`).
        """
        # pylint: disable=too-many-branches
        if _checked:
            if not is_member(set1):
                return _undef.make_or_raise_undef2(set1)
            if not is_member(set2):
                return _undef.make_or_raise_undef2(set2)
        else:
            assert is_member_or_undef(set1)
            assert is_member_or_undef(set2)
            if set1 is _undef.Undef() or set2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _mo.Set(set1.data.difference(set2.data), direct_load=True)
        if not result.is_empty:
            # Relation flags:
            if set1.cached_is_relation:
                result.cache_relation(CacheStatus.IS)
                if set1.cached_is_absolute:
                    result.cache_absolute(CacheStatus.IS)
                if set1.cached_is_functional:
                    result.cache_functional(CacheStatus.IS)
                if set1.cached_is_right_functional:
                    result.cache_right_functional(CacheStatus.IS)
            # Clan flags:
            if set1.cached_is_clan:
                result.cache_clan(CacheStatus.IS)
                if set1.cached_is_absolute:
                    result.cache_absolute(CacheStatus.IS)
                if set1.cached_is_functional:
                    result.cache_functional(CacheStatus.IS)
                if set1.cached_is_right_functional:
                    result.cache_right_functional(CacheStatus.IS)
                if set1.cached_is_reflexive:
                    result.cache_reflexive(CacheStatus.IS)
                if set1.cached_is_symmetric:
                    result.cache_symmetric(CacheStatus.IS)
                if set1.cached_is_transitive:
                    result.cache_transitive(CacheStatus.IS)
                if set1.cached_is_regular:
                    result.cache_regular(CacheStatus.IS)
                if set1.cached_is_right_regular:
                    result.cache_right_regular(CacheStatus.IS)
        return result

    @staticmethod
    def substrict(set1: 'P( M )', set2: 'P( M )', _checked=True) -> 'P( M )':
        r"""Return ``set1`` if it is a subset of ``set2``, otherwise return `Undef()`.

        :return: Return the :term:`substriction` of ``set1`` and ``set1``; that is, return ``set1``
            if it is a :term:`subset` of ``set2`` or `Undef()` if not. Also return `Undef()` if
            ``set1`` or ``set2`` are not :term:`set`\s (that is, instances of :class:`~.Set`).
        """
        # pylint: disable=too-many-branches
        if _checked:
            if not is_member(set1):
                return _undef.make_or_raise_undef2(set1)
            if not is_member(set2):
                return _undef.make_or_raise_undef2(set2)
        else:
            assert is_member_or_undef(set1)
            assert is_member_or_undef(set2)
            if set1 is _undef.Undef() or set2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        if not is_subset_of(set1, set2, _checked=False):
            return _undef.make_or_raise_undef(2)
        if not set1.is_empty:
            # Relation flags:
            if set1.cached_is_relation:
                if set2.cached_is_absolute:
                    set1.cache_absolute(CacheStatus.IS)
                if set2.cached_is_functional:
                    set1.cache_functional(CacheStatus.IS)
                if set2.cached_is_right_functional:
                    set1.cache_right_functional(CacheStatus.IS)
            # Clan flags:
            if set1.cached_is_clan:
                if set2.cached_is_absolute:
                    set1.cache_absolute(CacheStatus.IS)
                if set2.cached_is_functional:
                    set1.cache_functional(CacheStatus.IS)
                if set2.cached_is_right_functional:
                    set1.cache_right_functional(CacheStatus.IS)
                if set2.cached_is_regular:
                    set1.cache_regular(CacheStatus.IS)
                if set2.cached_is_right_regular:
                    set1.cache_right_regular(CacheStatus.IS)
        return set1

    @staticmethod
    def superstrict(set1: 'P( M )', set2: 'P( M )', _checked=True) -> 'P( M )':
        r"""Return ``set1`` if it is a superset of ``set2``, otherwise return `Undef()`.

        :return: Return the :term:`superstriction` of ``set1`` and ``set1``; that is, return
            ``set1`` if it is a :term:`superset` of ``set2`` or `Undef()` if not. Also return
            `Undef()` if ``set1`` or ``set2`` are not :term:`set`\s (that is, instances of
            :class:`~.Set`).
        """
        # pylint: disable=too-many-branches
        if _checked:
            if not is_member(set1):
                return _undef.make_or_raise_undef2(set1)
            if not is_member(set2):
                return _undef.make_or_raise_undef2(set2)
        else:
            assert is_member_or_undef(set1)
            assert is_member_or_undef(set2)
            if set1 is _undef.Undef() or set2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        if not is_superset_of(set1, set2, _checked=False):
            return _undef.make_or_raise_undef(2)
        if not set1.is_empty:
            # Relation flags:
            if set1.cached_is_relation:
                if set2.cached_is_not_absolute:
                    set1.cache_absolute(CacheStatus.IS_NOT)
                if set2.cached_is_not_functional:
                    set1.cache_functional(CacheStatus.IS_NOT)
                if set2.cached_is_not_right_functional:
                    set1.cache_right_functional(CacheStatus.IS_NOT)
            # Clan flags:
            if set1.cached_is_clan:
                if set2.cached_is_not_absolute:
                    set1.cache_absolute(CacheStatus.IS_NOT)
                if set2.cached_is_not_functional:
                    set1.cache_functional(CacheStatus.IS_NOT)
                if set2.cached_is_not_right_functional:
                    set1.cache_right_functional(CacheStatus.IS_NOT)
                if set2.cached_is_not_regular:
                    set1.cache_regular(CacheStatus.IS_NOT)
                if set2.cached_is_not_right_regular:
                    set1.cache_right_regular(CacheStatus.IS_NOT)
        return set1

    # ----------------------------------------------------------------------------------------------
    # Algebra relations.

    @staticmethod
    def is_subset_of(set1: 'P( M )', set2: 'P( M )', _checked=True) -> bool:
        r"""Return whether ``set1`` is a subset of ``set2``.

        :return: ``True`` if ``set1`` is a :term:`subset` of ``set2``, ``False`` if not. Return
            `Undef()` if ``set1`` or ``set2`` are not :term:`set`\s (that is, instances of
            :class:`~.Set`).
        """
        if _checked:
            if not is_member(set1):
                return _undef.make_or_raise_undef2(set1)
            if not is_member(set2):
                return _undef.make_or_raise_undef2(set2)
        else:
            assert is_member_or_undef(set1)
            assert is_member_or_undef(set2)
            if set1 is _undef.Undef() or set2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        return set1.data.issubset(set2.data)

    @staticmethod
    def is_superset_of(set1: 'P( M )', set2: 'P( M )', _checked=True) -> bool:
        r"""Return whether ``set1`` is a superset of ``set2``.

        :return: ``True`` if ``set1`` is a :term:`superset` of ``set2``, ``False`` if not. Return
            `Undef()` if ``set1`` or ``set2`` are not :term:`set`\s (that is, instances of
            :class:`~.Set`).
        """
        if _checked:
            if not is_member(set1):
                return _undef.make_or_raise_undef2(set1)
            if not is_member(set2):
                return _undef.make_or_raise_undef2(set2)
        else:
            assert is_member_or_undef(set1)
            assert is_member_or_undef(set2)
            if set1 is _undef.Undef() or set2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        return set1.data.issuperset(set2.data)


# For convenience, make the members of class Algebra (they are all static functions) available at
# the module level.

# pylint: disable=invalid-name

#: Convenience redirection to `Algebra.union`.
union = Algebra.union
#: Convenience redirection to `Algebra.intersect`.
intersect = Algebra.intersect
#: Convenience redirection to `Algebra.minus`.
minus = Algebra.minus
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
    return 'Sets(M): {ground_set}'.format(ground_set=str(get_ground_set()))


def get_ground_set() -> _structure.Structure:
    """Return the :term:`ground set` of this :term:`algebra`."""
    return _structure.PowerSet(_structure.GenesisSetM())


def get_absolute_ground_set() -> _structure.Structure:
    """Return the :term:`absolute ground set` of this :term:`algebra`."""
    return _structure.PowerSet(_structure.GenesisSetA())


def is_member(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is a member of the :term:`ground set` of this :term:`algebra`.

     :return: ``True`` if ``obj`` is a :term:`set` (an instance of :class:`~.Set`),
        ``False`` if not.
     """
    return obj.is_set


def is_member_or_undef(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is either a member of the :term:`ground set` of this :term:`algebra`
        or :class:`~.Undef`.

     :return: ``True`` if ``obj`` is either a :term:`relation` or :class:`~.Undef`,
        ``False`` if not.
    """
    return obj is _undef.Undef() or is_member(obj)


def is_absolute_member(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is a member of the :term:`absolute ground set` of this algebra.

     :return: ``True`` if ``obj`` is an :term:`absolute set`, ``False`` if not.
    """
    if not obj.is_set:
        # If known to not be a set, it's also not an absolute set. No further checking or caching.
        return False
    # From this point on, `obj` is known to be a set.
    if obj.cached_absolute == CacheStatus.UNKNOWN:
        import algebraixlib.algebras.clans as _clans
        import algebraixlib.algebras.relations as _relations

        # In order to find out whether this is an absolute set, we need to know whether `obj` is a
        # relation or a clan (both sets). If it is one of these, it is not an absolute set -- but
        # we also don't know whether it is an absolute relation or clan. So we return `False` but
        # don't cache anything. (But we have now cached that it is a relation or a clan.)
        if _relations.is_member(obj) or _clans.is_member(obj):
            return False
        is_absolute_set = all(elem.is_atom for elem in obj)
        obj.cache_absolute(CacheStatus.from_bool(is_absolute_set))
    # In order to determine whether this is an absolute set, we need to also examine whether this
    # is a relation or a clan (both are sets). Absolute relations and absolute clans are not
    # absolute sets.
    return obj.cached_is_absolute and not obj.cached_is_relation and not obj.cached_is_clan


# --------------------------------------------------------------------------------------------------
# Related operations, not formally part of the algebra.

def multify(set_: 'P( M )', _checked=True) -> 'P( M x N )':
    """Return a :term:`multiset` based on ``set_`` where all multiples are set to 1."""
    if _checked:
        if not is_member(set_):
            return _undef.make_or_raise_undef2(set_)
    else:
        assert is_member_or_undef(set_)
        if set_ is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    result = _mo.Multiset(set_.data, direct_load=True)
    if not result.is_empty:
        result.cache_multiclan(set_.cached_clan)
        if set_.cached_is_relation:
            # We don't yet have a concept of multirelations (multisets of couplets). This would be
            # handled here.
            pass
        elif set_.cached_is_clan:
            result.cache_absolute(set_.cached_absolute)
            result.cache_functional(set_.cached_functional)
            result.cache_right_functional(set_.cached_right_functional)
            result.cache_reflexive(set_.cached_reflexive)
            result.cache_symmetric(set_.cached_symmetric)
            result.cache_transitive(set_.cached_transitive)
            result.cache_regular(set_.cached_regular)
            result.cache_right_regular(set_.cached_right_regular)
        if set_.cached_is_not_relation and set_.cached_is_not_clan:
            # set_ is known to be a plain set.
            result.cache_absolute(set_.cached_absolute)
            result.cache_functional(CacheStatus.N_A)
            result.cache_right_functional(CacheStatus.N_A)
            result.cache_reflexive(CacheStatus.N_A)
            result.cache_symmetric(CacheStatus.N_A)
            result.cache_transitive(CacheStatus.N_A)
            result.cache_regular(CacheStatus.N_A)
            result.cache_right_regular(CacheStatus.N_A)
    return result


def big_union(set_: 'PP( M )', _checked=True) -> 'P( M )':
    """Return the union of all members of ``set_``.

    :return: The :term:`union` of all members of ``set_`` or `Undef()` if ``set_`` or any of its
        members are not instances of :class:`~.Set`.

    Example code:

    .. code::

        from algebraixlib.mathobjects import Set
        from algebraixlib.algebras.sets import big_union
        big_union(Set(Set('a', 'b'), Set('b', 'c')))
        # Output: Set(Atom('a'), Atom('b'), Atom('c'))
        big_union(Set(Set('a', 'b'), 'a'))
        # Output: <algebraixlib.undef.Undef at 0x4004978>
    """
    if _checked:
        if not is_member(set_):
            return _undef.make_or_raise_undef2(set_)
        for element in set_:
            if not is_member(element):
                return _undef.make_or_raise_undef(2)
    else:
        assert is_member_or_undef(set_)
        if set_ is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    return chain_binary_operation(set_, _functools.partial(union, _checked=False), is_member)


def big_intersect(set_: 'PP( M )', _checked=True) -> 'P( M )':
    """Return the intersection of all members of ``set_``.

    :return: The :term:`intersection` of all members of ``set_`` or `Undef()` if ``set_`` or any of
        its members are not instances of :class:`~.Set`.

    Example code:

    .. code::

        from algebraixlib.mathobjects import Set
        from algebraixlib.algebras.sets import big_intersect
        big_intersect(Set(Set('a', 'b'), Set('b', 'c')))
        # Output: Set(Atom('b'))
        big_intersect(Set(Set('a', 'b'), 'a'))
        # Output: <algebraixlib.undef.Undef at 0x4004978>
    """
    if _checked:
        if not is_member(set_):
            return _undef.make_or_raise_undef2(set_)
        for element in set_:
            if not is_member(element):
                return _undef.make_or_raise_undef(2)
    else:
        assert is_member_or_undef(set_)
        if set_ is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    return chain_binary_operation(set_, _functools.partial(intersect, _checked=False), is_member)


def single(set_: _mo.Set):
    """Return the single element of ``set_``.

    :return: Return the single element of ``set_``, or `Undef()` if ``set_`` has not exactly one
        element or is not a :term:`set` (that is, an instance of :class:`~.Set`).
    """
    if not is_member(set_):
        return _undef.make_or_raise_undef2(set_)
    if set_.cardinality == 1:
        return next(iter(set_))
    return _undef.make_or_raise_undef(2)


def some(set_: _mo.Set):
    """Return 'some' element of ``set_``. Use with caution - may be non-deterministic.

    :return: Some element of ``set_``, or `Undef()` if ``set_`` is empty or is not a :term:`set`
        (that is, an instance of :class:`~.Set`).

    .. note:: This function should only be used in contexts where the way the return value will be
        utilized by the calling function is invariant of the particular element returned; the
        element of ``set_`` that is returned is non-deterministic.

        This function is only intended to be used in (mostly implementation) scenarios where it
        does not matter which element of ``set_`` is retrieved, because the expressions that
        consume that value will be invariant with respect to the exact element of ``set_`` that is
        returned.
    """
    if not is_member(set_):
        return _undef.make_or_raise_undef2(set_)
    if len(set_) > 0:
        return next(iter(set_))
    return _undef.make_or_raise_undef(2)


def power_set(set_: _mo.Set):
    """Return the :term:`power set` of ``set_``."""
    if not is_member(set_):
        return _undef.make_or_raise_undef2(set_)
    from itertools import combinations
    result = []
    for subset_size in range(set_.cardinality + 1):
        subset_combinations = combinations(set_, subset_size)
        result.extend(_mo.Set(comb) for comb in subset_combinations)
    result = _mo.Set(result)
    if not result.is_empty:
        if set_.cached_is_relation:
            result.cache_clan(CacheStatus.IS)
            result.cache_absolute(set_.cached_absolute)
            result.cache_functional(set_.cached_functional)
            result.cache_right_functional(set_.cached_right_functional)
            result.cache_regular(CacheStatus.IS_NOT)
            result.cache_right_regular(CacheStatus.IS_NOT)
    return result


def power_up(set_: _mo.Set):
    """'Add a set of braces' around the elements of ``set_``.

    :return: A :class:`~.Set` where every element is a ``Set`` that contains exactly one element
        of ``set_`` and where there is exactly one element-``Set`` for every element of ``set_``.
    """
    if not is_member(set_):
        return _undef.make_or_raise_undef2(set_)
    result = _mo.Set((_mo.Set(element) for element in set_), direct_load=True)
    if not result.is_empty:
        if set_.cached_is_relation:
            result.cache_clan(CacheStatus.IS)
            result.cache_absolute(set_.cached_absolute)
            result.cache_functional(CacheStatus.IS)
            result.cache_right_functional(CacheStatus.IS)
    return result


def restrict(set_: 'P( M )', selector: _collections.Callable) -> 'P( M )':
    """Return a set with all the elements from ``set_`` for which the predicate ``selector`` returns
    ``True``.

    :param set_: The source data. Must be a :term:`set`.
    :param selector: A :class:`~collections.abc.Callable` that accepts as single argument a
        :class:`~.MathObject` and returns a `bool` that indicates whether the element is
        in the result set (``True``) or not (``False``).
    """
    # pylint: disable=too-many-branches
    if not is_member(set_):
        return _undef.make_or_raise_undef2(set_)
    result = _mo.Set((element for element in set_ if selector(element)), direct_load=True)
    if not result.is_empty:
        # Relation flags:
        if set_.cached_is_relation:
            result.cache_relation(CacheStatus.IS)
            if set_.cached_is_absolute:
                result.cache_absolute(CacheStatus.IS)
            if set_.cached_is_functional:
                result.cache_functional(CacheStatus.IS)
            if set_.cached_is_right_functional:
                result.cache_right_functional(CacheStatus.IS)
        # Clan flags:
        if set_.cached_is_clan:
            result.cache_clan(CacheStatus.IS)
            if set_.cached_is_absolute:
                result.cache_absolute(CacheStatus.IS)
            if set_.cached_is_functional:
                result.cache_functional(CacheStatus.IS)
            if set_.cached_is_right_functional:
                result.cache_right_functional(CacheStatus.IS)
            if set_.cached_is_reflexive:
                result.cache_reflexive(CacheStatus.IS)
            if set_.cached_is_symmetric:
                result.cache_symmetric(CacheStatus.IS)
            if set_.cached_is_transitive:
                result.cache_transitive(CacheStatus.IS)
            if set_.cached_is_regular:
                result.cache_regular(CacheStatus.IS)
            if set_.cached_is_right_regular:
                result.cache_right_regular(CacheStatus.IS)
    return result


def chain_binary_operation(set_, binary_op, is_algebra_member):
    r"""Chain all elements of ``set_`` with the binary operation ``binary_op`` and return the
    result.

    :param set_: A :term:`set` of sets or :term:`multiset`\s.
    :param binary_op: The operation through which the members of ``set_`` are chained. It must be
        commutative and associative.
    :param is_algebra_member: The ``is_member()`` function of the :term:`algebra` of which the
        elements of ``set_`` must be members.
    :return: A member of ``algebra`` that is the result of chaining all elements of ``set_`` with
        the :term:`binary operation` ``binary_op``.
    """
    if not is_member(set_):
        return _undef.make_or_raise_undef2(set_)

    if set_.is_empty:
        return set_

    set_itr = iter(set_)
    element1 = next(set_itr)
    if not is_algebra_member(element1):
        return _undef.make_or_raise_undef()

    result = element1
    for element in set_itr:
        if not is_algebra_member(element):
            return _undef.make_or_raise_undef()
        result = binary_op(result, element)
    return result
