"""This module contains the :term:`algebra of relations` and related functionality."""

# $Id: relations.py 22614 2015-07-15 18:14:53Z gfiedler $
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

import algebraixlib.algebras.couplets as _couplets
import algebraixlib.algebras.sets as _sets
import algebraixlib.mathobjects as _mo
import algebraixlib.extension as _extension
import algebraixlib.structure as _structure
from algebraixlib.undef import make_or_raise_undef as _make_or_raise_undef


# --------------------------------------------------------------------------------------------------

class Algebra:
    """Provide the operations and relations that are members of the :term:`algebra of relations`.

    This class contains only static member functions. Its main purpose is to provide a namespace for
    and highlight the operations and relations that belong to the algebra of relations. All member
    functions are also available at the enclosing module scope.
    """
    # ----------------------------------------------------------------------------------------------
    # Unary algebra operations.

    @staticmethod
    def transpose(rel: 'P(M x M)', _checked=True) -> 'P(M x M)':
        """Return a relation where the left components and right components of all couplets are
        swapped.

        :return: The :term:`unary extension` of :term:`transposition` from the
            :term:`algebra of couplets` to the :term:`algebra of relations`, applied to the
            :term:`relation` ``rel``, or `Undef()` if ``rel`` is not a relation.
        """
        if _checked:
            if not is_member(rel):
                return _make_or_raise_undef()
        else:
            assert is_member(rel)
        return _extension.unary_extend(rel, partial(_couplets.transpose, _checked=False),
                                       _checked=False).cache_is_relation(True)

    # ----------------------------------------------------------------------------------------------
    # Binary algebra operations.

    @staticmethod
    def compose(rel1: 'P(M x M)', rel2: 'P(M x M)', _checked=True) -> 'P(M x M)':
        """Return the composition of ``rel1`` with ``rel2``.

        :return: The :term:`binary extension` of :term:`composition` from the :term:`algebra of
            couplets` to the :term:`algebra of relations`, applied to the :term:`relation`\s
            ``rel1`` and ``rel2``, or `Undef()` if ``rel1`` or ``rel2`` are not relations.
        """
        if _checked:
            if not is_member(rel1):
                return _make_or_raise_undef()
            if not is_member(rel2):
                return _make_or_raise_undef()
        else:
            assert is_member(rel1)
            assert is_member(rel2)
        return _extension.binary_extend(rel1, rel2, partial(
            _couplets.compose, _checked=False), _checked=False).cache_is_relation(True)

    @staticmethod
    def functional_union(rel1: 'P(M x M)', rel2: 'P(M x M)', _checked=True) -> 'P(M x M)':
        """Return the union of ``rel1`` and ``rel2`` if it is a function, otherwise `Undef()`.

        :return: The :term:`left-functional union` of the :term:`relation`\s ``rel1`` and ``rel2``;
            that is, the :term:`union` if the result is :term:`left-functional`, otherwise
            `Undef()`. Also return `Undef()` if ``rel1`` or ``rel2`` are not relations.
        """
        if _checked:
            if not is_member(rel1):
                return _make_or_raise_undef()
            if not is_member(rel2):
                return _make_or_raise_undef()
        else:
            assert is_member(rel1)
            assert is_member(rel2)
        rel_union = _sets.union(rel1, rel2, _checked=False).cache_is_relation(True)
        if not is_left_functional(rel_union, _checked=False):
            return _make_or_raise_undef(2)
        return rel_union

    @staticmethod
    def right_functional_union(rel1: 'P(M x M)', rel2: 'P(M x M)', _checked=True) -> 'P(M x M)':
        """Return the union of ``rel1`` and ``rel2`` if it is right-functional, otherwise
        `Undef()`.

        :return: The :term:`right-functional union` of the :term:`relation`\s ``rel1`` and
            ``rel2``; that is, the :term:`union` if the result is :term:`right-functional`,
            otherwise `Undef()`. Also return `Undef()` if ``rel1`` or ``rel2`` are not relations.
        """
        if _checked:
            if not is_member(rel1):
                return _make_or_raise_undef()
            if not is_member(rel2):
                return _make_or_raise_undef()
        else:
            assert is_member(rel1)
            assert is_member(rel2)
        rel_union = _sets.union(rel1, rel2, _checked=False).cache_is_relation(True)
        if not is_right_functional(rel_union, _checked=False):
            return _make_or_raise_undef(2)
        return rel_union


