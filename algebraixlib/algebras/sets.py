"""This module contains the :term:`algebra of sets` and related functionality."""

<<<<<<< HEAD
# $Id: sets.py 22804 2015-08-14 17:43:32Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-08-14 12:43:32 -0500 (Fri, 14 Aug 2015) $
=======
# $Id: sets.py 22702 2015-07-28 20:20:56Z jaustell $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-28 15:20:56 -0500 (Tue, 28 Jul 2015) $
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
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
<<<<<<< HEAD
import algebraixlib.undef as _undef
=======
from algebraixlib.undef import make_or_raise_undef as _make_or_raise_undef
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272


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
<<<<<<< HEAD
        # pylint: disable=too-many-branches
        if _checked:
            if not is_member(set1):
                return _undef.make_or_raise_undef()
            if not is_member(set2):
                return _undef.make_or_raise_undef()
=======
        if _checked:
            if not is_member(set1):
                return _make_or_raise_undef()
            if not is_member(set2):
                return _make_or_raise_undef()
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
        else:
            assert is_member(set1)
            assert is_member(set2)
        values = set1.data.union(set2.data)
<<<<<<< HEAD
        result = _mo.Set(values, direct_load=True)
        if not result.is_empty:
            # Relation flags:
            if set1.cached_is_relation and set2.cached_is_relation:
                result.cache_relation(_mo.CacheStatus.IS)
                if set1.cached_is_absolute and set2.cached_is_absolute:
                    result.cache_absolute(_mo.CacheStatus.IS)
                elif set1.cached_is_not_absolute or set2.cached_is_not_absolute:
                    result.cache_absolute(_mo.CacheStatus.IS_NOT)
                if set1.cached_is_not_functional or set2.cached_is_not_functional:
                    result.cache_functional(_mo.CacheStatus.IS_NOT)
                if set1.cached_is_not_right_functional or set2.cached_is_not_right_functional:
                    result.cache_right_functional(_mo.CacheStatus.IS_NOT)
            elif set1.cached_is_not_relation or set2.cached_is_not_relation:
                result.cache_relation(_mo.CacheStatus.IS_NOT)
            # Clan flags:
            if set1.cached_is_clan and set2.cached_is_clan:
                result.cache_clan(_mo.CacheStatus.IS)
                if set1.cached_is_absolute and set2.cached_is_absolute:
                    result.cache_absolute(_mo.CacheStatus.IS)
                elif set1.cached_is_not_absolute or set2.cached_is_not_absolute:
                    result.cache_absolute(_mo.CacheStatus.IS_NOT)
                if set1.cached_is_functional and set2.cached_is_functional:
                    result.cache_functional(_mo.CacheStatus.IS)
                elif set1.cached_is_not_functional or set2.cached_is_not_functional:
                    result.cache_functional(_mo.CacheStatus.IS_NOT)
                if set1.cached_is_right_functional and set2.cached_is_right_functional:
                    result.cache_right_functional(_mo.CacheStatus.IS)
                elif set1.cached_is_not_right_functional or set2.cached_is_not_right_functional:
                    result.cache_right_functional(_mo.CacheStatus.IS_NOT)
                if set1.cached_is_not_regular or set2.cached_is_not_regular:
                    result.cache_regular(_mo.CacheStatus.IS_NOT)
                if set1.cached_is_not_right_regular or set2.cached_is_not_right_regular:
                    result.cache_right_regular(_mo.CacheStatus.IS_NOT)
            elif set1.cached_is_not_clan or set2.cached_is_not_clan:
                result.cache_clan(_mo.CacheStatus.IS_NOT)
        return result
=======
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
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272

    @staticmethod
    def intersect(set1: 'P( M )', set2: 'P( M )', _checked=True) -> 'P( M )':
        r"""Return the intersection of ``set1`` with ``set2``.

        :return: The :term:`binary intersection` of ``set1`` and ``set2`` or `Undef()` if ``set1``
            or ``set2`` are not :term:`set`\s (that is, instances of :class:`~.Set`).
        """
<<<<<<< HEAD
        # pylint: disable=too-many-branches
        if _checked:
            if not is_member(set1):
                return _undef.make_or_raise_undef()
            if not is_member(set2):
                return _undef.make_or_raise_undef()
