r"""This module contains the :term:`algebra of clans` and related functionality.

A :term:`clan` is also a :term:`set` (of :term:`relation`\s), and inherits all operations
of the :term:`algebra of sets`. These are provided in :mod:`~.algebras.sets`.
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

import algebraixlib.algebras.relations as _relations
import algebraixlib.algebras.sets as _sets
import algebraixlib.mathobjects as _mo
import algebraixlib.extension as _extension
import algebraixlib.structure as _structure
import algebraixlib.undef as _undef

from ..cache_status import CacheStatus

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
                return _undef.make_or_raise_undef2(clan)
        else:
            assert is_member_or_undef(clan)
            if clan is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.unary_extend(clan, _functools.partial(
            _relations.transpose, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_clan(CacheStatus.IS)
            result.cache_absolute(clan.cached_absolute)
            result.cache_functional(clan.cached_right_functional)
            result.cache_right_functional(clan.cached_functional)
            result.cache_reflexive(clan.cached_reflexive)
            result.cache_symmetric(clan.cached_symmetric)
            result.cache_transitive(clan.cached_transitive)
            result.cache_regular(clan.cached_right_regular)
            result.cache_right_regular(clan.cached_regular)
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
                return _undef.make_or_raise_undef2(clan1)
            if not is_member(clan2):
                return _undef.make_or_raise_undef2(clan2)
        else:
            assert is_member_or_undef(clan1)
            assert is_member_or_undef(clan2)
            if clan1 is _undef.Undef() or clan2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.binary_extend(clan1, clan2, _functools.partial(
            _relations.compose, _checked=False), _checked=False).cache_clan(CacheStatus.IS)
        if not result.is_empty:
            result.cache_clan(CacheStatus.IS)
            if clan1.cached_is_absolute and clan2.cached_is_absolute:
                result.cache_absolute(CacheStatus.IS)
            if clan1.cached_is_functional and clan2.cached_is_functional:
                result.cache_functional(CacheStatus.IS)
            if clan1.cached_is_right_functional and clan2.cached_is_right_functional:
                result.cache_right_functional(CacheStatus.IS)
        return result

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
                return _undef.make_or_raise_undef2(clan1)
            if not is_member(clan2):
                return _undef.make_or_raise_undef2(clan2)
        else:
            assert is_member_or_undef(clan1)
            assert is_member_or_undef(clan2)
            if clan1 is _undef.Undef() or clan2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.binary_extend(clan1, clan2, _functools.partial(
            _sets.union, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_clan(CacheStatus.IS)
            if clan1.cached_is_not_functional or clan2.cached_is_not_functional:
                result.cache_functional(CacheStatus.IS_NOT)
            if clan1.cached_is_not_right_functional or clan2.cached_is_not_right_functional:
                result.cache_right_functional(CacheStatus.IS_NOT)
        return result

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
                return _undef.make_or_raise_undef2(clan1)
            if not is_member(clan2):
                return _undef.make_or_raise_undef2(clan2)
        else:
            assert is_member_or_undef(clan1)
            assert is_member_or_undef(clan2)
            if clan1 is _undef.Undef() or clan2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.binary_extend(clan1, clan2, _functools.partial(
            _relations.functional_union, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_clan(CacheStatus.IS)
            result.cache_functional(CacheStatus.IS)
            if clan1.cached_is_not_right_functional or clan2.cached_is_not_right_functional:
                result.cache_right_functional(CacheStatus.IS_NOT)
        return result

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
                return _undef.make_or_raise_undef2(lhs)
            if not is_member(rhs):
                return _undef.make_or_raise_undef2(rhs)
        else:
            assert is_member_or_undef(lhs)
            assert is_member_or_undef(rhs)
            if lhs is _undef.Undef() or rhs is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        cfu = cross_functional_union(lhs, rhs, _checked=False)
        lhs_rest = _mo.Set(
            lhs_elem for lhs_elem in lhs
            if cross_functional_union(_mo.Set(lhs_elem, direct_load=True), rhs).is_empty)
        result = _sets.union(cfu, lhs_rest, _checked=False)
        if not result.is_empty:
            result.cache_clan(CacheStatus.IS)
            if lhs.cached_is_functional:
                result.cache_functional(CacheStatus.IS)
            if lhs.cached_is_not_right_functional or rhs.cached_is_not_right_functional:
                result.cache_right_functional(CacheStatus.IS_NOT)
            if not rhs.is_empty and not lhs_rest.is_empty:
                result.cache_regular(CacheStatus.IS_NOT)
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
                return _undef.make_or_raise_undef2(clan1)
            if not is_member(clan2):
                return _undef.make_or_raise_undef2(clan2)
        else:
            assert is_member_or_undef(clan1)
            assert is_member_or_undef(clan2)
            if clan1 is _undef.Undef() or clan2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.binary_extend(clan1, clan2, _functools.partial(
            _relations.right_functional_union, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_clan(CacheStatus.IS)
            result.cache_right_functional(CacheStatus.IS)
            if clan1.cached_is_not_functional or clan2.cached_is_not_functional:
                result.cache_functional(CacheStatus.IS_NOT)
        return result

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
                return _undef.make_or_raise_undef2(clan1)
            if not is_member(clan2):
                return _undef.make_or_raise_undef2(clan2)
        else:
            assert is_member_or_undef(clan1)
            assert is_member_or_undef(clan2)
            if clan1 is _undef.Undef() or clan2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.binary_extend(clan1, clan2, _functools.partial(
            _sets.intersect, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_clan(CacheStatus.IS)
            if clan1.cached_is_functional or clan2.cached_is_functional:
                result.cache_functional(CacheStatus.IS)
            if clan1.cached_is_right_functional or clan2.cached_is_right_functional:
                result.cache_right_functional(CacheStatus.IS)
        return result

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
                return _undef.make_or_raise_undef2(clan1)
            if not is_member(clan2):
                return _undef.make_or_raise_undef2(clan2)
        else:
            assert is_member_or_undef(clan1)
            assert is_member_or_undef(clan2)
            if clan1 is _undef.Undef() or clan2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.binary_extend(clan1, clan2, _functools.partial(
            _sets.substrict, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_clan(CacheStatus.IS)
            if clan1.cached_is_functional or clan2.cached_is_functional:
                result.cache_functional(CacheStatus.IS)
            if clan1.cached_is_right_functional or clan2.cached_is_right_functional:
                result.cache_right_functional(CacheStatus.IS)
            if clan1.cached_is_reflexive:
                result.cache_reflexive(CacheStatus.IS)
            if clan1.cached_is_symmetric:
                result.cache_symmetric(CacheStatus.IS)
            if clan1.cached_is_transitive:
                result.cache_transitive(CacheStatus.IS)
            if clan1.cached_is_regular:
                result.cache_regular(CacheStatus.IS)
            if clan1.cached_is_right_regular:
                result.cache_right_regular(CacheStatus.IS)
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
                return _undef.make_or_raise_undef2(clan1)
            if not is_member(clan2):
                return _undef.make_or_raise_undef2(clan2)
        else:
            assert is_member_or_undef(clan1)
            assert is_member_or_undef(clan2)
            if clan1 is _undef.Undef() or clan2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.binary_extend(clan1, clan2, _functools.partial(
            _sets.superstrict, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_clan(CacheStatus.IS)
            if clan1.cached_is_functional:
                result.cache_functional(CacheStatus.IS)
            if clan1.cached_is_right_functional:
                result.cache_right_functional(CacheStatus.IS)
            if clan1.cached_is_reflexive:
                result.cache_reflexive(CacheStatus.IS)
            if clan1.cached_is_symmetric:
                result.cache_symmetric(CacheStatus.IS)
            if clan1.cached_is_transitive:
                result.cache_transitive(CacheStatus.IS)
            if clan1.cached_is_regular:
                result.cache_regular(CacheStatus.IS)
            if clan1.cached_is_right_regular:
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

# pylint: enable=invalid-name

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

     :return: ``True`` if ``obj`` is a :term:`clan`, ``False`` if not.

    .. note:: This function may call :meth:`~.MathObject.get_ground_set` on ``obj``. The result of
        this operation is cached.
    """
    if obj.cached_clan == CacheStatus.UNKNOWN:
        is_clan = obj.get_ground_set().is_subset(get_ground_set())
        obj.cache_clan(CacheStatus.from_bool(is_clan))
    return obj.cached_is_clan


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
    if obj.cached_is_not_clan:
        # If known to not be a clan, it's also not an absolute clan. No further caching.
        return False
    # The `or` clause in this `if` statement is a safety thing. It should never hit.
    if obj.cached_absolute == CacheStatus.UNKNOWN or obj.cached_clan == CacheStatus.UNKNOWN:
        # The 'absolute' state has not yet been cached. Determine whether obj is an absolute clan.
        is_absolute_clan = obj.get_ground_set().is_subset(get_absolute_ground_set())
        if obj.cached_clan == CacheStatus.UNKNOWN:
            if is_absolute_clan:
                # If it is an absolute clan, it is also a clan.
                obj.cache_clan(CacheStatus.IS)
            else:
                # If it is not an absolute clan, it may still be a clan.
                is_clan = is_member(obj)
                if not is_clan:
                    # If it is neither an absolute clan nor a clan, exit. (That it is not a clan
                    # has already been cached in is_member().)
                    return False
        # At this point, cached_clan == IS. Cache whether this is an absolute clan.
        assert obj.cached_is_clan
        obj.cache_absolute(CacheStatus.from_bool(is_absolute_clan))
    # At this point, cached_clan == IS. Return whether it is an absolute clan.
    return obj.cached_is_absolute


