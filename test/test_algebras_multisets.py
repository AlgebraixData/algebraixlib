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

import collections as _collections
from algebraixlib.mathobjects import Multiset, Atom, Set, Couplet

from algebraixlib.structure import GenesisSetA, GenesisSetM, GenesisSetN, PowerSet, CartesianProduct
from algebraixlib.undef import Undef, RaiseOnUndef, UndefException

import algebraixlib.extension as extension

from algebraixlib.algebras.multisets import \
    get_ground_set, get_absolute_ground_set, get_name, is_member, is_absolute_member, \
    union, big_union, intersect, big_intersect, minus, add, demultify, \
    is_subset_of, is_superset_of, single, some, substrict, superstrict

# noinspection PyUnresolvedReferences
from data_mathobjects import basic_multisets


_set1 = Multiset('a', 'b', 'c')
_set2 = Multiset('b', 'c', 'd')
# _numeric_set1 = Multiset([1, 2, 3])
_set1u2 = Multiset('a', 'b', 'c', 'd')
_set1i2 = Multiset('b', 'c')
_set1m2 = Multiset('a')
_set1a2 = Multiset('a', 'b', 'b', 'c', 'c', 'd')
_ab_c = Multiset([Multiset('a', 'b'), Multiset('c')])
_ac_a = Multiset([Multiset('a', 'c'), Multiset('a')])

_multiset1 = Multiset(_collections.Counter("bad"))
_multiset2 = Multiset(_collections.Counter("dog"))
_multiset3 = Multiset(_collections.Counter("baddog"))
_multiset4 = Multiset(_collections.Counter("badog"))
_multiset_magic = Multiset(_collections.Counter("abracadabra"))
_multiset_ba = Multiset(_collections.Counter("ba"))


