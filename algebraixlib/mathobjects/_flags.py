"""This package-private module contains the class ``Flags`` that is used to cache certain properties
of ``MathObject``s. This code is internal and transient."""

<<<<<<< HEAD
# $Id: _flags.py 22803 2015-08-14 17:08:50Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-08-14 12:08:50 -0500 (Fri, 14 Aug 2015) $
=======
# $Id: _flags.py 22687 2015-07-27 17:43:05Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-27 12:43:05 -0500 (Mon, 27 Jul 2015) $
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
import ctypes as _ctypes

<<<<<<< HEAD
from .utils import CacheStatus


# --------------------------------------------------------------------------------------------------

# noinspection PyAttributeOutsideInit
class _Bitfields(_ctypes.Structure):
    """A class that represents a C-style structure composed of bitfields.

    Each member in ``_fields_`` is a 2-bit bitfield. Each bitfield has an explicit setter and
    getter. The possible values for the bitfields are the members of `~utils.CacheStatus`
    (`UNKNOWN`, `IS`, `IS_NOT` or `N_A`). The bitfields may only change if their value is
    `UNKNOWN`; any other value makes the bitfield immutable. (The setters make sure of that; see
    ``_setter_helper``.)
    """
    # pylint: disable=too-many-instance-attributes, missing-docstring
    # pylint: disable=attribute-defined-outside-init

    #: `FIELDS` contains the names of the fields in this cache. The names start with an underscore,
    #: to indicate that they are private and should only be accessed through their accessors.
    FIELDS = [
        # pylint: disable=bad-continuation
        # These four are used to indicate the type. They only use two states and could be 1 bit.
        '_atom',                #: Is an Atom. Used as 2-state flag.
        '_couplet',             #: Is a member of couplets (is a Couplet). Used as 2-state flag.
        '_set',                 #: Is a member of sets (is a Set). Used as 2-state flag.
        '_multiset',            #: Is a member of multisets (is a Multiset). Used as 2-state flag.

        # The remainder use all four states.
                                # Algebra membership:
        '_relation',            #: Is a member of relations (is a Set of Couplets).
        '_clan',                #: Is a member of clans (is a Set of Sets of Couplets).
        '_multiclan',           #: Is a member of multiclans (is a Multiset of Sets of Couplets).
        '_absolute',            #: Is absolute (the lowest part of the definition has only Atoms).
                                # Relation properties (relations, clans, multiclans):
        '_functional',          #: Is functional.
        '_right_functional',    #: Is right-functional.
        '_reflexive',           #: Is reflexive (also couplets).
        '_symmetric',           #: Is symmetric.
        '_transitive',          #: Is transitive.
                                # Clan properties (clans, multiclans):
        '_regular',             #: Is regular.
        '_right_regular',       #: Is right-regular.
    ]

    #: The definition of the members of the (C-style) struct that holds the data of this class.
    #: Every bitfield contains 2 bits (4 states).
    _fields_ = [(name, _ctypes.c_uint8, 2) for name in FIELDS]

    @staticmethod
    def _setter_helper(flags, value: int) -> int:
        assert flags == CacheStatus.UNKNOWN or flags == value
        assert 0 <= value <= 3
        return value

    @property
    def atom(self) -> int:
        return self._atom

    @atom.setter
    def atom(self, value: int):
        self._atom = self._setter_helper(self._atom, value)

    @property
    def couplet(self) -> int:
        return self._couplet

    @couplet.setter
    def couplet(self, value: int):
        self._couplet = self._setter_helper(self._couplet, value)

    @property
    def set(self) -> int:
        return self._set

    @set.setter
    def set(self, value: int):
        self._set = self._setter_helper(self._set, value)

    @property
    def multiset(self) -> int:
        return self._multiset

    @multiset.setter
    def multiset(self, value: int):
        self._multiset = self._setter_helper(self._multiset, value)

    @property
    def relation(self) -> int:
        return self._relation

    @relation.setter
    def relation(self, value: int):
        self._relation = self._setter_helper(self._relation, value)

    @property
    def clan(self) -> int:
        return self._clan

    @clan.setter
    def clan(self, value: int):
        self._clan = self._setter_helper(self._clan, value)

    @property
    def multiclan(self) -> int:
        return self._multiclan

    @multiclan.setter
    def multiclan(self, value: int):
        self._multiclan = self._setter_helper(self._multiclan, value)

    @property
    def absolute(self) -> int:
        return self._absolute

    @absolute.setter
    def absolute(self, value: int):
        self._absolute = self._setter_helper(self._absolute, value)

    @property
    def functional(self) -> int:
        return self._functional

    @functional.setter
    def functional(self, value: int):
        self._functional = self._setter_helper(self._functional, value)

    @property
    def right_functional(self) -> int:
        return self._right_functional

    @right_functional.setter
    def right_functional(self, value: int):
        self._right_functional = self._setter_helper(self._right_functional, value)

    @property
    def reflexive(self) -> int:
        return self._reflexive

    @reflexive.setter
    def reflexive(self, value: int):
        self._reflexive = self._setter_helper(self._reflexive, value)

    @property
    def symmetric(self) -> int:
        return self._symmetric

    @symmetric.setter
    def symmetric(self, value: int):
        self._symmetric = self._setter_helper(self._symmetric, value)

    @property
    def transitive(self) -> int:
        return self._transitive

    @transitive.setter
    def transitive(self, value: int):
        self._transitive = self._setter_helper(self._transitive, value)

    @property
    def regular(self) -> int:
        return self._regular

    @regular.setter
    def regular(self, value: int):
        self._regular = self._setter_helper(self._regular, value)

    @property
    def right_regular(self) -> int:
        return self._right_regular

    @right_regular.setter
    def right_regular(self, value: int):
        self._right_regular = self._setter_helper(self._right_regular, value)


