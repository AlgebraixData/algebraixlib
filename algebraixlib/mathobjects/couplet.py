"""A math object that represents a couplet."""

# $Id: couplet.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import algebraixlib.structure as _structure
from algebraixlib.util.miscellaneous import get_hash as _get_hash

from algebraixlib.mathobjects.atom import auto_convert
from algebraixlib.mathobjects.mathobject import MathObject


class Couplet(MathObject):
    """A couplet, consisting of a 'left component' `MathObject` and a 'right' `MathObject`."""

    def __init__(self, left, right=None, direct_load=False):
        """Construct an instance, consisting of two `MathObject` instances ``left`` and
        ``right``.

        If either of the arguments is not a `MathObject`, make it an :class:`~.Atom` with the
        argument as value.
        """
        super().__init__()
        if direct_load:
            assert isinstance(left, MathObject)
            assert isinstance(right, MathObject)
            self._left = left
            self._right = right
        else:
            self._left = auto_convert(left)
            self._right = auto_convert(right)
        self._hash = 0

    @property
    def left(self):
        """Read-only property; return the left component of this instance."""
        return self._left

    @property
    def right(self):
        """Read-only property; return the right of this instance."""
        return self._right

    def get_ground_set(self):
        """Return the ground set of the lowest-level algebra of this `MathObject`.
        """
        return _structure.CartesianProduct(
            self.left.get_ground_set(), self.right.get_ground_set())

    def is_reflexive(self):
        """Return ``True`` if this :class:`Couplet` is reflexive.

        Reflexive means that left and right are equal.
        """
        return self.left == self.right

    def is_symmetric(self):
        """Return ``True`` if this :class:`Couplet` is symmetric.

        Reflexive means that left and right are equal.
        """
        return self.left == self.right

    def get_repr(self):
        """Return the instance's code representation."""
        return 'Couplet(left={left}, right={right})'.format(
            left=repr(self.left), right=repr(self.right))

    def get_str(self):
        """Return the instance's string representation (the string representation of the value)."""
        return '({left}->{right})'.format(left=str(self.left), right=str(self.right))

    # ----------------------------------------------------------------------------------------------

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
            self._hash = _get_hash('algebraixlib.mathobjects.couplet.Couplet', self.left, self.right)
        return self._hash

    def __repr__(self):
        """Return the instance's code representation."""
        return self.get_repr()

    def __str__(self):
        """Return the instance's string representation."""
        return self.get_str()
