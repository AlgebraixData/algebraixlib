"""This module contains """

# $Id: flags.py 22614 2015-07-15 18:14:53Z gfiedler $
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
from ctypes import c_uint32, Structure


class Flags(Structure):
    """The bits only convey information if they are True...False only indicates not initialized.
    For instance to determine if a Set() is a Clan use "Set().is_clan()".  To verify that a Set() is
    not a clan do not use "not Set().is_clan()", but instead use Set().is_not_clan()
    """
    _fields_ = [(name, c_uint32, 1) for name in [
        "_relation", "_not_relation",
        "_clan", "_not_clan",
        "_multiclan", "_not_multiclan",
        "_left_functional", "_not_left_functional",
        "_right_functional", "_not_right_functional",
        "_left_regular", "_not_left_regular",
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
    def not_left_functional(self) -> bool:
        return self._not_left_functional

    @property
    def left_functional(self) -> bool:
        return self._left_functional

    @left_functional.setter
    def left_functional(self, value: bool):
        if value:
            assert not self._not_left_functional
            self._left_functional = True
        else:
            assert not self._left_functional
            self._not_left_functional = True

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
    def not_left_regular(self) -> bool:
        return self._not_left_regular

    @property
    def left_regular(self) -> bool:
        return self._left_regular

    @left_regular.setter
    def left_regular(self, value: bool):
        if value:
            assert not self._not_left_regular
            self._left_regular = True
        else:
            assert not self._left_regular
            self._not_left_regular = True

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