# For convenience, make the members of class Algebra (they are all static functions) available at
# the module level.

#: Convenience redirection to `Algebra.transpose`.
transpose = Algebra.transpose
#: Convenience redirection to `Algebra.compose`.
compose = Algebra.compose
#: Convenience redirection to `Algebra.functional_union`.
functional_union = Algebra.functional_union
#: Convenience redirection to `Algebra.right_functional_union`.
right_functional_union = Algebra.right_functional_union


# --------------------------------------------------------------------------------------------------
# Metadata functions.

def get_name() -> str:
    """Return the name and :term:`ground set` of this :term:`algebra` in string form."""
    return 'Relations(M): {ground_set}'.format(ground_set=str(get_ground_set()))


def get_ground_set() -> _structure.Structure:
    """Return the :term:`ground set` of this :term:`algebra`."""
    return _structure.PowerSet(_couplets.get_ground_set())


def get_absolute_ground_set() -> _structure.Structure:
    """Return the :term:`absolute ground set` of this :term:`algebra`."""
    return _structure.PowerSet(_couplets.get_absolute_ground_set())


def is_member(obj: _mo.MathObject) -> bool:
    """Return ``True`` if ``obj`` is a member of the :term:`ground set` of this :term:`algebra`.

    .. note:: This function may call :meth:`~.MathObject.get_ground_set` on ``obj``. The result
        of this operation is cached.
    """
    _mo.raise_if_not_mathobject(obj)
    if not obj.cached_is_relation and not obj.cached_is_not_relation:
        obj.cache_is_relation(obj.get_ground_set().is_subset(get_ground_set()))
    return obj.cached_is_relation


def is_absolute_member(obj: _mo.MathObject) -> bool:
    """Return ``True`` if ``obj`` is a member of the :term:`absolute ground set` of this algebra.

     :return: ``True`` if ``obj`` is an :term:`absolute relation`.

    .. note:: This function calls :meth:`~.MathObject.get_ground_set` on ``obj``."""
    _mo.raise_if_not_mathobject(obj)
    return obj.get_ground_set().is_subset(get_absolute_ground_set())


# --------------------------------------------------------------------------------------------------
# Related operations, not formally part of the algebra.

def get_lefts(rel: 'P(M x M)', _checked=True) -> 'P( M )':
    """Return the set of the left components of all couplets in the relation ``rel``.

    :return: The :term:`left set` of the :term:`relation` ``rel`` or `Undef()` if ``rel`` is not a
        :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _make_or_raise_undef()
    else:
        assert is_member(rel)
    return _mo.Set((e.left for e in rel), direct_load=True)


def get_rights(rel: 'P(M x M)', _checked=True) -> 'P( M )':
    """Return the set of the right components of all couplets in the relation ``rel``.

    :return: The :term:`right set` of the :term:`relation` ``rel`` or `Undef()` if ``rel`` is not a
        :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _make_or_raise_undef()
    else:
        assert is_member(rel)
    return _mo.Set((e.right for e in rel), direct_load=True)


