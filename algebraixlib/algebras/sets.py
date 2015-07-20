"""This module contains the :term:`algebra of sets` and related functionality."""

# $Id: sets.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import collections as _collections
from functools import partial

import algebraixlib.mathobjects as _mo
import algebraixlib.structure as _structure
from algebraixlib.undef import make_or_raise_undef as _make_or_raise_undef


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
        """Return the union of ``set1`` with ``set2``.

        :return: The :term:`binary union` of ``set1`` and ``set2`` or `Undef()` if ``set1`` or
            ``set2`` are not :term:`set`\s (that is, instances of :class:`~.Set`).
        """
        if _checked:
            if not is_member(set1):
                return _make_or_raise_undef()
            if not is_member(set2):
                return _make_or_raise_undef()
        else:
            assert is_member(set1)
            assert is_member(set2)
        values = set1.data.union(set2.data)
        ret = _mo.Set(values, direct_load=True)
        if not ret.is_empty:
            # Relay relation flags
            if set1.cached_is_relation and set2.cached_is_relation:
                ret.cache_is_relation(True)
            elif set1.cached_is_not_relation or set2.cached_is_not_relation:
                ret.cache_is_relation(False)

            # Relay clan flags
            if set1.cached_is_clan and set2.cached_is_clan:
                ret.cache_is_clan(True)
            elif set1.cached_is_not_clan or set2.cached_is_not_clan:
                ret.cache_is_clan(False)
        return ret

    @staticmethod
    def intersect(set1: 'P( M )', set2: 'P( M )', _checked=True) -> 'P( M )':
        """Return the intersection of ``set1`` with ``set2``.

        :return: The :term:`binary intersection` of ``set1`` and ``set2`` or `Undef()` if ``set1``
            or ``set2`` are not :term:`set`\s (that is, instances of :class:`~.Set`).
        """
        if _checked:
            if not is_member(set1):
                return _make_or_raise_undef()
            if not is_member(set2):
                return _make_or_raise_undef()
        else:
            assert is_member(set1)
            assert is_member(set2)
        values = set1.data.intersection(set2.data)
        ret = _mo.Set(values, direct_load=True)
        if not ret.is_empty:
            if set1.cached_is_clan and set2.cached_is_clan:
                ret.cache_is_clan(True)
            if set1.cached_is_relation and set2.cached_is_relation:
                ret.cache_is_relation(True)
        return ret

    @staticmethod
    def minus(set1: 'P( M )', set2: 'P( M )', _checked=True) -> 'P( M )':
        """Return the set difference of ``set1`` and ``set2``.

        :return: The :term:`difference` of ``set1`` and ``set2`` or `Undef()` if ``set1`` or
            ``set2`` are not :term:`set`\s (that is, instances of :class:`~.Set`).
        """
        if _checked:
            if not is_member(set1):
                return _make_or_raise_undef()
            if not is_member(set2):
                return _make_or_raise_undef()
        else:
            assert is_member(set1)
            assert is_member(set2)
        result = _mo.Set(set1.data.difference(set2.data), direct_load=True)
        if not result.is_empty:
            if set1.cached_is_clan or set1.cached_is_not_clan:
                result.cache_is_clan(set1.cached_is_clan)
            if set1.cached_is_relation or set1.cached_is_not_relation:
                result.cache_is_relation(set1.cached_is_relation)
            if set1.cached_is_left_functional or set1.cached_is_not_left_functional:
                result.cache_is_left_functional(set1.cached_is_left_functional)
        return result

    @staticmethod
    def substrict(set1: 'P( M )', set2: 'P( M )', _checked=True) -> 'P( M )':
        """Return ``set1`` if it is a subset of ``set2``, otherwise return `Undef()`.

        :return: Return the :term:`substriction` of ``set1`` and ``set1``; that is, return ``set1``
            if it is a :term:`subset` of ``set2`` or `Undef()` if not. Also return `Undef()` if
            ``set1`` or ``set2`` are not :term:`set`\s (that is, instances of :class:`~.Set`).
        """
        if _checked:
            if not is_member(set1):
                return _make_or_raise_undef()
            if not is_member(set2):
                return _make_or_raise_undef()
        else:
            assert is_member(set1)
            assert is_member(set2)
        if not is_subset_of(set1, set2, _checked=False):
            return _make_or_raise_undef(2)
        return set1

    @staticmethod
    def superstrict(set1: 'P( M )', set2: 'P( M )', _checked=True) -> 'P( M )':
        """Return ``set1`` if it is a superset of ``set2``, otherwise return `Undef()`.

        :return: Return the :term:`superstriction` of ``set1`` and ``set1``; that is, return
            ``set1`` if it is a :term:`subset` of ``set2`` or `Undef()` if not. Also return
            `Undef()` if ``set1`` or ``set2`` are not :term:`set`\s (that is, instances of
            :class:`~.Set`).
        """
        if _checked:
            if not is_member(set1):
                return _make_or_raise_undef()
            if not is_member(set2):
                return _make_or_raise_undef()
        else:
            assert is_member(set1)
            assert is_member(set2)
        if not is_superset_of(set1, set2, _checked=False):
            return _make_or_raise_undef(2)
        return set1

    # --------------------------------------------------------------------------------------------------
    # Algebra relations.

    @staticmethod
    def is_subset_of(set1: 'P( M )', set2: 'P( M )', _checked=True) -> bool:
        """Return whether ``set1`` is a subset of ``set2``.

        :return: ``True`` if ``set1`` is a :term:`subset` of ``set2``, ``False`` if not. Return
            `Undef()` if ``set1`` or ``set2`` are not :term:`set`\s (that is, instances of
            :class:`~.Set`).
        """
        if _checked:
            if not is_member(set1):
                return _make_or_raise_undef()
            if not is_member(set2):
                return _make_or_raise_undef()
        else:
            assert is_member(set1)
            assert is_member(set2)
        return set1.data.issubset(set2.data)

    @staticmethod
    def is_superset_of(set1: 'P( M )', set2: 'P( M )', _checked=True) -> bool:
        """Return whether ``set1`` is a superset of ``set2``.

        :return: ``True`` if ``set1`` is a :term:`superset` of ``set2``, ``False`` if not. Return
            `Undef()` if ``set1`` or ``set2`` are not :term:`set`\s (that is, instances of
            :class:`~.Set`).
        """
        if _checked:
            if not is_member(set1):
                return _make_or_raise_undef()
            if not is_member(set2):
                return _make_or_raise_undef()
        else:
            assert is_member(set1)
            assert is_member(set2)
        return set1.data.issuperset(set2.data)