# --------------------------------------------------------------------------------------------------
# Related operations, not formally part of the algebra.

def get_lefts(clan: 'PP(M x M)', _checked=True) -> 'P( M )':
    r"""Return the set of the left components of all couplets in all relations in ``clan``.

    :return: The :term:`union` of the :term:`left set`\s of all :term:`relation`\s in ``clan`` or
        `Undef()` if ``clan`` is not a :term:`clan`.
    """
    if _checked:
        if not is_member(clan):
            return _undef.make_or_raise_undef2(clan)
    else:
        assert is_member_or_undef(clan)
        if clan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if clan.is_empty:
        # The left set of an empty set is the empty set
        return clan
    clan_itr = iter(clan)
    left_set = _relations.get_lefts(next(clan_itr), _checked=False)
    for rel in clan_itr:
        left_set = _sets.union(
            _relations.get_lefts(rel, _checked=False), left_set, _checked=False)
    if not left_set.is_empty:
        if clan.cached_is_absolute:
            left_set.cache_absolute(CacheStatus.IS)
    return left_set


def get_rights(clan: 'PP(M x M)', _checked=True) -> "P( M )":
    r"""Return the set of the right components of all couplets in all relations in ``clan``.

    :return: The :term:`union` of the :term:`right set`\s of all :term:`relation`\s in ``clan`` or
        `Undef()` if ``clan`` is not a :term:`clan`.
    """
    if _checked:
        if not is_member(clan):
            return _undef.make_or_raise_undef2(clan)
    else:
        assert is_member_or_undef(clan)
        if clan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if clan.is_empty:
        # The right set of an empty set is the empty set
        return clan
    clan_itr = iter(clan)
    right_set = _relations.get_rights(next(clan_itr), _checked=False)
    for rel in clan_itr:
        right_set = _sets.union(
            _relations.get_rights(rel, _checked=False), right_set, _checked=False)
    if not right_set.is_empty:
        if clan.cached_is_absolute:
            right_set.cache_absolute(CacheStatus.IS)
    return right_set