class Flags(_ctypes.Union):
    """A type that works similarly to a C-style union. The contents can be accessed by either
    :attr:`f` (accesses the individual flags) or by :attr:`asint` (allows us to access all members
    as a single integer, for example for single-statement initialization).

    In order to make :attr:`asint` work with different byte orders, the best way for static
    initializations is to create a temp instance of `Flags`, set the appropriate flags,
    get the integer value and store it as static initialization value. This initialization value
    is then matched to the given system's byte order. The value itself changes with the byte
    order, but the initialization code doesn't. See the various ``_init_cache()`` functions.

    .. :attribute:: f

        Provide access to the `_Bitfields` member of this class (a C-style ``struct`` wrapped as
        Python class).

    .. :attribute:: asint

        Provide access to the bits and bytes in the `_Bitfields` member :attr:`f` as integer. Use
        this for two purposes: read to get the associated integer value of a `Flags` class in
        which you have set the desired bytes, and use it (in the constructor or after construction)
        to set the bits of the structure to a value that you have read before. Do not hardcode it
        to an integer value -- the meaning of that value is dependent on the byte order of the
        system.
    """
    # pylint: disable=too-few-public-methods

    # Define the type for the integer access to the structure (through `asint`) and make sure that
    # it is big enough to hold all values for the `_Bitfields` structure.
    asint_type = _ctypes.c_uint32
    assert _ctypes.sizeof(_Bitfields) <= _ctypes.sizeof(asint_type)

    #: The definition of the members of the (C-style) union that holds the data of this class.
    _fields_ = [('f', _Bitfields), ('asint', asint_type)]
=======

# noinspection PyAttributeOutsideInit
class Flags(_ctypes.Structure):
    """Each bit in ``_fields_`` is set when a ``MathObject`` "is known to be" what the bit's name
    indicates. If a bit is not set, this means that whether or not the ``MathObject`` has the given
    property is not known -- not that the given property is ``False``.

    For example, if the bit ``_clan`` (accessor ``clan``) is ``False``, this does not mean that the
    ``MathObject`` is not a clan, it means that it is not known whether it is a clan. If this bit
    is ``True``, it is known that the ``MathObject`` is a clan (and the corresponding bit
    ``_not_clan`` must not be also ``True``).
    """
    _fields_ = [(name, _ctypes.c_uint32, 1) for name in [
        "_relation", "_not_relation",
        "_clan", "_not_clan",
        "_multiclan", "_not_multiclan",
        "_functional", "_not_functional",
        "_right_functional", "_not_right_functional",
        "_regular", "_not_regular",
        "_reflexive", "_not_reflexive",
        "_symmetric", "_not_symmetric",
        "_transitive", "_not_transitive"
    ]]

    @property
    def not_relation(self) -> bool:
        return self._not_relation

    @property
    def relation(self) -> bool:
        return self._relation

    @relation.setter
    def relation(self, value: bool):
        if value:
            assert not self._not_relation
            self._relation = True
        else:
            assert not self._relation
            self._not_relation = True

    @property
    def not_clan(self) -> bool:
        return self._not_clan

    @property
    def clan(self) -> bool:
        return self._clan

    @clan.setter
    def clan(self, value: bool):
        if value:
            assert not self._not_clan
            self._clan = True
        else:
            assert not self._clan
            self._not_clan = True

    @property
    def not_multiclan(self) -> bool:
        return self._not_multiclan

    @property
    def multiclan(self) -> bool:
        return self._multiclan

    @multiclan.setter
    def multiclan(self, value: bool):
        if value:
            assert not self._not_multiclan
            self._multiclan = True
        else:
            assert not self._multiclan
            self._not_multiclan = True

    @property
    def not_functional(self) -> bool:
        return self._not_functional

    @property
    def functional(self) -> bool:
        return self._functional

    @functional.setter
    def functional(self, value: bool):
        if value:
            assert not self._not_functional
            self._functional = True
        else:
            assert not self._functional
            self._not_functional = True

    @property
    def not_right_functional(self) -> bool:
        return self._not_right_functional

    @property
    def right_functional(self) -> bool:
        return self._right_functional

    @right_functional.setter
    def right_functional(self, value: bool):
        if value:
            assert not self._not_right_functional
            self._right_functional = True
        else:
            assert not self._right_functional
            self._not_right_functional = True

    @property
    def not_regular(self) -> bool:
        return self._not_regular

    @property
    def regular(self) -> bool:
        return self._regular

    @regular.setter
    def regular(self, value: bool):
        if value:
            assert not self._not_regular
            self._regular = True
        else:
            assert not self._regular
            self._not_regular = True

    @property
    def not_reflexive(self) -> bool:
        return self._not_reflexive

    @property
    def reflexive(self) -> bool:
        return self._reflexive

    @reflexive.setter
    def reflexive(self, value: bool):
        if value:
            assert not self._not_reflexive
            self._reflexive = True
        else:
            assert not self._reflexive
            self._not_reflexive = True

    @property
    def not_symmetric(self) -> bool:
        return self._not_symmetric

    @property
    def symmetric(self) -> bool:
        return self._symmetric

    @symmetric.setter
    def symmetric(self, value: bool):
        if value:
            assert not self._not_symmetric
            self._symmetric = True
        else:
            assert not self._symmetric
            self._not_symmetric = True

    @property
    def not_transitive(self) -> bool:
        return self._not_transitive

    @property
    def transitive(self) -> bool:
        return self._transitive

    @transitive.setter
    def transitive(self, value: bool):
        if value:
            assert not self._not_transitive
            self._transitive = True
        else:
            assert not self._transitive
            self._not_transitive = True
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