=======
        if _checked:
            if not is_member(set1):
                return _make_or_raise_undef()
            if not is_member(set2):
                return _make_or_raise_undef()
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
        else:
            assert is_member(set1)
            assert is_member(set2)
        values = set1.data.intersection(set2.data)
<<<<<<< HEAD
        result = _mo.Set(values, direct_load=True)
        if not result.is_empty:
            # Relation flags:
            if set1.cached_is_relation or set2.cached_is_relation:
                result.cache_relation(_mo.CacheStatus.IS)
                if set1.cached_is_absolute or set2.cached_is_absolute:
                    result.cache_absolute(_mo.CacheStatus.IS)
                if set1.cached_is_functional or set2.cached_is_functional:
                    result.cache_functional(_mo.CacheStatus.IS)
                if set1.cached_is_right_functional or set2.cached_is_right_functional:
                    result.cache_right_functional(_mo.CacheStatus.IS)
            # Clan flags:
            if set1.cached_is_clan or set2.cached_is_clan:
                result.cache_clan(_mo.CacheStatus.IS)
                if set1.cached_is_absolute or set2.cached_is_absolute:
                    result.cache_absolute(_mo.CacheStatus.IS)
                if set1.cached_is_functional or set2.cached_is_functional:
                    result.cache_functional(_mo.CacheStatus.IS)
                if set1.cached_is_right_functional or set2.cached_is_right_functional:
                    result.cache_right_functional(_mo.CacheStatus.IS)
                if set1.cached_is_regular or set2.cached_is_regular:
                    result.cache_regular(_mo.CacheStatus.IS)
                if set1.cached_is_right_regular or set2.cached_is_right_regular:
                    result.cache_right_regular(_mo.CacheStatus.IS)
        return result
=======
        ret = _mo.Set(values, direct_load=True)
        if not ret.is_empty:
            if set1.cached_is_clan and set2.cached_is_clan:
                ret.cache_is_clan(True)
            if set1.cached_is_relation and set2.cached_is_relation:
                ret.cache_is_relation(True)
        return ret
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272

    @staticmethod
    def minus(set1: 'P( M )', set2: 'P( M )', _checked=True) -> 'P( M )':
        r"""Return the set difference of ``set1`` and ``set2``.

        :return: The :term:`difference` of ``set1`` and ``set2`` or `Undef()` if ``set1`` or
            ``set2`` are not :term:`set`\s (that is, instances of :class:`~.Set`).
        """
<<<<<<< HEAD
        # pylint: disable=too-many-branches
        if _checked:
            if not is_member(set1):
                return _undef.make_or_raise_undef()
            if not is_member(set2):
                return _undef.make_or_raise_undef()
=======
        if _checked:
            if not is_member(set1):
                return _make_or_raise_undef()
            if not is_member(set2):
                return _make_or_raise_undef()
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
        else:
            assert is_member(set1)
            assert is_member(set2)
        result = _mo.Set(set1.data.difference(set2.data), direct_load=True)
        if not result.is_empty:
<<<<<<< HEAD
            # Relation flags:
            if set1.cached_is_relation:
                result.cache_relation(_mo.CacheStatus.IS)
                if set1.cached_is_absolute:
                    result.cache_absolute(_mo.CacheStatus.IS)
                if set1.cached_is_functional:
                    result.cache_functional(_mo.CacheStatus.IS)
                if set1.cached_is_right_functional:
                    result.cache_right_functional(_mo.CacheStatus.IS)
            # Clan flags:
            if set1.cached_is_clan:
                result.cache_clan(_mo.CacheStatus.IS)
                if set1.cached_is_absolute:
                    result.cache_absolute(_mo.CacheStatus.IS)
                if set1.cached_is_functional:
                    result.cache_functional(_mo.CacheStatus.IS)
                if set1.cached_is_right_functional:
                    result.cache_right_functional(_mo.CacheStatus.IS)
                if set1.cached_is_reflexive:
                    result.cache_reflexive(_mo.CacheStatus.IS)
                if set1.cached_is_symmetric:
                    result.cache_symmetric(_mo.CacheStatus.IS)
                if set1.cached_is_transitive:
                    result.cache_transitive(_mo.CacheStatus.IS)
                if set1.cached_is_regular:
                    result.cache_regular(_mo.CacheStatus.IS)
                if set1.cached_is_right_regular:
                    result.cache_right_regular(_mo.CacheStatus.IS)
