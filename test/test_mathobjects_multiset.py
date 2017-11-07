"""Test the mathobjects.set module."""

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

from algebraixlib.mathobjects import Atom, Couplet, Multiset, Set
from algebraixlib.cache_status import CacheStatus
from algebraixlib.structure import CartesianProduct, GenesisSetN, GenesisSetA, PowerSet, Structure
from algebraixlib.undef import Undef


# Ground set structures for the basic_sets.
_atom_multiset_struct = PowerSet(CartesianProduct(GenesisSetA(), GenesisSetN()))


class MultisetTest(unittest.TestCase):
    """Test the Set class."""

    print_examples = False

#     def test_Multiset(self):
#         """Create various forms of Sets."""
#         if self.print_examples:
#             print('(printing examples)')  # Make 'nosetests -s' more readable.
#         for test_set_name in basic_multisets.keys():
#             self._multiset_assert(test_set_name)
#         self.assertEqual("{}", str(Multiset()))
#         self.assertTrue(Multiset(1) < Multiset(2))
#
#     def _multiset_assert(self, test_set_name):
#         """Assert that 'set' is a proper Set with elements 'elements'."""
#         test_multiset = basic_multisets[test_set_name]
#         elements = test_multiset._test_val
#         # Convert strings to char arrays so that we can rewrite them.
#         if type(elements) == str:
#             elements = [ch for ch in elements]
#         # Convert the elements container into Atoms if they are values.
#         if not isinstance(elements, collections.Iterable):
#             elements = [elements]
#         for idx, el in enumerate(elements):
#             if not isinstance(el, MathObject):
#                 elements[idx] = Atom(el)
#         # Test the type structure.
#         self.assertTrue(isinstance(test_multiset, MathObject))
#         self.assertFalse(isinstance(test_multiset, Atom))
#         self.assertFalse(isinstance(test_multiset, Couplet))
#         self.assertFalse(isinstance(test_multiset, Set))
#         self.assertFalse(isinstance(test_multiset, Multiset))
#         # Compare the values.
#         vals = {}
#         for el in elements:
#             if repr(el) not in vals:
#                 vals[repr(el)] = 1
#             else:
#                 vals[repr(el)] += 1
#         for el in test_multiset:
#             if repr(el) not in vals:
#                 vals[repr(el)] = 1
#             else:
#                 vals[repr(el)] += 1
#         for key in vals.keys():
#             self.assertEqual(vals[key], 2)
#         # Test that the representation caching doesn't change the value.
#         multiset_repr = repr(test_multiset)
#         self.assertEqual(multiset_repr, repr(test_multiset))
#         # Make sure that the representation evaluates to a set that compares equal.
#         repr_exec = 'self.assertEqual(test_multiset, {0})'.format(repr(test_multiset))
#         exec(repr_exec)
#         # Check structure.
# #        self.assertEqual(test_set.get_ground_set(), _basic_sets_structs[test_set_name])
#         # Print the representation and the string conversion.
#         if self.print_examples:
#             print('repr(Multiset({elements}) = {repr}'.format(
#                 elements=','.join(str(el) for el in elements), repr=repr(test_multiset)))
#             print('str(Multiset({elements})) = {str}'.format(
#                 elements=','.join(str(el) for el in elements), str=str(test_multiset)))

    def test_invalid_constructs(self):
        """Test invalid Multisets."""
        self.assertRaises(TypeError, lambda: Multiset(Undef()))
        # self.assertRaises(TypeError, lambda: Multiset([['a']]))

    def test_membership(self):
        s = Multiset({'a': 2, 'b': 1})
        self.assertTrue(Atom('a') in s)
        self.assertTrue('a' in s)
        self.assertTrue('b' in s)
        self.assertFalse('c' in s)
        self.assertTrue(s.has_element(Atom('a')))
        self.assertFalse(s.has_element(Atom('c')))

        test_list = [Atom('a'), Atom('a'), Atom('b')]
        multiset_iter = iter(s)
        for i in multiset_iter:
            self.assertTrue(i in test_list)
            test_list.remove(i)

    def test_basic_multiset(self):
        m = Multiset(_collections.Counter({'a': 2, 'b': 1}))
        self.assertEqual(m.cardinality, 3)

        m_repr = repr(m)
        m_str = str(m)

        self.assertEqual(m_repr, "Multiset({Atom('a'): 2, Atom('b'): 1})")
        self.assertEqual(m_str, "['a':2, 'b':1]")
        self.assertEqual(m.get_multiplicity(Atom('a')), 2)
        self.assertEqual(m.get_multiplicity(Atom('b')), 1)
        m_struct = m.get_ground_set()
        self.assertEqual(m_struct, _atom_multiset_struct)

        single_m = Multiset(Set([1, 2, 3, 4]), direct_load=True)
        self.assertEqual(single_m.cardinality, 1)
        self.assertEqual(repr(single_m), "Multiset({Set(Atom(1), Atom(2), Atom(3), Atom(4)): 1})")
        self.assertEqual(str(single_m), "[{1, 2, 3, 4}:1]")

        empty_m = Multiset()
        self.assertEqual(empty_m.cardinality, 0)
        self.assertEqual(repr(empty_m), "Multiset({})")
        self.assertEqual(str(empty_m), "[]")

        for element in m:
            self.assertTrue(isinstance(element, Atom))

    def test_multiset_with_one_empty_element(self):
        m = Multiset(Set())
        self.assertEqual(m.cardinality, 1)

        m_repr = repr(m)
        m_str = str(m)

        self.assertEqual(m_repr, "Multiset({Set(): 1})")
        self.assertEqual(m_str, "[{}:1]")
        self.assertEqual(m.get_multiplicity(Set()), 1)
        self.assertEqual(m.get_multiplicity(Atom('b')), 0)
        m_struct = m.get_ground_set()
        m_expected_struct = PowerSet(CartesianProduct(Structure(), GenesisSetN()))
        self.assertEqual(m_struct, m_expected_struct)

        import algebraixlib.algebras.multiclans as _multiclans
        self.assertTrue(_multiclans.is_member(m))
        self.assertTrue(_multiclans.is_absolute_member(m))

    def test_getitem(self):
        self.assertEqual(Multiset()['callable'], Multiset())

        # Creating multiclans (multisets of relations)
        multiset1 = Multiset({Couplet('b', 'w'): 2, Couplet('b', 'y'): 3})
        multiset2 = Multiset({Couplet('a', 'x'): 5, Couplet('x', 'y'): 1})

        right_values1 = multiset1[Atom('b')]
        self.assertEqual(right_values1, Multiset({Atom('w'): 2, Atom('y'): 3}))
        right_values2 = multiset2[Atom('b')]
        self.assertEqual(right_values2, Multiset())

    def test_flags_empty_set(self):
        s = Multiset()

        self.assertEqual(s.cached_relation, CacheStatus.IS_NOT)
        self.assertEqual(s.cached_clan, CacheStatus.IS_NOT)
        self.assertEqual(s.cached_multiclan, CacheStatus.IS)
        self.assertEqual(s.cached_functional, CacheStatus.IS)
        self.assertEqual(s.cached_right_functional, CacheStatus.IS)
        self.assertEqual(s.cached_regular, CacheStatus.IS)
        self.assertEqual(s.cached_reflexive, CacheStatus.IS)
        self.assertEqual(s.cached_symmetric, CacheStatus.IS)
        self.assertEqual(s.cached_transitive, CacheStatus.IS)

        self.assertRaises(AssertionError, lambda: s.cache_relation(CacheStatus.IS))
        self.assertRaises(AssertionError, lambda: s.cache_clan(CacheStatus.IS))
        self.assertRaises(AssertionError, lambda: s.cache_multiclan(CacheStatus.IS_NOT))
        s.cache_multiclan(CacheStatus.IS)

        self.assertRaises(Exception, lambda: s.cache_transitive(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: s.cache_functional(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: s.cache_right_functional(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: s.cache_regular(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: s.cache_reflexive(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: s.cache_symmetric(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: s.cache_transitive(CacheStatus.IS_NOT))


# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
