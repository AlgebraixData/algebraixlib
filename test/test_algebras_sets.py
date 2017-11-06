"""Test the algebras.sets module."""

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
import inspect
import os
import unittest

from algebraixlib.mathobjects import Atom, Couplet, Set, Multiset
from algebraixlib.cache_status import CacheStatus
from algebraixlib.structure import GenesisSetA, GenesisSetM, PowerSet
from algebraixlib.undef import Undef, RaiseOnUndef, UndefException
import algebraixlib.extension as _extension

from algebraixlib.algebras.sets import \
    get_ground_set, get_absolute_ground_set, get_name, is_member, is_absolute_member, \
    union, big_union, intersect, big_intersect, minus, power_set, power_up, restrict, \
    is_subset_of, is_superset_of, single, some, substrict, superstrict, multify

# noinspection PyUnresolvedReferences
from data_mathobjects import basic_sets


_set1 = Set('a', 'b', 'c')
_set2 = Set('b', 'c', 'd')
_numeric_set1 = Set(1, 2, 3)
_set1u2 = Set('a', 'b', 'c', 'd')
_set1i2 = Set('b', 'c')
_set1m2 = Set('a')
_ab_c = Set(Set('a', 'b'), Set('c'))
_ac_a = Set(Set('a', 'c'), Set('a'))