=======
            if set1.cached_is_clan or set1.cached_is_not_clan:
                result.cache_is_clan(set1.cached_is_clan)
            if set1.cached_is_relation or set1.cached_is_not_relation:
                result.cache_is_relation(set1.cached_is_relation)
            if set1.cached_is_functional:
                result.cache_is_functional(set1.cached_is_functional)
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
        return result

    @staticmethod
    def substrict(set1: 'P( M )', set2: 'P( M )', _checked=True) -> 'P( M )':
        r"""Return ``set1`` if it is a subset of ``set2``, otherwise return `Undef()`.

        :return: Return the :term:`substriction` of ``set1`` and ``set1``; that is, return ``set1``
            if it is a :term:`subset` of ``set2`` or `Undef()` if not. Also return `Undef()` if
            ``set1`` or ``set2`` are not :term:`set`\s (that is, instances of :class:`~.Set`).
        """
<<<<<<< HEAD
        # pylint: disable=too-many-branches
        if _checked:
            if not is_member(set1):
                return _undef.make_or_raise_undef()
            if not is_member(set2):
                return _undef.make_or_raise_undef()
=======
        if _checked:
            if not is_member(set1):
                return _make_or_raise_undef()
            if not is_member(set2):
                return _make_or_raise_undef()
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
        else:
            assert is_member(set1)
            assert is_member(set2)
        if not is_subset_of(set1, set2, _checked=False):
<<<<<<< HEAD
            return _undef.make_or_raise_undef(2)
        if not set1.is_empty:
            # Relation flags:
            if set1.cached_is_relation:
                if set2.cached_is_absolute:
                    set1.cache_absolute(_mo.CacheStatus.IS)
                if set2.cached_is_functional:
                    set1.cache_functional(_mo.CacheStatus.IS)
                if set2.cached_is_right_functional:
                    set1.cache_right_functional(_mo.CacheStatus.IS)
            # Clan flags:
            if set1.cached_is_clan:
                if set2.cached_is_absolute:
                    set1.cache_absolute(_mo.CacheStatus.IS)
                if set2.cached_is_functional:
                    set1.cache_functional(_mo.CacheStatus.IS)
                if set2.cached_is_right_functional:
                    set1.cache_right_functional(_mo.CacheStatus.IS)
                if set2.cached_is_regular:
                    set1.cache_regular(_mo.CacheStatus.IS)
                if set2.cached_is_right_regular:
                    set1.cache_right_regular(_mo.CacheStatus.IS)
=======
            return _make_or_raise_undef(2)
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
        return set1

    @staticmethod
    def superstrict(set1: 'P( M )', set2: 'P( M )', _checked=True) -> 'P( M )':
        r"""Return ``set1`` if it is a superset of ``set2``, otherwise return `Undef()`.

        :return: Return the :term:`superstriction` of ``set1`` and ``set1``; that is, return
<<<<<<< HEAD
            ``set1`` if it is a :term:`superset` of ``set2`` or `Undef()` if not. Also return
            `Undef()` if ``set1`` or ``set2`` are not :term:`set`\s (that is, instances of
            :class:`~.Set`).
        """
        # pylint: disable=too-many-branches
        if _checked:
            if not is_member(set1):
                return _undef.make_or_raise_undef()
            if not is_member(set2):
                return _undef.make_or_raise_undef()
