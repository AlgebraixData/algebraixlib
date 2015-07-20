"""Test the algebras.clans module."""

# $Id: test_algebras_multiclans.py 22614 2015-07-15 18:14:53Z gfiedler $
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
from algebraixlib.structure import CartesianProduct, GenesisSetA, GenesisSetM, GenesisSetN, PowerSet
from data_mathobjects import algebra_multiclans as ac
from algebraixlib.undef import RaiseOnUndef, Undef, UndefException

from algebraixlib.algebras.multiclans import \
    get_ground_set, get_absolute_ground_set, get_name, is_member, is_absolute_member, \
    compose, transpose, cross_union, functional_cross_union, \
    right_functional_cross_union, cross_intersect, substrict, superstrict


class MulticlansTest(unittest.TestCase):
    """Test the algebras.clans module."""

    print_examples = False

    def test_metadata(self):
        self.assertEqual(get_ground_set(), PowerSet(CartesianProduct(
            PowerSet(CartesianProduct(GenesisSetM(), GenesisSetM())), GenesisSetN())))
        self.assertEqual(get_absolute_ground_set(), PowerSet(CartesianProduct(
            PowerSet(CartesianProduct(GenesisSetA(), GenesisSetA())), GenesisSetN())))
        self.assertEqual(get_name(), 'Multiclans(M): P(P(M x M) x N)')

    def test_membership(self):
        self.assertTrue(is_member(Multiset(Set(Couplet(1, 2)))))
        self.assertFalse(is_member(Multiset(Couplet(3, 4))))
        self.assertTrue(is_absolute_member(Multiset(Set(Couplet(1, 2)))))
        self.assertFalse(is_absolute_member(Multiset(Set(Couplet(Set([2, 3]), 4)))))
        # noinspection PyTypeChecker
        self.assertRaises(TypeError, lambda: is_member(3))

    def test_set_ordering(self):
        self.assertEqual(ac['clan1'], ac['clan1reordered'])

    def test_compose(self):
        """Basic tests of clans.compose()."""
        self._check_wrong_argument_types_binary(compose)
        # Compose.
        result = compose(ac['clan1'], ac['clan2'])
        self.assertEqual(result, ac['clan1comp2'])
        result = compose(ac['clan2'], ac['clan1'])
        expected = ac['clan2comp1']
        self.assertEqual(result, expected)

    def test_transpose(self):
        """Basic tests of clans.transpose()."""
        self._check_wrong_argument_type_unary(transpose)
        # Transpose.
        result = transpose(ac['clan1'])
        self.assertEqual(result, ac['clan1transp'])

    def test_union(self):
        """Basic tests of clans.cross_union()."""
        self._check_wrong_argument_types_binary(cross_union)
        result = cross_union(ac['clan1'], ac['clan2'])
        self.assertEqual(result, ac['clan1union2'])

    def test_functional_cross_union(self):
        """Basic tests of clans.functional_cross_union()."""
        self._check_wrong_argument_types_binary(functional_cross_union)
        # Left-functional cross union.
        result = functional_cross_union(ac['clan1'], ac['clan2'])
        self.assertEqual(result, ac['clan1union2'])
        result = functional_cross_union(ac['clan1'], ac['clan3'])
        self.assertEqual(result, ac['clan1sfcu3'])
        result = functional_cross_union(ac['clan1'], ac['clan4'])
        self.assertEqual(result, ac['clan1sfcu4'])

    def test_right_functional_cross_union(self):
        """Basic tests of clans.right_functional_cross_union()."""
        self._check_wrong_argument_types_binary(right_functional_cross_union)
        # Right-functional cross union.
        result = right_functional_cross_union(ac['clan1'], ac['clan2'])
        self.assertEqual(result, ac['clan1union2'])
        result = right_functional_cross_union(ac['clan1'], ac['clan3'])
        self.assertEqual(result, ac['clan1cfcu3'])
        result = right_functional_cross_union(ac['clan1'], ac['clan4'])
        self.assertEqual(result, ac['clan1cfcu4'])

    def test_intersect(self):
        """Basic tests of clans.intersect()."""
        self._check_wrong_argument_types_binary(cross_intersect)
        result = cross_intersect(ac['clan1'], ac['clan3'])
        self.assertEqual(result, ac['clan1inters3'])

    def test_substrict(self):
        """Basic tests of clans.substrict()."""
        self._check_wrong_argument_types_binary(substrict)
        # Substriction.
        result = substrict(ac['clan1'], ac['clan2'])
        self.assertEqual(result, Multiset())
        result = substrict(ac['clan1'], ac['clan3'])
        self.assertEqual(result, ac['clan1subsupstr3'])

    def test_superstrict(self):
        """Basic tests of clans.superstrict()."""
        self._check_wrong_argument_types_binary(superstrict)
        # Superstriction.
        result = superstrict(ac['clan1'], ac['clan2'])
        self.assertEqual(result, Multiset())
        result = superstrict(ac['clan1'], ac['clan3'])
        self.assertEqual(result, ac['clan1subsupstr3'])

    # ----------------------------------------------------------------------------------------------

    def _check_wrong_argument_type_unary(self, operation):
        self.assertRaises(TypeError, lambda: operation(3))
        self.assertIs(operation(Atom(3)), Undef())
        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: operation(Set('a', 'b')))
        RaiseOnUndef.reset()

    def _check_wrong_argument_types_binary(self, operation):
        self.assertRaises(TypeError, lambda: operation(3, 4))
        self.assertRaises(TypeError, lambda: operation(Multiset(Set(Couplet(1, 2))), 3))
        self.assertIs(operation(Atom(3), Atom(4)), Undef())
        self.assertIs(operation(Multiset(Set(Couplet(1, 2))), Atom(3)), Undef())
        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: operation(Couplet(1, 2), Couplet(3, 4)))
        RaiseOnUndef.reset()

# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
