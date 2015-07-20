"""Definitions for extending and other set operations that P(M) is not closed under."""

# $Id: extension.py 22614 2015-07-15 18:14:53Z gfiedler $
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

import algebraixlib.mathobjects as _mo
import algebraixlib.undef as _ud


def binary_extend(set1: 'P( M )', set2: 'P( M )', op, _checked=True) -> 'P( M )':
    r"""Return the :term:`binary extension` of ``op`` from one :term:`algebra` to another algebra.

    :param set1: A :term:`set` with elements on which ``op`` operates.
    :param set2: A set with elements on which ``op`` operates.
    :param op: A :term:`binary operation` that operates on the elements of ``set1`` and ``set2``.
    :return: A set that consists of the defined results of ``op`` when executed on all combinations
        of the elements of ``set1`` and ``set2``, or `Undef()` if either set is not a
        :class:`~.Set`.
    """
    if _checked:
        if not isinstance(set1, _mo.Set):
            return _ud.make_or_raise_undef()
        if not isinstance(set2, _mo.Set):
            return _ud.make_or_raise_undef()
    else:
        assert isinstance(set1, _mo.Set)
        assert isinstance(set2, _mo.Set)

    def _get_values(_set1, _set2):
        for e1 in _set1:
            for e2 in _set2:
                result = op(e1, e2)
                if result is not _ud.Undef():
                    yield result

    return _mo.Set(_get_values(set1, set2), direct_load=True)


def binary_multi_extend(multiset1: 'P( M x N )', multiset2: 'P( M x N )', op,
                      _checked=True) -> 'P( M x N )':
    r"""Return the :term:`binary extension` of ``op`` from one :term:`algebra` to another algebra.

    :param multiset1: A :term:`multiset` with elements on which ``op`` operates.
    :param multiset2: A multiset with elements on which ``op`` operates.
    :param op: A :term:`binary operation` that operates on the elements of ``multiset1`` and ``multiset2``.
    :return: A multiset that consists of the defined results of ``op`` when executed on all
        combinations of the elements of ``multiset1`` and ``multiset2``, or `Undef()` if either
        set is not a :class:`~.Multiset`.
    """
    if _checked:
        if not isinstance(multiset1, _mo.Multiset):
            return _ud.make_or_raise_undef()
        if not isinstance(multiset2, _mo.Multiset):
            return _ud.make_or_raise_undef()
    else:
        assert isinstance(multiset1, _mo.Multiset)
        assert isinstance(multiset2, _mo.Multiset)

    def _get_values(_set1, _set2):
        return_count = _collections.Counter()
        for elem1, multi1 in _set1.data.items():
            for elem2, multi2 in _set2.data.items():
                result = op(elem1, elem2)
                if result is not _ud.Undef():
                    return_count[result] += multi1 * multi2

        return return_count

    return _mo.Multiset(_get_values(multiset1, multiset2), direct_load=True)


def unary_extend(set1: 'P( M )', op, _checked=True) -> 'P( M )':
    r"""Return the :term:`unary extension` of ``op`` from one :term:`algebra` to another algebra.

    :param set1: A :term:`set` with elements on which ``op`` operates.
    :param op: A :term:`unary operation` that operates on the elements of ``set1``.
    :return: A set that consists of the defined results of ``op`` when executed on the elements of
        ``set1``, or `Undef()` if ``set1`` is not a :class:`~.Set`.
    """
    if _checked:
        if not isinstance(set1, _mo.Set):
            return _ud.make_or_raise_undef()
    else:
        assert isinstance(set1, _mo.Set)

    def _get_values(_set):
        for e in _set:
            result = op(e)
            if result is not _ud.Undef():
                yield result

    return _mo.Set(_get_values(set1), direct_load=True)


def unary_multi_extend(multiset1: 'P( M x N )', op, _checked=True) -> 'P( M x N )':
    r"""Return the :term:`unary extension` of ``op`` from one :term:`algebra` to another algebra.

    :param multiset1: A :term:`multiset` with elements on which ``op`` operates.
    :param op: A :term:`unary operation` that operates on the elements of ``multiset1``.
    :return: A set that consists of the defined results of ``op`` when executed on the elements of
        ``multiset1``, or `Undef()` if ``set1`` is not a :class:`~.Multiset`.
    """
    if _checked:
        if not isinstance(multiset1, _mo.Multiset):
            return _ud.make_or_raise_undef()
    else:
        assert isinstance(multiset1, _mo.Multiset)

    def _get_values(_multiset):
        return_count = _collections.Counter()
        for elem, multi in _multiset.data.items():
            result = op(elem)
            if result is not _ud.Undef():
                return_count[result] += multi

        return return_count

    return _mo.Multiset(_get_values(multiset1))
