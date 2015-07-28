r"""This module contains the :term:`algebra of clans` and related functionality.

A :term:`clan` is also a :term:`set` (of :term:`relation`\s), and inherits all operations
of the :term:`algebra of sets`. These are provided in :mod:`~.algebras.sets`.
"""

# $Id: clans.py 22702 2015-07-28 20:20:56Z jaustell $
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
    """Provide the operations and relations that are members of the :term:`algebra of clans`.

    This class contains only static member functions. Its main purpose is to provide a namespace for
    and highlight the operations and relations that belong to the algebra of clans. All member
    functions are also available at the enclosing module scope.
    """
    # ----------------------------------------------------------------------------------------------
    # Unary algebra operations.

    @staticmethod
    def transpose(clan: 'PP(M x M)', _checked=True) -> 'PP(M x M)':
        """Return a clan where all relations have their left and right components swapped.

        :return: The :term:`unary extension` of :term:`transposition` from the :term:`algebra of
            relations` to the :term:`algebra of clans`, applied to ``clan``, or `Undef()` if
            ``clan`` is not a :term:`clan`.
        """
        if _checked:
            if not is_member(clan):
                return _make_or_raise_undef()
        else:
            assert is_member(clan)
        result = _extension.unary_extend(clan, _functools.partial(
            _relations.transpose, _checked=False), _checked=False).cache_is_clan(True)
        if not result.is_empty:
            if clan.cached_is_functional or clan.cached_is_not_functional:
                result.cache_is_right_functional(clan.cached_is_functional)
            if clan.cached_is_right_functional or clan.cached_is_not_right_functional:
                result.cache_is_functional(clan.cached_is_right_functional)
        return result

    # ----------------------------------------------------------------------------------------------
    # Binary algebra operations.

    @staticmethod
    def compose(clan1: 'PP(M x M)', clan2: 'PP(M x M)', _checked=True) -> 'PP(M x M)':
        r"""Return the composition of ``clan1`` with ``clan2``.

        :return: The :term:`binary extension` of :term:`composition` from the
            :term:`algebra of relations` to the :term:`algebra of clans`, applied to ``clan1``
            and ``clan2``, or `Undef()` if ``clan1`` or ``clan2`` are not :term:`clan`\s.
        """
        if _checked:
            if not is_member(clan1):
                return _make_or_raise_undef()
            if not is_member(clan2):
                return _make_or_raise_undef()
        else:
            assert is_member(clan1)
            assert is_member(clan2)
        return _extension.binary_extend(clan1, clan2, _functools.partial(
            _relations.compose, _checked=False), _checked=False).cache_is_clan(True)

    @staticmethod
    def cross_union(clan1: 'PP(M x M)', clan2: 'PP(M x M)', _checked=True) -> 'PP(M x M)':
        r"""Return the cross-union of ``clan1`` and ``clan2``.

        The :term:`cross-union` of two :term:`clan`\s is a clan that contains the result of
        unioning every :term:`relation` from one clan with every relation from the other clan.

        :return: The :term:`binary extension` of :term:`union` from the :term:`algebra of relations`
            (which inherits it from the :term:`algebra of sets`) to the :term:`algebra of clans`
            applied to ``clan1`` and ``clan2``, or `Undef()` if ``clan1`` or ``clan2`` are not
            clans.
        """
        if _checked:
            if not is_member(clan1):
                return _make_or_raise_undef()
            if not is_member(clan2):
                return _make_or_raise_undef()
        else:
            assert is_member(clan1)
            assert is_member(clan2)
        return _extension.binary_extend(
            clan1, clan2, _functools.partial(
                _sets.union, _checked=False), _checked=False).cache_is_clan(True)

    @staticmethod
    def cross_functional_union(clan1: 'PP(M x M)', clan2: 'PP(M x M)',
                               _checked=True) -> 'PP(M x M)':
        r"""Return the cross-functional union of ``clan1`` and ``clan2``.

        The :term:`cross-functional union` of two :term:`clan`\s is the :term:`cross-union` of
        these clans, but removing all resulting :term:`relation`\s that are not :term:`function`\s.

        :return: The :term:`binary extension` of the :term:`functional union` from the
            :term:`algebra of relations` to the :term:`algebra of clans`, applied to ``clan1`` and
            ``clan2``, or `Undef()` if ``clan1`` or ``clan2`` are not clans.
        """
        if _checked:
            if not is_member(clan1):
                return _make_or_raise_undef()
            if not is_member(clan2):
                return _make_or_raise_undef()
        else:
            assert is_member(clan1)
            assert is_member(clan2)
        return _extension.binary_extend(
            clan1, clan2, _functools.partial(_relations.functional_union, _checked=False),
            _checked=False).cache_is_clan(True).cache_is_functional(True)

    @staticmethod
    def lhs_cross_functional_union(lhs: 'PP( MxM )', rhs: 'PP( MxM )',
                                   _checked=True) -> 'PP(M x M)':
        """Return the :term:`lhs-cross-functional union` ('left join') of ``lhs`` and ``rhs``.

        This operation results in a :term:`clan` that contains every :term:`relation` of a
        :term:`cross-functional union`, but also contains all relations in ``lhs`` that
        are not already part of one of the resulting relations.

        :param lhs: All relations in this clan are guaranteed to be represented in the result.
        :return: The resulting clan or `Undef()` if ``lhs`` or ``rhs`` are not clans.
        """
        if _checked:
            if not is_member(lhs):
                return _make_or_raise_undef()
            if not is_member(rhs):
                return _make_or_raise_undef()
        else:
            assert is_member(lhs)
            assert is_member(rhs)

        result = _sets.union(
            cross_functional_union(lhs, rhs, _checked=False),
            _mo.Set(lhs_elem for lhs_elem in lhs if cross_functional_union(
                _mo.Set(lhs_elem, direct_load=True), rhs).is_empty), _checked=False)

        if lhs.cached_is_functional:
            result.cache_is_functional(True)
        return result

    @staticmethod
    def cross_right_functional_union(clan1: 'PP(M x M)', clan2: 'PP(M x M)',
                                     _checked=True) -> 'PP(M x M)':
        r"""Return the cross-right-functional union of ``clan1`` and ``clan2``.

        The :term:`cross-right-functional union` of two :term:`clan`\s is the :term:`cross-union`
        of these clans, but removing all resulting :term:`relation`\s that are not
        :term:`right-functional`.

        :return: The :term:`binary extension` of the :term:`right-functional union` from the
            :term:`algebra of relations` to the :term:`algebra of clans`, applied to ``clan1`` and
            ``clan2``, or `Undef()` if ``clan1`` or ``clan2`` are not :term:`clan`\s.
        """
        if _checked:
            if not is_member(clan1):
                return _make_or_raise_undef()
            if not is_member(clan2):
                return _make_or_raise_undef()
        else:
            assert is_member(clan1)
            assert is_member(clan2)
        return _extension.binary_extend(
            clan1, clan2, _functools.partial(_relations.right_functional_union, _checked=False),
            _checked=False).cache_is_clan(True).cache_is_right_functional(True)

    @staticmethod
    def cross_intersect(clan1: 'PP(M x M)', clan2: 'PP(M x M)', _checked=True) -> 'PP(M x M)':
        r"""Return the cross-intersection of ``clan1`` and ``clan2``.

        The :term:`cross-intersection` of two :term:`clan`\s is a clan that contains the result of
        intersecting every :term:`relation` from one clan with every relation from the other clan.

        :return: The :term:`binary extension` of :term:`intersection` from the :term:`algebra of
            relations` (which inherits it from the :term:`algebra of sets`) to the :term:`algebra of
            clans` applied to ``clan1`` and ``clan2``, or `Undef()` if ``clan1`` or ``clan2`` are
            not :term:`clan`\s.
        """
        if _checked:
            if not is_member(clan1):
                return _make_or_raise_undef()
            if not is_member(clan2):
                return _make_or_raise_undef()
        else:
            assert is_member(clan1)
            assert is_member(clan2)
        return _extension.binary_extend(
            clan1, clan2, _functools.partial(
                _sets.intersect, _checked=False), _checked=False).cache_is_clan(True)

    @staticmethod
    def substrict(clan1: 'PP(M x M)', clan2: 'PP(M x M)', _checked=True) -> 'PP(M x M)':
        r"""Return the substriction of ``clan1`` and ``clan2``.

        The :term:`substriction` of two :term:`clan`\s is a clan that contains all
        :term:`relation`\s from ``clan1`` that are a :term:`subset` of a relation from ``clan2``.

        :return: The :term:`binary extension` of :term:`substriction` from the :term:`algebra of
            sets` to the :term:`algebra of clans` applied to ``clan1`` and ``clan2``, or `Undef()`
            if ``clan1`` or ``clan2`` are not clans.
        """
        if _checked:
            if not is_member(clan1):
                return _make_or_raise_undef()
            if not is_member(clan2):
                return _make_or_raise_undef()
        else:
            assert is_member(clan1)
            assert is_member(clan2)
        result = _extension.binary_extend(
            clan1, clan2, _functools.partial(
                _sets.substrict, _checked=False), _checked=False).cache_is_clan(True)
        # The subset of clan1 that is returned has all properties of clan1
        if not result.is_empty:
            result.copy_flags(clan1)
        return result

    @staticmethod
    def superstrict(clan1: 'PP(M x M)', clan2: 'PP(M x M)', _checked=True) -> 'PP(M x M)':
        r"""Return the superstriction of ``clan1`` and ``clan2``.

        The :term:`superstriction` of two :term:`clan`\s is a clan that contains all
        :term:`relation`\s from ``clan1`` that are a :term:`superset` of a relation from ``clan2``.

        :return: The :term:`binary extension` of :term:`superstriction` from the :term:`algebra of
            sets` to the :term:`algebra of clans` applied to ``clan1`` and ``clan2``, or `Undef()`
            if ``clan1`` or ``clan2`` are not clans.
        """
        if _checked:
            if not is_member(clan1):
                return _make_or_raise_undef()
            if not is_member(clan2):
                return _make_or_raise_undef()
        else:
            assert is_member(clan1)
            assert is_member(clan2)
        result = _extension.binary_extend(clan1, clan2, _functools.partial(
            _sets.superstrict, _checked=False)).cache_is_clan(True)

        # The subset of clan1 that is returned has all properties of clan1
        if not result.is_empty:
            result.copy_flags(clan1)
        return result


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
#: Convenience redirection to `Algebra.lhs_cross_functional_union`.
lhs_cross_functional_union = Algebra.lhs_cross_functional_union
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
    return 'Clans(M): {ground_set}'.format(ground_set=str(get_ground_set()))


