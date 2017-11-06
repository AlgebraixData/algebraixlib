"""Accessors for the properties of a generic `MathObject` that redirect to the appropriate algebra.

The accessors here check what algebra a given `MathObject` belongs to, then call the property
function of this algebra.
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
import algebraixlib.algebras.clans as _clans
import algebraixlib.algebras.couplets as _couplets
import algebraixlib.algebras.multiclans as _multiclans
import algebraixlib.algebras.relations as _relations
import algebraixlib.mathobjects as _mo
import algebraixlib.undef as _undef

from ..cache_status import CacheStatus


# --------------------------------------------------------------------------------------------------

def is_functional(mo: _mo.MathObject, _checked: bool=True) -> bool:
    r"""Return whether ``mo`` is :term:`functional` or `Undef()` if not applicable.

    Is implemented for :term:`relation`\s, :term:`clan`\s, :term:`multiclan`\s and :term:`set`\s
    of (sets of ...) clans. Is also defined (but not yet implemented) for any combination of sets
    or :term:`multiset`\s of relations.
    """
    # pylint: disable=too-many-return-statements
    if _checked:
        if not isinstance(mo, _mo.MathObject):
            return _undef.make_or_raise_undef()

    # Check cache status.
    if mo.cached_functional == CacheStatus.IS:
        return True
    if mo.cached_functional == CacheStatus.IS_NOT:
        return False
    if mo.cached_functional == CacheStatus.N_A:
        return _undef.make_or_raise_undef(2)

    # Check type (functional is only defined on Sets and Multisets) and algebra memberships.
    if not mo.is_set and not mo.is_multiset:
        mo.cache_functional(CacheStatus.N_A)
        return _undef.make_or_raise_undef(2)
    if _relations.is_member(mo):
        return _relations.is_functional(mo, _checked=False)
    if _clans.is_member(mo):
        return _clans.is_functional(mo, _checked=False)
    if _multiclans.is_member(mo):
        return _multiclans.is_functional(mo, _checked=False)

    # Check higher (not yet defined) algebras.
    functional = _is_powerset_property(mo, _clans.get_ground_set(), is_functional)
    if functional is not _undef.Undef():
        mo.cache_functional(CacheStatus.from_bool(functional))
        return functional

    # Nothing applied: 'functional' is not defined.
    mo.cache_functional(CacheStatus.N_A)
    return _undef.make_or_raise_undef(2)


def is_right_functional(mo: _mo.MathObject, _checked: bool=True) -> bool:
    r"""Return whether ``mo`` is :term:`right-functional` or `Undef()` if not applicable.

    Is implemented for :term:`relation`\s, :term:`clan`\s, :term:`multiclan`\s and :term:`set`\s
    of (sets of ...) clans. Is also defined (but not yet implemented) for any combination of sets
    or :term:`multiset`\s of relations.
    """
    # pylint: disable=too-many-return-statements
    if _checked:
        if not isinstance(mo, _mo.MathObject):
            return _undef.make_or_raise_undef()

    # Check cache status.
    if mo.cached_right_functional == CacheStatus.IS:
        return True
    if mo.cached_right_functional == CacheStatus.IS_NOT:
        return False
    if mo.cached_right_functional == CacheStatus.N_A:
        return _undef.make_or_raise_undef(2)

    # Check type (right-functional is only defined on Sets and Multisets) and algebra memberships.
    if not mo.is_set and not mo.is_multiset:
        mo.cache_right_functional(CacheStatus.N_A)
        return _undef.make_or_raise_undef(2)
    if _relations.is_member(mo):
        return _relations.is_right_functional(mo, _checked=False)
    if _clans.is_member(mo):
        return _clans.is_right_functional(mo, _checked=False)
    if _multiclans.is_member(mo):
        return _multiclans.is_right_functional(mo, _checked=False)

    # Check higher (not yet defined) algebras.
    right_functional = _is_powerset_property(mo, _clans.get_ground_set(), is_right_functional)
    if right_functional is not _undef.Undef():
        mo.cache_right_functional(CacheStatus.from_bool(right_functional))
        return right_functional

    # Nothing applied: 'right-functional' is not defined.
    mo.cache_right_functional(CacheStatus.N_A)
    return _undef.make_or_raise_undef(2)


def is_bijective(mo: _mo.MathObject, _checked: bool=True) -> bool:
    r"""Return whether ``mo`` is :term:`bijective` or `Undef()` if not applicable.

    Is implemented for :term:`relation`\s, :term:`clan`\s, :term:`multiclan`\s and :term:`set`\s
    of (sets of ...) clans. Is also defined (but not yet implemented) for any combination of sets
    or :term:`multiset`\s of relations.
    """
    if _checked:
        if not isinstance(mo, _mo.MathObject):
            return _undef.make_or_raise_undef()

    # is_functional and is_right_functional are (un)defined for the same constructs, so the order
    # of evaluation is not important.

    functional = is_functional(mo, _checked=False)
    if functional is _undef.Undef() or not functional:
        return functional

    right_functional = is_right_functional(mo, _checked=False)
    if right_functional is _undef.Undef() or not right_functional:
        return right_functional

    return True


def is_reflexive(mo: _mo.MathObject, _checked: bool=True) -> bool:
    r"""Return whether ``mo`` is :term:`reflexive` or `Undef()` if not applicable.

    Is implemented for :term:`couplet`\s, :term:`relation`\s, :term:`clan`\s, :term:`multiclan`\s
    and  :term:`set`\s of (sets of ...) clans. Is also defined (but not yet implemented) for any
    combination of sets or :term:`multiset`\s of relations.
    """
    # pylint: disable=too-many-return-statements
    if _checked:
        if not isinstance(mo, _mo.MathObject):
            return _undef.make_or_raise_undef()

    # Check cache status.
    if mo.cached_reflexive == CacheStatus.IS:
        return True
    if mo.cached_reflexive == CacheStatus.IS_NOT:
        return False
    if mo.cached_reflexive == CacheStatus.N_A:
        return _undef.make_or_raise_undef(2)

    # Check types and algebra memberships.
    if _couplets.is_member(mo):
        return _couplets.is_reflexive(mo, _checked=False)
    if not mo.is_set and not mo.is_multiset:
        mo.cache_reflexive(CacheStatus.N_A)
        return _undef.make_or_raise_undef(2)
    if _relations.is_member(mo):
        return _relations.is_reflexive(mo, _checked=False)
    if _clans.is_member(mo):
        return _clans.is_reflexive(mo, _checked=False)
    if _multiclans.is_member(mo):
        return _multiclans.is_reflexive(mo, _checked=False)

    # Check higher (not yet defined) algebras.
    reflexive = _is_powerset_property(mo, _clans.get_ground_set(), is_reflexive)
    if reflexive is not _undef.Undef():
        mo.cache_reflexive(CacheStatus.from_bool(reflexive))
        return reflexive

    # Nothing applied: 'reflexive' is not defined.
    mo.cache_reflexive(CacheStatus.N_A)
    return _undef.make_or_raise_undef(2)


def is_symmetric(mo: _mo.MathObject, _checked: bool=True) -> bool:
    r"""Return whether ``mo`` is :term:`symmetric` or `Undef()` if not applicable.

    Is implemented for :term:`relation`\s, :term:`clan`\s, :term:`multiclan`\s and :term:`set`\s
    of (sets of ...) clans. Is also defined (but not yet implemented) for any combination of sets
    or :term:`multiset`\s of relations.
    """
    # pylint: disable=too-many-return-statements
    if _checked:
        if not isinstance(mo, _mo.MathObject):
            return _undef.make_or_raise_undef()

    # Check cache status.
    if mo.cached_symmetric == CacheStatus.IS:
        return True
    if mo.cached_symmetric == CacheStatus.IS_NOT:
        return False
    if mo.cached_symmetric == CacheStatus.N_A:
        return _undef.make_or_raise_undef(2)

    # Check type (symmetric is only defined on Sets and Multisets) and algebra memberships.
    if not mo.is_set and not mo.is_multiset:
        mo.cache_symmetric(CacheStatus.N_A)
        return _undef.make_or_raise_undef(2)
    if _relations.is_member(mo):
        return _relations.is_symmetric(mo, _checked=False)
    if _clans.is_member(mo):
        return _clans.is_symmetric(mo, _checked=False)
    if _multiclans.is_member(mo):
        return _multiclans.is_symmetric(mo, _checked=False)

    # Check higher (not yet defined) algebras.
    symmetric = _is_powerset_property(mo, _relations.get_ground_set(), is_symmetric)
    if symmetric is not _undef.Undef():
        mo.cache_symmetric(CacheStatus.from_bool(symmetric))
        return symmetric

    # Nothing applied: 'symmetric' is not defined.
    mo.cache_symmetric(CacheStatus.N_A)
    return _undef.make_or_raise_undef(2)


def is_transitive(mo: _mo.MathObject, _checked: bool=True) -> bool:
    r"""Return whether ``mo`` is :term:`transitive` or `Undef()` if not applicable.

    Is implemented for :term:`relation`\s, :term:`clan`\s, :term:`multiclan`\s and :term:`set`\s
    of (sets of ...) clans. Is also defined (but not yet implemented) for any combination of sets
    or :term:`multiset`\s of relations.
    """
    # pylint: disable=too-many-return-statements
    if _checked:
        if not isinstance(mo, _mo.MathObject):
            return _undef.make_or_raise_undef()

    # Check cache status.
    if mo.cached_transitive == CacheStatus.IS:
        return True
    if mo.cached_transitive == CacheStatus.IS_NOT:
        return False
    if mo.cached_transitive == CacheStatus.N_A:
        return _undef.make_or_raise_undef(2)

    # Check type (transitive is only defined on Sets and Multisets) and algebra memberships.
    if not mo.is_set and not mo.is_multiset:
        mo.cache_transitive(CacheStatus.N_A)
        return _undef.make_or_raise_undef(2)
    if _relations.is_member(mo):
        return _relations.is_transitive(mo, _checked=False)
    if _clans.is_member(mo):
        return _clans.is_transitive(mo, _checked=False)
    if _multiclans.is_member(mo):
        return _multiclans.is_transitive(mo, _checked=False)

    # Check higher (not yet defined) algebras.
    transitive = _is_powerset_property(mo, _relations.get_ground_set(), is_transitive)
    if transitive is not _undef.Undef():
        mo.cache_transitive(CacheStatus.from_bool(transitive))
        return transitive

    # Nothing applied: 'transitive' is not defined.
    mo.cache_transitive(CacheStatus.N_A)
    return _undef.make_or_raise_undef(2)


def is_equivalence_relation(mo: _mo.MathObject, _checked: bool=True) -> bool:
    r"""Return whether ``mo`` is an :term:`equivalence relation` or `Undef()` if not applicable.

    Is implemented for :term:`relation`\s, :term:`clan`\s, :term:`multiclan`\s and :term:`set`\s
    of (sets of ...) clans. Is also defined (but not yet implemented) for any combination of sets
    or :term:`multiset`\s of relations.
    """
    if _checked:
        if not isinstance(mo, _mo.MathObject):
            return _undef.make_or_raise_undef()

    # is_reflexive is the only one that is defined for couplets, so it must be evaluated last or it
    # may result in erroneous `False` returns.

    symmetric = is_symmetric(mo, _checked=False)
    if symmetric is _undef.Undef() or not symmetric:
        return symmetric

    transitive = is_transitive(mo, _checked=False)
    if transitive is _undef.Undef() or not transitive:
        return transitive

    reflexive = is_reflexive(mo, _checked=False)
    if reflexive is _undef.Undef() or not reflexive:
        return reflexive

    return True


def is_regular(mo: _mo.MathObject, _checked: bool=True) -> bool:
    r"""Return whether ``mo`` is :term:`regular` or `Undef()` if not applicable.

    Is implemented for :term:`clan`\s, :term:`multiclan`\s and :term:`set`\s of (sets of ...) clans.
    Is also defined (but not yet implemented) for any combination of sets or :term:`multiset`\s
    of clans.
    """
    # pylint: disable=too-many-return-statements
    if _checked:
        if not isinstance(mo, _mo.MathObject):
            return _undef.make_or_raise_undef()

    # Check cache status.
    if mo.cached_regular == CacheStatus.IS:
        return True
    if mo.cached_regular == CacheStatus.IS_NOT:
        return False
    if mo.cached_regular == CacheStatus.N_A:
        return _undef.make_or_raise_undef(2)

    # Check type (regular is only defined on Sets and Multisets) and algebra memberships.
    if not mo.is_set and not mo.is_multiset:
        mo.cache_regular(CacheStatus.N_A)
        return _undef.make_or_raise_undef(2)
    if _clans.is_member(mo):
        return _clans.is_regular(mo, _checked=False)
    if _multiclans.is_member(mo):
        return _multiclans.is_regular(mo, _checked=False)

    # Check higher (not yet defined) algebras.
    if mo.get_ground_set().get_powerset_level(_clans.get_ground_set()) > 0:
        mo_iter = iter(mo)
        elem1 = next(mo_iter)
        if not is_regular(elem1):
            mo.cache_regular(CacheStatus.IS_NOT)
            return False
        elem1_lefts = elem1.get_lefts()
        regular = all(
            is_regular(elem, _checked=False) and elem.get_lefts() == elem1_lefts
            for elem in mo_iter)
        mo.cache_regular(CacheStatus.from_bool(regular))
        return mo.cached_is_regular

    # Nothing applied: 'regular' is not defined.
    mo.cache_regular(CacheStatus.N_A)
    return _undef.make_or_raise_undef(2)


def is_right_regular(mo: _mo.MathObject, _checked: bool=True) -> bool:
    r"""Return whether ``mo`` is :term:`right-regular` or `Undef()` if not applicable.

    Is implemented for :term:`clan`\s, :term:`multiclan`\s and :term:`set`\s of (sets of ...) clans.
    Is also defined (but not yet implemented) for any combination of sets or :term:`multiset`\s
    of clans.
    """
    # pylint: disable=too-many-return-statements
    if _checked:
        if not isinstance(mo, _mo.MathObject):
            return _undef.make_or_raise_undef()

    # Check cache status.
    if mo.cached_right_regular == CacheStatus.IS:
        return True
    if mo.cached_right_regular == CacheStatus.IS_NOT:
        return False
    if mo.cached_right_regular == CacheStatus.N_A:
        return _undef.make_or_raise_undef(2)

    # Check type (right-regular is only defined on Sets and Multisets) and algebra memberships.
    if not mo.is_set and not mo.is_multiset:
        mo.cache_right_regular(CacheStatus.N_A)
        return _undef.make_or_raise_undef(2)
    if _clans.is_member(mo):
        return _clans.is_right_regular(mo, _checked=False)
    if _multiclans.is_member(mo):
        return _multiclans.is_right_regular(mo, _checked=False)

    # Check higher (not yet defined) algebras.
    if mo.get_ground_set().get_powerset_level(_clans.get_ground_set()) > 0:
        mo_iter = iter(mo)
        elem1 = next(mo_iter)
        if not is_right_regular(elem1):
            mo.cache_right_regular(CacheStatus.IS_NOT)
            return False
        elem1_rights = elem1.get_rights()
        right_regular = all(
            is_right_regular(elem, _checked=False) and elem.get_rights() == elem1_rights
            for elem in mo_iter)
        mo.cache_right_regular(CacheStatus.from_bool(right_regular))
        return mo.cached_is_right_regular

    # Nothing applied: 'right-regular' is not defined.
    mo.cache_right_regular(CacheStatus.N_A)
    return _undef.make_or_raise_undef(2)


# --------------------------------------------------------------------------------------------------

def _is_powerset_property(mo: _mo.MathObject, ground_set, method) -> bool:
    """Return ``True`` if ``method`` returns ``True`` for all members of ``mo`` and ``mo`` is an
    element of an n-th power set of ``ground_set``.

    :param mo: The `MathObject` on which to operate. Must be a :term:`set`.
    :param ground_set: The :term:`ground set` of which the set ``mo`` should be part of (at the
        n-th :term:`power set` level).
    :param method: A property function (must return ``True``, ``False`` or `Undef()`) that should
        be run on all elements of ``mo``. It must be a function in this module.
    :return: ``True`` if this instance is element of an n-th power set of ``ground_set``
        and all set elements return ``True`` for ``method``, ``False`` if it is an element
        of an n-th power set but any element returned ``False`` for ``method``, or `Undef()`
        if it  isn't an element of an n-th power set.
    """
    if mo.get_ground_set().get_powerset_level(ground_set) > 0:
        for element in mo:
            result = method(element)
            if result is _undef.Undef() or not result:
                return result
        return True
    return _undef.Undef()
