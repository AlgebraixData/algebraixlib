"""This module contains the :term:`algebra of clans`."""

# $Id: clans.py 22614 2015-07-15 18:14:53Z gfiedler $
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
    """Provide the operations and relations that are members of the :term:`algebra of clans`.

    This class contains only static member functions. Its main purpose is to provide a namespace for
    and highlight the operations and relations that belong to the algebra of clans. All member
    functions are also available at the enclosing module scope.
    """
    # --------------------------------------------------------------------------------------------------
    # Unary algebra operations.

    @staticmethod
    def transpose(clan: 'PP(M x M)', _checked=True) -> 'PP(M x M)':
        """Return the :term:`transposition` of the :term:`clan` ``clan``.

        :return: The :term:`unary extension` of :term:`transposition` from the :term:`algebra of
            relations` to the :term:`algebra of clans`, applied to ``clan``, or `Undef()` if
            ``clan`` is not a :term:`clan`.
        """
        if _checked:
            if not is_member(clan):
                return _make_or_raise_undef()
        else:
            assert is_member(clan)
        result = _extension.unary_extend(clan, partial(_relations.transpose, _checked=False),
                                         _checked=False).cache_is_clan(True)
        if not result.is_empty:
            if clan.cached_is_left_functional or clan.cached_is_not_left_functional:
                result.cache_is_right_functional(clan.cached_is_left_functional)
            if clan.cached_is_right_functional or clan.cached_is_not_right_functional:
                result.cache_is_left_functional(clan.cached_is_right_functional)
        return result

    # --------------------------------------------------------------------------------------------------
    # Binary algebra operations.

    @staticmethod
    def compose(clan1: 'PP(M x M)', clan2: 'PP(M x M)', _checked=True) -> 'PP(M x M)':
        r"""Return the :term:`composition` of ``clan1`` with ``clan2``.

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
        return _extension.binary_extend(clan1, clan2, partial(_relations.compose, _checked=False),
                                        _checked=False).cache_is_clan(True)

    @staticmethod
    def cross_union(clan1: 'PP(M x M)', clan2: 'PP(M x M)', _checked=True) -> 'PP(M x M)':
        r"""Return the :term:`cross-union` of ``clan1`` and ``clan2``.

        :return: The :term:`binary extension` of :term:`union` from the :term:`algebra of relations`
            (which inherits it from the :term:`algebra of sets`) to the :term:`algebra of clans`
            applied to ``clan1`` and ``clan2``, or `Undef()` if ``clan1`` or ``clan2`` are not
            :term:`clan`\s.
        """
        if _checked:
            if not is_member(clan1):
                return _make_or_raise_undef()
            if not is_member(clan2):
                return _make_or_raise_undef()
        else:
            assert is_member(clan1)
            assert is_member(clan2)
        return _extension.binary_extend(clan1, clan2, partial(_sets.union, _checked=False),
                                        _checked=False).cache_is_clan(True)

    @staticmethod
    def functional_cross_union(clan1: 'PP(M x M)', clan2: 'PP(M x M)',
                               _checked=True) -> 'PP(M x M)':
        r"""Return the :term:`left-functional cross-union` of ``clan1`` and ``clan2``.

        :return: The :term:`binary extension` of the :term:`left-functional union` from the
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
        return _extension.binary_extend(clan1, clan2,
                                        partial(_relations.functional_union, _checked=False),
                                        _checked=False).cache_is_clan(True)

    @staticmethod
    def lhs_functional_cross_union(lhs: 'PP( MxM )', rhs: 'PP( MxM )', _checked=True):
        """This data manipulations preforms a left functional cross union, then unions the left hand
        side elements that were not cross unioned.

        :param lhs: The priority left hand clan for this operation
        :param rhs: The right hand clan to preform the cross union with
        :return: PP(MxM) resulting math object
        """
        if _checked:
            if not is_member(lhs):
                return _make_or_raise_undef()
            if not is_member(rhs):
                return _make_or_raise_undef()
        else:
            assert is_member(lhs)
            assert is_member(rhs)

        def _functional_cross_union(clan1: 'PP(M x M)', clan2: 'PP(M x M)') -> 'PP(M x M)':
            """Return the :term:`left-functional cross-union` of ``clan1`` and ``clan2``."""
            assert is_member(clan1)
            assert is_member(clan2)

            return _extension.binary_extend(
                clan1, clan2, partial(_relations.functional_union, _checked=False),
                _checked=False).cache_is_clan(True)

        return _sets.union(
            _functional_cross_union(lhs, rhs),
            _mo.Set(lhs_elem for lhs_elem in lhs if _functional_cross_union(
                _mo.Set(lhs_elem, direct_load=True), rhs).is_empty), _checked=False)

    @staticmethod
    def right_functional_cross_union(clan1: 'PP(M x M)', clan2: 'PP(M x M)',
                                     _checked=True) -> 'PP(M x M)':
        r"""Return the :term:`right-functional cross-union` of ``clan1`` and ``clan2``.

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
        return _extension.binary_extend(clan1, clan2,
                                        partial(_relations.right_functional_union,
                                                _checked=False), _checked=False).cache_is_clan(True)

    @staticmethod
    def cross_intersect(clan1: 'PP(M x M)', clan2: 'PP(M x M)', _checked=True) -> 'PP(M x M)':
        r"""Return the :term:`cross-intersection` of ``clan1`` and ``clan2``.

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
        return _extension.binary_extend(clan1, clan2, partial(_sets.intersect, _checked=False),
                                        _checked=False).cache_is_clan(True)

    @staticmethod
    def substrict(clan1: 'PP(M x M)', clan2: 'PP(M x M)', _checked=True) -> 'PP(M x M)':
        r"""Return the :term:`binary extension` of :term:`substriction` of ``clan1`` and ``clan2``.

        :return: The :term:`binary extension` of :term:`substriction` from the :term:`algebra of
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
        return _extension.binary_extend(clan1, clan2, partial(_sets.substrict, _checked=False),
                                        _checked=False).cache_is_clan(True)

    @staticmethod
    def superstrict(clan1: 'PP(M x M)', clan2: 'PP(M x M)', _checked=True) -> 'PP(M x M)':
        r"""Return a Set of every element of clan1 that is a superset of any element of clan2.

        :return: The :term:`binary extension` of :term:`superstriction` from the :term:`algebra of
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
        return _extension.binary_extend(clan1, clan2, partial(
            _sets.superstrict, _checked=False)).cache_is_clan(True)

transpose = Algebra.transpose
compose = Algebra.compose
cross_union = Algebra.cross_union
functional_cross_union = Algebra.functional_cross_union
lhs_functional_cross_union = Algebra.lhs_functional_cross_union
right_functional_cross_union = Algebra.right_functional_cross_union
cross_intersect = Algebra.cross_intersect
substrict = Algebra.substrict
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
    """Return ``True`` if ``obj`` is a member of the :term:`ground set` of this :term:`algebra`.

    .. note:: This function calls :meth:`~.MathObject.get_ground_set` on ``obj``.
    """
    _mo.raise_if_not_mathobject(obj)
    if not obj.cached_is_clan and not obj.cached_is_not_clan:
        obj.cache_is_clan(obj.get_ground_set().is_subset(get_ground_set()))
    return obj.cached_is_clan


def is_absolute_member(obj: _mo.MathObject) -> bool:
    """Return ``True`` if ``obj`` is a member of the :term:`absolute ground set` of this algebra.

     :return: ``True`` if ``obj`` is an :term:`absolute clan`.

    .. note:: This function calls :meth:`~.MathObject.get_ground_set` on ``obj``.
    """
    _mo.raise_if_not_mathobject(obj)
    return obj.get_ground_set().is_subset(get_absolute_ground_set())


# --------------------------------------------------------------------------------------------------
# Utility operations that are not formally part of the algebra.


def get_lefts(clan: 'PP(M x M)', _checked=True) -> 'P( M )':
    r"""Return the :term:`left set` of this :term:`clan`.

    :return: The :term:`union` of the :term:`left set`\s of all :term:`relation`\s in the
        :term:`clan` or `Undef()` if ``clan`` is not a clan.
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
    if not left_set.is_empty:
        left_set.cache_is_relation(False).cache_is_clan(False)
    return left_set


def get_rights(clan: 'PP(M x M)', _checked=True) -> "P( M )":
    r"""Return the :term:`right set` of this :term:`clan`.

    :return: The :term:`union` of the :term:`right set`\s of all :term:`relation`\s in the
        :term:`clan` or `Undef()` if ``clan`` is not a clan.
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
    if not right_set.is_empty:
        right_set.cache_is_relation(False).cache_is_clan(False)
    return right_set


def is_left_regular(clan, _checked=True) -> bool:
    """Return ``True`` if ``clan`` is :term:`left-regular`.

    :return: ``True`` if ``clan`` is :term:`left-regular` or `Undef()` if ``clan`` is not a
        :term:`clan`.
    """
    if _checked:
        if not is_member(clan):
            return _make_or_raise_undef()
    else:
        assert is_member(clan)

    if not clan.cached_is_left_regular and not clan.cached_is_not_left_regular:
        # NOTE: The empty case is handled in Set().__init__ via flags initialization
        if clan.cached_is_not_left_functional:
            clan.cache_is_left_regular(False)
            return False
        itr = iter(clan)
        rel = next(itr)
        if not rel.is_left_functional():
            clan.cache_is_left_regular(False)
            return False
        left_set = rel.get_left_set()
        regular = all(rel.is_left_functional() and left_set == rel.get_left_set() for rel in itr)
        clan.cache_is_left_regular(regular)
    return clan.cached_is_left_regular


def project(clan: 'PP(M x M)', *lefts) -> 'PP(M x M)':
    r"""Return a :term:`clan` with the :term:`left component`\s from ``clan`` with the values in
    ``lefts``.  See :term:`project`.

    :param clan: The source data. Must be a :term:`clan`.
    :param lefts: The names of the lefts to return. (If you want to pass in an iterable, you need
        to prefix it with a ``*``.)
    :return: A clan with only the lefts as indicated by ``lefts``.
    """
    clan = compose(clan, diag(*lefts))
    return clan


def from_set(left: '( M )', *values: '( M )') -> 'PP(M x M)':
    """Return a clan where all relations contain a single couplet with the same left component.

    :param left: The :term:`left component` of all :term:`couplet`\s in the returned :term:`clan`.
    :param values: The :term:`right component`\s of the couplets in the returned clan.
    :return: A clan where every :term:`relation` consists of a single couplet with a left component
        of ``left`` and a right component from ``values``.
    """
    left_mo = _mo.auto_convert(left)
    clan = _mo.Set((_mo.Set(_mo.Couplet(left_mo, _mo.auto_convert(right), direct_load=True),
                            direct_load=True).cache_is_relation(True)
                    for right in values), direct_load=True).cache_is_clan(True)
    return clan


def from_dict(dict1: dict) -> 'PP(M x M)':
    """Return a :term:`clan` with a single :term:`relation` where the :term:`couplet`\s are the
    elements of ``dict1``."""
    clan = _mo.Set(_mo.Set((_mo.Couplet(left, right) for left, right in dict1.items()),
                           direct_load=True).cache_is_relation(True),
                   direct_load=True).cache_is_clan(True)
    return clan


def diag(*args) -> 'PP(M x M)':
    """Return a 'clan :term:`diagonal`' of the arguments."""
    clan = _mo.Set(_mo.Set((_mo.Couplet(elem, elem) for elem in args),
                           direct_load=True).cache_is_relation(True).cache_is_left_functional(True),
                   direct_load=True).cache_is_clan(True)
    return clan


def defined_at(clan, left):
    """Return the portion of clan where relations in clan are defined for left"""
    clan = _extension.unary_extend(clan, partial(
        _relations.defined_at, left=left)).cache_is_clan(True)
    return clan
