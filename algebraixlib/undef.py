r"""Facilities for representing and working with the concept of "undefined".

Most operations are not defined for all types of data: :term:`set` operations may not be defined on
:term:`couplet`\s, :term:`multiset` operations may not be defined on sets, and so on. When an
operation is not defined for a given input, it returns the singleton `Undef()`. This return value
can then be taken into account by the caller. In some cases it is an error, in other cases the
result is simply ignored.
"""

# $Id: undef.py 22691 2015-07-27 22:46:23Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-27 17:46:23 -0500 (Mon, 27 Jul 2015) $
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


class Undef:
    """A singleton class that represents the concept of "undefined".

    Instances of this class are not treated as a value by the operations in this library;
    specifically, it will never appear as the value of an :class:`~.Atom`.
    """
    _instance = None

    def __new__(cls):
        """Override ``__new__`` to create a singleton class."""
        if Undef._instance is None:
            Undef._instance = super().__new__(cls)
        return Undef._instance

    def __eq__(self, other):
        """Prevent comparisons on Undef; raise a TypeError."""
        raise TypeError("== is not supported by Undef")

    def __ne__(self, other):
        """Prevent comparisons on Undef; raise a TypeError."""
        raise TypeError("!= is not supported by Undef")

    def __bool__(self):
        """Prevent comparisons on Undef; raise a TypeError."""
        raise TypeError("Boolean conversion is not supported by Undef")

    def __repr__(self):
        """Return the instance's code representation."""
        return 'Undef()'

    def __str__(self):
        """Return the instance's string representation."""
        return 'undef'


class RaiseOnUndef:
    """Manage the level for `make_or_raise_undef`. Implemented as static class."""

    #: The 'normal' level.
    _reset_level = 0
    #: The current level.
    _level = _reset_level

    def __init__(self):
        raise AssertionError("Don't instantiate RaiseOnUndef class. Use it as a static class only.")

    @staticmethod
    def get_level():
        """Return the current level for raising an `UndefException`.

        The exception is raised if the ``level`` argument of `make_or_raise_undef` is less than or
        equal to the value returned here.
        """
        return RaiseOnUndef._level

    @staticmethod
    def set_level(temp_value):
        """Set the level for raising an `UndefException` temporarily to ``temp_value``."""
        RaiseOnUndef._level = temp_value

    @staticmethod
    def reset():
        """Reset the level for raising an `UndefException` back to its initial value."""
        RaiseOnUndef._level = RaiseOnUndef._reset_level


class UndefException(Exception):
    """This exception is raised when the ``level`` argument of `make_or_raise_undef` is less than or
    equal to the `RaiseOnUndef` level."""
    pass


def make_or_raise_undef(level=1):
    """Raise `UndefException` if ``level`` is less than or equal to the `RaiseOnUndef` level,
    otherwise return `Undef()`.

    :param level: An integer >= 1. Default is 1.

    .. note:: Use 1 (or no argument) for the cases that are most likely to be errors (like wrong
        argument types). Use higher numbers for cases that may return `Undef()` on purpose.
    """
    if level <= RaiseOnUndef.get_level():
        raise UndefException("Result is undefined. See also 'undef.RaiseOnUndef'.")
    return Undef()
