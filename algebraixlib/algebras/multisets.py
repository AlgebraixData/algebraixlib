"""This module contains the :term:`algebra of multisets` and related functionality."""

# $Id: multisets.py 22702 2015-07-28 20:20:56Z jaustell $
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

import algebraixlib.algebras.sets as _sets
import algebraixlib.mathobjects as _mo
import algebraixlib.structure as _structure
from algebraixlib.undef import make_or_raise_undef as _make_or_raise_undef


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
        if _checked:
            if not is_member(multiset1):
                return _make_or_raise_undef()
            if not is_member(multiset2):
                return _make_or_raise_undef()
        else:
            assert is_member(multiset1)
            assert is_member(multiset2)
        values = multiset1.data | multiset2.data
        return _mo.Multiset(values, direct_load=True)

    @staticmethod
    def intersect(multiset1: 'P( M x N )', multiset2: 'P( M x N )', _checked=True) -> 'P( M x N )':
        """Return the multiset intersection of ``multiset1`` with ``multiset2``.

        :return: The :term:`multiset intersection` of ``multiset1`` and ``multiset2`` or `Undef()`
            if ``multiset1`` or ``multiset2`` are not instances of :class:`~.Multiset`.
        """
        if _checked:
            if not is_member(multiset1):
                return _make_or_raise_undef()
            if not is_member(multiset2):
                return _make_or_raise_undef()
        else:
            assert is_member(multiset1)
            assert is_member(multiset2)
        values = multiset1.data & multiset2.data
        return _mo.Multiset(values)

    @staticmethod
    def minus(multiset1: 'P( M x N )', multiset2: 'P( M x N )', _checked=True) -> 'P( M x N )':
        """Return the multiset difference of ``multiset1`` and ``multiset2``.

        :return: The :term:`multiset difference` of ``multiset1`` and ``multiset2`` or `Undef()`
            if ``multiset1`` or ``multiset2`` are not instances of :class:`~.Multiset`.
        """
        if _checked:
            if not is_member(multiset1):
                return _make_or_raise_undef()
            if not is_member(multiset2):
                return _make_or_raise_undef()
        else:
            assert is_member(multiset1)
            assert is_member(multiset2)
        values = multiset1.data - multiset2.data
        return _mo.Multiset(values)

    @staticmethod
    def addition(multiset1: 'P( M x N )', multiset2: 'P( M x N )', _checked=True) -> 'P( M x N )':
        """Return the multiset addition of ``multiset1`` and ``multiset2``.

        :return: The :term:`multiset addition` of ``multiset1`` and ``multiset2`` or `Undef()` if
            ``multiset1`` or ``multiset2`` are not instances of :class:`~.Multiset`.
        """
        if _checked:
            if not is_member(multiset1):
                return _make_or_raise_undef()
            if not is_member(multiset2):
                return _make_or_raise_undef()
        else:
            assert is_member(multiset1)
            assert is_member(multiset2)
        values = multiset1.data + multiset2.data
        return _mo.Multiset(values)

    @staticmethod
    def substrict(multiset1: 'P( M x N )', multiset2: 'P( M x N )', _checked=True) -> 'P( M x N )':
        """Return ``multiset1`` if ``multiset1`` is a subset of ``multiset2`` or `Undef()` if not.

        :return: The :term:`substriction` of ``multiset1`` and ``multiset2`` (may return `Undef()`).
            Also return `Undef()` if ``multiset1`` or ``multiset2`` are not instances of
            :class:`~.Multiset`.
        """
        if _checked:
            if not is_member(multiset1):
                return _make_or_raise_undef()
            if not is_member(multiset2):
                return _make_or_raise_undef()
        else:
            assert is_member(multiset1)
            assert is_member(multiset2)
        if not is_subset_of(multiset1, multiset2, _checked=False):
            return _make_or_raise_undef(2)
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
                return _make_or_raise_undef()
            if not is_member(multiset2):
                return _make_or_raise_undef()
        else:
            assert is_member(multiset1)
            assert is_member(multiset2)
        if not is_superset_of(multiset1, multiset2, _checked=False):
            return _make_or_raise_undef(2)
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
                return _make_or_raise_undef()
            if not is_member(multiset2):
                return _make_or_raise_undef()
        else:
            assert is_member(multiset1)
            assert is_member(multiset2)
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
                return _make_or_raise_undef()
            if not is_member(multiset2):
                return _make_or_raise_undef()
        else:
            assert is_member(multiset1)
            assert is_member(multiset2)
        for key in multiset2.data.keys():
            if not multiset1.data[key] >= multiset2.data[key]:
                return False
        return True


# For convenience, make the members of class Algebra (they are all static functions) available at
# the module level.

#: Convenience redirection to `Algebra.union`.
union = Algebra.union
#: Convenience redirection to `Algebra.intersect`.
intersect = Algebra.intersect
#: Convenience redirection to `Algebra.minus`.
minus = Algebra.minus
#: Convenience redirection to `Algebra.addition`.
addition = Algebra.addition
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

     :return: ``True`` if ``obj`` is an instance of :class:`~.Multiset`, ``False`` if not.
     """
    _mo.raise_if_not_mathobject(obj)
    return isinstance(obj, _mo.Multiset)


def is_absolute_member(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is a member of the :term:`absolute ground set` of this algebra.

     :return: ``True`` if ``obj`` is an :term:`absolute set`, ``False`` if not.

    .. note:: This function calls :meth:`~.MathObject.get_ground_set` on ``obj``."""
    _mo.raise_if_not_mathobject(obj)
    return obj.get_ground_set().is_subset(get_absolute_ground_set())


# --------------------------------------------------------------------------------------------------
# Related operations, not formally part of the algebra.

def demultify(multiset: 'P( M x N )', _checked=True) -> 'P( M )':
    """Return a :term:`set` based on ``multiset`` that contains all elements without multiples."""
    if _checked:
        if not is_member(multiset):
            return _make_or_raise_undef()
    else:
        assert is_member(multiset)
    return _mo.Set(multiset.data.keys(), direct_load=True)


def big_union(set_of_multisets: 'PP( M x N )', _checked=True) -> 'P( M x N )':
    """Return the set_of_multisets union of all members of ``set_of_multisets``.

    :return: The :term:`multiset union` of all members of ``set_of_multisets`` or `Undef()` if
        ``set_of_multisets`` is not a :class:`~.Set` or any of its members are not instances of
        :class:`~.Multiset`.
    """
    if _checked:
        if not isinstance(set_of_multisets, _mo.Set):
            return _make_or_raise_undef()
        for element in set_of_multisets:
            if not is_member(element):
                return _make_or_raise_undef()
    else:
        assert isinstance(set_of_multisets, _mo.Set)
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
            return _make_or_raise_undef()
        for element in set_of_multisets:
            if not is_member(element):
                return _make_or_raise_undef()
    else:
        assert isinstance(set_of_multisets, _mo.Set)
    return _sets.chain_binary_operation(
        set_of_multisets, _functools.partial(intersect, _checked=False), is_member)
