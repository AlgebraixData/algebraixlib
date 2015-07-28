"""This package-private module contains the class ``Flags`` that is used to cache certain properties
of ``MathObject``s. This code is internal and transient."""

# $Id: _flags.py 22687 2015-07-27 17:43:05Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-27 12:43:05 -0500 (Mon, 27 Jul 2015) $
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
