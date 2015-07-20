"""Test the mathobjects.set module."""

# $Id: test_mathobjects_set.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import collections
import inspect
import io
import os
import unittest

import algebraixlib.algebras.relations as relations
import algebraixlib.algebras.sets as sets
from algebraixlib.mathobjects import Atom, Couplet, MathObject, Set
from algebraixlib.structure import CartesianProduct, GenesisSetA, PowerSet, Structure
from algebraixlib.undef import Undef
# noinspection PyProtectedMember
from algebraixlib.io.csv import _convert_clan_to_list_of_dicts, export_csv

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

    def test_is_powerset_property_method_return_undef(self):
        s1 = Set({Set({Set({Atom(3)})})})
        s2 = Set({Atom(1)}).get_ground_set()
        self.assertIs(s1._is_powerset_property(s2, 'get_left_set'), Undef())

    def test_left_regular(self):
        lefts = basic_sets['left func/lefts']
        self.assertTrue(Set().is_left_regular())
        self.assertIs(lefts.is_left_regular(), Undef())
        self.assertIs(basic_sets['left func'].is_left_regular(), Undef())
        self.assertTrue(basic_clans['left func'].is_left_regular())
        self.assertFalse(basic_clans['left func2'].is_left_regular())
        self.assertFalse(basic_clans['not left func'].is_left_regular())
        embedded_has_irregular_left = Set(basic_sets['left func'], basic_sets['not left func'])
        self.assertFalse(embedded_has_irregular_left.is_left_regular())
        self.assertTrue(basic_hordes['left func'].is_left_regular())
        self.assertFalse(basic_hordes['left func2'].is_left_regular())

        s = basic_sets['left func']
        self.assertFalse(s.cached_is_left_regular)
        self.assertFalse(s.cached_is_not_left_regular)

    def test_left_functional(self):
        self.assertTrue(Set().is_left_functional())
        self.assertIs(Undef(), Set('a', 'b', 'c').is_left_functional())
        f = basic_sets['left func'].is_left_functional()
        self.assertTrue(f)
        f = basic_sets['not left func'].is_left_functional()
        self.assertFalse(f)
        f = basic_clans['left func'].is_left_functional()
        self.assertTrue(f)
        f = basic_clans['not left func'].is_left_functional()
        self.assertFalse(f)
        f = basic_hordes['left func'].is_left_functional()
        self.assertTrue(f)
        f = basic_hordes['not left func'].is_left_functional()
        self.assertFalse(f)

        s = basic_sets['left func']
        self.assertTrue(s.cached_is_left_functional)
        self.assertFalse(s.cached_is_not_left_functional)
        s = basic_sets['not left func']
        self.assertFalse(s.cached_is_left_functional)
        self.assertTrue(s.cached_is_not_left_functional)

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
        self.assertTrue(Set().is_right_functional())
        self.assertIs(Undef(), Set('a', 'b', 'c').is_right_functional())
        f = basic_sets['left func'].is_right_functional()
        self.assertTrue(f)
        f = basic_sets['not right func'].is_right_functional()
        self.assertFalse(f)
        f = basic_clans['left func'].is_right_functional()
        self.assertTrue(f)
        f = basic_clans['not right func'].is_right_functional()
        self.assertFalse(f)
        f = basic_hordes['left func'].is_right_functional()
        self.assertTrue(f)
        f = basic_hordes['not right func'].is_right_functional()
        self.assertFalse(f)

        s = basic_sets['left func']
        self.assertTrue(s.cached_is_right_functional)
        self.assertFalse(s.cached_is_not_right_functional)
        s = basic_sets['not right func']
        self.assertFalse(s.cached_is_right_functional)
        self.assertTrue(s.cached_is_not_right_functional)

    def test_bijection(self):
        self.assertTrue(Set().is_bijection())
        self.assertIs(Undef(), Set('a', 'b', 'c').is_bijection())
        f = basic_sets['left func'].is_bijection()
        self.assertTrue(f)
        f = basic_sets['not left func'].is_bijection()
        self.assertFalse(f)
        f = basic_sets['not right func'].is_bijection()
        self.assertFalse(f)
        f = basic_clans['left func'].is_bijection()
        self.assertTrue(f)
        f = basic_clans['not right func'].is_bijection()
        self.assertFalse(f)
        f = basic_hordes['left func'].is_bijection()
        self.assertTrue(f)
        f = basic_hordes['not right func'].is_bijection()
        self.assertFalse(f)

        s = basic_sets['left func']
        self.assertTrue(s.cached_is_left_functional)
        self.assertTrue(s.cached_is_right_functional)
        self.assertFalse(s.cached_is_not_left_functional)
        self.assertFalse(s.cached_is_not_right_functional)
        s = basic_sets['not left func']
        self.assertFalse(s.cached_is_left_functional)
        self.assertTrue(s.cached_is_not_left_functional)
        # The right flags aren't checked if left fails
        self.assertFalse(s.cached_is_right_functional)
        self.assertFalse(s.cached_is_not_right_functional)

    def test_reflexive(self):
        self.assertTrue(Set().is_reflexive())
        self.assertIs(Undef(), Set('a', 'b', 'c').is_reflexive())
        f = basic_sets['not left func'].is_reflexive()
        self.assertFalse(f)
        f = basic_sets['diagonal'].is_reflexive()
        self.assertTrue(f)
        f = basic_clans['not left func'].is_reflexive()
        self.assertFalse(f)
        f = basic_clans['diagonal'].is_reflexive()
        self.assertTrue(f)
        f = basic_hordes['not left func'].is_reflexive()
        self.assertFalse(f)
        f = basic_hordes['diagonal'].is_reflexive()
        self.assertTrue(f)

        s = basic_sets['diagonal']
        self.assertTrue(s.cached_is_reflexive)
        self.assertFalse(s.cached_is_not_reflexive)
        s = basic_sets['not left func']
        self.assertFalse(s.cached_is_reflexive)
        self.assertTrue(s.cached_is_not_reflexive)

    def test_symmetric(self):
        self.assertTrue(Set().is_symmetric())
        self.assertTrue(Set([Couplet(s, c) for s, c in zip('abcd', 'badc')]).is_symmetric())
        self.assertIs(Undef(), Set('a', 'b', 'c').is_symmetric())
        f = basic_sets['not left func'].is_symmetric()
        self.assertFalse(f)
        f = basic_sets['diagonal'].is_symmetric()
        self.assertTrue(f)
        f = basic_clans['not left func'].is_symmetric()
        self.assertFalse(f)
        f = basic_clans['diagonal'].is_symmetric()
        self.assertTrue(f)
        f = basic_hordes['not left func'].is_symmetric()
        self.assertFalse(f)
        f = basic_hordes['diagonal'].is_symmetric()
        self.assertTrue(f)

        s = basic_sets['diagonal']
        self.assertTrue(s.cached_is_symmetric)
        self.assertFalse(s.cached_is_not_symmetric)
        s = basic_sets['not left func']
        self.assertFalse(s.cached_is_symmetric)
        self.assertTrue(s.cached_is_not_symmetric)

    def test_transitive(self):
        self.assertTrue(Set().is_transitive())
        self.assertTrue(Set([Couplet(s, c) for c, s in zip('aba', 'bcc')]).is_transitive())
        self.assertIs(Undef(), Set('a', 'b', 'c').is_transitive())
        rel = Set(Couplet(s, c) for c, s in zip('aba', 'bcd'))
        self.assertFalse(rel.is_transitive())
        f = basic_sets['left func'].is_transitive()
        self.assertTrue(f)
        f = basic_sets['not left func'].is_transitive()
        self.assertTrue(f)
        f = basic_sets['diagonal'].is_transitive()
        self.assertTrue(f)
        f = basic_clans['not left func'].is_transitive()
        self.assertTrue(f)
        f = basic_clans['diagonal'].is_transitive()
        self.assertTrue(f)
        f = basic_hordes['not left func'].is_transitive()
        self.assertTrue(f)
        f = basic_hordes['diagonal'].is_transitive()
        self.assertTrue(f)

        s = basic_sets['left func']
        self.assertTrue(s.cached_is_transitive)
        self.assertFalse(s.cached_is_not_transitive)

        self.assertFalse(rel.cached_is_transitive)
        self.assertTrue(rel.cached_is_not_transitive)

    def test_equivalence_relation(self):
        self.assertTrue(Set().is_equivalence_relation())
        self.assertFalse(Set([Couplet(s, c) for c, s in
                              zip('aba', 'bcc')]).is_equivalence_relation())
        self.assertIs(Undef(), Set('a', 'b', 'c').is_equivalence_relation())
        self.assertFalse(Set([Couplet(s, c) for c, s in
                              zip('aba', 'bcd')]).is_equivalence_relation())
        f = basic_sets['left func'].is_equivalence_relation()
        self.assertFalse(f)
        f = basic_sets['not left func'].is_equivalence_relation()
        self.assertFalse(f)
        f = basic_sets['diagonal'].is_equivalence_relation()
        self.assertTrue(f)
        f = basic_clans['not left func'].is_equivalence_relation()
        self.assertFalse(f)
        f = basic_clans['diagonal'].is_equivalence_relation()
        self.assertTrue(f)
        f = basic_hordes['not left func'].is_equivalence_relation()
        self.assertFalse(f)
        f = basic_hordes['diagonal'].is_equivalence_relation()
        self.assertTrue(f)

        s = basic_sets['diagonal']
        self.assertTrue(s.cached_is_reflexive)
        self.assertFalse(s.cached_is_not_reflexive)
        self.assertTrue(s.cached_is_symmetric)
        self.assertFalse(s.cached_is_not_symmetric)
        self.assertTrue(s.cached_is_transitive)
        self.assertFalse(s.cached_is_not_transitive)

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

    def test_flags_set(self):
        s = Set(1, 2, 3)
        self.assertFalse(s.cached_is_relation)
        self.assertFalse(s.cached_is_not_relation)
        self.assertFalse(s.cached_is_clan)
        self.assertFalse(s.cached_is_not_clan)
        self.assertTrue(sets.is_member(s))  # This will NOT trigger structure check
        self.assertFalse(s.cached_is_relation)
        self.assertFalse(s.cached_is_not_relation)
        self.assertFalse(s.cached_is_clan)
        self.assertFalse(s.cached_is_not_clan)
        self.assertFalse(relations.is_member(s))  # This will trigger structure check
        self.assertFalse(s.cached_is_relation)
        self.assertTrue(s.cached_is_not_relation)
        self.assertFalse(s.cached_is_clan)
        self.assertFalse(s.cached_is_not_clan)

    def test_flags_relation(self):
        r = Set(Couplet(s, c) for s, c in zip('abc', [1, 2, 3]))
        self.assertFalse(r.cached_is_relation)
        self.assertFalse(r.cached_is_not_relation)
        self.assertFalse(r.cached_is_clan)
        self.assertFalse(r.cached_is_not_clan)
        self.assertTrue(sets.is_member(r))  # This will NOT trigger structure check
        self.assertFalse(r.cached_is_relation)
        self.assertFalse(r.cached_is_not_relation)
        self.assertFalse(r.cached_is_clan)
        self.assertFalse(r.cached_is_not_clan)
        self.assertTrue(relations.is_member(r))  # This will trigger structure check
        self.assertTrue(r.cached_is_relation)
        self.assertFalse(r.cached_is_not_relation)
        self.assertFalse(r.cached_is_clan)
        self.assertTrue(r.cached_is_not_clan)

# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