class MultiSetsTest(unittest.TestCase):
    """Test the algebras.sets module."""

    def test_simple_operations(self):
        result = union(_multiset1, _multiset2)
        self.assertEqual(result, Multiset(_collections.Counter("badog")))

        result = add(_multiset1, _multiset2)
        self.assertEqual(result, _multiset3)

        result = intersect(_multiset1, _multiset2)
        self.assertEqual(result, Multiset(_collections.Counter("d")))

        result = minus(_multiset_magic, _multiset1)
        self.assertEqual(result, Multiset(_collections.Counter("racaabra")))

        p1 = Multiset(_collections.Counter("aaa"))
        p2 = Multiset(_collections.Counter("bbb"))
        p3 = Multiset(_collections.Counter("ccc"))
        combined = Set({p1, p2, p3})
        result = big_union(combined)
        self.assertEqual(result, Multiset(_collections.Counter("abc" * 3)))

        result = big_intersect(Set(
            {_multiset_magic, Multiset(_collections.Counter("abc" * 3)),
             Multiset("a", "a", "b", "c")}))
        self.assertEqual(result, Multiset(_collections.Counter("aabc")))

    def test_metadata(self):
        self.assertEqual(get_ground_set(),
            PowerSet(CartesianProduct(GenesisSetM(), GenesisSetN())))
        self.assertEqual(get_absolute_ground_set(),
            PowerSet(CartesianProduct(GenesisSetA(), GenesisSetN())))
        self.assertEqual(get_name(), 'Multisets(M): P(M x N)')

    # noinspection PyTypeChecker
    def test_membership(self):
        self.assertTrue(is_member(Multiset()))
        self.assertTrue(is_member(Multiset(3)))
        self.assertFalse(is_member(Atom(3)))
        self.assertTrue(is_absolute_member(Multiset(3)))
        self.assertFalse(is_absolute_member(Multiset(Couplet(3, 4))))
        self.assertRaises(AttributeError, lambda: is_member(3))

    def test_union(self):
        self._check_wrong_argument_types_binary(union)
        result = union(_set1, _set2)
        self.assertEqual(result, _set1u2)
        abc_ab_ac = Multiset([Multiset('a', 'b', 'c'), Multiset('a', 'b'), Multiset('a', 'c'),
                              Multiset('a', 'c')])
        ab_c = _ab_c
        ac_a = _ac_a
        cu = extension.binary_multi_extend(ab_c, ac_a, union)
        self.assertEqual(cu, abc_ab_ac)

    def test_big_union(self):
        self._check_wrong_argument_types_unary(big_union)
        result = big_union(Set([_set1, _set2]))
        self.assertEqual(result, _set1u2)

    def test_intersect(self):
        self._check_wrong_argument_types_binary(intersect)

        result = intersect(_set1, _set2)
        self.assertEqual(result, _set1i2)
        a_c_0 = Multiset([Multiset('a'), Multiset('a'), Multiset('c'), Multiset()])
        ci = extension.binary_multi_extend(_ab_c, _ac_a, intersect)
        self.assertEqual(ci, a_c_0)

    def test_big_intersect(self):
        self._check_wrong_argument_types_unary(big_intersect)

        result = big_intersect(Set([_set1, _set2]))
        self.assertEqual(result, _set1i2)

    def test_minus(self):
        self._check_wrong_argument_types_binary(minus)

        result = minus(_set1, _set2)
        self.assertEqual(result, _set1m2)

    def test_addition(self):
        self._check_wrong_argument_types_binary(add)

        result = add(_set1, _set2)
        self.assertEqual(result, _set1a2)

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

    def test_demultify(self):
        letters = [l for l in "abracadabra"]
        self.assertIs(demultify(Set(letters)), Undef())
        set1 = demultify(Multiset(letters))
        self.assertTrue(isinstance(set1, Set))
        self.assertEqual(set1.cardinality, 5)  # set only unique letters
        letters = [l for l in "abrcd"]
        self.assertEqual(set1, Set(letters))

    def test_single(self):
        # self._check_wrong_argument_types_unary(single)
        self.assertIs(single(Undef()), Undef())
        self.assertIs(single(_set1), Undef())
        self.assertEqual(single(_set1m2), Atom('a'))
        self.assertIs(single(_set1), Undef())

    def test_some(self):
        # self._check_wrong_argument_types_unary(some)
        self.assertIs(some(Undef()), Undef())
        self.assertIs(some(Multiset()), Undef())
        self.assertEqual(some(_set1m2), Atom('a'))
        self.assertTrue(some(_set1) in _set1)

    def test_less_than(self):
        for value_key1, ms1 in basic_multisets.items():
            for value_key2, ms2 in basic_multisets.items():
                self.assertNotEqual(ms1 < ms2, NotImplemented)
                self.assertNotEqual(ms2 < ms1, NotImplemented)
                if ms1 == ms2:
                    self.assertFalse(ms1 < ms2)
                    self.assertFalse(ms2 < ms1)
            for mo in [Atom(1), Couplet(1, 2)]:
                self.assertTrue(mo < ms1)
            for mo in [Set(1, 2, 3)]:
                self.assertTrue(ms1 < mo)

    def _check_wrong_argument_types_unary(self, operation):
        """Negative tests for set algebra unary operations."""
        self.assertIs(operation(Atom(3)), Undef())
        self.assertIs(operation(Set(Atom(3))), Undef())
        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: operation(Atom(3)))
        self.assertRaises(UndefException, lambda: operation(Multiset(Atom(3))))
        RaiseOnUndef.reset()

        self.assertIs(operation(Undef()), Undef())
        self.assertIs(operation(Undef(), _checked=False), Undef())

    def _check_wrong_argument_types_binary(self, operation):
        """Negative tests for set algebra binary operations."""
        self.assertRaises(AttributeError, lambda: operation(3, Multiset(Atom(3))))
        self.assertIs(operation(Atom(3), Multiset(Atom(4))), Undef())
        self.assertRaises(TypeError, lambda: operation(Multiset(Atom(3), 4)))
        self.assertIs(operation(Multiset(Atom(3)), Atom(4)), Undef())
        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: operation(Atom(3), Multiset(Atom(4))))
        self.assertRaises(UndefException, lambda: operation(Multiset(Atom(3)), Atom(4)))
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