def is_functional(clan, _checked=True) -> bool:
    """Return whether ``clan`` is functional.

    :return: ``True`` if every :term:`relation` in ``clan`` is :term:`functional` (is a
        :term:`function`), ``False`` if not, or `Undef()` if ``clan`` is not a :term:`clan`.
    """
    if _checked:
        if not is_member(clan):
            return _undef.make_or_raise_undef2(clan)
    else:
        assert is_member_or_undef(clan)
        if clan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if clan.cached_functional == CacheStatus.UNKNOWN:
        # The empty set is already handled in Set().__init__ via flags initialization.
        functional = all(_relations.is_functional(rel, _checked=False) for rel in clan)
        clan.cache_functional(CacheStatus.from_bool(functional))
    return clan.cached_is_functional


def is_right_functional(clan, _checked=True) -> bool:
    """Return whether ``clan`` is right-functional.

    :return: ``True`` if every :term:`relation` in ``clan`` is :term:`right-functional`, ``False``
        if not, or `Undef()` if ``clan`` is not a :term:`clan`.
    """
    if _checked:
        if not is_member(clan):
            return _undef.make_or_raise_undef2(clan)
    else:
        assert is_member_or_undef(clan)
        if clan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if clan.cached_right_functional == CacheStatus.UNKNOWN:
        # The empty set is already handled in Set().__init__ via flags initialization.
        right_functional = all(_relations.is_right_functional(rel, _checked=False) for rel in clan)
        clan.cache_right_functional(CacheStatus.from_bool(right_functional))
    return clan.cached_is_right_functional