=======
            ``set1`` if it is a :term:`subset` of ``set2`` or `Undef()` if not. Also return
            `Undef()` if ``set1`` or ``set2`` are not :term:`set`\s (that is, instances of
            :class:`~.Set`).
        """
        if _checked:
            if not is_member(set1):
                return _make_or_raise_undef()
            if not is_member(set2):
                return _make_or_raise_undef()
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
        else:
            assert is_member(set1)
            assert is_member(set2)
        if not is_superset_of(set1, set2, _checked=False):
<<<<<<< HEAD
            return _undef.make_or_raise_undef(2)
        if not set1.is_empty:
            # Relation flags:
            if set1.cached_is_relation:
                if set2.cached_is_not_absolute:
                    set1.cache_absolute(_mo.CacheStatus.IS_NOT)
                if set2.cached_is_not_functional:
                    set1.cache_functional(_mo.CacheStatus.IS_NOT)
                if set2.cached_is_not_right_functional:
                    set1.cache_right_functional(_mo.CacheStatus.IS_NOT)
            # Clan flags:
            if set1.cached_is_clan:
                if set2.cached_is_not_absolute:
                    set1.cache_absolute(_mo.CacheStatus.IS_NOT)
                if set2.cached_is_not_functional:
                    set1.cache_functional(_mo.CacheStatus.IS_NOT)
                if set2.cached_is_not_right_functional:
                    set1.cache_right_functional(_mo.CacheStatus.IS_NOT)
                if set2.cached_is_not_regular:
                    set1.cache_regular(_mo.CacheStatus.IS_NOT)
                if set2.cached_is_not_right_regular:
                    set1.cache_right_regular(_mo.CacheStatus.IS_NOT)
=======
            return _make_or_raise_undef(2)
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
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
<<<<<<< HEAD
                return _undef.make_or_raise_undef()
            if not is_member(set2):
                return _undef.make_or_raise_undef()
=======
                return _make_or_raise_undef()
            if not is_member(set2):
                return _make_or_raise_undef()
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
        else:
            assert is_member(set1)
            assert is_member(set2)
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
<<<<<<< HEAD
                return _undef.make_or_raise_undef()
            if not is_member(set2):
                return _undef.make_or_raise_undef()
=======
                return _make_or_raise_undef()
            if not is_member(set2):
                return _make_or_raise_undef()
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
        else:
            assert is_member(set1)
            assert is_member(set2)
        return set1.data.issuperset(set2.data)


# For convenience, make the members of class Algebra (they are all static functions) available at
# the module level.

<<<<<<< HEAD
# pylint: disable=invalid-name

=======
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
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

<<<<<<< HEAD
# pylint: enable=invalid-name
=======
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272

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

<<<<<<< HEAD
     :return: ``True`` if ``obj`` is a :term:`set` (an instance of :class:`~.Set`),
        ``False`` if not.
     """
    return obj.is_set
=======
     :return: ``True`` if ``obj`` is an instance of :class:`~.Set`, ``False`` if not.
     """
    _mo.raise_if_not_mathobject(obj)
    return isinstance(obj, _mo.Set)
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272


def is_absolute_member(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is a member of the :term:`absolute ground set` of this algebra.

     :return: ``True`` if ``obj`` is an :term:`absolute set`, ``False`` if not.
<<<<<<< HEAD
    """
    if not obj.is_set:
        # If known to not be a set, it's also not an absolute set. No further checking or caching.
        return False
    # From this point on, `obj` is known to be a set.
    if obj.cached_absolute == _mo.CacheStatus.UNKNOWN:
        import algebraixlib.algebras.clans as _clans
        import algebraixlib.algebras.relations as _relations

        # In order to find out whether this is an absolute set, we need to know whether `obj` is a
        # relation or a clan (both sets). If it is one of these, it is not an absolute set -- but
        # we also don't know whether it is an absolute relation or clan. So we return `False` but
        # don't cache anything. (But we have now cached that it is a relation or a clan.)
        if _relations.is_member(obj) or _clans.is_member(obj):
            return False
        is_absolute_set = all(elem.is_atom for elem in obj)
        obj.cache_absolute(_mo.CacheStatus.from_bool(is_absolute_set))
    # In order to determine whether this is an absolute set, we need to also examine whether this
    # is a relation or a clan (both are sets). Absolute relations and absolute clans are not
    # absolute sets.
    return obj.cached_is_absolute and not obj.cached_is_relation and not obj.cached_is_clan
=======

    .. note:: This function calls :meth:`~.MathObject.get_ground_set` on ``obj``."""
    _mo.raise_if_not_mathobject(obj)
    return obj.get_ground_set().is_subset(get_absolute_ground_set())
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272


# --------------------------------------------------------------------------------------------------
# Related operations, not formally part of the algebra.

<<<<<<< HEAD
def multify(set_: 'P( M )', _checked=True) -> 'P( M x N )':
    """Return a :term:`multiset` based on ``set_`` where all multiples are set to 1."""
    if _checked:
        if not is_member(set_):
            return _undef.make_or_raise_undef()
    else:
        assert is_member(set_)
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
            result.cache_functional(_mo.CacheStatus.N_A)
            result.cache_right_functional(_mo.CacheStatus.N_A)
            result.cache_reflexive(_mo.CacheStatus.N_A)
            result.cache_symmetric(_mo.CacheStatus.N_A)
            result.cache_transitive(_mo.CacheStatus.N_A)
            result.cache_regular(_mo.CacheStatus.N_A)
            result.cache_right_regular(_mo.CacheStatus.N_A)
    return result


def big_union(set_: 'PP( M )', _checked=True) -> 'P( M )':
    """Return the union of all members of ``set_``.

    :return: The :term:`union` of all members of ``set_`` or `Undef()` if ``set_`` or any of its