def get_right(rel: 'P(M x M)', left: '( M )', _checked=True) -> '( M )':
    """Return the single :term:`right component` associated with the :term:`left component` ``left``.

    In general, use with :term:`left-functional` :term:`relation`\s; that is, relations where
    all left components appear at most once.

    :return: The single :term:`right component` associated with the :term:`left component`
        ``left``, or `Undef()` if there is not exactly one element with the left component
        ``left`` in ``rel`` or ``rel`` is not a :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _make_or_raise_undef()
    else:
        assert is_member(rel)
    left = _mo.auto_convert(left)
    result = None
    for elem in rel:
        assert isinstance(elem, _mo.Couplet)
        if elem.left == left:
            if result is not None:
                return _make_or_raise_undef()  # Early Undef() exit if more than one found.
            result = elem.right
    if result is None:
        return _make_or_raise_undef()  # Undef() exit if none found.
    return result


def get_left(rel: 'P(M x M)', right: '( M )', _checked=True) -> '( M )':
    """Return the single :term:`left component` associated with the :term:`right component` ``right``.

    In general, use with :term:`right-functional` :term:`relation`\s; that is, relations
    where all right components appear at most once.

    :return: The single :term:`left component` associated with the :term:`right component`
        ``right``, or `Undef()` if there is not exactly one element with the right component
        ``right`` in ``rel`` or ``rel`` is not a :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _make_or_raise_undef()
    else:
        assert is_member(rel)
    right = _mo.auto_convert(right)
    result = None
    for elem in rel:
        assert isinstance(elem, _mo.Couplet)
        if elem.right == right:
            if result is not None:
                return _make_or_raise_undef()  # Early Undef() exit if more than one found.
            result = elem.left
    if result is None:
        return _make_or_raise_undef()  # Undef() exit if none found.
    return result


def is_left_functional(rel, _checked=True) -> bool:
    """Return ``True`` if ``rel`` is :term:`left-functional`.

    :return: ``True`` if ``rel`` is :term:`left-functional` or `Undef()` if ``rel`` is not a
        :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _make_or_raise_undef()
    else:
        assert is_member(rel)
    if not rel.cached_is_left_functional and not rel.cached_is_not_left_functional:
        left_set = get_lefts(rel, _checked=False)
        rel.cache_is_left_functional(left_set.cardinality == rel.cardinality)
    return rel.cached_is_left_functional


def is_right_functional(rel, _checked=True) -> bool:
    """Return ``True`` if ``rel`` is :term:`right-functional`.

    :return: ``True`` if ``rel`` is :term:`right-functional` or `Undef()` if ``rel`` is not a
        :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _make_or_raise_undef()
    else:
        assert is_member(rel)
    if not rel.cached_is_right_functional and not rel.cached_is_not_right_functional:
        right_set = get_rights(rel, _checked=False)
        rel.cache_is_right_functional(right_set.cardinality == rel.cardinality)
    return rel.cached_is_right_functional


def is_reflexive(rel, _checked=True) -> bool:
    """Return ``True`` if ``rel`` is :term:`reflexive`.

    :return: ``True`` if ``rel`` is :term:`reflexive` or `Undef()` if ``rel`` is not a
        :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _make_or_raise_undef()
    else:
        assert is_member(rel)
    if not rel.cached_is_reflexive and not rel.cached_is_not_reflexive:
        reflexive = all(couplet.is_reflexive() for couplet in rel)
        rel.cache_is_reflexive(reflexive)
    return rel.cached_is_reflexive


def is_symmetric(rel, _checked=True) -> bool:
    """Return ``True`` if ``rel`` is :term:`symmetric`.

    :return: ``True`` if ``rel`` is :term:`symmetric` or `Undef()` if ``rel`` is not a
        :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _make_or_raise_undef()
    else:
        assert is_member(rel)
    if not rel.cached_is_symmetric and not rel.cached_is_not_symmetric:
        symmetric = all(rel.has_element(
            _couplets.transpose(couplet, _checked=False)) for couplet in rel)
        rel.cache_is_symmetric(symmetric)
    return rel.cached_is_symmetric


