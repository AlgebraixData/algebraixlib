r"""Facilities for representing and working with the concept of "undefined".

Most operations are not defined for all types of data: :term:`set` operations may not be defined on
:term:`couplet`\s, :term:`multiset` operations may not be defined on sets, and so on. When an
operation is not defined for a given input, it returns the singleton `Undef()`. This return value
can then be taken into account by the caller. In some cases it is an error, in other cases the
result is simply ignored.
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
from algebraixlib.tmp_sqlda_op import tmp_sqlda_op
from .cache_status import CacheStatus


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

    # ----------------------------------------------------------------------------------------------
    # Property cache functions.

    # Indicate MathObject type (2-state binary logic).

    @property
    def is_atom(self) -> bool:
        """Return ``False`` since :class:`~.Undef` is not an :class:`~.Atom`."""
        return False

    @property
    def is_couplet(self) -> bool:
        """Return ``False`` since :class:`~.Undef` is not a :class:`~.Couplet`."""
        return False

    @property
    def is_multiset(self) -> bool:
        """Return ``False`` since :class:`~.Undef` is not a :class:`~.Multiset`."""
        return False

    @property
    def is_set(self) -> bool:
        """Return ``False`` since :class:`~.Undef` is not a :class:`~.Set`."""
        return False

    # Indicate algebra membership.

    @property
    def cached_relation(self) -> int:
        """Return the cached state of being a :term:`relation`. See [PropCache]_."""
        return CacheStatus.IS_NOT

    @property
    def cached_is_relation(self) -> bool:
        """Return ``False`` since ``self`` is known not to be a :term:`relation`.
        See [PropCache]_."""
        return False

    @property
    def cached_is_not_relation(self) -> bool:
        """Return ``True`` since ``self`` is known not to be a :term:`relation`.
        See [PropCache]_."""
        return True

    @property
    def cached_clan(self) -> int:
        """Return the cached state of being a :term:`clan`. See [PropCache]_."""
        return CacheStatus.IS_NOT

    @property
    def cached_is_clan(self) -> bool:
        """Return ``False`` since ``self`` is known not to be a :term:`clan`. See [PropCache]_."""
        return False

    @property
    def cached_is_not_clan(self) -> bool:
        """Return ``True`` since ``self`` is known not to be a :term:`clan`. See [PropCache]_."""
        return True

    @property
    def cached_multiclan(self) -> int:
        """Return the cached state of being a :term:`multiclan`. See [PropCache]_."""
        return CacheStatus.IS_NOT

    @property
    def cached_is_multiclan(self) -> bool:
        """Return ``False`` since ``self`` is known to not be a :term:`multiclan`.
        See [PropCache]_."""
        return False

    @property
    def cached_is_not_multiclan(self) -> bool:
        """Return ``True`` since ``self`` is known not to be a :term:`multiclan`.
        See [PropCache]_."""
        return True

    @property
    def cached_absolute(self) -> int:
        """Return the cached state of being :term:`absolute`. See [PropCache]_.

        .. note:: Keep in mind that this does not tell you what kind of absolute algebra member
            this is. For example, an absolute :term:`relation` is a non-absolute :term:`set`.
        """
        return CacheStatus.IS_NOT

    @property
    def cached_is_absolute(self) -> bool:
        """Return ``False`` since ``self`` is known not to be :term:`absolute`. See [PropCache]_.

        .. note:: Keep in mind that this does not tell you what kind of absolute algebra member
            this is known to be. For example, an absolute :term:`relation` is a non-absolute
            :term:`set`.
        """
        return False

    @property
    def cached_is_not_absolute(self) -> bool:
        """Return ``True`` since ``self`` is known not to be :term:`absolute`. See [PropCache]_.

        .. note:: Keep in mind that this does not tell you what kind of absolute algebra member
            this is known not to be. For example, an absolute :term:`relation` is a non-absolute
            :term:`set`.
        """
        return True

    # Relation properties (defined on relations, clans, multiclans).

    @property
    def cached_functional(self) -> int:
        """Return the cached state of being :term:`functional`. See [PropCache]_."""
        return CacheStatus.N_A

    @property
    def cached_is_functional(self) -> bool:
        """Return ``False`` since :term:`functional` does not apply. See [PropCache]_."""
        return False

    @property
    def cached_is_not_functional(self) -> bool:
        """Return ``False`` since :term:`functional` does not apply. See [PropCache]_."""
        return False

    @property
    def cached_right_functional(self) -> int:
        """Return the cached state of being :term:`right-functional`. See [PropCache]_."""
        return CacheStatus.N_A

    @property
    def cached_is_right_functional(self) -> bool:
        """Return ``False`` since :term:`right-functional` does not apply. See [PropCache]_."""
        return False

    @property
    def cached_is_not_right_functional(self) -> bool:
        """Return ``False`` since :term:`right-functional` does not apply. See [PropCache]_."""
        return False

    @property
    def cached_reflexive(self) -> int:
        """Return the cached state of being :term:`reflexive`. See [PropCache]_."""
        return CacheStatus.N_A

    @property
    def cached_is_reflexive(self) -> bool:
        """Return ``False`` since :term:`reflexive` does not apply. See [PropCache]_."""
        return False

    @property
    def cached_is_not_reflexive(self) -> bool:
        """Return ``False`` since :term:`reflexive` does not apply. See [PropCache]_."""
        return False

    @property
    def cached_symmetric(self) -> int:
        """Return the cached state of being :term:`symmetric`. See [PropCache]_."""
        return CacheStatus.N_A

    @property
    def cached_is_symmetric(self) -> bool:
        """Return ``False`` since :term:`symmetric` does not apply. See [PropCache]_."""
        return False

    @property
    def cached_is_not_symmetric(self) -> bool:
        """Return ``False`` since :term:`symmetric` does not apply. See [PropCache]_."""
        return False

    @property
    def cached_transitive(self) -> int:
        """Return the cached state of being :term:`transitive`. See [PropCache]_."""
        return CacheStatus.N_A

    @property
    def cached_is_transitive(self) -> bool:
        """Return ``False`` since :term:`transitive` does not apply. See [PropCache]_."""
        return False

    @property
    def cached_is_not_transitive(self) -> bool:
        """Return ``False`` since :term:`transitive` does not apply. See [PropCache]_."""
        return False

    # Clan properties (defined on clans, multiclans).

    @property
    def cached_regular(self) -> int:
        """Return the cached state of being :term:`regular`. See [PropCache]_."""
        return CacheStatus.N_A

    @property
    def cached_is_regular(self) -> bool:
        """Return ``False`` since :term:`regular` does not apply. See [PropCache]_."""
        return False

    @property
    def cached_is_not_regular(self) -> bool:
        """Return ``False`` since :term:`regular` does not apply. See [PropCache]_."""
        return False

    @property
    def cached_right_regular(self) -> int:
        """Return the cached state of being :term:`right-regular`. See [PropCache]_."""
        return CacheStatus.N_A

    @property
    def cached_is_right_regular(self) -> bool:
        """Return ``False`` since :term:`right-regular` does not apply. See [PropCache]_."""
        return False

    @property
    def cached_is_not_right_regular(self) -> bool:
        """Return ``False`` since :term:`right-regular` does not apply. See [PropCache]_."""
        return False


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


def make_or_raise_undef2(obj):
    """Raise `UndefException` if ``level`` is less than or equal to the `RaiseOnUndef` level,
    otherwise return `Undef()`.

    :param obj: Causes ``level`` argument to `make_or_raise_undef` to be 2 if `Undef()`
    """
    if obj is Undef():
        return make_or_raise_undef(2)
    return make_or_raise_undef()


@tmp_sqlda_op(True)
def make_undef():
    """Return `Undef()`. Used where a hashable instance that evaluates to `Undef()` is needed."""
    return Undef()
