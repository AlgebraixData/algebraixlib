r"""Provide the class :class:`Atom` that represents :term:`atom`\s and the function
:func:`auto_convert` that passes through instances of `MathObject`\s and converts other types into
:class:`Atom` instances.
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
import functools as _functools

import algebraixlib.structure as _structure
from algebraixlib.util.miscellaneous import get_hash as _get_hash

from .mathobject import MathObject
from ..cache_status import CacheStatus
from ._flags import Flags as _Flags


# --------------------------------------------------------------------------------------------------

def auto_convert(arg):
    """Return always a `MathObject`. If ``arg`` is not a `MathObject`, make it an :class:`Atom`.

    This function is used in several constructors as convenience wrapper to allow the creation of
    `MathObject` instances from non-`MathObject` values.
    """
    return arg if isinstance(arg, MathObject) else Atom(arg)


def _init_cache() -> int:
    """Initialization function for `Atom._INIT_CACHE`."""
    flags = _Flags()
    # Known to be true:
    flags.f.atom = CacheStatus.IS
    flags.f.absolute = CacheStatus.IS
    # Known to be false:
    flags.f.couplet = CacheStatus.IS_NOT
    flags.f.set = CacheStatus.IS_NOT
    flags.f.relation = CacheStatus.IS_NOT
    flags.f.clan = CacheStatus.IS_NOT
    flags.f.multiset = CacheStatus.IS_NOT
    flags.f.multiclan = CacheStatus.IS_NOT
    # Known to be undefined/not apply:
    flags.f.functional = CacheStatus.N_A
    flags.f.right_functional = CacheStatus.N_A
    flags.f.regular = CacheStatus.N_A
    flags.f.reflexive = CacheStatus.N_A
    flags.f.symmetric = CacheStatus.N_A
    flags.f.transitive = CacheStatus.N_A
    return flags.asint


@_functools.total_ordering
class Atom(MathObject):
    """Represent a value (of a non-`MathObject`, hashable type) like numbers or strings.

    All instances of :class:`Atom` are members of :term:`set A` (:math:`A`), or conversely,
    :term:`set A` is the set of all instances of :class:`Atom`.

    .. note:: Instances of :class:`Atom` are immutable and hashable. Therefore they only accept
        immutable and hashable values.
    """

    def __new__(cls, value, direct_load=False):
        """If ``value`` is an instance of :class:`Atom`, reuse it.

        This mechanism is used to reduce the number of created :class:`Atom` instances. We then
        need to check in ``__init__`` whether we have an already initialized instance or still have
        to initialize it. ``__init__`` is always called after ``__new__``.

        :return: ``value`` if it is an instance of :class:`Atom` (in this case we simply reuse it).
            If not, follow the normal path for creating an instance.
        """
        # pylint: disable=unused-argument
        if isinstance(value, Atom):
            return value
        return super().__new__(cls)

    _INIT_CACHE = _init_cache()

    def __init__(self, value, direct_load=False):
        """
        :param value: The value of this instance. May not be an instance of `MathObject` other
            than :class:`Atom`. (If it is of type :class:`Atom`, the instance is re-used; see
            `__new__`.) ``value`` must be immutable and hashable.
        :param direct_load: Set to ``True`` if you can be sure that ``value`` is not an instance of
            `MathObject`. Default is ``False``.
        :raise: `TypeError` if ``value`` is not hashable.
        """
        # Check whether we received an already initialized instance (by __new__).
        if hasattr(self, '_value'):
            return

        super().__init__(self._INIT_CACHE)

        if direct_load:
            assert not isinstance(value, MathObject)
        else:
            if isinstance(value, MathObject):
                raise TypeError("'value' must not be a MathObject")
        self._value = value
        self._hash = _get_hash('algebraixlib.mathobjects.atom.Atom', self._value)

    # ----------------------------------------------------------------------------------------------
    # Characteristics of the instance.

    @property
    def value(self) -> '( A )':
        """Read-only; return the value of this instance. Is always a member of :term:`set A`."""
        return self._value

    @property
    def type(self):
        """Read-only; return the type of this instance."""
        return type(self._value)

    def get_ground_set(self) -> _structure.Structure:
        """Return the :term:`ground set` of the lowest-level algebra of ``self``. Is always
        :math:`A`.
        """
        return _structure.GenesisSetA()

    # ----------------------------------------------------------------------------------------------
    # (Python-)Special functions.

    def __eq__(self, other):
        """A value-based comparison for equality. Return ``True`` if types and values match.

        Type-matching follows Python rules, so ``not Atom(1) == Atom(1.0)``.
        """
        if isinstance(other, Atom):
            # NOTE: using the explicit type check vs isinstance(other.value, type(self.value)
            # ..to prevent True being compared equal to 1..ie isinstance(True, type(1)) == True
            if other.type != self.type:
                return False
            return other.value == self.value
        return NotImplemented

    def __ne__(self, other):
        """A value-based comparison for inequality. Return ``True`` if types or values don't match.

        Type-matching follows Python rules, so ``Atom(1) != Atom(1.0)``.
        """
        if isinstance(other, Atom):
            # NOTE: using the explicit type check vs isinstance(other.value, type(self.value)
            # ..to prevent True being compared equal to 1..ie isinstance(True, type(1)) == True
            # noinspection PyPep8
            if type(other.value) != type(self.value):
                return True
            return other.value != self.value
        return NotImplemented

    # noinspection PyUnresolvedReferences
    def __lt__(self, other):
        """A value-based comparison for less than. Return ``True`` if ``self < other``.

        This implementation must be aligned with `__eq__`; an object must not be equal to and less
        than another object at the same time.

        :return Normally a `bool` (`True` if ``self`` is less than ``other``), or `NotImplemented`
            if the types can't be compared.
        """
        if not isinstance(other, MathObject):
            return NotImplemented
        if other.is_atom:
            try:
                if self.type == other.type:
                    return self.value < other.value
            except TypeError:
                pass
            return repr(self.value) < repr(other.value)
        else:
            return super()._less_than(other)

    def __hash__(self):
        """Return a hash based on the value calculated during construction."""
        return self._hash

    def __repr__(self):
        """Return the instance's code representation."""
        return 'Atom({value})'.format(value=repr(self._value))

    def __str__(self):
        """Return the instance's string representation."""
        return repr(self._value)

    def __getnewargs__(self):
        """Necessary to allow Atom to be pickled"""
        return Atom.__repr__(self),
