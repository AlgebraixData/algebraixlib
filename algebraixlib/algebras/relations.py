r"""This module contains the :term:`algebra of relations` and related functionality.

A :term:`relation` is also a :term:`set` (of :term:`couplet`\s), and inherits all operations
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

import algebraixlib.algebras.couplets as _couplets
import algebraixlib.algebras.sets as _sets
import algebraixlib.mathobjects as _mo
import algebraixlib.extension as _extension
import algebraixlib.structure as _structure
import algebraixlib.undef as _undef

from ..cache_status import CacheStatus


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
        """Return a relation where all couplets have their left and right components swapped.

        :return: The :term:`unary extension` of :term:`transposition` from the
            :term:`algebra of couplets` to the :term:`algebra of relations`, applied to the
            :term:`relation` ``rel``, or `Undef()` if ``rel`` is not a relation.
        """
        if _checked:
            if not is_member(rel):
                return _undef.make_or_raise_undef2(rel)
        else:
            assert is_member_or_undef(rel)
            if rel is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.unary_extend(rel, _functools.partial(
            _couplets.transpose, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_relation(CacheStatus.IS)
            result.cache_absolute(rel.cached_absolute)
            result.cache_functional(rel.cached_right_functional)
            result.cache_right_functional(rel.cached_functional)
            result.cache_reflexive(rel.cached_reflexive)
            result.cache_symmetric(rel.cached_symmetric)
            result.cache_transitive(rel.cached_transitive)
        return result

    # ----------------------------------------------------------------------------------------------
    # Binary algebra operations.

    @staticmethod
    def compose(rel1: 'P(M x M)', rel2: 'P(M x M)', _checked=True) -> 'P(M x M)':
        r"""Return the composition of ``rel1`` with ``rel2``.

        :return: The :term:`binary extension` of :term:`composition` from the :term:`algebra of
            couplets` to the :term:`algebra of relations`, applied to the :term:`relation`\s
            ``rel1`` and ``rel2``, or `Undef()` if ``rel1`` or ``rel2`` are not relations.
        """
        if _checked:
            if not is_member(rel1):
                return _undef.make_or_raise_undef2(rel1)
            if not is_member(rel2):
                return _undef.make_or_raise_undef2(rel2)
        else:
            assert is_member_or_undef(rel1)
            assert is_member_or_undef(rel2)
            if rel1 is _undef.Undef() or rel2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _extension.binary_extend(rel1, rel2, _functools.partial(
            _couplets.compose, _checked=False), _checked=False)
        if not result.is_empty:
            result.cache_relation(CacheStatus.IS)
            if rel1.cached_is_absolute and rel2.cached_is_absolute:
                result.cache_absolute(CacheStatus.IS)
            if rel1.cached_is_functional and rel2.cached_is_functional:
                result.cache_functional(CacheStatus.IS)
            if rel1.cached_is_right_functional and rel2.cached_is_right_functional:
                result.cache_right_functional(CacheStatus.IS)
        return result

    @staticmethod
    def functional_union(rel1: 'P(M x M)', rel2: 'P(M x M)', _checked=True) -> 'P(M x M)':
        r"""Return the union of ``rel1`` and ``rel2`` if it is a function, otherwise `Undef()`.

        :return: The :term:`functional union` of the :term:`relation`\s ``rel1`` and ``rel2``;
            that is, the :term:`union` if the result is a :term:`function`, otherwise
            `Undef()`. Also return `Undef()` if ``rel1`` or ``rel2`` are not relations.
        """
        if _checked:
            if not is_member(rel1):
                return _undef.make_or_raise_undef2(rel1)
            if not is_member(rel2):
                return _undef.make_or_raise_undef2(rel2)
        else:
            assert is_member_or_undef(rel1)
            assert is_member_or_undef(rel2)
            if rel1 is _undef.Undef() or rel2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _sets.union(rel1, rel2, _checked=False)
        assert result.cached_is_relation

        if not is_functional(result, _checked=False):
            return _undef.make_or_raise_undef(2)
        return result

    @staticmethod
    def right_functional_union(rel1: 'P(M x M)', rel2: 'P(M x M)', _checked=True) -> 'P(M x M)':
        r"""Return the union of ``rel1`` and ``rel2`` if it is right-functional, otherwise
        `Undef()`.

        :return: The :term:`right-functional union` of the :term:`relation`\s ``rel1`` and
            ``rel2``; that is, the :term:`union` if the result is :term:`right-functional`,
            otherwise `Undef()`. Also return `Undef()` if ``rel1`` or ``rel2`` are not relations.
        """
        if _checked:
            if not is_member(rel1):
                return _undef.make_or_raise_undef2(rel1)
            if not is_member(rel2):
                return _undef.make_or_raise_undef2(rel2)
        else:
            assert is_member_or_undef(rel1)
            assert is_member_or_undef(rel2)
            if rel1 is _undef.Undef() or rel2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        rel_union = _sets.union(rel1, rel2, _checked=False).cache_relation(CacheStatus.IS)
        if not is_right_functional(rel_union, _checked=False):
            return _undef.make_or_raise_undef(2)
        return rel_union


# For convenience, make the members of class Algebra (they are all static functions) available at
# the module level.

# pylint: disable=invalid-name

#: Convenience redirection to `Algebra.transpose`.
transpose = Algebra.transpose
#: Convenience redirection to `Algebra.compose`.
compose = Algebra.compose
#: Convenience redirection to `Algebra.functional_union`.
functional_union = Algebra.functional_union
#: Convenience redirection to `Algebra.right_functional_union`.
right_functional_union = Algebra.right_functional_union

# pylint: enable=invalid-name

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
    """Return whether ``obj`` is a member of the :term:`ground set` of this :term:`algebra`.

     :return: ``True`` if ``obj`` is a :term:`relation`, ``False`` if not.

    .. note:: This function may call :meth:`~.MathObject.get_ground_set` on ``obj``. The result
        of this operation is cached.
    """
    if obj.cached_relation == CacheStatus.UNKNOWN:
        is_relation = obj.get_ground_set().is_subset(get_ground_set())
        obj.cache_relation(CacheStatus.from_bool(is_relation))
    return obj.cached_is_relation


def is_member_or_undef(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is either a member of the :term:`ground set` of this :term:`algebra`
        or :class:`~.Undef`.

     :return: ``True`` if ``obj`` is either a :term:`relation` or :class:`~.Undef`,
        ``False`` if not.
    """
    return obj is _undef.Undef() or is_member(obj)


