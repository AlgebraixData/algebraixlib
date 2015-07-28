"""This module contains the :term:`algebra of couplets` and related functionality."""

# $Id: couplets.py 22702 2015-07-28 20:20:56Z jaustell $
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
import algebraixlib.mathobjects as _mo
import algebraixlib.structure as _structure
from algebraixlib.undef import make_or_raise_undef as _make_or_raise_undef


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
                return _make_or_raise_undef()
        else:
            assert is_member(couplet)
        return _mo.Couplet(left=couplet.right, right=couplet.left, direct_load=True)

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
                return _make_or_raise_undef()
            if not is_member(couplet2):
                return _make_or_raise_undef()
        else:
            assert is_member(couplet1)
            assert is_member(couplet2)
        if couplet1.left != couplet2.right:
            return _make_or_raise_undef(2)
        return _mo.Couplet(left=couplet2.left, right=couplet1.right, direct_load=True)


# For convenience, make the members of class Algebra (they are all static functions) available at
# the module level.

#: Convenience redirection to `Algebra.transpose`.
transpose = Algebra.transpose
#: Convenience redirection to `Algebra.compose`.
compose = Algebra.compose


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

     :return: ``True`` if ``obj`` is an instance of :class:`~.Couplet`, ``False`` if not.
    """
    _mo.raise_if_not_mathobject(obj)
    return isinstance(obj, _mo.Couplet)


def is_absolute_member(obj: _mo.MathObject) -> bool:
    """Return whether ``obj`` is a member of the :term:`absolute ground set` of this algebra.

     :return: ``True`` if ``obj`` is an :term:`absolute couplet`, ``False`` if not.

    .. note:: This function calls :meth:`~.MathObject.get_ground_set` on ``obj``.
    """
    _mo.raise_if_not_mathobject(obj)
    return obj.get_ground_set().is_subset(get_absolute_ground_set())
