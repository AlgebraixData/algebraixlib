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
import collections
import inspect
import io
import os
import unittest

from algebraixlib.algebras.properties import is_functional, is_right_functional, is_bijective, \
    is_reflexive, is_symmetric, is_transitive, is_equivalence_relation, is_regular
import algebraixlib.algebras.relations as relations
import algebraixlib.algebras.sets as sets
from algebraixlib.mathobjects import Atom, Couplet, MathObject, Set
from algebraixlib.cache_status import CacheStatus
from algebraixlib.structure import CartesianProduct, GenesisSetA, PowerSet, Structure
from algebraixlib.undef import Undef

# noinspection PyProtectedMember
from algebraixlib.import_export.csv import _convert_clan_to_list_of_dicts, export_csv
# noinspection PyUnresolvedReferences
from data_mathobjects import basic_sets, basic_clans, algebra_clans, basic_hordes


# Ground set structures for the basic_sets.
_atom_set_struct = PowerSet(GenesisSetA())
_relation_struct = PowerSet(CartesianProduct(GenesisSetA(), GenesisSetA()))
_basic_sets_structs = {
    'empty': Structure(),
    'contains empty': PowerSet(Structure()),
    'num in dict': _atom_set_struct,
    'str in array': _atom_set_struct,
    'single num': _atom_set_struct,
    'single Coupl': _relation_struct,
    'left func': _relation_struct,
    'left func/lefts': _atom_set_struct,
    'left func/rights': _atom_set_struct,
    'not left func': _relation_struct,
    'not right func': _relation_struct,
    'diagonal': _relation_struct,
}


