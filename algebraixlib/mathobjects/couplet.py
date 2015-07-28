"""Provide the class :class:`~.Couplet`; it represents a :term:`couplet`."""

# $Id: couplet.py 22702 2015-07-28 20:20:56Z jaustell $
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
import algebraixlib.structure as _structure
import algebraixlib.util.miscellaneous as _misc

from algebraixlib.mathobjects.atom import auto_convert
from algebraixlib.mathobjects.mathobject import MathObject


# --------------------------------------------------------------------------------------------------

class Couplet(MathObject):
    """A :term:`couplet` containing a :term:`left component` and a :term:`right component`."""

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
        super().__init__()
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
        self._flags._not_relation = True
        self._flags._not_clan = True
        self._flags._not_multiclan = True

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

    def is_reflexive(self) -> bool:
        """Return whether this :term:`couplet` is :term:`reflexive`."""
        return self.left == self.right

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
        """A value-based comparison for less than. Return ``True`` if ``self < other``."""
        return not isinstance(other, Couplet) or (repr(self) < repr(other))

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
