"""Provide the class :class:`~.Couplet`; it represents a :term:`couplet`."""

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

import algebraixlib.structure as _structure
import algebraixlib.undef as _undef
import algebraixlib.util.miscellaneous as _misc
from algebraixlib.tmp_sqlda_op import tmp_sqlda_op

from .atom import auto_convert
from .mathobject import MathObject
from ..cache_status import CacheStatus
from ._flags import Flags as _Flags


# --------------------------------------------------------------------------------------------------

def _init_cache() -> int:
    """Initialization function for `Couplet._INIT_CACHE`."""
    flags = _Flags()
    # Known to be true:
    flags.f.couplet = CacheStatus.IS
    # Known to be false:
    flags.f.atom = CacheStatus.IS_NOT
    flags.f.set = CacheStatus.IS_NOT
    flags.f.relation = CacheStatus.IS_NOT
    flags.f.clan = CacheStatus.IS_NOT
    flags.f.multiset = CacheStatus.IS_NOT
    flags.f.multiclan = CacheStatus.IS_NOT
    # Known to be undefined/not apply:
    flags.f.functional = CacheStatus.N_A
    flags.f.right_functional = CacheStatus.N_A
    flags.f.regular = CacheStatus.N_A
    flags.f.symmetric = CacheStatus.N_A
    flags.f.transitive = CacheStatus.N_A
    return flags.asint


@tmp_sqlda_op(True)
def make_couplet(*args):
    """Factory wrapper to create a :class:`~.Couplet`."""
    for arg in args:
        if arg is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    return Couplet(*args)


@tmp_sqlda_op(True)
def make_couplet_unchecked(*args):
    """Factory wrapper to create a :class:`~.Couplet` (unchecked version)."""
    for arg in args:
        if arg is _undef.Undef():
            return _undef.make_or_raise_undef(2)
    return Couplet(*args, direct_load=True)


@_functools.total_ordering
class Couplet(MathObject):
    """A :term:`couplet` containing a :term:`left component` and a :term:`right component`."""

    _INIT_CACHE = _init_cache()

    def __init__(self, left, right=None, direct_load=False):
        """
        :param left: The :term:`left component` of the couplet, and the default value for the
            :term:`right component` (see ``right``). If this argument is not a `MathObject`, it is
            converted into an :class:`~.Atom`.
        :param right: (Optional) The :term:`right component` of the couplet. If this argument is
            not a `MathObject`, it is converted into an :class:`~.Atom`. If this argument is
            missing, the value of ``left`` is used and a :term:`reflexive` couplet where
            :term:`left` and :term:`right` are the same is created.
        :param direct_load: (Optional) Set to ``True`` if you know that both ``left`` and ``right``
            are instances of `MathObject`.
        """
        super().__init__(self._INIT_CACHE)
        if direct_load:
            assert isinstance(left, MathObject)
            self._left = left
            if right is None:
                self._right = self._left
            else:
                assert isinstance(right, MathObject)
                self._right = right
        else:
            self._left = auto_convert(left)
            if right is None:
                self._right = self._left
            else:
                self._right = auto_convert(right)
        self._hash = 0

    # ----------------------------------------------------------------------------------------------
    # Characteristics of the instance.

    @property
    def left(self) -> '( M )':
        """Read-only property; return the :term:`left component` of this instance."""
        return self._left

    @property
    def right(self) -> '( M )':
        """Read-only property; return the :term:`right component` of this instance."""
        return self._right

    def get_ground_set(self) -> _structure.Structure:
        """Return the :term:`ground set` of the lowest-level algebra of ``self``.
        """
        return _structure.CartesianProduct(
            self.left.get_ground_set(), self.right.get_ground_set())

    # ----------------------------------------------------------------------------------------------
    # (Python-)Special functions.

    def __eq__(self, other):
        """A value-based comparison for equality. Return ``True`` if type and both members match."""
        return isinstance(other, Couplet) \
            and (self.left == other.left) and (self.right == other.right)

    def __ne__(self, other):
        """A value-based comparison for inequality. Return ``True`` if type or members don't match.
        """
        return not isinstance(other, Couplet) \
            or (self.left != other.left) or (self.right != other.right)

    def __lt__(self, other):
        """A value-based comparison for less than. Return ``True`` if ``self < other``.

        This implementation must be aligned with `__eq__`; an object must not be equal to and less
        than another object at the same time.

        :return Normally a `bool` (`True` if ``self`` is less than ``other``), or `NotImplemented`
            if the types can't be compared.
        """
        if not isinstance(other, MathObject):
            return NotImplemented
        if other.is_couplet:
            return repr(self) < repr(other)
        else:
            return super()._less_than(other)

    def __hash__(self):
        """Return a hash based on the value that is calculated on demand and cached."""
        if not self._hash:
            self._hash = _misc.get_hash(
                'algebraixlib.mathobjects.couplet.Couplet', self.left, self.right)
        return self._hash

    def __repr__(self):
        """Return the instance's code representation."""
        return 'Couplet(left={left}, right={right})'.format(
            left=repr(self.left), right=repr(self.right))

    def __str__(self):
        """Return the instance's string representation."""
        return '({left}->{right})'.format(left=str(self.left), right=str(self.right))