class SetTest(unittest.TestCase):
    """Test the Set class."""

    print_examples = False

    def test_Set(self):
        """Create various forms of Sets."""
        if self.print_examples:
            print('(printing examples)')  # Make 'nosetests -s' more readable.
        for test_set_name in basic_sets.keys():
            self._set_assert(test_set_name)
        self.assertEqual("{}", str(Set()))
        self.assertTrue(Set(1) < Set(2))
        s1 = Set('abc')
        s2 = Set('a', 'b', 'c')
        s3 = Set(['a', 'b', 'c'])
        s4 = Set({Atom(a) for a in 'abc'}, direct_load=True)
        self.assertNotEquals(s1, s2)
        self.assertEqual(s2, s3)
        self.assertEqual(s3, s4)

    def _set_assert(self, test_set_name):
        """Assert that 'set' is a proper Set with elements 'elements'."""
        test_set = basic_sets[test_set_name]
        elements = test_set._test_val
        # Convert strings to char arrays so that we can rewrite them.
        if type(elements) == str:
            elements = [ch for ch in elements]
        # Convert the elements container into Atoms if they are values.
        if not isinstance(elements, collections.Iterable):
            elements = [elements]
        for idx, el in enumerate(elements):
            if not isinstance(el, MathObject):
                elements[idx] = Atom(el)
        # Test the type structure.
        self.assertTrue(isinstance(test_set, MathObject))
        self.assertFalse(isinstance(test_set, Atom))
        self.assertFalse(isinstance(test_set, Couplet))
        self.assertTrue(isinstance(test_set, Set))
        # Compare the values.
        vals = {}
        for el in elements:
            if repr(el) not in vals:
                vals[repr(el)] = 1
            else:
                vals[repr(el)] += 1
        for el in test_set:
            if repr(el) not in vals:
                vals[repr(el)] = 1
            else:
                vals[repr(el)] += 1
        for key in vals.keys():
            self.assertEqual(vals[key], 2)
        # Test that the representation caching doesn't change the value.
        set_repr = repr(test_set)
        self.assertEqual(set_repr, repr(test_set))
        # Make sure that the representation evaluates to a set that compares equal.
        repr_exec = 'self.assertEqual(test_set, {0})'.format(repr(test_set))
        exec(repr_exec)
        # Check structure.
        self.assertEqual(test_set.get_ground_set(), _basic_sets_structs[test_set_name])
        # Print the representation and the string conversion.
        if self.print_examples:
            print('repr(Set({elements}) = {repr}'.format(
                elements=','.join(str(el) for el in elements), repr=repr(test_set)))
            print('str(Set({elements})) = {str}'.format(
                elements=','.join(str(el) for el in elements), str=str(test_set)))

    def test_invalid_constructs(self):
        """Test invalid Sets."""
        self.assertRaises(TypeError, lambda: Set(Undef()))
        self.assertRaises(TypeError, lambda: Set([['a']]))

    def test_membership(self):
        s = Set('a', 'b')
        self.assertTrue(Atom('a') in s)
        self.assertTrue('a' in s)
        self.assertTrue('b' in s)
        self.assertFalse('c' in s)
        self.assertTrue(s.has_element(Atom('a')))
        self.assertFalse(s.has_element(Atom('c')))

    def test_get_left_set(self):
        lefts = basic_sets['left func/lefts']
        right = basic_sets['left func/rights']
        self.assertEqual(Set(), Set().get_left_set())
        self.assertIs(lefts.get_left_set(), Undef())
        ss = basic_sets['left func'].get_left_set()
        self.assertEqual(ss, lefts)
        self.assertNotEqual(ss, right)
        ss = basic_clans['left func'].get_left_set()
        self.assertEqual(ss, lefts)
        lefts2 = Set('a', 'b', 'c', 'd', 'e', 'f')
        ss = basic_clans['left func2'].get_left_set()
        self.assertEqual(ss, lefts2)
        self.assertNotEqual(ss, right)
        ss = basic_hordes['left func'].get_left_set()
        self.assertEqual(ss, lefts)
        self.assertNotEqual(ss, right)
        lefts2 = Set('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i')
        ss = basic_hordes['left func2'].get_left_set()
        self.assertEqual(ss, lefts2)

    def test_get_right_set(self):
        lefts = basic_sets['left func/lefts']
        right = basic_sets['left func/rights']
        self.assertEqual(Set(), Set().get_right_set())
        self.assertIs(lefts.get_right_set(), Undef())
        cs = basic_sets['left func'].get_right_set()
        self.assertEqual(cs, right)
        self.assertNotEqual(cs, lefts)
        ss = basic_clans['left func'].get_right_set()
        self.assertEqual(ss, right)
        right2 = Set(range(1, 7))
        ss = basic_clans['left func2'].get_right_set()
        self.assertEqual(ss, right2)
        self.assertNotEqual(ss, right)
        ss = basic_hordes['left func'].get_right_set()
        self.assertEqual(ss, right)
        self.assertNotEqual(ss, lefts)
        right2 = Set(range(1, 10))
        ss = basic_hordes['left func2'].get_right_set()
        self.assertEqual(ss, right2)

    def test_regular(self):
        lefts = basic_sets['left func/lefts']
        self.assertTrue(is_regular(Set()))
        self.assertIs(is_regular(lefts), Undef())
        self.assertIs(is_regular(basic_sets['left func']), Undef())
        self.assertTrue(is_regular(basic_clans['left func']))
        self.assertFalse(is_regular(basic_clans['left func2']))
        self.assertFalse(is_regular(basic_clans['not left func']))
        embedded_has_irregular_left = Set(basic_sets['left func'], basic_sets['not left func'])
        self.assertFalse(is_regular(embedded_has_irregular_left))

        s = basic_sets['left func']
        self.assertEqual(s.cached_regular, CacheStatus.N_A)

    def test_functional(self):
        self.assertTrue(is_functional(Set()))
        self.assertIs(Undef(), is_functional(Set('a', 'b', 'c')))
        f = is_functional(basic_sets['left func'])
        self.assertTrue(f)
        f = is_functional(basic_sets['not left func'])
        self.assertFalse(f)
        f = is_functional(basic_clans['left func'])
        self.assertTrue(f)
        f = is_functional(basic_clans['not left func'])
        self.assertFalse(f)
        f = is_functional(basic_hordes['left func'])
        self.assertTrue(f)
        f = is_functional(basic_hordes['not left func'])
        self.assertFalse(f)

        s = basic_sets['left func']
        self.assertEqual(s.cached_functional, CacheStatus.IS)
        s = basic_sets['not left func']
        self.assertEqual(s.cached_functional, CacheStatus.IS_NOT)

    def test_callable(self):
        # Undefined:
        self.assertIs(Set()('callable'), Undef())
        for set_not_func in [basic_sets[name] for name in [
                'empty', 'num in dict', 'str in array', 'single num', 'left func/lefts',
                'left func/rights', 'not left func']]:
            self.assertIs(set_not_func('callable'), Undef())
        # Function:
        set1 = basic_sets['left func']
        self.assertEqual(set1('a'), Atom(1))
        self.assertEqual(set1('b'), Atom(2))
        self.assertEqual(set1('c'), Atom(3))
        set1 = basic_sets['diagonal']
        for left in relations.get_lefts(set1):
            self.assertEqual(set1(left), left)

    def test_getitem(self):
        # Undefined:
        self.assertEqual(Set()['callable'], Set())
        for set_not_func in [basic_sets[name] for name in [
                'num in dict', 'str in array', 'single num', 'left func/lefts',
                'left func/rights']]:
            self.assertIs(set_not_func['callable'], Undef())
        # Relation:
        set1 = basic_sets['left func']
        self.assertEqual(set1['a'], Set(1))
        self.assertEqual(set1['b'], Set(2))
        self.assertEqual(set1['c'], Set(3))
        set1 = basic_sets['not left func']
        self.assertEqual(set1['a'], Set(1, 4))
        self.assertEqual(set1['b'], Set(2))
        self.assertEqual(set1['c'], Set(3))
        set1 = basic_sets['diagonal']
        for left in relations.get_lefts(set1):
            self.assertEqual(set1[left], Set(left))
        # Clan of relations:
        self.assertEqual(algebra_clans['clan1']['a'], Set(1, 4))
        self.assertEqual(algebra_clans['clan2']['x'], Set('a'))
        self.assertEqual(algebra_clans['clan2']['zzz'], Set('zzz'))
        self.assertEqual(algebra_clans['clan3']['c'], Set(3, 5))
        self.assertEqual(algebra_clans['clan4'][3], Set('c'))
        self.assertEqual(algebra_clans['clan4'][5], Set('b', 'c'))
        self.assertEqual(algebra_clans['clan5']['b'], Set(2, 5))
        self.assertEqual(algebra_clans['clan5']['c'], Set(3))
        self.assertEqual(algebra_clans['clan5']['d'], Set())

    def test_right_functional(self):
        self.assertTrue(is_right_functional(Set()))
        self.assertIs(is_right_functional(Set('a', 'b', 'c')), Undef())
        f = is_right_functional(basic_sets['left func'])
        self.assertTrue(f)
        f = is_right_functional(basic_sets['not right func'])
        self.assertFalse(f)
        f = is_right_functional(basic_clans['left func'])
        self.assertTrue(f)
        f = is_right_functional(basic_clans['not right func'])
        self.assertFalse(f)
        f = is_right_functional(basic_hordes['left func'])
        self.assertTrue(f)
        f = is_right_functional(basic_hordes['not right func'])
        self.assertFalse(f)

        s = basic_sets['left func']
        self.assertEqual(s.cached_right_functional, CacheStatus.IS)
        s = basic_sets['not right func']
        self.assertEqual(s.cached_right_functional, CacheStatus.IS_NOT)

    def test_bijection(self):
        self.assertTrue(is_bijective(Set()))
        self.assertIs(is_bijective(Set('a', 'b', 'c')), Undef())
        f = is_bijective(basic_sets['left func'])
        self.assertTrue(f)
        f = is_bijective(basic_sets['not left func'])
        self.assertFalse(f)
        f = is_bijective(basic_sets['not right func'])
        self.assertFalse(f)
        f = is_bijective(basic_clans['left func'])
        self.assertTrue(f)
        f = is_bijective(basic_clans['not right func'])
        self.assertFalse(f)
        f = is_bijective(basic_hordes['left func'])
        self.assertTrue(f)
        f = is_bijective(basic_hordes['not right func'])
        self.assertFalse(f)

        s = basic_sets['left func']
        self.assertEqual(s.cached_functional, CacheStatus.IS)
        self.assertEqual(s.cached_right_functional, CacheStatus.IS)
        s = basic_sets['not left func']
        self.assertEqual(s.cached_functional, CacheStatus.IS_NOT)
        # The right flags aren't checked if left fails
        self.assertEqual(s.cached_right_functional, CacheStatus.UNKNOWN)

    def test_reflexive(self):
        self.assertTrue(is_reflexive(Set()))
        self.assertIs(is_reflexive(Set('a', 'b', 'c')), Undef())
        f = is_reflexive(basic_sets['not left func'])
        self.assertFalse(f)
        f = is_reflexive(basic_sets['diagonal'])
        self.assertTrue(f)
        f = is_reflexive(basic_clans['not left func'])
        self.assertFalse(f)
        f = is_reflexive(basic_clans['diagonal'])
        self.assertTrue(f)
        f = is_reflexive(basic_hordes['not left func'])
        self.assertFalse(f)
        f = is_reflexive(basic_hordes['diagonal'])
        self.assertTrue(f)

        s = basic_sets['diagonal']
        self.assertEqual(s.cached_reflexive, CacheStatus.IS)
        s = basic_sets['not left func']
        self.assertEqual(s.cached_reflexive, CacheStatus.IS_NOT)

    def test_symmetric(self):
        self.assertTrue(is_symmetric(Set()))
        self.assertTrue(is_symmetric(Set([Couplet(s, c) for s, c in zip('abcd', 'badc')])))
        self.assertIs(is_symmetric(Set('a', 'b', 'c')), Undef())
        f = is_symmetric(basic_sets['not left func'])
        self.assertFalse(f)
        f = is_symmetric(basic_sets['diagonal'])
        self.assertTrue(f)
        f = is_symmetric(basic_clans['not left func'])
        self.assertFalse(f)
        f = is_symmetric(basic_clans['diagonal'])
        self.assertTrue(f)
        f = is_symmetric(basic_hordes['not left func'])
        self.assertFalse(f)
        f = is_symmetric(basic_hordes['diagonal'])
        self.assertTrue(f)

        s = basic_sets['diagonal']
        self.assertEqual(s.cached_symmetric, CacheStatus.IS)
        s = basic_sets['not left func']
        self.assertEqual(s.cached_symmetric, CacheStatus.IS_NOT)

    def test_transitive(self):
        self.assertTrue(is_transitive(Set()))
        self.assertTrue(is_transitive(Set()))
        self.assertTrue(is_transitive(Set([Couplet(s, c) for c, s in zip('aba', 'bcc')])))
        self.assertIs(is_transitive(Set('a', 'b', 'c')), Undef())

        rel = Set(Couplet(s, c) for c, s in zip('aba', 'bcd'))
        self.assertFalse(is_transitive(rel))
        self.assertEqual(rel.cached_transitive, CacheStatus.IS_NOT)

        f = is_transitive(basic_sets['left func'])
        self.assertTrue(f)
        f = is_transitive(basic_sets['not left func'])
        self.assertTrue(f)
        f = is_transitive(basic_sets['diagonal'])
        self.assertTrue(f)
        f = is_transitive(basic_clans['not left func'])
        self.assertTrue(f)
        f = is_transitive(basic_clans['diagonal'])
        self.assertTrue(f)
        f = is_transitive(basic_hordes['not left func'])
        self.assertTrue(f)
        f = is_transitive(basic_hordes['diagonal'])
        self.assertTrue(f)

        s = basic_sets['left func']
        self.assertEqual(s.cached_transitive, CacheStatus.IS)

    def test_equivalence_relation(self):
        self.assertTrue(is_equivalence_relation(Set()))
        self.assertFalse(is_equivalence_relation(
            Set([Couplet(s, c) for c, s in zip('aba', 'bcc')])))
        self.assertIs(is_equivalence_relation(Set('a', 'b', 'c')), Undef())
        self.assertFalse(is_equivalence_relation(
            Set([Couplet(s, c) for c, s in zip('aba', 'bcd')])))
        f = is_equivalence_relation(basic_sets['left func'])
        self.assertFalse(f)
        f = is_equivalence_relation(basic_sets['not left func'])
        self.assertFalse(f)
        f = is_equivalence_relation(basic_sets['diagonal'])
        self.assertTrue(f)
        f = is_equivalence_relation(basic_clans['not left func'])
        self.assertFalse(f)
        f = is_equivalence_relation(basic_clans['diagonal'])
        self.assertTrue(f)
        f = is_equivalence_relation(basic_hordes['not left func'])
        self.assertFalse(f)
        f = is_equivalence_relation(basic_hordes['diagonal'])
        self.assertTrue(f)

        s = basic_sets['diagonal']
        self.assertEqual(s.cached_reflexive, CacheStatus.IS)
        self.assertEqual(s.cached_symmetric, CacheStatus.IS)
        self.assertEqual(s.cached_transitive, CacheStatus.IS)

    def test_project(self):
        clan = basic_clans['left func']

        if self.print_examples:
            ss = clan.get_left_set()
            pc = _convert_clan_to_list_of_dicts(ss, clan)
            print(clan)
            print(ss)
            print(pc)
        csv = io.StringIO()
        export_csv(clan, csv)
        csv_str = csv.getvalue()
        self.assertEqual(csv_str, "a,b,c\r\n1,2,3\r\n")
        if self.print_examples:
            # \r doesn't print well in the (PyCharm?) console
            csv_str_pr = 'csv:\n' + csv_str.replace('\r\n', '\n')
            print(csv_str_pr)

        clan = Set(Set([Couplet(s, c) for s, c in zip('abcd', [1, 2, 3, "foo, bar"])]))
        csv = io.StringIO()
        export_csv(clan, csv)
        csv_str = csv.getvalue()
        self.assertEqual(csv_str, """a,b,c,d\r\n1,2,3,"foo, bar"\r\n""")

    def test_flags_empty_set(self):
        s = Set()
        self.assertEqual(s.cached_relation, CacheStatus.IS)
        self.assertEqual(s.cached_clan, CacheStatus.IS)
        self.assertEqual(s.cached_multiclan, CacheStatus.IS_NOT)
        self.assertEqual(s.cached_functional, CacheStatus.IS)
        self.assertEqual(s.cached_right_functional, CacheStatus.IS)
        self.assertEqual(s.cached_regular, CacheStatus.IS)
        self.assertEqual(s.cached_reflexive, CacheStatus.IS)
        self.assertEqual(s.cached_symmetric, CacheStatus.IS)
        self.assertEqual(s.cached_transitive, CacheStatus.IS)

        self.assertRaises(AssertionError, lambda: s.cache_relation(CacheStatus.IS_NOT))
        self.assertRaises(AssertionError, lambda: s.cache_clan(CacheStatus.IS_NOT))
        self.assertRaises(AssertionError, lambda: s.cache_multiclan(CacheStatus.IS))

        self.assertRaises(AssertionError, lambda: s.cache_transitive(CacheStatus.IS_NOT))
        self.assertRaises(AssertionError, lambda: s.cache_functional(CacheStatus.IS_NOT))
        self.assertRaises(AssertionError, lambda: s.cache_right_functional(CacheStatus.IS_NOT))
        self.assertRaises(AssertionError, lambda: s.cache_regular(CacheStatus.IS_NOT))
        self.assertRaises(AssertionError, lambda: s.cache_reflexive(CacheStatus.IS_NOT))
        self.assertRaises(AssertionError, lambda: s.cache_symmetric(CacheStatus.IS_NOT))
        self.assertRaises(AssertionError, lambda: s.cache_transitive(CacheStatus.IS_NOT))

    def test_flags_set(self):
        s = Set(1, 2, 3)
        self.assertEqual(s.cached_relation, CacheStatus.UNKNOWN)
        self.assertEqual(s.cached_clan, CacheStatus.UNKNOWN)
        self.assertTrue(sets.is_member(s))  # This will NOT trigger structure check
        self.assertEqual(s.cached_relation, CacheStatus.UNKNOWN)
        self.assertEqual(s.cached_clan, CacheStatus.UNKNOWN)
        self.assertFalse(relations.is_member(s))  # This will trigger structure check
        self.assertEqual(s.cached_relation, CacheStatus.IS_NOT)
        self.assertEqual(s.cached_clan, CacheStatus.UNKNOWN)

    def test_flags_relation(self):
        r = Set(Couplet(s, c) for s, c in zip('abc', [1, 2, 3]))
        self.assertEqual(r.cached_relation, CacheStatus.UNKNOWN)
        self.assertEqual(r.cached_clan, CacheStatus.UNKNOWN)
        self.assertTrue(sets.is_member(r))  # This will NOT trigger structure check
        self.assertEqual(r.cached_relation, CacheStatus.UNKNOWN)
        self.assertEqual(r.cached_clan, CacheStatus.UNKNOWN)
        self.assertTrue(relations.is_member(r))  # This will trigger structure check
        self.assertEqual(r.cached_relation, CacheStatus.IS)
        self.assertEqual(r.cached_clan, CacheStatus.IS_NOT)

# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