def is_regular(clan, _checked=True) -> bool:
    """Return whether ``clan`` is (left-)regular.

    :return: ``True`` if ``clan`` is :term:`regular`, ``False`` if not, or `Undef()` if ``clan``
        is not a :term:`clan`.
    """
    if _checked:
        if not is_member(clan):
            return _undef.make_or_raise_undef2(clan)
    else:
        assert is_member_or_undef(clan)
        if clan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if clan.cached_regular == CacheStatus.UNKNOWN:
        # The empty set is already handled in Set().__init__ via flags initialization.
        if clan.cached_is_not_functional:
            clan.cache_regular(CacheStatus.IS_NOT)
            return False
        itr = iter(clan)
        rel = next(itr)
        if not _relations.is_functional(rel):
            clan.cache_regular(CacheStatus.IS_NOT)
            return False
        left_set = rel.get_left_set()
        regular = all(
            _relations.is_functional(rel) and left_set == rel.get_left_set() for rel in itr)
        clan.cache_regular(CacheStatus.from_bool(regular))
    return clan.cached_is_regular


def is_right_regular(clan, _checked=True) -> bool:
    """Return whether ``clan`` is right-regular.

    :return: ``True`` if ``clan`` is :term:`right-regular`, ``False`` if not, or `Undef()` if
        ``clan`` is not a :term:`clan`.
    """
    if _checked:
        if not is_member(clan):
            return _undef.make_or_raise_undef2(clan)
    else:
        assert is_member_or_undef(clan)
        if clan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if clan.cached_right_regular == CacheStatus.UNKNOWN:
        # The empty set is already handled in Set().__init__ via flags initialization.
        if clan.cached_is_not_right_functional:
            clan.cache_right_regular(CacheStatus.IS_NOT)
            return False
        itr = iter(clan)
        rel = next(itr)
        if not _relations.is_right_functional(rel):
            clan.cache_right_regular(CacheStatus.IS_NOT)
            return False
        right_set = rel.get_right_set()
        right_regular = all(
            _relations.is_right_functional(rel) and right_set == rel.get_right_set() for rel in itr)
        clan.cache_right_regular(CacheStatus.from_bool(right_regular))
    return clan.cached_is_right_regular


def is_reflexive(clan, _checked=True) -> bool:
    """Return whether ``clan`` is reflexive.

    :return: ``True`` if every :term:`relation` in ``clan`` is :term:`reflexive`, ``False`` if
        not, or `Undef()` if ``clan`` is not a :term:`clan`.
    """
    if _checked:
        if not is_member(clan):
            return _undef.make_or_raise_undef2(clan)
    else:
        assert is_member_or_undef(clan)
        if clan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if clan.cached_reflexive == CacheStatus.UNKNOWN:
        # The empty set is already handled in Set().__init__ via flags initialization.
        reflexive = all(_relations.is_reflexive(rel, _checked=False) for rel in clan)
        clan.cache_reflexive(CacheStatus.from_bool(reflexive))
    return clan.cached_reflexive == CacheStatus.IS


def is_symmetric(clan, _checked=True) -> bool:
    """Return whether ``clan`` is symmetric.

    :return: ``True`` if every :term:`relation` in ``clan`` is :term:`symmetric`, ``False`` if
        not, or `Undef()` if ``clan`` is not a :term:`clan`.
    """
    if _checked:
        if not is_member(clan):
            return _undef.make_or_raise_undef2(clan)
    else:
        assert is_member_or_undef(clan)
        if clan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if clan.cached_symmetric == CacheStatus.UNKNOWN:
        # The empty set is already handled in Set().__init__ via flags initialization.
        symmetric = all(_relations.is_symmetric(rel, _checked=False) for rel in clan)
        clan.cache_symmetric(CacheStatus.from_bool(symmetric))
    return clan.cached_symmetric == CacheStatus.IS