def is_absolute_member(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is a member of the :term:`absolute ground set` of this algebra.

     :return: ``True`` if ``obj`` is an :term:`absolute relation`, ``False`` if not.

    .. note:: This function may call :meth:`~.MathObject.get_ground_set` on ``obj``. The result
        of this operation is cached.
    """
    if obj.cached_is_not_relation:
        # If known to not be a relation, it's also not an absolute relation. No further caching.
        return False
    # The `or` clause in this `if` statement is a safety thing. It should never hit.
    if obj.cached_absolute == CacheStatus.UNKNOWN \
            or obj.cached_relation == CacheStatus.UNKNOWN:
        # The 'absolute' state has not yet been cached. Determine whether obj is an absolute
        # relation.
        is_absolute_relation = obj.get_ground_set().is_subset(get_absolute_ground_set())
        if obj.cached_relation == CacheStatus.UNKNOWN:
            if is_absolute_relation:
                # If it is an absolute relation, it is also a relation.
                obj.cache_relation(CacheStatus.IS)
            else:
                # If it is not an absolute relation, it may still be a relation.
                is_relation = is_member(obj)
                if not is_relation:
                    # If it is neither an absolute relation nor a relation, exit. (That it is not a
                    # relation has already been cached in is_member().)
                    return False
        # At this point, cached_relation == IS. Cache whether this is an absolute relation.
        assert obj.cached_is_relation
        obj.cache_absolute(CacheStatus.from_bool(is_absolute_relation))
    # At this point, cached_relation == IS. Return whether it is an absolute relation.
    return obj.cached_is_absolute


# --------------------------------------------------------------------------------------------------
# Related operations, not formally part of the algebra.

def get_lefts(rel: 'P(M x M)', _checked=True) -> 'P( M )':
    """Return the set of the left components of all couplets in the relation ``rel``.

    :return: The :term:`left set` of the :term:`relation` ``rel`` or `Undef()` if ``rel`` is not a
        relation.
    """
    if _checked:
        if not is_member(rel):
            return _undef.make_or_raise_undef2(rel)
    else:
        assert is_member_or_undef(rel)
        if rel is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    result = _mo.Set((e.left for e in rel), direct_load=True)
    if not result.is_empty:
        if rel.cached_is_absolute:
            result.cache_absolute(CacheStatus.IS)
    return result


def get_rights(rel: 'P(M x M)', _checked=True) -> 'P( M )':
    """Return the set of the right components of all couplets in the relation ``rel``.

    :return: The :term:`right set` of the :term:`relation` ``rel`` or `Undef()` if ``rel`` is not a
        relation.
    """
    if _checked:
        if not is_member(rel):
            return _undef.make_or_raise_undef2(rel)
    else:
        assert is_member_or_undef(rel)
        if rel is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    result = _mo.Set((e.right for e in rel), direct_load=True)
    if not result.is_empty:
        if rel.cached_is_absolute:
            result.cache_absolute(CacheStatus.IS)
    return result


def get_rights_for_left(rel: 'P(M x M)', left: '( M )', _checked=True) -> 'P( M )':
    """Return the set of the right components of all couplets in the relation ``rel`` associated
    with the :term:`left component` ``left``.

    :return: The :term:`right set` of the :term:`relation` ``rel`` associated with the :term:`left
        component` or `Undef()` if ``rel`` is not a :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _undef.make_or_raise_undef2(rel)
        if left is _undef.Undef():
            return _mo.Set()
        left = _mo.auto_convert(left)
    else:
        assert is_member_or_undef(rel)
        assert _mo.is_mathobject_or_undef(left)
        if rel is _undef.Undef():
            return _undef.make_or_raise_undef(2)
        if left is _undef.Undef():
            return _mo.Set()
    result = _mo.Set((elem.right for elem in rel if elem.left == left), direct_load=True)
    if not result.is_empty:
        if rel.cached_is_absolute:
            result.cache_absolute(CacheStatus.IS)
    return result


def get_right(rel: 'P(M x M)', left: '( M )', _checked=True) -> '( M )':
    r"""Return the right component of the couplet that has a left component of ``left``.

    In general, use with :term:`function`\s; that is, :term:`relation`\s where all
    :term:`left component`\s appear at most once.

    :return: The :term:`right component` of the :term:`couplet` that has a :term:`left component`
        of ``left``, or `Undef()` if there is not exactly one couplet with the left component
        ``left`` in ``rel`` or ``rel`` is not a :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _undef.make_or_raise_undef2(rel)
        if left is _undef.Undef():
            return _undef.make_or_raise_undef(2)
        left = _mo.auto_convert(left)
    else:
        assert is_member_or_undef(rel)
        assert _mo.is_mathobject_or_undef(left)
        if left is _undef.Undef() or rel is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    result = None
    for elem in rel:
        assert elem.is_couplet
        if elem.left == left:
            if result is not None:
                return _undef.make_or_raise_undef()  # Early Undef() exit if more than one found.
            result = elem.right
    if result is None:
        return _undef.make_or_raise_undef()  # Undef() exit if none found.
    return result


def get_left(rel: 'P(M x M)', right: '( M )', _checked=True) -> '( M )':
    r"""Return the left component of the couplet that has a right component of ``right``.

    In general, use with :term:`right-functional` :term:`relation`\s; that is, relations
    where all :term:`right component`\s appear at most once.

    :return: The :term:`left component` of the :term:`couplet` that has a :term:`right component`
        of ``right``, or `Undef()` if there is not exactly one couplet with the right component
        ``right`` in ``rel`` or ``rel`` is not a :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _undef.make_or_raise_undef2(rel)
        if right is _undef.Undef():
            return _undef.make_or_raise_undef(2)
        right = _mo.auto_convert(right)
    else:
        assert is_member_or_undef(rel)
        assert _mo.is_mathobject_or_undef(right)
        if right is _undef.Undef() or rel is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    result = None
    for elem in rel:
        assert elem.is_couplet
        if elem.right == right:
            if result is not None:
                return _undef.make_or_raise_undef()  # Early Undef() exit if more than one found.
            result = elem.left
    if result is None:
        return _undef.make_or_raise_undef()  # Undef() exit if none found.
    return result


def is_functional(rel, _checked=True) -> bool:
    """Return whether ``rel`` is left-functional (is a function).

    :return: ``True`` if ``rel`` is a :term:`function`, ``False`` if not, or `Undef()` if ``rel`` is
        not a :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _undef.make_or_raise_undef2(rel)
    else:
        assert is_member_or_undef(rel)
        if rel is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if rel.cached_functional == CacheStatus.UNKNOWN:
        left_set = get_lefts(rel, _checked=False)
        functional = (left_set.cardinality == rel.cardinality)
        rel.cache_functional(CacheStatus.from_bool(functional))
    return rel.cached_is_functional


def is_right_functional(rel, _checked=True) -> bool:
    """Return whether ``rel`` is right-functional.

    :return: ``True`` if ``rel`` is :term:`right-functional`, ``False`` if not, or `Undef()` if
        ``rel`` is not a :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _undef.make_or_raise_undef2(rel)
    else:
        assert is_member_or_undef(rel)
        if rel is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if rel.cached_right_functional == CacheStatus.UNKNOWN:
        right_set = get_rights(rel, _checked=False)
        right_functional = (right_set.cardinality == rel.cardinality)
        rel.cache_right_functional(CacheStatus.from_bool(right_functional))
    return rel.cached_is_right_functional


def is_reflexive(rel, _checked=True) -> bool:
    """Return whether ``rel`` is reflexive.

    :return: ``True`` if ``rel`` is :term:`reflexive`, ``False`` if it is not, or `Undef()` if
        ``rel`` is not a :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _undef.make_or_raise_undef2(rel)
    else:
        assert is_member_or_undef(rel)
        if rel is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if rel.cached_reflexive == CacheStatus.UNKNOWN:
        reflexive = all(_couplets.is_reflexive(couplet, _checked=False) for couplet in rel)
        rel.cache_reflexive(CacheStatus.from_bool(reflexive))
    return rel.cached_reflexive == CacheStatus.IS


def is_symmetric(rel, _checked=True) -> bool:
    """Return whether ``rel`` is symmetric.

    :return: ``True`` if ``rel`` is :term:`symmetric`, ``False`` if it is not, or `Undef()` if
        ``rel`` is not a :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _undef.make_or_raise_undef2(rel)
    else:
        assert is_member_or_undef(rel)
        if rel is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if rel.cached_symmetric == CacheStatus.UNKNOWN:
        symmetric = all(rel.has_element(
            _couplets.transpose(couplet, _checked=False)) for couplet in rel)
        rel.cache_symmetric(CacheStatus.from_bool(symmetric))
    return rel.cached_symmetric == CacheStatus.IS


def is_transitive(rel, _checked=True) -> bool:
    """Return whether ``rel`` is transitive.

    :return: ``True`` if ``rel`` is :term:`transitive`, ``False`` if it is not, or `Undef()` if
        ``rel`` is not a :term:`relation`.
    """
    if _checked:
        if not is_member(rel):
            return _undef.make_or_raise_undef2(rel)
    else:
        assert is_member_or_undef(rel)
        if rel is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if rel.cached_transitive == CacheStatus.UNKNOWN:
        transitive = True
        for couplet1 in rel:
            for couplet2 in rel:
                if couplet1.left == couplet2.right:
                    if not rel.has_element(_mo.Couplet(couplet2.left, couplet1.right)):
                        transitive = False
                        break
        rel.cache_transitive(CacheStatus.from_bool(transitive))
    return rel.cached_transitive == CacheStatus.IS


def fill_lefts(rel: 'P(M x M)', renames: 'P(M x M)', _checked=True) -> 'P(M x M)':
    r"""Return the left components in ``rel`` that are missing in ``renames`` as a diagonal
    unioned with ``renames``.

    The purpose is to create a :term:`relation` that can be used with the :term:`composition`
    operation to change (rename) one or more :term:`left component`\s and leave the rest alone.

    :param rel: The :term:`relation` that provides the full :term:`left set`.
    :param renames: A relation where the :term:`right component`\s are meant to be
        :term:`composition` 'origins' and the :term:`left component`\s composition 'targets'.
    :return: A relation that contains all members of ``renames`` unioned with a :term:`diagonal`
        that consists of all left components in ``rel`` that are missing in ``renames``.
    """
    if _checked:
        if not is_member(rel):
            return _undef.make_or_raise_undef2(rel)
        if not is_member(renames):
            return _undef.make_or_raise_undef2(renames)
    else:
        assert is_member_or_undef(rel)
        assert is_member_or_undef(renames)
        if rel is _undef.Undef() or renames is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    missing_lefts = _sets.minus(get_lefts(rel, _checked=False),
                                get_rights(renames, _checked=False), _checked=False)
    diag_missing_lefts = diag(*missing_lefts, _checked=False)
    result = _sets.union(renames, diag_missing_lefts, _checked=False)
    assert result.cached_is_relation
    return result


def rename(rel: 'P(M x M)', renames: 'P(M x M)', _checked=True) -> 'P(M x M)':
    r"""Return a relation where left components in ``rel`` are renamed according to ``renames``.

    :param rel: The :term:`relation` with the :term:`left component`\s to rename.
    :param renames: A relation where the :term:`right component`\s are the current left components
        in ``rel`` and the  left components are the new left components to use in ``rel``.
    :return: A version of ``rel`` where some left components of the member :term:`couplet`\s are
        changed (renamed), according to ``renames``.
    """
    if _checked:
        if not is_member(rel):
            return _undef.make_or_raise_undef2(rel)
        if not is_member(renames):
            return _undef.make_or_raise_undef2(renames)
    else:
        assert is_member_or_undef(rel)
        assert is_member_or_undef(renames)
        if rel is _undef.Undef() or renames is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    renames_complete = fill_lefts(rel, renames, _checked=False)
    result = compose(rel, renames_complete, _checked=False)
    return result


def swap(rel: 'P(M x M)', swaps: 'P(M x M)', _checked=True) -> 'P(M x M)':
    r"""Return a relation where  components in ``rel`` are swapped according to ``swaps``.

    :param rel: The :term:`relation` with the :term:`left component`\s to swap.
    :param swaps: A relation where both :term:`right component`\s and left components are current
        left components in ``rel``.  These left components are swapped.
    :return: A version of ``rel`` where some left components of the member :term:`couplet`\s are
        swapped, according to ``swaps``.
    """
    if _checked:
        if not is_member(rel):
            return _undef.make_or_raise_undef2(rel)
        if not is_member(swaps):
            return _undef.make_or_raise_undef2(swaps)
    else:
        assert is_member_or_undef(rel)
        assert is_member_or_undef(swaps)
        if rel is _undef.Undef() or swaps is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    renames = _sets.union(swaps, transpose(swaps, _checked=False), _checked=False)
    return rename(rel, renames, _checked=False)


def functional_add(func: 'P(M x M)', element: 'M x M') -> 'P(M x M)':
    """Add ``element`` to ``func`` and return the new functional relation.

    :param func: The source data. Must be a :term:`function`. It must not contain a :term:`couplet`
        with the same :term:`left component` as ``element``.
    :param element: The element to be added to ``func``. Must be a :class:`~.Couplet` and its
        :term:`left component` must not be a left component in ``func``.
    :return: The new relation, composed of ``func`` and ``element``.
    """
    if not is_member(func) or not is_functional(func):
        return _undef.make_or_raise_undef2(func)
    if not _couplets.is_member(element):
        return _undef.make_or_raise_undef2(element)
    if _sets.is_subset_of(_mo.Set(element.left), get_lefts(func)):
        return _undef.make_or_raise_undef(2)
    element_func = _mo.Set(element).cache_relation(CacheStatus.IS)
    result = _sets.union(func, element_func)
    assert result.cached_is_relation and is_functional(result)
    result.cache_functional(CacheStatus.IS)
    return result


def from_dict(dict1: dict) -> 'P(M x M)':
    r"""Return a :term:`relation` where the :term:`couplet`\s are the elements of ``dict1``."""
    return _mo.Set((_mo.Couplet(left, right) for left, right in dict1.items()), direct_load=True)\
        .cache_relation(CacheStatus.IS).cache_functional(CacheStatus.IS)


def diag(*args, _checked=True) -> 'P(M x M)':
    """Return the :term:`diagonal` of the set comprising the elements in ``*args``."""
    for element in args:
        if element is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    rel = _mo.Set((_mo.Couplet(el, direct_load=not _checked) for el in args), direct_load=True)
    rel.cache_relation(CacheStatus.IS)
    rel.cache_functional(CacheStatus.IS).cache_right_functional(CacheStatus.IS)
    rel.cache_reflexive(CacheStatus.IS).cache_symmetric(CacheStatus.IS)
    return rel


def defined_at(rel, left, _checked=True):
    """Return ``rel`` if it has a :term:`couplet` with left component ``left`` else `Undef()`."""
    result = get_rights_for_left(rel, left, _checked)
    if result is _undef.Undef() or not result:
        return _undef.make_or_raise_undef2(result)
    return rel
