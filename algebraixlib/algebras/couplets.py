"""This module contains the :term:`algebra of couplets` and related functionality."""

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
import algebraixlib.mathobjects as _mo
import algebraixlib.structure as _structure
import algebraixlib.undef as _undef

from ..cache_status import CacheStatus


# --------------------------------------------------------------------------------------------------

class Algebra:
    """Provide the operations and relations that are members of the :term:`algebra of couplets`.

    This class contains only static member functions. Its main purpose is to provide a namespace for
    and highlight the operations and relations that belong to the algebra of couplets. All member
    functions are also available at the enclosing module scope.
    """
    # ----------------------------------------------------------------------------------------------
    # Unary algebra operations.

    @staticmethod
    def transpose(couplet: '(M x M)', _checked=True) -> '(M x M)':
        """Return the transposition of ``couplet`` (right and left components swapped).

        :return: The :term:`transposition` of ``couplet`` or `Undef()` if ``couplet`` is not an
            instance of :class:`~.Couplet`.
        """
        if _checked:
            if not is_member(couplet):
                return _undef.make_or_raise_undef2(couplet)
        else:
            assert is_member_or_undef(couplet)
            if couplet is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        result = _mo.Couplet(left=couplet.right, right=couplet.left, direct_load=True)
        result.cache_absolute(couplet.cached_absolute).cache_reflexive(couplet.cached_reflexive)
        return result

    # ----------------------------------------------------------------------------------------------
    # Binary algebra operations.

    @staticmethod
    def compose(couplet1: '(M x M)', couplet2: '(M x M)', _checked=True) -> '(M x M)':
        """Return the composition of ``couplet1`` with ``couplet2``.

        :return: The :term:`composition` of ``couplet1`` with ``couplet2`` (which may be undefined,
            in which case the result is `Undef()`) or `Undef()` if ``couplet1`` or ``couplet2`` are
            not instances of :class:`~.Couplet`.
        """
        if _checked:
            if not is_member(couplet1):
                return _undef.make_or_raise_undef2(couplet1)
            if not is_member(couplet2):
                return _undef.make_or_raise_undef2(couplet2)
        else:
            assert is_member_or_undef(couplet1)
            assert is_member_or_undef(couplet2)
            if couplet1 is _undef.Undef() or couplet2 is _undef.Undef():
                return _undef.make_or_raise_undef(2)
        if couplet1.left != couplet2.right:
            return _undef.make_or_raise_undef(2)
        return _mo.Couplet(left=couplet2.left, right=couplet1.right, direct_load=True)


# For convenience, make the members of class Algebra (they are all static functions) available at
# the module level.

# pylint: disable=invalid-name

#: Convenience redirection to `Algebra.transpose`.
transpose = Algebra.transpose
#: Convenience redirection to `Algebra.compose`.
compose = Algebra.compose

# pylint: enable=invalid-name

# --------------------------------------------------------------------------------------------------
# Metadata functions.


def get_name() -> str:
    """Return the name and :term:`ground set` of this :term:`algebra` in string form."""
    return 'Couplets(M): {ground_set}'.format(ground_set=str(get_ground_set()))


def get_ground_set() -> _structure.Structure:
    """Return the :term:`ground set` of this :term:`algebra`."""
    return _structure.CartesianProduct(_structure.GenesisSetM(), _structure.GenesisSetM())


def get_absolute_ground_set() -> _structure.Structure:
    """Return the :term:`absolute ground set` of this :term:`algebra`."""
    return _structure.CartesianProduct(_structure.GenesisSetA(), _structure.GenesisSetA())


def is_member(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is a member of the :term:`ground set` of this :term:`algebra`.

     :return: ``True`` if ``obj`` is a :term:`couplet` (an instance of :class:`~.Couplet`),
        ``False`` if not.
    """
    return obj.is_couplet


def is_member_or_undef(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is either a member of the :term:`ground set` of this :term:`algebra`
        or :class:`~.Undef`.

     :return: ``True`` if ``obj`` is either a :term:`couplet` (an instance of :class:`~.Couplet`) or
        :class:`~.Undef`, ``False`` if not.
    """
    return obj.is_couplet or obj is _undef.Undef()


def is_absolute_member(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is a member of the :term:`absolute ground set` of this algebra.

    :type obj: _mo.MathObject|_mo.Couplet
    :return: ``True`` if ``obj`` is an :term:`absolute couplet`, ``False`` if not.
    """
    if not obj.is_couplet:
        # If known to not be a couplet, it's also not an absolute couplet. No further caching.
        return False
    # From this point on, `obj` is known to be a couplet.
    if obj.cached_absolute == CacheStatus.UNKNOWN:
        is_absolute_couplet = obj.left.is_atom and obj.right.is_atom
        obj.cache_absolute(CacheStatus.from_bool(is_absolute_couplet))
    return obj.cached_is_absolute


# --------------------------------------------------------------------------------------------------
# Related operations, not formally part of the algebra.

def is_reflexive(couplet: '(M x M)', _checked=True) -> bool:
    """Return whether ``couplet`` is reflexive.

    :return: ``True`` if ``couplet`` is :term:`reflexive`, ``False`` if it is not, or `Undef()` if
        ``couplet`` is not a :term:`couplet`.
    """
    if _checked:
        if not is_member(couplet):
            return _undef.make_or_raise_undef2(couplet)
    else:
        assert is_member_or_undef(couplet)
        if couplet is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    if couplet.cached_reflexive == CacheStatus.UNKNOWN:
        reflexive = (couplet.left == couplet.right)
        couplet.cache_reflexive(CacheStatus.from_bool(reflexive))
    return couplet.cached_reflexive == CacheStatus.IS
