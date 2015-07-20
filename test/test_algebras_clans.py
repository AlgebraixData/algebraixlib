"""Test the algebras.clans module."""

# $Id: test_algebras_clans.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import io
import os
import textwrap
import unittest

from algebraixlib.io.csv import import_csv
from algebraixlib.mathobjects import Atom, Couplet, Set
from algebraixlib.structure import CartesianProduct, GenesisSetA, GenesisSetM, PowerSet
from algebraixlib.undef import RaiseOnUndef, Undef, UndefException
from algebraixlib.algebras.clans import *

# noinspection PyUnresolvedReferences
from data_mathobjects import algebra_clans as ac


class ClansTest(unittest.TestCase):
    """Test the algebras.clans module."""

    print_examples = False

    def test_metadata(self):
        self.assertEqual(get_ground_set(), PowerSet(
            PowerSet(CartesianProduct(GenesisSetM(), GenesisSetM()))))
        self.assertEqual(get_absolute_ground_set(), PowerSet(
            PowerSet(CartesianProduct(GenesisSetA(), GenesisSetA()))))
        self.assertEqual(get_name(), 'Clans(M): PP(M x M)')

    def test_membership(self):
        self.assertTrue(is_member(Set(Set(Couplet(1, 2)))))
        self.assertFalse(is_member(Set(Couplet(3, 4))))
        self.assertTrue(is_absolute_member(Set(Set(Couplet(1, 2)))))
        self.assertFalse(is_absolute_member(Set(Set(Couplet(Set([2, 3]), 4)))))
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
        self.assertEqual(result, ac['clan2comp1'])

    def test_transpose(self):
        """Basic tests of clans.transpose()."""
        self._check_wrong_argument_type_unary(transpose)
        result = transpose(ac['clan1'])
        self.assertEqual(result, ac['clan1transp'])

        c = ac['clan3']
        # Query the flag properties to verify propagation
        self.assertTrue(c.is_left_functional())
        self.assertFalse(c.is_right_functional())
        self.assertTrue(c.is_left_regular())
        r = transpose(c)

        self.assertTrue(c.cached_is_left_functional)
        self.assertFalse(c.cached_is_not_left_functional)
        self.assertFalse(c.cached_is_right_functional)
        self.assertTrue(c.cached_is_not_right_functional)

        # Without query, the result should have propagated flags
        self.assertFalse(r.cached_is_left_functional)
        self.assertTrue(r.cached_is_not_left_functional)
        self.assertTrue(r.cached_is_right_functional)
        self.assertFalse(r.cached_is_not_right_functional)
        self.assertFalse(r.cached_is_left_regular)  # Can't propagate
        self.assertFalse(r.cached_is_not_left_regular)
        self.assertFalse(r.is_left_regular())

    def test_union(self):
        """Basic tests of clans.union()."""
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

    def test_left_functional_cross_union(self):
        """Test for left_functional_cross_union."""
        table_a = import_csv(self._get_table_a())
        table_b = import_csv(self._get_table_b())

        # Calculate left join.
        result = lhs_functional_cross_union(table_a, table_b)

        # Test result set properties
        self.assertEqual(result.is_empty, False)
        self.assertEqual(result.cardinality, 8)
        expected = import_csv(self._get_result_left_functional_cross_union())
        self.assertEqual(result, expected)

        if self.print_examples:
            print('Expected set: {0}'.format(expected))
            print('Result set: {0}'.format(result))

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
        self.assertEqual(result, Set())
        result = substrict(ac['clan1'], ac['clan3'])
        self.assertEqual(result, ac['clan1subsupstr3'])

    def test_superstrict(self):
        """Basic tests of clans.superstrict()."""
        self._check_wrong_argument_types_binary(superstrict)
        # Superstriction.
        result = superstrict(ac['clan1'], ac['clan2'])
        self.assertEqual(result, Set())
        result = superstrict(ac['clan1'], ac['clan3'])
        self.assertEqual(result, ac['clan1subsupstr3'])

    def test_get_lefts(self):
        """Basic tests of clans.get_lefts()."""
        self._check_wrong_argument_type_unary(get_lefts)
        # Left set.
        for clan_idx in range(1, 6):
            clan_name = 'clan' + str(clan_idx)
            lefts_name = clan_name + '/lefts'
            result = get_lefts(ac[clan_name])
            self.assertEqual(result, ac[lefts_name])

        # The left set of a Set containing an empty Set is the empty set
        empty = get_lefts(Set(Set()))
        self.assertEqual(empty, Set())

        # The left set of an empty set is the empty set
        empty = get_lefts(Set())
        self.assertEqual(empty, Set())

    def test_get_rights(self):
        """Basic tests of clans.get_rights()."""
        self._check_wrong_argument_type_unary(get_rights)
        # Right set.
        for clan_idx in range(1, 6):
            clan_name = 'clan' + str(clan_idx)
            rights_name = clan_name + '/rights'
            result = get_rights(ac[clan_name])
            self.assertEqual(result, ac[rights_name])

        # The right set of a Set containing an empty Set is the empty set
        empty = get_rights(Set(Set()))
        self.assertEqual(empty, Set())

        # The right set of an empty set is the empty set
        empty = get_rights(Set())
        self.assertEqual(empty, Set())

    def test_left_functional_cache(self):
        """Basic tests of is_left_functional()."""
        c = ac['clan3']
        self.assertFalse(c.cached_is_left_functional)
        self.assertFalse(c.cached_is_not_left_functional)
        self.assertTrue(c.is_left_functional())
        self.assertTrue(c.cached_is_left_functional)
        self.assertFalse(c.cached_is_not_left_functional)
        self.assertTrue(c.is_left_functional())
        c = ac['clan4']
        self.assertFalse(c.cached_is_left_functional)
        self.assertFalse(c.cached_is_not_left_functional)
        self.assertFalse(c.is_left_functional())
        self.assertFalse(c.cached_is_left_functional)
        self.assertTrue(c.cached_is_not_left_functional)

    def test_right_functional_cache(self):
        """Basic tests of is_right_functional()."""
        c = ac['clan4']
        self.assertFalse(c.cached_is_right_functional)
        self.assertFalse(c.cached_is_not_right_functional)
        self.assertTrue(c.is_right_functional())
        self.assertTrue(c.cached_is_right_functional)
        self.assertFalse(c.cached_is_not_right_functional)
        self.assertTrue(c.is_right_functional())
        c = ac['clan3']
        self.assertFalse(c.cached_is_right_functional)
        self.assertFalse(c.cached_is_not_right_functional)
        self.assertFalse(c.is_right_functional())
        self.assertFalse(c.cached_is_right_functional)
        self.assertTrue(c.cached_is_not_right_functional)

    def test_left_regular_cache(self):
        """Basic tests of is_left_regular()."""
        c = ac['clan3']
        self.assertFalse(c.cached_is_left_regular)
        self.assertFalse(c.cached_is_not_left_regular)
        self.assertTrue(c.is_left_regular())
        self.assertTrue(c.cached_is_left_regular)
        self.assertFalse(c.cached_is_not_left_regular)
        self.assertTrue(c.is_left_regular())
        c = ac['clan5']
        self.assertFalse(c.cached_is_left_regular)
        self.assertFalse(c.cached_is_not_left_regular)
        self.assertFalse(c.is_left_regular())
        self.assertFalse(c.cached_is_left_regular)
        self.assertTrue(c.cached_is_not_left_regular)

    # ----------------------------------------------------------------------------------------------

    def _check_wrong_argument_type_unary(self, operation):
        self.assertRaises(TypeError, lambda: operation(3))
        self.assertIs(operation(Atom(3)), Undef())
        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: operation(Set('a', 'b')))
        RaiseOnUndef.reset()

    def _check_wrong_argument_types_binary(self, operation):
        self.assertRaises(TypeError, lambda: operation(3, 4))
        self.assertRaises(TypeError, lambda: operation(Set(Set(Couplet(1, 2))), 3))
        self.assertIs(operation(Atom(3), Atom(4)), Undef())
        self.assertIs(operation(Set(Set(Couplet(1, 2))), Atom(3)), Undef())
        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: operation(Couplet(1, 2), Couplet(3, 4)))
        RaiseOnUndef.reset()

    @staticmethod
    def _get_table_a():
        csv_text = textwrap.dedent("""\
            PK,AValue
            1,FOX
            2,COP
            3,TAXI
            6,WASHINGTON
            7,DELL
            5,ARIZONA
            4,LINCOLN
            10,LUCENT
            """)
        return io.StringIO(csv_text)

    @staticmethod
    def _get_table_b():
        csv_text = textwrap.dedent("""\
            PK,BValue
            1,TROT
            2,CAR
            3,CAB
            6,MONUMENT
            7,PC
            8,MICROSOFT
            9,APPLE
            11,SCOTCH
            """)
        return io.StringIO(csv_text)

    @staticmethod
    def _get_result_left_functional_cross_union():
        csv_text = textwrap.dedent("""\
            PK,AValue,BValue
            1,FOX,TROT
            2,COP,CAR
            3,TAXI,CAB
            4,LINCOLN,
            5,ARIZONA,
            6,WASHINGTON,MONUMENT
            7,DELL,PC
            10,LUCENT,
            """)
        return io.StringIO(csv_text)


# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