=======
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
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
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
<<<<<<< HEAD
        if not isinstance(set_, _mo.Set):
            return _undef.make_or_raise_undef()
        for element in set_:
            if not is_member(element):
                return _undef.make_or_raise_undef()
    else:
        assert set_.is_set
    return chain_binary_operation(set_, _functools.partial(union, _checked=False), is_member)


def big_intersect(set_: 'PP( M )', _checked=True) -> 'P( M )':
    """Return the intersection of all members of ``set_``.

    :return: The :term:`intersection` of all members of ``set_`` or `Undef()` if ``set_`` or any of
=======
        if not isinstance(set1, _mo.Set):
            return _make_or_raise_undef()
        for element in set1:
            if not is_member(element):
                return _make_or_raise_undef()
    else:
        assert isinstance(set1, _mo.Set)
    return chain_binary_operation(set1, _functools.partial(union, _checked=False), is_member)


def big_intersect(set1: 'PP( M )', _checked=True) -> 'P( M )':
    """Return the intersection of all members of ``set1``.

    :return: The :term:`intersection` of all members of ``set1`` or `Undef()` if ``set1`` or any of
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
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
<<<<<<< HEAD
        if not isinstance(set_, _mo.Set):
            return _undef.make_or_raise_undef()
        for element in set_:
            if not is_member(element):
                return _undef.make_or_raise_undef()
    else:
        assert set_.is_set
    return chain_binary_operation(set_, _functools.partial(intersect, _checked=False), is_member)


def single(set_: _mo.Set):
    """Return the single element of ``set_``.

    :return: Return the single element of ``set_``, or `Undef()` if ``set_`` has not exactly one
        element or is not a :term:`set` (that is, an instance of :class:`~.Set`).
    """
    if not is_member(set_):
        return _undef.make_or_raise_undef()
    if set_.cardinality == 1:
        return next(iter(set_))
    return _undef.make_or_raise_undef(2)


def some(set_: _mo.Set):
    """Return 'some' element of ``set_``. Use with caution - may be non-deterministic.

    :return: Some element of ``set_``, or `Undef()` if ``set_`` is empty or is not a :term:`set`
=======
        if not isinstance(set1, _mo.Set):
            return _make_or_raise_undef()
        for element in set1:
            if not is_member(element):
                return _make_or_raise_undef()
    else:
        assert isinstance(set1, _mo.Set)
    return chain_binary_operation(set1, _functools.partial(intersect, _checked=False), is_member)


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
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
        (that is, an instance of :class:`~.Set`).

    .. note:: This function should only be used in contexts where the way the return value will be
        utilized by the calling function is invariant of the particular element returned; the
<<<<<<< HEAD
        element of ``set_`` that is returned is non-deterministic.

        This function is only intended to be used in (mostly implementation) scenarios where it
        does not matter which element of ``set_`` is retrieved, because the expressions that
        consume that value will be invariant with respect to the exact element of ``set_`` that is
        returned.
    """
    if not is_member(set_):
        return _undef.make_or_raise_undef()
    if len(set_) > 0:
        return next(iter(set_))
    return _undef.make_or_raise_undef()


def power_set(set_: _mo.Set):
    """Return the :term:`power set` of ``set_``."""
    from itertools import combinations
    result = []
    for subset_size in range(set_.cardinality + 1):
        subset_combinations = combinations(set_, subset_size)
        result.extend(_mo.Set(comb) for comb in subset_combinations)
    result = _mo.Set(result)
    if not result.is_empty:
        if set_.cached_is_relation:
            result.cache_clan(_mo.CacheStatus.IS)
            result.cache_absolute(set_.cached_absolute)
            result.cache_functional(set_.cached_functional)
            result.cache_right_functional(set_.cached_right_functional)
            result.cache_regular(_mo.CacheStatus.IS_NOT)
            result.cache_right_regular(_mo.CacheStatus.IS_NOT)
    return result


