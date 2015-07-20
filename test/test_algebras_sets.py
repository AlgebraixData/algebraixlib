"""Test the algebras.sets module."""

# $Id: test_algebras_sets.py 22614 2015-07-15 18:14:53Z gfiedler $
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

from algebraixlib.mathobjects import Atom, Couplet, Set, Multiset
from algebraixlib.structure import GenesisSetA, GenesisSetM, PowerSet
from algebraixlib.undef import Undef, RaiseOnUndef, UndefException
import algebraixlib.extension as _extension

from algebraixlib.algebras.sets import \
    get_ground_set, get_absolute_ground_set, get_name, is_member, is_absolute_member, \
    union, big_union, intersect, big_intersect, minus, \
    is_subset_of, is_superset_of, substrict, superstrict, multify


_set1 = Set('a', 'b', 'c')
_set2 = Set('b', 'c', 'd')
_numeric_set1 = Set([1, 2, 3])
_set1u2 = Set('a', 'b', 'c', 'd')
_set1i2 = Set('b', 'c')
_set1m2 = Set('a')
_ab_c = Set([Set('a', 'b'), Set('c')])
_ac_a = Set([Set('a', 'c'), Set('a')])


class SetsTest(unittest.TestCase):
    """Test the algebras.sets module."""

    print_examples = False

    def test_metadata(self):
        self.assertEqual(get_ground_set(), PowerSet(GenesisSetM()))
        self.assertEqual(get_absolute_ground_set(), PowerSet(GenesisSetA()))
        self.assertEqual(get_name(), 'Sets(M): P(M)')

    def test_membership(self):
        self.assertTrue(is_member(Set()))
        self.assertTrue(is_member(Set(3)))
        self.assertFalse(is_member(Atom(3)))
        self.assertTrue(is_absolute_member(Set(3)))
        self.assertFalse(is_absolute_member(Set(Couplet(3, 4))))
        self.assertRaises(TypeError, lambda: is_member(3))

    def test_union(self):
        self._check_wrong_argument_types_binary(union)

        result = union(_set1, _set2)
        self.assertEqual(result, _set1u2)
        abc_ab_ac = Set([Set('a', 'b', 'c'), Set('a', 'b'), Set('a', 'c')])
        cu = _extension.binary_extend(_ab_c, _ac_a, union)
        self.assertEqual(cu, abc_ab_ac)

    def test_big_union(self):
        self._check_wrong_argument_types_unary(big_union)

        result = big_union(Set([_set1, _set2]))
        self.assertEqual(result, _set1u2)
        self.assertEqual(Set(), big_union(Set()))

    def test_intersect(self):
        self._check_wrong_argument_types_binary(intersect)

        result = intersect(_set1, _set2)
        self.assertEqual(result, _set1i2)
        a_c_0 = Set([Set('a'), Set('c'), Set()])
        ci = _extension.binary_extend(_ab_c, _ac_a, intersect)
        self.assertEqual(ci, a_c_0)

    def test_big_intersect(self):
        self._check_wrong_argument_types_unary(big_intersect)

        result = big_intersect(Set([_set1, _set2]))
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
        letters = [l for l in "abracadabra"]
        self.assertIs(multify(Multiset(letters)), Undef())
        multiset = multify(Set(letters))  # Set object drops duplicates
        self.assertTrue(isinstance(multiset, Multiset))
        self.assertEqual(multiset.cardinality, 5)  # multiset of unique items
        letters = [l for l in "abrcd"]
        self.assertEqual(multiset, Multiset(letters))

    def _check_wrong_argument_types_unary(self, operation):
        """Negative tests for set algebra unary operations."""
        self.assertIs(operation(Atom(3)), Undef())
        self.assertIs(operation(Set(Atom(3))), Undef())

        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: operation(Atom(3)))
        self.assertRaises(UndefException, lambda: operation(Set(Atom(3))))
        RaiseOnUndef.reset()

    def _check_wrong_argument_types_binary(self, operation):
        """Negative tests for set algebra binary operations."""
        self.assertRaises(TypeError, lambda: operation(3, Set(Atom(3))))
        self.assertIs(operation(Atom(3), Set(Atom(4))), Undef())
        self.assertRaises(TypeError, lambda: operation(Set(Atom(3), 4)))
        self.assertIs(operation(Set(Atom(3)), Atom(4)), Undef())

        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: operation(Atom(3), Set(Atom(4))))
        self.assertRaises(UndefException, lambda: operation(Set(Atom(3)), Atom(4)))
        RaiseOnUndef.reset()


# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
