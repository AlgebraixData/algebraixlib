"""Test the algebras.sets module."""

# $Id: test_algebras_multisets.py 22614 2015-07-15 18:14:53Z gfiedler $
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
    union, big_union, intersect, big_intersect, minus, addition, demultify, \
    is_subset_of, is_superset_of, substrict, superstrict


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

    print_examples = False

    def test_simple_operations(self):
        result = union(_multiset1, _multiset2)
        self.assertEqual(result, Multiset(_collections.Counter("badog")))

        result = addition(_multiset1, _multiset2)
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
        self.assertEqual(result, Multiset(_collections.Counter("abc"*3)))

        result = big_intersect(Set(
            {_multiset_magic, Multiset(_collections.Counter("abc"*3)),
             Multiset("a", "a", "b", "c")}))
        self.assertEqual(result, Multiset(_collections.Counter("aabc")))

    def test_metadata(self):
        self.assertEqual(get_ground_set(), PowerSet(CartesianProduct(GenesisSetM(), GenesisSetN())))
        self.assertEqual(get_absolute_ground_set(), PowerSet(CartesianProduct(GenesisSetA(), GenesisSetN())))
        self.assertEqual(get_name(), 'Multisets(M): P(M x N)')

    def test_membership(self):
        self.assertTrue(is_member(Multiset()))
        self.assertTrue(is_member(Multiset(3)))
        self.assertFalse(is_member(Atom(3)))
        self.assertTrue(is_absolute_member(Multiset(3)))
        self.assertFalse(is_absolute_member(Multiset(Couplet(3, 4))))
        self.assertRaises(TypeError, lambda: is_member(3))

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
        self._check_wrong_argument_types_binary(addition)

        result = addition(_set1, _set2)
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

    def _check_wrong_argument_types_unary(self, operation):
        """Negative tests for set algebra unary operations."""
        self.assertIs(operation(Atom(3)), Undef())
        self.assertIs(operation(Set(Atom(3))), Undef())

        RaiseOnUndef.set_level(1)

        self.assertRaises(UndefException, lambda: operation(Atom(3)))
        self.assertRaises(UndefException, lambda: operation(Multiset(Atom(3))))
        RaiseOnUndef.reset()

    def _check_wrong_argument_types_binary(self, operation):
        """Negative tests for set algebra binary operations."""
        self.assertRaises(TypeError, lambda: operation(3, Multiset(Atom(3))))
        self.assertIs(operation(Atom(3), Multiset(Atom(4))), Undef())
        self.assertRaises(TypeError, lambda: operation(Multiset(Atom(3), 4)))
        self.assertIs(operation(Multiset(Atom(3)), Atom(4)), Undef())
        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: operation(Atom(3), Multiset(Atom(4))))
        self.assertRaises(UndefException, lambda: operation(Multiset(Atom(3)), Atom(4)))
        RaiseOnUndef.reset()

# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