def get_ground_set() -> _structure.Structure:
    """Return the :term:`ground set` of this :term:`algebra`."""
    return _structure.PowerSet(_relations.get_ground_set())


def get_absolute_ground_set() -> _structure.Structure:
    """Return the :term:`absolute ground set` of this :term:`algebra`."""
    return _structure.PowerSet(_relations.get_absolute_ground_set())


def is_member(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is a member of the :term:`ground set` of this :term:`algebra`.

    .. note:: This function may call :meth:`~.MathObject.get_ground_set` on ``obj``. The result of
        this operation is cached.
    """
    _mo.raise_if_not_mathobject(obj)
    if not obj.cached_is_clan and not obj.cached_is_not_clan:
        obj.cache_is_clan(obj.get_ground_set().is_subset(get_ground_set()))
    return obj.cached_is_clan


def is_absolute_member(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is a member of the :term:`absolute ground set` of this algebra.

     :return: Whether ``obj`` is an :term:`absolute clan`.

    .. note:: This function calls :meth:`~.MathObject.get_ground_set` on ``obj``.
    """
    _mo.raise_if_not_mathobject(obj)
    return obj.get_ground_set().is_subset(get_absolute_ground_set())


# --------------------------------------------------------------------------------------------------
# Related operations, not formally part of the algebra.

def get_lefts(clan: 'PP(M x M)', _checked=True) -> 'P( M )':
    r"""Return the set of the left components of all couplets in all relations in ``clan``.

    :return: The :term:`union` of the :term:`left set`\s of all :term:`relation`\s in ``clan`` or
        `Undef()` if ``clan`` is not a :term:`clan`.
    """
    if _checked:
        if not is_member(clan):
            return _make_or_raise_undef()
    else:
        assert is_member(clan)
    if clan.is_empty:
        # The left set of an empty set is the empty set
        return clan
    clan_itr = iter(clan)
    left_set = _relations.get_lefts(next(clan_itr), _checked=False)
    for rel in clan_itr:
        left_set = _sets.union(
            _relations.get_lefts(rel, _checked=False), left_set, _checked=False)
    return left_set


def get_rights(clan: 'PP(M x M)', _checked=True) -> "P( M )":
    r"""Return the set of the right components of all couplets in all relations in ``clan``.

    :return: The :term:`union` of the :term:`right set`\s of all :term:`relation`\s in ``clan`` or
        `Undef()` if ``clan`` is not a :term:`clan`.
    """
    if _checked:
        if not is_member(clan):
            return _make_or_raise_undef()
    else:
        assert is_member(clan)
    if clan.is_empty:
        # The right set of an empty set is the empty set
        return clan
    clan_itr = iter(clan)
    right_set = _relations.get_rights(next(clan_itr), _checked=False)
    for rel in clan_itr:
        right_set = _sets.union(
            _relations.get_rights(rel, _checked=False), right_set, _checked=False)
    return right_set


def is_regular(clan, _checked=True) -> bool:
    """Return whether ``clan`` is regular.

    :return: ``True`` if ``clan`` is :term:`regular`, ``False`` if not or `Undef()` if ``clan``
        is not a :term:`clan`.
    """
    if _checked:
        if not is_member(clan):
            return _make_or_raise_undef()
    else:
        assert is_member(clan)

    if not clan.cached_is_regular and not clan.cached_is_not_regular:
        # NOTE: The empty case is handled in Set().__init__ via flags initialization
        if clan.cached_is_not_functional:
            clan.cache_is_regular(False)
            return False
        itr = iter(clan)
        rel = next(itr)
        if not rel.is_functional():
            clan.cache_is_regular(False)
            return False
        left_set = rel.get_left_set()
        regular = all(rel.is_functional() and left_set == rel.get_left_set() for rel in itr)
        clan.cache_is_regular(regular)
    return clan.cached_is_regular


def project(clan: 'PP(M x M)', *lefts) -> 'PP(M x M)':
    r"""Return a clan that contains only the couplets with lefts from ``clan`` that match ``lefts``.

    :param clan: The source data. Must be a :term:`clan`.
    :param lefts: The names of the :term:`left component`\s to match. (If you want to pass in an
        iterable, you need to prefix it with an asterisk ``*``.)
    :return: The :term:`projection` of ``clan`` (a clan that contains only :term:`couplet`\s with
        left components as indicated by ``lefts``), or `Undef()` if ``clan`` is not a clan.
    """
    clan = compose(clan, diag(*lefts))
    return clan


def from_set(left: '( M )', *values: '( M )') -> 'PP(M x M)':
    r"""Return a clan where all relations contain a single couplet with the same left component.

    :param left: The :term:`left component` of all :term:`couplet`\s in the returned :term:`clan`.
    :param values: The :term:`right component`\s of the couplets in the returned clan. (If you want
        to pass in an iterable, you need to prefix it with an asterisk ``*``.)
    :return: A clan where every :term:`relation` consists of a single couplet with a left component
        of ``left`` and a right component from ``values``.
    """
    left_mo = _mo.auto_convert(left)
    clan = _mo.Set((_mo.Set(_mo.Couplet(left_mo, _mo.auto_convert(right), direct_load=True),
                            direct_load=True).cache_is_relation(True)
                    for right in values), direct_load=True).cache_is_clan(True)
    return clan


def from_dict(dict1: dict) -> 'PP(M x M)':
    r"""Return a :term:`clan` with a single :term:`relation` where the :term:`couplet`\s are the
    elements of ``dict1``."""
    clan = _mo.Set(_mo.Set((_mo.Couplet(left, right) for left, right in dict1.items()),
                           direct_load=True).cache_is_relation(True),
                   direct_load=True).cache_is_clan(True)
    return clan


def diag(*args, _checked=True) -> 'PP(M x M)':
    """Return a clan diagonal of the arguments.

    :param args: Pass in the elements from which the :term:`clan diagonal` is formed. (If you want
        to pass in an iterable, you need to prefix it with an asterisk ``*``.)
    """
    clan = _mo.Set(_relations.diag(*args, _checked=_checked), direct_load=True).cache_is_clan(True)
    return clan


def defined_at(clan, left, _checked=True):
    r"""Return the :term:`relation`\s of ``clan`` that are defined for ``left``."""
    clan = _extension.unary_extend(clan, _functools.partial(
        _relations.defined_at, left=left, _checked=_checked), _checked=_checked).cache_is_clan(True)
    return clan