def power_up(set_: _mo.Set):
    """'Add a set of braces' around the elements of ``set_``.

    :return: A :class:`~.Set` where every element is a ``Set`` that contains exactly one element
        of ``set_`` and where there is exactly one element-``Set`` for every element of ``set_``.
    """
    result = _mo.Set((_mo.Set(element) for element in set_), direct_load=True)
    if not result.is_empty:
        if set_.cached_is_relation:
            result.cache_clan(_mo.CacheStatus.IS)
            result.cache_absolute(set_.cached_absolute)
            result.cache_functional(_mo.CacheStatus.IS)
            result.cache_right_functional(_mo.CacheStatus.IS)
    return result


def restrict(set_: 'P( M )', selector: _collections.Callable) -> 'P( M )':
    """Return a set with all the elements from ``set_`` for which the predicate ``selector`` returns
    ``True``.

    :param set_: The source data. Must be a :term:`set`.
=======
        element of ``set1`` that is returned is non-deterministic.

        This function is only intended to be used in (mostly implementation) scenarios where it
        does not matter which element of ``set1`` is retrieved, because the expressions that
        consume that value will be invariant with respect to the exact element of ``set1`` that is
        returned.
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
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
    :param selector: A :class:`~collections.abc.Callable` that accepts as single argument a
        :class:`~.MathObject` and returns a `bool` that indicates whether the element is
        in the result set (``True``) or not (``False``).
    """
<<<<<<< HEAD
    # pylint: disable=too-many-branches
    if not is_member(set_):
        return _undef.make_or_raise_undef()
    result = _mo.Set((element for element in set_ if selector(element)), direct_load=True)
    if not result.is_empty:
        # Relation flags:
        if set_.cached_is_relation:
            result.cache_relation(_mo.CacheStatus.IS)
            if set_.cached_is_absolute:
                result.cache_absolute(_mo.CacheStatus.IS)
            if set_.cached_is_functional:
                result.cache_functional(_mo.CacheStatus.IS)
            if set_.cached_is_right_functional:
                result.cache_right_functional(_mo.CacheStatus.IS)
        # Clan flags:
        if set_.cached_is_clan:
            result.cache_clan(_mo.CacheStatus.IS)
            if set_.cached_is_absolute:
                result.cache_absolute(_mo.CacheStatus.IS)
            if set_.cached_is_functional:
                result.cache_functional(_mo.CacheStatus.IS)
            if set_.cached_is_right_functional:
                result.cache_right_functional(_mo.CacheStatus.IS)
            if set_.cached_is_reflexive:
                result.cache_reflexive(_mo.CacheStatus.IS)
            if set_.cached_is_symmetric:
                result.cache_symmetric(_mo.CacheStatus.IS)
            if set_.cached_is_transitive:
                result.cache_transitive(_mo.CacheStatus.IS)
            if set_.cached_is_regular:
                result.cache_regular(_mo.CacheStatus.IS)
            if set_.cached_is_right_regular:
                result.cache_right_regular(_mo.CacheStatus.IS)
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
        return _undef.make_or_raise_undef()

    if set_.is_empty:
        return set_

    set_itr = iter(set_)
    element1 = next(set_itr)
    if not is_algebra_member(element1):
        return _undef.make_or_raise_undef()
=======
    if not is_member(set1):
        return _make_or_raise_undef()
    return _mo.Set((element for element in set1 if selector(element)),
                   direct_load=True).cache_is_clan(True)


def chain_binary_operation(set1, binary_op, is_algebra_member):
    r"""Chain all elements of ``set1`` with the binary operation ``binary_op`` and return the
    result.

    :param set1: A :term:`set` of sets or :term:`multiset`\s.
    :param binary_op: The operation through which the members of ``set1`` are chained. It must be
        commutative and associative.
    :param is_algebra_member: The ``is_member()`` function of the :term:`algebra` of which the
        elements of ``set1`` must be members.
    :return: A member of ``algebra`` that is the result of chaining all elements of ``set1`` with
        the :term:`binary operation` ``binary_op``.
    """
    if not is_member(set1):
        return _make_or_raise_undef()

    if set1.is_empty:
        return set1

    set_itr = iter(set1)
    element1 = next(set_itr)
    if not is_algebra_member(element1):
        return _make_or_raise_undef()
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272

    result = element1
    for element in set_itr:
        if not is_algebra_member(element):
<<<<<<< HEAD
            return _undef.make_or_raise_undef()
=======
            return _make_or_raise_undef()
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
        result = binary_op(result, element)
    return result
