"""Test the algebras.clans module."""

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

from algebraixlib.mathobjects import Atom, Couplet, Set, Multiset
from algebraixlib.structure import CartesianProduct, GenesisSetA, GenesisSetM, GenesisSetN, PowerSet
from algebraixlib.undef import RaiseOnUndef, Undef, UndefException

from algebraixlib.algebras.multiclans import \
    get_ground_set, get_absolute_ground_set, get_name, is_member, is_absolute_member, \
    compose, transpose, cross_union, cross_functional_union, \
    cross_right_functional_union, cross_intersect, substrict, superstrict, get_lefts, get_rights, \
    get_rights_for_left, is_functional, is_right_functional, is_regular, is_right_regular, \
    is_reflexive, is_symmetric, is_transitive, project, defined_at, diag, from_dict

# noinspection PyUnresolvedReferences
from data_mathobjects import algebra_multiclans as ac


class MulticlansTest(unittest.TestCase):
    """Test the algebras.clans module."""

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
        self.assertFalse(is_absolute_member(Multiset(Set(Couplet(Set(2, 3), 4)))))
        self.assertFalse(is_absolute_member(Set(2, 3)))
        # noinspection PyTypeChecker
        self.assertRaises(AttributeError, lambda: is_member(3))

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

    def test_cross_functional_union(self):
        """Basic tests of clans.cross_functional_union()."""
        self._check_wrong_argument_types_binary(cross_functional_union)
        # cross-functional union.
        result = cross_functional_union(ac['clan1'], ac['clan2'])
        self.assertEqual(result, ac['clan1union2'])
        result = cross_functional_union(ac['clan1'], ac['clan3'])
        self.assertEqual(result, ac['clan1sfcu3'])
        result = cross_functional_union(ac['clan1'], ac['clan4'])
        self.assertEqual(result, ac['clan1sfcu4'])

    def test_cross_right_functional_union(self):
        """Basic tests of clans.cross_right_functional_union()."""
        self._check_wrong_argument_types_binary(cross_right_functional_union)
        # cross-right-functional union.
        result = cross_right_functional_union(ac['clan1'], ac['clan2'])
        self.assertEqual(result, ac['clan1union2'])
        result = cross_right_functional_union(ac['clan1'], ac['clan3'])
        self.assertEqual(result, ac['clan1cfcu3'])
        result = cross_right_functional_union(ac['clan1'], ac['clan4'])
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

    def test_get_lefts(self):
        """Basic tests of clans.get_lefts()."""
        self._check_wrong_argument_type_unary(get_lefts)
        self.assertEqual(get_lefts(Multiset()), Multiset())

    def test_get_rights(self):
        """Basic tests of clans.get_rights()."""
        self._check_wrong_argument_type_unary(get_rights)
        self.assertEqual(get_rights(Multiset()), Multiset())

    def test_get_rights_for_left(self):
        """Basic tests of clans.get_rights_for_left()."""
        mc = ac['clan1']
        self.assertEqual(Set(), get_rights_for_left(mc, Undef()))
        self.assertEqual(Set(), get_rights_for_left(mc, Undef(), _checked=False))

        self.assertIs(get_rights_for_left(Undef(), 'a'), Undef())
        self.assertRaises(AssertionError, lambda: get_rights_for_left(Undef(), 'a', _checked=False))
        self.assertIs(get_rights_for_left(Undef(), Atom('a'), _checked=False), Undef())

    def test_is_functional(self):
        """Basic tests of multiclans.is_functional()."""
        self._check_wrong_argument_type_unary(is_functional)

    def test_is_right_functional(self):
        """Basic tests of multiclans.is_right_functional()."""
        self._check_wrong_argument_type_unary(is_right_functional)

    def test_is_regular(self):
        """Basic tests of multiclans.is_regular()."""
        self._check_wrong_argument_type_unary(is_regular)

    def test_is_right_regular(self):
        """Basic tests of multiclans.is_right_regular()."""
        self._check_wrong_argument_type_unary(is_right_regular)

    def test_is_reflexive(self):
        """Basic tests of multiclans.is_reflexive()."""
        self._check_wrong_argument_type_unary(is_reflexive)

    def test_is_symmetric(self):
        """Basic tests of multiclans.is_symmetric()."""
        self._check_wrong_argument_type_unary(is_symmetric)

    def test_is_transitive(self):
        """Basic tests of multiclans.is_transitive()."""
        self._check_wrong_argument_type_unary(is_transitive)

    def test_from_dict(self):
        """Basic tests of multiclans.from_dict()."""
        c1 = Multiset(Set(Couplet('a', 1), Couplet('b', 2)))
        self.assertEqual(c1, from_dict({'a': 1, 'b': 2}))
        self.assertRaises(AttributeError, lambda: from_dict(Undef()))

    def test_diag(self):
        """Basic tests of multiclans.diag()."""
        clan1 = Multiset(Set(Couplet('a'), Couplet('b')))
        self.assertEqual(diag('a', 'b'), clan1)
        self.assertEqual(diag(), Multiset(Set()))

        self.assertIs(diag(Undef()), Undef())
        self.assertIs(diag(Undef(), _checked=False), Undef())

    def test_project(self):
        """Basic tests of multiclans.project()."""
        self.assertIs(project(Undef(), Undef()), Undef())
        c1 = ac['clan1']
        self.assertIs(project(c1, Undef()), Undef())
        c2 = Multiset(Set(Couplet('a', 1)), Set(Couplet('a', 4)))
        self.assertEqual(project(c1, 'a'), c2)

    def test_defined_at(self):
        c1 = ac['clan1']
        self.assertEqual(defined_at(c1, 'a'), c1)

        self.assertIs(defined_at(c1, 'd'), Undef())
        self.assertIs(defined_at(c1, Undef()), Undef())
        self.assertIs(defined_at(Undef(), 'a'), Undef())
        self.assertRaises(AssertionError, lambda: defined_at(c1, 'a', _checked=False))
        self.assertIs(defined_at(Undef(), Atom('a'), _checked=False), Undef())
        self.assertEqual(defined_at(c1, Atom('a'), _checked=False), c1)

    # ----------------------------------------------------------------------------------------------

    def _check_wrong_argument_type_unary(self, operation):
        self.assertRaises(AttributeError, lambda: operation(3))
        self.assertIs(operation(Atom(3)), Undef())
        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: operation(Set('a', 'b')))
        RaiseOnUndef.reset()

        self.assertIs(operation(Undef()), Undef())
        self.assertIs(operation(Undef(), _checked=False), Undef())

    def _check_wrong_argument_types_binary(self, operation):
        self.assertRaises(AttributeError, lambda: operation(3, 4))
        self.assertRaises(AttributeError, lambda: operation(Multiset(Set(Couplet(1, 2))), 3))
        self.assertIs(operation(Atom(3), Atom(4)), Undef())
        self.assertIs(operation(Multiset(Set(Couplet(1, 2))), Atom(3)), Undef())
        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: operation(Couplet(1, 2), Couplet(3, 4)))
        RaiseOnUndef.reset()

        c = ac['clan1']
        self.assertIs(operation(c, Undef()), Undef())
        self.assertIs(operation(c, Undef(), _checked=False), Undef())
        self.assertIs(operation(Undef(), c), Undef())
        self.assertIs(operation(Undef(), c, _checked=False), Undef())

# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
