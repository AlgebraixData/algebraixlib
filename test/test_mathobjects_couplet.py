"""Testing the mathobjects.couplet module."""

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

from algebraixlib.algebras.properties import is_functional, is_right_functional, is_bijective, \
    is_reflexive, is_transitive, is_equivalence_relation
from algebraixlib.mathobjects import Atom, Couplet, MathObject, Multiset, Set
from algebraixlib.cache_status import CacheStatus
from algebraixlib.structure import CartesianProduct, GenesisSetA, PowerSet
from algebraixlib.undef import Undef

# noinspection PyUnresolvedReferences
from data_mathobjects import basic_couplets


# Ground set structures for the basic_couplets.
_basic_couplet_struct = CartesianProduct(GenesisSetA(), GenesisSetA())
_complex_couplet_struct = CartesianProduct(_basic_couplet_struct, PowerSet(GenesisSetA()))
_basic_couplets_structs = {
    '2->3': _basic_couplet_struct,
    "'4'->'5'": _basic_couplet_struct,
    "6->'7'": _basic_couplet_struct,
    'Coupl->Set': _complex_couplet_struct
}


class CoupletTest(unittest.TestCase):
    """Test the Couplet class."""

    print_examples = False

    def test_Couplet(self):
        """Create various forms of Couplets."""
        if self.print_examples:
            print('(printing examples)')  # Make 'nosetests -s' more readable.
        for test_couplet_name in basic_couplets.keys():
            self._couplet_assert(test_couplet_name)

    def _couplet_assert(self, test_couplet_name):
        """Assert that 'couplet' is a proper Couplet with left 'left' and right 'right'."""
        test_couplet = basic_couplets[test_couplet_name]
        left = test_couplet._test_val['left']
        right = test_couplet._test_val['right']
        couplet = Couplet(left=left, right=right)
        # Convert the arguments into Atoms if they are values.
        if not isinstance(left, MathObject):
            left = Atom(left)
        if not isinstance(right, MathObject):
            right = Atom(right)
        # Test the type structure.
        self.assertTrue(isinstance(couplet, MathObject))
        self.assertFalse(isinstance(couplet, Atom))
        self.assertTrue(isinstance(couplet, Couplet))
        self.assertFalse(isinstance(couplet, Set))
        # Compare the values of right and left.
        left_val = couplet.left
        right_val = couplet.right
        self.assertEqual(left_val, left)
        self.assertEqual(right_val, right)
        # Test that the representation caching doesn't change the value.
        couplet_repr = repr(couplet)
        self.assertEqual(couplet_repr, repr(couplet))
        # Check structure.
        self.assertEqual(test_couplet.get_ground_set(), _basic_couplets_structs[test_couplet_name])
        # Test left set and functionality.
        self.assertIs(couplet.get_left_set(), Undef())
        self.assertIs(is_functional(couplet), Undef())
        self.assertIs(couplet('callable'), Undef())
        # Make sure that the representation evaluates to a couplet that compares equal.
        repr_exec = 'self.assertEqual(couplet, {0})'.format(repr(couplet))
        exec(repr_exec)
        # Print the representation and the string conversion.
        if self.print_examples:
            print('repr(Couplet(left={left}, right={right})) = {repr}'.format(
                left=repr(left_val), right=repr(right_val), repr=couplet_repr))
            print('str(Couplet(left={left}, right={right})) = {str}'.format(
                left=str(left_val), right=str(right_val), str=str(couplet)))

    def test_operators(self):
        """Test operators"""
        a = Atom(1)
        c = Couplet(1, 2)
        self.assertTrue(a != c)
        self.assertTrue(c != a)

    def test_less_than(self):
        for value_key1, cp1 in basic_couplets.items():
            for value_key2, cp2 in basic_couplets.items():
                self.assertNotEqual(cp1 < cp2, NotImplemented)
                self.assertNotEqual(cp2 < cp1, NotImplemented)
                if cp1 == cp2:
                    self.assertFalse(cp1 < cp2)
                    self.assertFalse(cp2 < cp1)
            for mo in [Atom(1)]:
                self.assertTrue(mo < cp1)
            for mo in [Multiset(1, 2, 3), Set(1, 2, 3)]:
                self.assertTrue(cp1 < mo)

    def test_invalid_constructs(self):
        """Test invalid Couplets."""
        self.assertRaises(TypeError, lambda: Couplet(Undef(), 2))
        self.assertRaises(TypeError, lambda: Couplet(1, right=Undef()))

    def test_properties(self):
        def _test_undef(cc):
            self.assertIs(cc.get_left_set(), Undef())
            self.assertIs(is_functional(cc), Undef())
            self.assertIs(cc.get_right_set(), Undef())
            self.assertIs(is_right_functional(cc), Undef())
            self.assertIs(is_bijective(cc), Undef())
            self.assertIs(is_transitive(cc), Undef())
            self.assertIs(is_equivalence_relation(cc), Undef())
        c = Couplet(1, 2)
        _test_undef(c)
        self.assertFalse(is_reflexive(c))
        c = Couplet(1)
        _test_undef(c)
        self.assertTrue(is_reflexive(c))

    def test_flags_cache(self):
        c = Couplet(1, 2)
        self.assertEqual(c.cached_relation, CacheStatus.IS_NOT)
        self.assertEqual(c.cached_clan, CacheStatus.IS_NOT)
        self.assertEqual(c.cached_multiclan, CacheStatus.IS_NOT)
        self.assertEqual(c.cached_functional, CacheStatus.N_A)
        self.assertEqual(c.cached_right_functional, CacheStatus.N_A)
        self.assertEqual(c.cached_regular, CacheStatus.N_A)
        self.assertEqual(c.cached_reflexive, CacheStatus.UNKNOWN)
        self.assertEqual(c.cached_symmetric, CacheStatus.N_A)
        self.assertEqual(c.cached_transitive, CacheStatus.N_A)

        is_reflexive(c)
        self.assertEqual(c.cached_reflexive, CacheStatus.IS_NOT)

        self.assertRaises(AssertionError, lambda: c.cache_relation(CacheStatus.IS))
        self.assertRaises(AssertionError, lambda: c.cache_clan(CacheStatus.IS))
        self.assertRaises(AssertionError, lambda: c.cache_multiclan(CacheStatus.IS))
        self.assertRaises(AssertionError, lambda: c.cache_reflexive(CacheStatus.IS))

        self.assertRaises(Exception, lambda: c.cache_transitive(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: c.cache_functional(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: c.cache_right_functional(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: c.cache_regular(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: c.cache_symmetric(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: c.cache_transitive(CacheStatus.IS_NOT))

    def test__str__(self):
        """Verify __str__() returns the representation of a Couplet object."""
        s = str(Couplet(1, 2))
        self.assertEqual(s, '(1->2)')

    def test_optional_right(self):
        """Test optional right"""
        c1 = Couplet(1, 1)
        c2 = Couplet(1)
        self.assertEqual(c1, c2)

# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
