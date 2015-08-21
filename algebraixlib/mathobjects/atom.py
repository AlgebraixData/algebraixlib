r"""Provide the class :class:`Atom` that represents :term:`atom`\s and the function
:func:`auto_convert` that passes through instances of `MathObject`\s and converts other types into
:class:`Atom` instances.
"""

<<<<<<< HEAD
# $Id: atom.py 22803 2015-08-14 17:08:50Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-08-14 12:08:50 -0500 (Fri, 14 Aug 2015) $
=======
# $Id: atom.py 22702 2015-07-28 20:20:56Z jaustell $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-28 15:20:56 -0500 (Tue, 28 Jul 2015) $
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
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

<<<<<<< HEAD
from .mathobject import MathObject
from .utils import CacheStatus
from ._flags import Flags as _Flags
=======
from algebraixlib.mathobjects.mathobject import MathObject
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272


# --------------------------------------------------------------------------------------------------

def auto_convert(arg):
    """Return always a `MathObject`. If ``arg`` is not a `MathObject`, make it an :class:`Atom`.

    This function is used in several constructors as convenience wrapper to allow the creation of
    `MathObject` instances from non-`MathObject` values.
    """
    return arg if isinstance(arg, MathObject) else Atom(arg)


<<<<<<< HEAD
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


=======
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
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
<<<<<<< HEAD
        # pylint: disable=unused-argument
=======
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
        if isinstance(value, Atom):
            return value
        return super().__new__(cls)

<<<<<<< HEAD
    _INIT_CACHE = _init_cache()

=======
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
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

<<<<<<< HEAD
        super().__init__(self._INIT_CACHE)
=======
        super().__init__()
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272

        if direct_load:
            assert not isinstance(value, MathObject)
        else:
            if isinstance(value, MathObject):
                raise TypeError("'value' must not be a MathObject")
        self._value = value
        self._hash = _get_hash('algebraixlib.mathobjects.atom.Atom', self._value)
<<<<<<< HEAD
=======
        self._flags._not_relation = True
        self._flags._not_clan = True
        self._flags._not_multiclan = True
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272

    # ----------------------------------------------------------------------------------------------
    # Characteristics of the instance.

    @property
    def value(self) -> '( A )':
        """Read-only; return the value of this instance. Is always a member of :term:`set A`."""
        return self._value

    def get_ground_set(self) -> _structure.Structure:
        """Return the :term:`ground set` of the lowest-level algebra of ``self``. Is always
        :math:`A`.
        """
        return _structure.GenesisSetA()

    # ----------------------------------------------------------------------------------------------
    # (Python-)Special functions.

    def __eq__(self, other):
        """A value-based comparison for equality. Return ``True`` if types and values match.

<<<<<<< HEAD
        Type-matching follows Python rules, so ``not Atom(1) == Atom(1.0)``.
        """
        return (isinstance(other, Atom)
                and isinstance(other.value, type(self.value))
                and other.value == self.value)
=======
        Type-matching follows Python rules, so ``Atom(1) != Atom(1.0)``.
        """
        return (isinstance(other, Atom) and isinstance(
            other.value, type(self.value)) and other.value == self.value)
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272

    def __ne__(self, other):
        """A value-based comparison for inequality. Return ``True`` if types or values don't match.

        Type-matching follows Python rules, so ``Atom(1) != Atom(1.0)``.
        """
<<<<<<< HEAD
        return (not isinstance(other, Atom)
                or not isinstance(other.value, type(self.value))
                or other.value != self.value)
=======
        return (not isinstance(other, Atom) or not isinstance(
            other.value, type(self.value)) or other.value != self.value)
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272

    def __lt__(self, other):
        """A value-based comparison for less than. Return ``True`` if ``self < other``."""
        return not isinstance(other, Atom) or (repr(self.value) < repr(other.value))

    def __hash__(self):
        """Return a hash based on the value calculated during construction."""
        return self._hash

    def __repr__(self):
        """Return the instance's code representation."""
        return 'Atom({value})'.format(value=repr(self._value))

    def __str__(self):
        """Return the instance's string representation."""
        return repr(self._value)
