"""Facilities for extending operations from one :term:`algebra` to another."""

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

import algebraixlib.algebras.multisets as _multisets
import algebraixlib.algebras.sets as _sets
import algebraixlib.mathobjects as _mo
import algebraixlib.undef as _undef


def binary_extend(set1: 'P( M )', set2: 'P( M )', op, _checked=True) -> 'P( M )':
    r"""Return the :term:`binary extension` of ``op`` from one :term:`algebra` to another algebra.

    For this extension, the elements of the extended algebra must be :term:`set`\s of the
    elements of the original algebra.

    :param set1: A :term:`set` with elements on which ``op`` operates.
    :param set2: A set with elements on which ``op`` operates.
    :param op: A :term:`binary operation` that operates on the elements of ``set1`` and ``set2``.
    :return: A set that consists of the defined results of ``op`` when executed on all combinations
        of the elements of ``set1`` and ``set2``, or `Undef()` if either set is not a
        :class:`~.Set`.
    """
    if _checked:
        if not _sets.is_member(set1):
            return _undef.make_or_raise_undef2(set1)
        if not _sets.is_member(set2):
            return _undef.make_or_raise_undef2(set2)
    else:
        assert _sets.is_member_or_undef(set1)
        assert _sets.is_member_or_undef(set2)
        if set1 is _undef.Undef() or set2 is _undef.Undef():
            return _undef.make_or_raise_undef(2)

    def _get_values(_set1, _set2):
        for e1 in _set1:
            for e2 in _set2:
                result = op(e1, e2)
                if result is not _undef.Undef():
                    yield result

    return _mo.Set(_get_values(set1, set2), direct_load=True)


def binary_multi_extend(multiset1: 'P( M x N )', multiset2: 'P( M x N )', op,
                        _checked=True) -> 'P( M x N )':
    r"""Return the :term:`binary extension` of ``op`` from one :term:`algebra` to another algebra.

    For this extension, the elements of the extended algebra must be :term:`multiset`\s of the
    elements of the original algebra.

    :param multiset1: A :term:`multiset` with elements on which ``op`` operates.
    :param multiset2: A multiset with elements on which ``op`` operates.
    :param op: A :term:`binary operation` that operates on the elements of ``multiset1`` and
        ``multiset2``.
    :return: A multiset that consists of the defined results of ``op`` when executed on all
        combinations of the elements of ``multiset1`` and ``multiset2``, or `Undef()` if either
        set is not a :class:`~.Multiset`.
    """
    if _checked:
        if not _multisets.is_member(multiset1):
            return _undef.make_or_raise_undef2(multiset1)
        if not _multisets.is_member(multiset2):
            return _undef.make_or_raise_undef2(multiset2)
    else:
        assert _multisets.is_member_or_undef(multiset1)
        assert _multisets.is_member_or_undef(multiset2)
        if multiset1 is _undef.Undef() or multiset2 is _undef.Undef():
            return _undef.make_or_raise_undef(2)

    def _get_values(_set1, _set2):
        return_count = _collections.Counter()
        for elem1, multi1 in _set1.data.items():
            for elem2, multi2 in _set2.data.items():
                result = op(elem1, elem2)
                if result is not _undef.Undef():
                    return_count[result] += multi1 * multi2

        return return_count

    return _mo.Multiset(_get_values(multiset1, multiset2), direct_load=True)


def unary_extend(set_: 'P( M )', op, _checked=True) -> 'P( M )':
    r"""Return the :term:`unary extension` of ``op`` from one :term:`algebra` to another algebra.

    For this extension, the elements of the extended algebra must be :term:`set`\s of the elements
    of the original algebra.

    :param set_: A :term:`set` with elements on which ``op`` operates.
    :param op: A :term:`unary operation` that operates on the elements of ``set_``.
    :return: A set that consists of the defined results of ``op`` when executed on the elements of
        ``set_``, or `Undef()` if ``set_`` is not a :class:`~.Set`.
    """
    if _checked:
        if not _sets.is_member(set_):
            return _undef.make_or_raise_undef2(set_)
    else:
        assert _sets.is_member_or_undef(set_)
        if set is _undef.Undef():
            return _undef.make_or_raise_undef(2)

    def _get_values(_set):
        for e in _set:
            result = op(e)
            if result is not _undef.Undef():
                yield result

    return _mo.Set(_get_values(set_), direct_load=True)


def unary_multi_extend(set_or_mset, op, _checked=True) -> 'P( M x N )':
    r"""Return the :term:`unary extension` of ``op`` from one :term:`algebra` to another algebra.

    For this extension, the elements of the extended algebra must be :term:`multiset`\s of the
    elements of the original algebra.

    :param set_or_mset: A :term:`set` or a :term:`multiset` with elements on which ``op`` operates.
    :param op: A :term:`unary operation` that operates on the elements of ``set_or_mset``.
    :return: A set that consists of the defined results of ``op`` when executed on the elements of
        ``set_or_mset``, or `Undef()` if ``set_or_mset`` is neither a set nor a multiset.
    """
    if _checked:
        if not _multisets.is_member(set_or_mset) and not _sets.is_member(set_or_mset):
            return _undef.make_or_raise_undef2(set_or_mset)
    else:
        assert _multisets.is_member(set_or_mset) or _sets.is_member(set_or_mset) \
               or set_or_mset is _undef.Undef()
        if set_or_mset is _undef.Undef():
            return _undef.make_or_raise_undef(2)

    def _get_values_set(set_):
        result_counter = _collections.Counter()
        for elem in set_:
            result = op(elem)
            if result is not _undef.Undef():
                result_counter[result] += 1
        return result_counter

    def _get_values_multiset(mset):
        result_counter = _collections.Counter()
        for elem, multiplicity in mset.data.items():
            result = op(elem)
            if result is not _undef.Undef():
                result_counter[result] += multiplicity
        return result_counter

    get_values = _get_values_multiset if _multisets.is_member(set_or_mset) else _get_values_set

    return _mo.Multiset(get_values(set_or_mset))