# For convenience, make the members of class Algebra (they are all static functions) available at
# the module level.

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
    """Return ``True`` if ``obj`` is a member of the :term:`ground set` of this :term:`algebra`.

     :return: ``True`` if ``obj`` is an instance of :class:`~.Set`.
     """
    _mo.raise_if_not_mathobject(obj)
    return isinstance(obj, _mo.Set)


def is_absolute_member(obj: _mo.MathObject) -> bool:
    """Return ``True`` if ``obj`` is a member of the :term:`absolute ground set` of this algebra.

     :return: ``True`` if ``obj`` is an :term:`absolute set`.

    .. note:: This function calls :meth:`~.MathObject.get_ground_set` on ``obj``."""
    _mo.raise_if_not_mathobject(obj)
    return obj.get_ground_set().is_subset(get_absolute_ground_set())


# --------------------------------------------------------------------------------------------------
# Related operations, not formally part of the algebra.

def multify(set1: 'P( M )', _checked=True) -> 'P( M x N )':
    """Return a :term:`multiset` based on ``set1`` where all multiples are set to 1."""
    if _checked:
        if not is_member(set1):
            return _make_or_raise_undef()
    else:
        assert is_member(set1)
    return _mo.Multiset(set1.data, direct_load=True)


def big_union(set1: 'PP( M )', _checked=True) -> 'P( M )':
    """Return the union of all members of ``set1``.

    :return: The :term:`union` of all members of ``set1`` or `Undef()` if ``set1`` or any of its
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
        if not isinstance(set1, _mo.Set):
            return _make_or_raise_undef()
        for element in set1:
            if not is_member(element):
                return _make_or_raise_undef()
    else:
        assert isinstance(set1, _mo.Set)
    return _extend_binary_operation(set1, partial(union, _checked=False))


def big_intersect(set1: 'PP( M )', _checked=True) -> 'P( M )':
    """Return the intersection of all members of ``set1``.

    :return: The :term:`intersection` of all members of ``set1`` or `Undef()` if ``set1`` or any of
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
        if not isinstance(set1, _mo.Set):
            return _make_or_raise_undef()
        for element in set1:
            if not is_member(element):
                return _make_or_raise_undef()
    else:
        assert isinstance(set1, _mo.Set)
    return _extend_binary_operation(set1, partial(intersect, _checked=False))


