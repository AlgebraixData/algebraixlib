"""An atomic math object that represents a value."""

# $Id: atom.py 22614 2015-07-15 18:14:53Z gfiedler $
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

from algebraixlib.mathobjects.mathobject import MathObject


def auto_convert(arg):
    """Return always a `MathObject`. If ``arg`` is not a `MathObject`, make it an :class:`Atom`.

    This function is used in several constructors as convenience wrapper to allow the creation of
    `MathObject` instances from non-`MathObject` values.
    """
    return arg if isinstance(arg, MathObject) else Atom(arg)


class Atom(MathObject):
    """An atomic math object. It represents a value (of a non-`MathObject`, hashable type).

    .. note:: Instances of :class:`Atom` are considered immutable. Therefore they only accept
        immutable values. Since an :class:`Atom` also needs to be hashable, the value itself also
        needs to be hashable.
    """

    def __new__(cls, value, direct_load=False):
        """If ``value`` is an :class:`Atom`, return that :class:`Atom`, else return a new
        :class:`Atom` initialized with ``value``.

        .. note:: This is used to reduce the number of created :class:`Atom` instances, but doesn't
            make the check in ``__init__`` unnecessary. ``__init__`` is always called after
            `__new__`.
        """
        if not direct_load and isinstance(value, Atom):
            return value
        return super().__new__(cls)

    def __init__(self, value, direct_load=False):
        """Construct an instance with the given ``value``.

        :param value: The value of the :class:`Atom`. May not be an instance of `MathObject` other
            than :class:`Atom`. (If it is of type :class:`Atom`, this :class:`Atom` is used.) The
            ``value`` must be immutable and hashable.
        """
        if hasattr(self, '_value'):
            return  # Already initialized
        super().__init__()

        if direct_load:
            assert not isinstance(value, MathObject)
        else:
            if isinstance(value, MathObject):
                raise TypeError("'value' must not be a MathObject")
        self._value = value
        # NOTE: Non-hashable values will generate TypeError..including Undef()
        self._hash = _get_hash('algebraixlib.mathobjects.atom.Atom', self._value)

    @property
    def value(self):
        """Read-only; return the value of this instance."""
        return self._value

    def get_ground_set(self):
        """Return the ground set of the lowest-level algebra of this `MathObject`. Is always
        :math:`A`.
        """
        return _structure.GenesisSetA()

    def get_repr(self):
        """Return the instance's code representation."""
        return 'Atom({value})'.format(value=repr(self._value))

    def get_str(self):
        """Return the instance's string representation (the string representation of the value)."""
        return repr(self._value)

    # ----------------------------------------------------------------------------------------------

    def __eq__(self, other):
        """A value-based comparison for equality. Return ``True`` if types and values match.
        NOTE: Atom(1) != Atom(1.0)
        """
        return (isinstance(other, Atom) and isinstance(other.value, type(self.value))
                and other.value == self.value)

    def __ne__(self, other):
        """A value-based comparison for inequality. Return ``True`` if types or values don't match.
        NOTE: Atom(1) != Atom(1.0)
        """
        return (not isinstance(other, Atom) or not isinstance(other.value, type(self.value))
                or other.value != self.value)

    def __lt__(self, other):
        """A value-based comparison for less than. Return ``True`` if ``self < other``."""
        return not isinstance(other, Atom) or (repr(self.value) < repr(other.value))

    def __hash__(self):
        """Return a hash based on the value calculated during construction."""
        return self._hash

    def __repr__(self):
        """Return the instance's code representation."""
        return self.get_repr()

    def __str__(self):
        """Return the instance's string representation."""
        return self.get_str()