def is_transitive(clan, _checked=True) -> bool:
    """Return whether ``clan`` is transitive.

    :return: ``True`` if every :term:`relation` in ``clan`` is :term:`transitive`, ``False`` if
        not, or `Undef()` if ``clan`` is not a :term:`clan`.
    """
    if _checked:
        if not is_member(clan):
            return _undef.make_or_raise_undef2(clan)
    else:
        assert is_member_or_undef(clan)
        if clan is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if clan.cached_transitive == CacheStatus.UNKNOWN:
        # The empty set is already handled in Set().__init__ via flags initialization.
        transitive = all(_relations.is_transitive(rel, _checked=False) for rel in clan)
        clan.cache_transitive(CacheStatus.from_bool(transitive))
    return clan.cached_transitive == CacheStatus.IS


def project(clan: 'PP(M x M)', *lefts) -> 'PP(M x M)':
    r"""Return a clan that contains only the couplets with lefts from ``clan`` that match ``lefts``.

    :param clan: The source data. Must be a :term:`clan`.
    :param lefts: The names of the :term:`left component`\s to match. (If you want to pass in an
        iterable, you need to prefix it with an asterisk ``*``.)
    :return: The :term:`projection` of ``clan`` (a clan that contains only :term:`couplet`\s with
        left components as indicated by ``lefts``), or `Undef()` if ``clan`` is not a clan.
    """
    if not is_member(clan):
        return _undef.make_or_raise_undef2(clan)
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
    clan = _mo.Set(
        (_mo.Set(_mo.Couplet(left_mo, _mo.auto_convert(right), direct_load=True), direct_load=True)
            .cache_relation(CacheStatus.IS)
            .cache_functional(CacheStatus.IS).cache_right_functional(CacheStatus.IS)
            for right in values),
        direct_load=True)
    clan.cache_clan(CacheStatus.IS)
    clan.cache_functional(CacheStatus.IS).cache_right_functional(CacheStatus.IS)
    clan.cache_regular(CacheStatus.IS).cache_right_regular(CacheStatus.IS)
    return clan


def from_dict(dict1: dict) -> 'PP(M x M)':
    r"""Return a :term:`clan` with a single :term:`relation` where the :term:`couplet`\s are the
    elements of ``dict1``."""
    rel = _mo.Set((_mo.Couplet(left, right) for left, right in dict1.items()), direct_load=True)
    rel.cache_relation(CacheStatus.IS)
    rel.cache_functional(CacheStatus.IS)
    clan = _mo.Set(rel, direct_load=True)
    clan.cache_clan(CacheStatus.IS)
    clan.cache_functional(CacheStatus.IS)
    clan.cache_regular(CacheStatus.IS)
    return clan


def diag(*args, _checked=True) -> 'PP(M x M)':
    """Return a clan diagonal of the arguments.

    :param args: Pass in the elements from which the :term:`clan diagonal` is formed. (If you want
        to pass in an iterable, you need to prefix it with an asterisk ``*``.)
    """
    rels = _relations.diag(*args, _checked=_checked)
    if rels is _undef.Undef():
        return _undef.make_or_raise_undef(2)
    clan = _mo.Set(rels, direct_load=True)
    clan.cache_clan(CacheStatus.IS)
    clan.cache_functional(CacheStatus.IS).cache_right_functional(CacheStatus.IS)
    clan.cache_reflexive(CacheStatus.IS).cache_symmetric(CacheStatus.IS)
    clan.cache_regular(CacheStatus.IS).cache_right_regular(CacheStatus.IS)
    return clan


def defined_at(clan: 'PP(M x M)', left: '( M )', _checked=True):
    r"""Return the :term:`relation`\s of ``clan`` that are defined for ``left``."""
    if not is_member(clan):
        return _undef.make_or_raise_undef(2)
    if left is _undef.Undef():
        return _undef.make_or_raise_undef(2)
    result = _extension.unary_extend(
        clan, _functools.partial(_relations.defined_at, left=left, _checked=_checked),
        _checked=_checked)
    if result is _undef.Undef() or not result:
        return _undef.make_or_raise_undef2(result)
    result.cache_clan(CacheStatus.IS)
    if not result.is_empty:
        if clan.cached_is_functional:
            result.cache_functional(CacheStatus.IS)
        if clan.cached_is_right_functional:
            result.cache_right_functional(CacheStatus.IS)
        if clan.cached_is_regular:
            result.cache_regular(CacheStatus.IS)
        if clan.cached_is_right_regular:
            result.cache_right_regular(CacheStatus.IS)
    return result
