"""Test the algebras.relations module."""

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

import algebraixlib.algebras.sets as sets
from algebraixlib.mathobjects import Atom, Couplet, Set
from algebraixlib.structure import CartesianProduct, GenesisSetA, GenesisSetM, PowerSet
from algebraixlib.undef import RaiseOnUndef, Undef, UndefException

from algebraixlib.algebras.relations import *

# noinspection PyUnresolvedReferences
from data_mathobjects import algebra_relations as ar


class RelationsTest(unittest.TestCase):
    """Test the algebras.relations module."""

    def test_metadata(self):
        self.assertEqual(get_ground_set(), PowerSet(CartesianProduct(GenesisSetM(), GenesisSetM())))
        self.assertEqual(get_absolute_ground_set(), PowerSet(
            CartesianProduct(GenesisSetA(), GenesisSetA())))
        self.assertEqual(get_name(), 'Relations(M): P(M x M)')

    # noinspection PyTypeChecker
    def test_membership(self):
        self.assertTrue(is_member(Set(Couplet(1, 2))))
        self.assertFalse(is_member(Couplet(3, 4)))
        self.assertFalse(is_member(Undef()))
        self.assertTrue(is_absolute_member(Set(Couplet(1, 2))))
        self.assertFalse(is_absolute_member(Set(Couplet(Set(3), 4))))
        self.assertFalse(is_absolute_member(Undef()))
        self.assertRaises(AttributeError, lambda: is_member(3))

        s = Set(Couplet('field', Set(Couplet('name', 'Value'))),
                Couplet('field', Set(Couplet('name', 'Year'), Atom('1960'))))
        self.assertTrue(is_member(s))

    def test_compose(self):
        """Basic tests of relations.compose()."""
        self._check_wrong_argument_types_binary(compose)
        # Compose.
        rel1 = ar['rel1']
        rel2 = ar['rel2']
        result = compose(rel1, rel2)
        self.assertEqual(result, ar['rel1comp2'])
        result = compose(rel1, rel1)
        self.assertEqual(result, ar['rel1comp1'])
        result = compose(rel2, rel2)
        self.assertEqual(result, ar['rel2comp2'])
        self.assertIs(compose(rel1, Undef()), Undef())
        self.assertIs(compose(Undef(), rel1), Undef())
        self.assertIs(compose(rel1, Undef(), _checked=False), Undef())
        self.assertIs(compose(Undef(), rel1, _checked=False), Undef())

    def test_compose_diagonal(self):
        """Compose sets with the diagonal (identity)."""
        self.assertEqual(compose(ar['rel1'], ar['reldiag']), ar['rel1'])
        self.assertEqual(compose(ar['rel2'], ar['reldiag']), ar['rel2'])
        self.assertEqual(compose(ar['rel1comp2'], ar['reldiag']), ar['rel1comp2'])
        self.assertEqual(compose(ar['rel1transp'], ar['reldiag']), ar['rel1transp'])
        # Commuted
        self.assertEqual(compose(ar['reldiag'], ar['rel1']), ar['rel1'])
        self.assertEqual(compose(ar['reldiag'], ar['rel2']), ar['rel2'])
        self.assertEqual(compose(ar['reldiag'], ar['rel1comp2']), ar['rel1comp2'])
        self.assertEqual(compose(ar['reldiag'], ar['rel1transp']), ar['rel1transp'])
        # Diagonal composed with itself
        self.assertEqual(compose(ar['reldiag'], ar['reldiag']), ar['reldiag'])

    def test_transpose(self):
        """Basic tests of relations.transpose()."""
        self._check_wrong_argument_type_unary(transpose)
        # Transpose.
        result = transpose(ar['rel1'])
        self.assertEqual(result, ar['rel1transp'])
        result = transpose(ar['reldiag'])
        self.assertEqual(result, ar['reldiag'])
        self.assertIs(transpose(Undef()), Undef())
        self.assertIs(transpose(Undef(), _checked=False), Undef())

    def test_functional_union(self):
        """Test relations.right_functional_union() which produces the union of two
        relations where the result must be functional."""
        self._check_wrong_argument_types_binary(functional_union)

        rel1 = ar['rel1']
        # Union of functional relations is the same as sets.union()
        result = functional_union(rel1, ar['rel2'])
        self.assertEqual(result, sets.union(rel1, ar['rel2']))

        # Union of non-functional relations is NOT the same as sets.union()
        result = functional_union(rel1, ar['reldiag'])
        self.assertIs(result, Undef())
        self.assertIsNot(result, sets.union(rel1, ar['reldiag']))

        self.assertIs(functional_union(rel1, Undef()), Undef())
        self.assertIs(functional_union(Undef(), rel1), Undef())
        self.assertIs(functional_union(rel1, Undef(), _checked=False), Undef())
        self.assertIs(functional_union(Undef(), rel1, _checked=False), Undef())

    def test_right_functional_union(self):
        """Test relations.right_functional_union() which produces the union of two
        relations where the result must be right functional."""
        self._check_wrong_argument_types_binary(right_functional_union)

        rel1 = ar['rel1']
        # Union of right functional relations is the same as sets.union()
        result = right_functional_union(rel1, ar['rel2'])
        self.assertEqual(result, sets.union(rel1, ar['rel2']))

        # Union of non-right functional relations is NOT the same as sets.union()
        result = right_functional_union(rel1, ar['reldiag'])
        self.assertIs(result, Undef())
        self.assertIsNot(result, sets.union(rel1, ar['reldiag']))

        self.assertIs(right_functional_union(rel1, Undef()), Undef())
        self.assertIs(right_functional_union(Undef(), rel1), Undef())
        self.assertIs(right_functional_union(rel1, Undef(), _checked=False), Undef())
        self.assertIs(right_functional_union(Undef(), rel1, _checked=False), Undef())

    def test_get_lefts(self):
        """Basic tests of relations.get_lefts()."""
        self._check_wrong_argument_type_unary(get_lefts)
        # left set.
        for rel_idx in range(1, 3):
            rel_name = 'rel' + str(rel_idx)
            lefts_names = rel_name + '/lefts'
            result = get_lefts(ar[rel_name])
            self.assertEqual(result, ar[lefts_names])

        self.assertIs(get_lefts(Undef()), Undef())
        self.assertIs(get_lefts(Undef(), _checked=False), Undef())

    def test_get_rights(self):
        """Basic tests of relations.get_rights()."""
        self._check_wrong_argument_type_unary(get_rights)
        # Right set.
        for rel_idx in range(1, 3):
            rel_name = 'rel' + str(rel_idx)
            rights_name = rel_name + '/rights'
            result = get_rights(ar[rel_name])
            self.assertEqual(result, ar[rights_name])

        self.assertIs(get_rights(Undef()), Undef())
        self.assertIs(get_rights(Undef(), _checked=False), Undef())

    def test_get_rights_for_left(self):
        """Basic tests of relations.get_rights_for_left()."""
        rel1 = Set(Couplet('a', 1), Couplet('a', 2), Couplet('b', 3))
        result = Set(1, 2)
        self.assertEqual(result, get_rights_for_left(rel1, 'a'))
        self.assertEqual(Set(), get_rights_for_left(rel1, Undef()))
        self.assertEqual(Set(), get_rights_for_left(rel1, Undef(), _checked=False))

        self.assertIs(get_rights_for_left(Undef(), 'a'), Undef())
        self.assertRaises(AssertionError, lambda: get_rights_for_left(Undef(), 'a', _checked=False))
        self.assertIs(get_rights_for_left(Undef(), Atom('a'), _checked=False), Undef())

    def test_get_left(self):
        """Basic tests of relations.get_left()."""
        self.assertRaises(AttributeError, lambda: get_left(3, 4))
        self.assertIs(get_left(Atom(3), 4), Undef())
        self.assertIs(get_left(Set(Couplet(1, 1), Couplet(2, 1)), Atom(1)), Undef())
        self.assertIs(get_left(Set(Couplet(1, 1), Couplet(1, 2)), Atom(0)), Undef())

        rel1 = ar['rel1']
        self.assertIs(get_left(rel1, Undef()), Undef())
        self.assertIs(get_left(rel1, Undef(), _checked=False), Undef())
        self.assertIs(get_left(Undef(), 'a'), Undef())
        self.assertRaises(AssertionError, lambda: get_left(Undef(), 'a', _checked=False))
        self.assertIs(get_left(Undef(), Atom('a'), _checked=False), Undef())

        for rel_idx in range(1, 3):
            rel_name = 'rel' + str(rel_idx)
            for couplet in ar[rel_name].data:
                left = couplet.left.value
                right = couplet.right.value
                result = get_left(ar[rel_name], right)
                self.assertEqual(result.value, left)

    def test_get_right(self):
        """Basic tests of relations.get_right()."""
        self.assertRaises(AttributeError, lambda: get_right(3, 4))
        self.assertIs(get_right(Atom(3), 4), Undef())
        self.assertIs(get_right(Set(Couplet(1, 2), Couplet(1, 3)), Atom(1)), Undef())
        self.assertIs(get_right(Set(Couplet(1, 2), Couplet(1, 3)), Atom(0)), Undef())

        rel1 = ar['rel1']
        self.assertIs(get_right(rel1, Undef()), Undef())
        self.assertIs(get_right(rel1, Undef(), _checked=False), Undef())
        self.assertIs(get_right(Undef(), 'a'), Undef())
        self.assertRaises(AssertionError, lambda: get_right(Undef(), 'a', _checked=False))
        self.assertIs(get_right(Undef(), Atom('a'), _checked=False), Undef())

        for rel_idx in range(1, 3):
            rel_name = 'rel' + str(rel_idx)
            for couplet in ar[rel_name].data:
                left = couplet.left.value
                right = couplet.right.value
                result = get_right(ar[rel_name], left)
                self.assertEqual(result.value, right)

    def test_is_functional(self):
        """Basic tests of relations.is_functional()."""
        self.assertRaises(AttributeError, lambda: is_functional(3))
        self.assertIs(is_functional(Atom(3)), Undef())
        self.assertIs(is_functional(Undef()), Undef())
        self.assertIs(is_functional(Undef(), _checked=False), Undef())
        for rel_idx in range(1, 3):
            rel_name = 'rel' + str(rel_idx)
            self.assertTrue(is_functional(ar[rel_name]))

    def test_is_right_functional(self):
        """Basic tests of relations.is_right_functional()."""
        self.assertRaises(AttributeError, lambda: is_right_functional(3))
        self.assertIs(is_right_functional(Atom(3)), Undef())
        self.assertIs(is_right_functional(Undef()), Undef())
        self.assertIs(is_right_functional(Undef(), _checked=False), Undef())
        for rel_idx in range(1, 3):
            rel_name = 'rel' + str(rel_idx)
            self.assertTrue(is_right_functional(ar[rel_name]))

    def test_is_reflexive(self):
        """Basic tests of relations.is_reflexive()."""
        self.assertRaises(AttributeError, lambda: is_reflexive(3))
        self.assertIs(is_reflexive(Atom(3)), Undef())
        self.assertIs(is_reflexive(Undef()), Undef())
        self.assertIs(is_reflexive(Undef(), _checked=False), Undef())
        self.assertTrue(is_reflexive(Set(Couplet('a', 'a'))))
        self.assertFalse(is_reflexive(Set(Couplet('a', 'b'))))

    def test_is_symmetric(self):
        """Basic tests of relations.is_symmetric()."""
        self.assertRaises(AttributeError, lambda: is_symmetric(3))
        self.assertIs(is_symmetric(Atom(3)), Undef())
        self.assertIs(is_symmetric(Undef()), Undef())
        self.assertIs(is_symmetric(Undef(), _checked=False), Undef())
        self.assertTrue(is_symmetric(Set(Couplet('a', 'b'), Couplet('b', 'a'))))
        self.assertFalse(is_symmetric(Set(Couplet('a', 'b'))))

    def test_is_transitive(self):
        """Basic tests of relations.is_transitive()."""
        self.assertRaises(AttributeError, lambda: is_transitive(3))
        self.assertIs(is_transitive(Atom(3)), Undef())
        self.assertIs(is_transitive(Undef()), Undef())
        self.assertIs(is_transitive(Undef(), _checked=False), Undef())
        self.assertTrue(is_transitive(Set(Couplet('a', 'b'), Couplet('b', 'c'), Couplet('a', 'c'))))
        self.assertFalse(is_transitive(Set(Couplet('a', 'b'), Couplet('b', 'c'))))

    def test_fill_lefts(self):
        rel1 = Set(Couplet('a', 1), Couplet('b', 2))
        rel2 = Set(Couplet('x', 'y'))
        exp = Set(Couplet('a'), Couplet('b'), Couplet('x', 'y'))
        self.assertEqual(fill_lefts(rel1, rel2), exp)

        self.assertIs(fill_lefts(rel1, Undef()), Undef())
        self.assertIs(fill_lefts(rel1, Undef(), _checked=False), Undef())
        self.assertIs(fill_lefts(Undef(), rel2), Undef())
        self.assertIs(fill_lefts(Undef(), rel2, _checked=False), Undef())

    def test_rename_swap(self):
        relation1a = Set(Couplet('a', 1), Couplet('b', 2))
        relation1b = Set(Couplet('a', 1), Couplet('a', 2))

        relation2a = Set(Couplet('a', 1), Couplet('b', 2), Couplet('c', 3),
                         Couplet('d', 4), Couplet('x', 5))
        relation2b = Set(Couplet('a', 1), Couplet('a', 2), Couplet('c', 3),
                         Couplet('d', 4), Couplet('x', 5))
        # rename b to a
        self.assertEqual(rename(relation1a, Set(Couplet('a', 'b'))), relation1b)
        self.assertEqual(rename(relation2a, Set(Couplet('a', 'b'))), relation2b)

        self.assertIs(rename(relation1a, Undef()), Undef())
        self.assertIs(rename(relation1a, Undef(), _checked=False), Undef())
        self.assertIs(rename(Undef(), relation1a), Undef())
        self.assertIs(rename(Undef(), relation1a, _checked=False), Undef())

        # swap a/b, c/d
        relation2c = Set(Couplet('b', 1), Couplet('a', 2), Couplet('d', 3),
                         Couplet('c', 4), Couplet('x', 5))
        self.assertEqual(swap(relation2a, Set(Couplet('a', 'b'), Couplet('c', 'd'))), relation2c)

        self.assertIs(swap(relation1a, Undef()), Undef())
        self.assertIs(swap(relation1a, Undef(), _checked=False), Undef())
        self.assertIs(swap(Undef(), relation1a), Undef())
        self.assertIs(swap(Undef(), relation1a, _checked=False), Undef())

    def test_functional_add(self):
        rel1 = Set(Couplet('a', 1))
        couplet = Couplet('b', 1)
        rel2 = Set(Couplet('a', 1), Couplet('b', 1))

        self.assertEqual(functional_add(rel1, couplet), rel2)
        self.assertIs(functional_add(rel1, Undef()), Undef())
        self.assertIs(functional_add(Undef(), couplet), Undef())

    def test_from_dict(self):
        rel1 = Set(Couplet('a', 1), Couplet('b', 2))
        self.assertEqual(rel1, from_dict({'a': 1, 'b': 2}))
        self.assertRaises(AttributeError, lambda: from_dict(Undef()))

    def test_diag(self):
        rel1 = Set(Couplet('a', 'a'), Couplet('b', 'b'))
        self.assertEqual(diag('a', 'b'), rel1)
        self.assertEqual(diag(), Set())

        self.assertIs(diag(Undef()), Undef())
        self.assertIs(diag(Undef(), _checked=False), Undef())

    def test_defined_at(self):
        rel1 = Set(Couplet('a', 1))
        self.assertEqual(defined_at(rel1, 'a'), rel1)

        self.assertIs(defined_at(rel1, 'b'), Undef())
        self.assertIs(defined_at(rel1, Undef()), Undef())
        self.assertIs(defined_at(Undef(), 'a'), Undef())
        self.assertRaises(AssertionError, lambda: defined_at(rel1, 'a', _checked=False))
        self.assertIs(defined_at(Undef(), Atom('a'), _checked=False), Undef())
        self.assertEqual(defined_at(rel1, Atom('a'), _checked=False), rel1)

    # ----------------------------------------------------------------------------------------------

    def _check_wrong_argument_type_unary(self, operation):
        self.assertRaises(AttributeError, lambda: operation(3))
        self.assertIs(operation(Atom(3)), Undef())
        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: operation(Set('a', 'b')))
        RaiseOnUndef.reset()

    def _check_wrong_argument_types_binary(self, operation):
        self.assertRaises(AttributeError, lambda: operation(3, Set(Couplet(1, 2))))
        self.assertRaises(AttributeError, lambda: operation(Set(Couplet(1, 2)), 4))
        self.assertIs(operation(Set(Couplet(1, 2)), Atom(4)), Undef())
        self.assertIs(operation(Atom(3), Set(Couplet(1, 2))), Undef())
        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: operation(Couplet(1, 2), Couplet(3, 4)))
        RaiseOnUndef.reset()

# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