def is_transitive(rel, _checked=True) -> bool:
    """Return ``True`` if ``rel`` is :term:`transitive`.

    :return: ``True`` if ``rel`` is :term:`transitive` or `Undef()` if ``rel`` is not a
        :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _make_or_raise_undef()
    else:
        assert is_member(rel)
    if not rel.cached_is_transitive and not rel.cached_is_not_transitive:
        transitive = True
        for couplet1 in rel:
            for couplet2 in rel:
                if couplet1.left == couplet2.right:
                    if not rel.has_element(_mo.Couplet(couplet2.left, couplet1.right)):
                        transitive = False
                        break
        rel.cache_is_transitive(transitive)
    return rel.cached_is_transitive


def fill_lefts(rel: 'P(M x M)', renames: 'P(M x M)', _checked=True) -> 'P(M x M)':
    """Return the left components in ``rel`` that are missing in ``renames`` as a diagonal
    unioned with ``renames``.

    :param rel: The :term:`relation` that provides the full :term:`left set`.
    :param renames: A relation where the :term:`right component`\s are meant to be
        :term:`composition` 'origins' and the :term:`left component`\s composition 'targets'.
    :return: A relation that contains all members of ``lefts`` unioned with a :term:`diagonal`
        that consists of all left components in ``rel`` that are missing in ``lefts``.
    """
    if _checked:
        if not is_member(rel):
            return _make_or_raise_undef()
        if not is_member(renames):
            return _make_or_raise_undef()
    else:
        assert is_member(rel)
        assert is_member(renames)
    missing_lefts = _sets.minus(get_lefts(rel, _checked=False),
                                get_rights(renames, _checked=False), _checked=False)
    diag_missing_lefts = diag(*missing_lefts)
    return _sets.union(renames, diag_missing_lefts, _checked=False).cache_is_relation(True)


def rename(rel: 'P(M x M)', renames: 'P(M x M)', _checked=True) -> 'P(M x M)':
    """Return a :term:`relation` where left components in ``rel`` are renamed according to ``renames``.

    :param rel: The relation with the left components to rename.
    :param renames: A relation where the right components are the current left components in
        ``rel`` and the  left components are the new left components to use in ``rel``.
    :return: A version of ``rel`` where the left components of the member couplets are renamed.
    """
    if _checked:
        if not is_member(rel):
            return _make_or_raise_undef()
        if not is_member(renames):
            return _make_or_raise_undef()
    else:
        assert is_member(rel)
        assert is_member(renames)
    renames_complete = fill_lefts(rel, renames, _checked=False)
    result = compose(rel, renames_complete, _checked=False)
    return result


def swap(rel: 'P(M x M)', swaps: 'P(M x M)', _checked=True) -> 'P(M x M)':
    """Return a :term:`relation` where  components in ``rel`` are swapped according to ``swaps``.

    :param rel: The relation with the left components to swap.
    :param swaps: A relation where both right components and left components are current left
        components in ``rel``.  These left components are swapped.
    :return: A version of ``rel`` where the left components of the member couplets are swapped.
    """
    if _checked:
        if not is_member(rel):
            return _make_or_raise_undef()
        if not is_member(swaps):
            return _make_or_raise_undef()
    else:
        assert is_member(rel)
        assert is_member(swaps)
    renames = _sets.union(swaps, transpose(swaps, _checked=False), _checked=False)
    return rename(rel, renames, _checked=False)


def functional_add(rel: 'P(M x M)', element: 'M x M') -> 'P(M x M)':
    """Add ``element`` to ``rel`` and return the new :term:`relation`.

    :param rel: The source data. Must be a :term:`relation`. It must not contain a :term:`couplet`
        with the same :term:`left component` as ``element``.
    :param element: The element to be added to ``rel``. Must be a :class:`~.Couplet` and its
        :term:`left component` must not be a left component in ``rel``.
    :return: The new relation, composed of ``rel`` and ``element``.
    """
    if not is_member(rel):
        return _make_or_raise_undef()
    if not isinstance(element, _mo.Couplet):
        return _make_or_raise_undef()
    if _sets.is_subset_of(_mo.Set(element.left), get_lefts(rel)):
        return _make_or_raise_undef(2)
    result_relation = _sets.union(rel, _mo.Set(element))
    return result_relation


def from_dict(dict1: dict) -> 'P(M x M)':
    """Return a :term:`relation` where the :term:`couplet`\s are the elements of ``dict1``."""
    return _mo.Set((_mo.Couplet(left, right) for left, right in dict1.items()),
                   direct_load=True).cache_is_relation(True).cache_is_left_functional(True)


def diag(*args) -> 'P(M x M)':
    """Return the :term:`diagonal` of the set comprising the elements in ``*args``."""
    return _mo.Set((_mo.Couplet(elem, elem) for elem in args),
                   direct_load=True).cache_is_left_functional(True)


def defined_at(rel, left):
    """Return the ``rel`` if it is defined at left else `Undef()`."""
    # if rel(left) is Undef():
    if not rel[left]:
        return _make_or_raise_undef(2)
    return rel