class SetsTest(unittest.TestCase):
    """Test the algebras.sets module."""

    def test_metadata(self):
        self.assertEqual(get_ground_set(), PowerSet(GenesisSetM()))
        self.assertEqual(get_absolute_ground_set(), PowerSet(GenesisSetA()))
        self.assertEqual(get_name(), 'Sets(M): P(M)')

    # noinspection PyTypeChecker
    def test_membership(self):
        self.assertTrue(is_member(Set()))
        self.assertTrue(is_member(Set(3)))
        self.assertFalse(is_member(Atom(3)))
        self.assertTrue(is_absolute_member(Set(3)))
        self.assertFalse(is_absolute_member(Set(Couplet(3, 4))))
        self.assertRaises(AttributeError, lambda: is_member(3))

    def test_union(self):
        self._check_wrong_argument_types_binary(union)

        result = union(_set1, _set2)
        self.assertEqual(result, _set1u2)
        abc_ab_ac = Set(Set('a', 'b', 'c'), Set('a', 'b'), Set('a', 'c'))
        cu = _extension.binary_extend(_ab_c, _ac_a, union)
        self.assertEqual(cu, abc_ab_ac)

    def test_union_flags(self):
        s1 = Set(1)
        s2 = Set(2)
        s3 = Set(1, 2)
        self.assertTrue(is_absolute_member(s1))
        self.assertTrue(is_absolute_member(s2))
        self.assertTrue(is_absolute_member(s3))
        result = union(s1, s2)
        self.assertEqual(s3, result)
        self.assertEqual(result.cached_is_absolute, CacheStatus.IS)

        from algebraixlib.algebras import relations as _rels

        rel1 = Set(Couplet('a', 1))
        rel2 = Set(Couplet('b', 2))
        rel3 = Set(Couplet('a', 1), Couplet('b', 2))
        self.assertTrue(_rels.is_absolute_member(rel1))
        self.assertTrue(_rels.is_absolute_member(rel2))
        result = union(rel1, rel2)
        self.assertEqual(rel3, result)
        self.assertEqual(result.cached_is_absolute, CacheStatus.IS)

        from algebraixlib.algebras import clans as _clans

        clan1 = Set(rel1)
        clan2 = Set(rel2)
        clan3 = Set(rel1, rel2)
        self.assertTrue(_clans.is_absolute_member(clan1))
        self.assertTrue(_clans.is_absolute_member(clan2))
        self.assertTrue(_clans.is_functional(clan1))
        self.assertTrue(_clans.is_functional(clan2))
        self.assertTrue(_clans.is_right_functional(clan1))
        self.assertTrue(_clans.is_right_functional(clan2))
        result = union(clan1, clan2)
        self.assertEqual(clan3, result)
        self.assertEqual(result.cached_absolute, CacheStatus.IS)
        self.assertEqual(result.cached_functional, CacheStatus.IS)
        self.assertEqual(result.cached_right_functional, CacheStatus.IS)

        clan4 = Set(Set(Couplet(s1, 1), Couplet(s1, 2)))
        clan5 = Set(rel1, Set(Couplet(s1, 1), Couplet(s1, 2)))
        self.assertFalse(_clans.is_absolute_member(clan4))
        self.assertFalse(_clans.is_functional(clan4))
        result = union(clan1, clan4)
        self.assertEqual(clan5, result)
        self.assertEqual(result.cached_absolute, CacheStatus.IS_NOT)
        self.assertEqual(result.cached_functional, CacheStatus.IS_NOT)

        rel1 = Set(Couplet('a', 1), Couplet('b', 2)).cache_relation(CacheStatus.IS)
        rel2 = Set(Couplet('c', 3))
        self.assertEqual(union(rel1, rel2).cached_relation, CacheStatus.UNKNOWN)
        self.assertTrue(_rels.is_member(rel2))
        self.assertEqual(union(rel1, rel2).cached_relation, CacheStatus.IS)

    def test_big_union(self):
        self._check_wrong_argument_types_unary(big_union)

        result = big_union(Set(_set1, _set2))
        self.assertEqual(result, _set1u2)
        self.assertEqual(Set(), big_union(Set()))

    def test_intersect(self):
        self._check_wrong_argument_types_binary(intersect)

        result = intersect(_set1, _set2)
        self.assertEqual(result, _set1i2)
        a_c_0 = Set(Set('a'), Set('c'), Set())
        ci = _extension.binary_extend(_ab_c, _ac_a, intersect)
        self.assertEqual(ci, a_c_0)

    def test_big_intersect(self):
        self._check_wrong_argument_types_unary(big_intersect)

        result = big_intersect(Set(_set1, _set2))
        self.assertEqual(result, _set1i2)
        self.assertEqual(Set(), big_intersect(Set()))

    def test_minus(self):
        self._check_wrong_argument_types_binary(minus)

        result = minus(_set1, _set2)
        self.assertEqual(result, _set1m2)

    def test_is_subset_of(self):
        self._check_wrong_argument_types_binary(is_subset_of)

        result1 = is_subset_of(_set1, _set1u2)
        self.assertTrue(result1)
        result2 = is_subset_of(_set1, _set2)
        self.assertFalse(result2)

    def test_is_superset_of(self):
        self._check_wrong_argument_types_binary(is_superset_of)

        result1 = is_superset_of(_set1u2, _set1)
        self.assertTrue(result1)
        result2 = is_superset_of(_set2, _set1)
        self.assertFalse(result2)

    def test_substrict(self):
        self._check_wrong_argument_types_binary(substrict)

        result1 = substrict(_set1, _set1u2)
        self.assertEqual(result1, _set1)
        result2 = substrict(_set1, _set2)
        self.assertIs(result2, Undef())

    def test_superstrict(self):
        self._check_wrong_argument_types_binary(superstrict)

        result1 = superstrict(_set1u2, _set1)
        self.assertEqual(result1, _set1u2)
        result2 = superstrict(_set2, _set1)
        self.assertIs(result2, Undef())

    def test_multify(self):
        self._check_argument_types_unary_undef(multify)

        letters = [l for l in "abracadabra"]
        self.assertIs(multify(Multiset(letters)), Undef())
        multiset = multify(Set(letters))  # Set object drops duplicates
        self.assertTrue(isinstance(multiset, Multiset))
        self.assertEqual(multiset.cardinality, 5)  # multiset of unique items
        letters = [l for l in "abrcd"]
        self.assertEqual(multiset, Multiset(letters))

    def test_single(self):
        # self._check_argument_types_unary_undef(single)
        self.assertIs(single(Undef()), Undef())

        self.assertIs(single(_set1), Undef())
        self.assertEqual(single(_set1m2), Atom('a'))

    def test_some(self):
        # self._check_argument_types_unary_undef(some)
        self.assertIs(some(Undef()), Undef())

        self.assertIs(some(Set()), Undef())
        result = some(_set1)
        self.assertTrue(result in _set1)

    def test_power_set(self):
        # self._check_argument_types_unary_undef(power_set)
        self.assertIs(power_set(Undef()), Undef())

        s1 = Set(1, 2, 3)
        p1 = Set(Set(), Set(1), Set(2), Set(3), Set(1, 2), Set(1, 3), Set(2, 3), Set(1, 2, 3))
        self.assertEqual(p1, power_set(s1))

    def test_power_up(self):
        # self._check_argument_types_unary_undef(power_up)
        self.assertIs(power_up(Undef()), Undef())

        s1 = Set(1, 2, 3)
        s2 = Set(Set(1), Set(2), Set(3))
        self.assertEqual(s2, power_up(s1))

    def test_restrict(self):
        self.assertIs(restrict(Undef(), Undef()), Undef())

        s1 = Set(1, 2, 3)

        self.assertRaises(TypeError, lambda: restrict(s1, Undef()))
        self.assertRaises(TypeError, lambda: restrict(s1, 1))
        self.assertRaises(TypeError, lambda: restrict(s1, 'a'))

        self.assertEqual(restrict(s1, lambda x: x.value < 3), Set(1, 2))
        self.assertEqual(restrict(s1, lambda x: x.value > 1), Set(2, 3))

    def test_less_than(self):
        for value_key1, set1 in basic_sets.items():
            for value_key2, set2 in basic_sets.items():
                self.assertNotEqual(set1 < set2, NotImplemented)
                self.assertNotEqual(set2 < set1, NotImplemented)
                if set1 == set2:
                    self.assertFalse(set1 < set2)
                    self.assertFalse(set2 < set1)
            for mo in [Atom(1), Couplet(1, 2), Multiset(1, 2, 3)]:
                self.assertTrue(mo < set1)

    def _check_argument_types_unary_undef(self, operation):
        """Negative tests for set algebra unary operations with Undef()."""
        self.assertIs(operation(Undef()), Undef())
        self.assertIs(operation(Undef(), _checked=False), Undef())

    def _check_wrong_argument_types_unary(self, operation):
        """Negative tests for set algebra unary operations."""
        self.assertIs(operation(Atom(3)), Undef())
        self.assertIs(operation(Set(Atom(3))), Undef())

        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: operation(Atom(3)))
        RaiseOnUndef.set_level(2)
        self.assertRaises(UndefException, lambda: operation(Set(Atom(3))))
        RaiseOnUndef.reset()

        self._check_argument_types_unary_undef(operation)

    def _check_wrong_argument_types_binary(self, operation):
        """Negative tests for set algebra binary operations."""
        self.assertRaises(AttributeError, lambda: operation(3, Set(Atom(3))))
        self.assertIs(operation(Atom(3), Set(Atom(4))), Undef())
        self.assertRaises(TypeError, lambda: operation(Set(Atom(3), 4)))
        self.assertIs(operation(Set(Atom(3)), Atom(4)), Undef())

        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: operation(Atom(3), Set(Atom(4))))
        self.assertRaises(UndefException, lambda: operation(Set(Atom(3)), Atom(4)))
        RaiseOnUndef.reset()

        self.assertIs(operation(_set1, Undef()), Undef())
        self.assertIs(operation(_set1, Undef(), _checked=False), Undef())
        self.assertIs(operation(Undef(), _set1), Undef())
        self.assertIs(operation(Undef(), _set1, _checked=False), Undef())


# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