def single(set1: _mo.Set):
    """Return the single element of ``set1``.

    :return: Return the single element of ``set1``, or `Undef()` if ``set1`` has not exactly one
        element or is not a :term:`set` (that is, an instance of :class:`~.Set`).
    """
    if not is_member(set1):
        return _make_or_raise_undef()
    if set1.cardinality == 1:
        return next(iter(set1))
    return _make_or_raise_undef(2)


def some(set1: _mo.Set):
    """Return 'some' element of ``set1``. Use with caution - may be non-deterministic.

    :return: Some element of ``set1``, or `Undef()` if ``set1`` is empty or is not a :term:`set`
        (that is, an instance of :class:`~.Set`).

    .. note:: This function should only be used in contexts where the way the return value will be
        utilized by the calling function is invariant of the particular element returned; the
        element of ``set1`` that is returned is non-deterministic.

        This function is only intended to be used in (mostly implementation) scenarios where it
        does not matter which element of ``set1`` is retrieved, because the expressions that
        consume that value will be invariant w.r.t. some of ``set1``.
    """
    if not is_member(set1):
        return _make_or_raise_undef()
    if len(set1) > 0:
        return next(iter(set1))
    return _make_or_raise_undef()


def power_set(set1: _mo.Set):
    """Return the :term:`power set` of ``set1``."""
    from itertools import combinations
    result = []
    for n in range(set1.cardinality + 1):
        n_combinations = combinations(set1, n)
        result.extend(_mo.Set(comb) for comb in n_combinations)
    return _mo.Set(result)


def power_up(set1: _mo.Set):
    """'Add a set of braces' around the elements of ``set1``.

    :return: A :class:`~.Set` where every element is a ``Set`` that contains exactly one element
        of ``set1`` and where there is exactly one element-``Set`` for every element of ``set1``.
    """
    return _mo.Set((_mo.Set(element) for element in set1), direct_load=True)


def restrict(set1: 'P( M )', selector: _collections.Callable) -> 'P( M )':
    """Return a set with all the elements from ``set1`` for which the predicate ``selector`` returns
    ``True``.

    :param set1: The source data. Must be a :term:`set`.
    :param selector: A :class:`~collections.abc.Callable` that accepts as single argument a
        :class:`~.MathObject` and returns a `bool` that indicates whether the element is
        in the result set (``True``) or not (``False``).
    """
    if not is_member(set1):
        return _make_or_raise_undef()
    return _mo.Set((element for element in set1 if selector(element)),
                   direct_load=True).cache_is_clan(True)


def _extend_binary_operation(set1: 'PP( M )', binary_op):
    """Extend a binary operation ``binary_op`` and apply it to all members of ``set1``."""
    if set1.is_empty:
        return set1
    elem_itr = iter(set1)
    element = next(elem_itr)
    assert is_member(element)
    result = element
    for element in elem_itr:
        assert is_member(element)
        result = binary_op(result, element)
    return result
