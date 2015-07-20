"""Test the algebras.relations module."""

# $Id: test_algebras_relations.py 22614 2015-07-15 18:14:53Z gfiedler $
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

from algebraixlib.mathobjects import Atom, Couplet, Set
from algebraixlib.structure import CartesianProduct, GenesisSetA, GenesisSetM, PowerSet
from data_mathobjects import algebra_relations as ar
from algebraixlib.undef import RaiseOnUndef, Undef, UndefException

from algebraixlib.algebras.relations import *
import algebraixlib.algebras.sets as sets


class RelationsTest(unittest.TestCase):
    """Test the algebras.relations module."""

    print_examples = False

    def test_metadata(self):
        self.assertEqual(get_ground_set(), PowerSet(CartesianProduct(GenesisSetM(), GenesisSetM())))
        self.assertEqual(get_absolute_ground_set(), PowerSet(
            CartesianProduct(GenesisSetA(), GenesisSetA())))
        self.assertEqual(get_name(), 'Relations(M): P(M x M)')

    # noinspection PyTypeChecker
    def test_membership(self):
        self.assertTrue(is_member(Set(Couplet(1, 2))))
        self.assertFalse(is_member(Couplet(3, 4)))
        self.assertTrue(is_absolute_member(Set(Couplet(1, 2))))
        self.assertFalse(is_absolute_member(Set(Couplet(Set(3), 4))))
        self.assertRaises(TypeError, lambda: is_member(3))

        s = Set(Couplet('field', Set(Couplet('name', 'Value'))),
                Couplet('field', Set(Couplet('name', 'Year'), Atom('1960'))))
        self.assertTrue(is_member(s))

    def test_compose(self):
        """Basic tests of relations.compose()."""
        self._check_wrong_argument_types_binary(compose)
        # Compose.
        # {(1^a),(2^b),(3^c)} * {(a^x),(zzz^zzz),(c^y)}
        result = compose(ar['rel1'], ar['rel2'])
        self.assertEqual(result, ar['rel1comp2'])
        # {(1^a),(2^b),(3^b)} * {(1^a),(2^b),(3^b)}
        result = compose(ar['rel1'], ar['rel1'])
        self.assertEqual(result, ar['rel1comp1'])
        # {(a^x),(zzz^zzz),(c^y)} * {(a^x),(zzz^zzz),(c^y)}
        result = compose(ar['rel2'], ar['rel2'])
        self.assertEqual(result, ar['rel2comp2'])

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

    def test_functional_union(self):
        """Test relations.right_functional_union() which produces the union of two
        relations where the result must be left functional."""
        self._check_wrong_argument_types_binary(functional_union)

        # Union of left functional relations is the same as sets.union()
        result = functional_union(ar['rel1'], ar['rel2'])
        self.assertEqual(result, sets.union(ar['rel1'], ar['rel2']))

        # Union of non-left functional relations is NOT the same as sets.union()
        result = functional_union(ar['rel1'], ar['reldiag'])
        self.assertIs(result, Undef())
        self.assertIsNot(result, sets.union(ar['rel1'], ar['reldiag']))

    def test_right_functional_union(self):
        """Test relations.right_functional_union() which produces the union of two
        relations where the result must be right functional."""
        self._check_wrong_argument_types_binary(right_functional_union)

        # Union of right functional relations is the same as sets.union()
        result = right_functional_union(ar['rel1'], ar['rel2'])
        self.assertEqual(result, sets.union(ar['rel1'], ar['rel2']))

        # Union of non-right functional relations is NOT the same as sets.union()
        result = right_functional_union(ar['rel1'], ar['reldiag'])
        self.assertIs(result, Undef())
        self.assertIsNot(result, sets.union(ar['rel1'], ar['reldiag']))

    def test_get_lefts(self):
        """Basic tests of relations.get_lefts()."""
        self._check_wrong_argument_type_unary(get_lefts)
        # left set.
        for rel_idx in range(1, 3):
            rel_name = 'rel' + str(rel_idx)
            lefts_names = rel_name + '/lefts'
            result = get_lefts(ar[rel_name])
            self.assertEqual(result, ar[lefts_names])

    def test_get_rights(self):
        """Basic tests of relations.get_rights()."""
        self._check_wrong_argument_type_unary(get_rights)
        # Right set.
        for rel_idx in range(1, 3):
            rel_name = 'rel' + str(rel_idx)
            rights_name = rel_name + '/rights'
            result = get_rights(ar[rel_name])
            self.assertEqual(result, ar[rights_name])

    def test_get_left(self):
        """Basic tests of relations.get_left()."""
        self.assertRaises(TypeError, lambda: get_left(3, 4))
        self.assertIs(get_left(Atom(3), 4), Undef())
        self.assertIs(get_left(Set(Couplet(1, 1), Couplet(2, 1)), Atom(1)), Undef())
        self.assertIs(get_left(Set(Couplet(1, 1), Couplet(1, 2)), Atom(0)), Undef())

        for rel_idx in range(1, 3):
            rel_name = 'rel' + str(rel_idx)
            for couplet in ar[rel_name].data:
                left = couplet.left.value
                right = couplet.right.value
                result = get_left(ar[rel_name], right)
                self.assertEqual(result.value, left)

    def test_get_right(self):
        """Basic tests of relations.get_right()."""
        self.assertRaises(TypeError, lambda: get_right(3, 4))
        self.assertIs(get_right(Atom(3), 4), Undef())
        self.assertIs(get_right(Set(Couplet(1, 2), Couplet(1, 3)), Atom(1)), Undef())
        self.assertIs(get_right(Set(Couplet(1, 2), Couplet(1, 3)), Atom(0)), Undef())

        for rel_idx in range(1, 3):
            rel_name = 'rel' + str(rel_idx)
            for couplet in ar[rel_name].data:
                left = couplet.left.value
                right = couplet.right.value
                result = get_right(ar[rel_name], left)
                self.assertEqual(result.value, right)

    def test_is_left_functional(self):
        """Basic tests of relations.is_left_functional()."""
        self.assertRaises(TypeError, lambda: is_left_functional(3))
        self.assertIs(is_left_functional(Atom(3)), Undef())
        for rel_idx in range(1, 3):
            rel_name = 'rel' + str(rel_idx)
            self.assertTrue(is_left_functional(ar[rel_name]))

    def test_is_right_functional(self):
        """Basic tests of relations.is_right_functional()."""
        self.assertRaises(TypeError, lambda: is_right_functional(3))
        self.assertIs(is_right_functional(Atom(3)), Undef())
        for rel_idx in range(1, 3):
            rel_name = 'rel' + str(rel_idx)
            self.assertTrue(is_right_functional(ar[rel_name]))

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

        # swap a/b, c/d
        relation2c = Set(Couplet('b', 1), Couplet('a', 2), Couplet('d', 3),
                         Couplet('c', 4), Couplet('x', 5))
        self.assertEqual(swap(relation2a, Set(Couplet('a', 'b'), Couplet('c', 'd'))), relation2c)

    def test_union(self):
        rel1 = Set(Couplet('a', 1), Couplet('b', 2)).cache_is_relation(True)
        rel2 = Set(Couplet('c', 3))
        self.assertFalse(sets.union(rel1, rel2).cached_is_relation)
        self.assertFalse(sets.union(rel1, rel2).cached_is_not_relation)
        self.assertTrue(is_member(rel2))
        self.assertTrue(sets.union(rel1, rel2).cached_is_relation)
        self.assertFalse(sets.union(rel1, rel2).cached_is_not_relation)

    # ----------------------------------------------------------------------------------------------

    def _check_wrong_argument_type_unary(self, operation):
        self.assertRaises(TypeError, lambda: operation(3))
        self.assertIs(operation(Atom(3)), Undef())
        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: operation(Set('a', 'b')))
        RaiseOnUndef.reset()

    def _check_wrong_argument_types_binary(self, operation):
        self.assertRaises(TypeError, lambda: operation(3, Set(Couplet(1, 2))))
        self.assertRaises(TypeError, lambda: operation(Set(Couplet(1, 2)), 4))
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
