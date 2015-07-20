"""Test the structure module."""

# $Id: test_structure.py 22614 2015-07-15 18:14:53Z gfiedler $
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

from data_structures import empties, setas, setms, setns, basic_cps, basic_unions, basic_pss
from algebraixlib.structure import CartesianProduct, GenesisSetA, GenesisSetM, GenesisSetN, PowerSet, Structure, Union


class StructureTest(unittest.TestCase):
    """Test the structure module."""

    print_examples = False

    def test_Structure(self):
        """Basic properties of empty set structure."""
        self._basic_assert(empties, Structure)
        self._equality_helper(empties)
        # Equality and subset relationships, hashing.
        for structs in setas, setms, basic_cps, basic_unions, basic_pss:
            for struct in structs.values():
                self._inequality_assert(Structure(), struct)
                self._subset_assert(Structure(), struct)
                self.assertNotEqual(hash(Structure()), hash(struct))

    def test_GenSetA(self):
        """Basic properties of genesis set A."""
        self._basic_assert(setas, GenesisSetA)
        self._equality_helper(setas)
        # Equality relationships.
        self._inequality_assert(GenesisSetA(), GenesisSetM())
        # Subset relationships.
        self._subset_assert(GenesisSetA(), GenesisSetM())
        # Test hashing.
        self.assertNotEqual(hash(GenesisSetA()), hash(GenesisSetM()))

    def test_GenSetM(self):
        """Basic properties of genesis set M."""
        self._basic_assert(setms, GenesisSetM)
        self._equality_helper(setms)
        # Equality relationships.
        self._inequality_assert(GenesisSetM(), GenesisSetA())
        # Subset relationships.
        self.assertFalse(GenesisSetM().is_subset(GenesisSetA()))
        self.assertFalse(GenesisSetM() <= GenesisSetA())
        # Test hashing.
        self.assertNotEqual(hash(GenesisSetM()), hash(GenesisSetA()))

    def test_GenSetN(self):
        """Basic properties of genesis set M."""
        self._basic_assert(setns, GenesisSetN)
        self._equality_helper(setns)
        # Equality relationships.
        self._inequality_assert(GenesisSetN(), GenesisSetA())
        # Subset relationships.
        self.assertFalse(GenesisSetN().is_subset(GenesisSetA()))
        self.assertFalse(GenesisSetN() <= GenesisSetA())
        # Test hashing.
        self.assertNotEqual(hash(GenesisSetN()), hash(GenesisSetA()))

    def test_CartesianProduct(self):
        """Basic properties of the cartesian product."""
        self._basic_assert(basic_cps, CartesianProduct)
        self._equality_helper(basic_cps)
        # Subset relationships.
        self._subset_assert(basic_cps['AxA'], basic_cps['AxM'])
        self._subset_assert(basic_cps['AxA'], basic_cps['MxM'])
        self._subset_assert(basic_cps['AxM'], basic_cps['MxM'])
        for cp in [basic_cps['AxA'], basic_cps['AxM'], basic_cps['MxM']]:
            self.assertFalse(cp.is_subset(basic_cps['Ax(AxA)']))

    def test_Union(self):
        """Basic properties and subset relationships of the union."""
        self._basic_assert(basic_unions, Union)
        self._equality_helper(basic_unions)
        # Equality relationships.
        self.assertEqual(basic_unions['M'], basic_unions['M-2'])
        self.assertEqual(basic_unions['M-4 U(AxM)'], basic_unions['M-4 U(AxM)-2'])
        # Subset relationships.
        self._subset_assert(basic_unions['A'], basic_unions['M'])
        self._subset_assert(basic_unions['A'], basic_unions['M-2'])
        self._subset_assert(basic_unions['A'], basic_unions['AU(AxA)'])
        self._subset_assert(basic_unions['A'], basic_unions['M-3 U(AxA)'])
        self._subset_assert(basic_unions['A'], basic_unions['M-4 U(AxM)'])
        self._subset_assert(basic_unions['A'], basic_unions['M-4 U(AxM)-2'])
        self._subset_assert(basic_unions['M'], basic_unions['M-2'])
        self._subset_deny(basic_unions['M'], basic_unions['AU(AxA)'])
        self._subset_assert(basic_unions['M'], basic_unions['M-3 U(AxA)'])
        self._subset_assert(basic_unions['M'], basic_unions['M-4 U(AxM)'])
        self._subset_assert(basic_unions['M'], basic_unions['M-4 U(AxM)-2'])
        self._subset_deny(basic_unions['M-2'], basic_unions['AU(AxA)'])
        self._subset_assert(basic_unions['M-2'], basic_unions['M-3 U(AxA)'])
        self._subset_assert(basic_unions['M-2'], basic_unions['M-4 U(AxM)'])
        self._subset_assert(basic_unions['M-2'], basic_unions['M-4 U(AxM)-2'])
        self._subset_assert(basic_unions['AU(AxA)'], basic_unions['M-3 U(AxA)'])
        self._subset_assert(basic_unions['AU(AxA)'], basic_unions['M-4 U(AxM)'])
        self._subset_assert(basic_unions['AU(AxA)'], basic_unions['M-4 U(AxM)-2'])
        self._subset_assert(basic_unions['M-3 U(AxA)'], basic_unions['M-4 U(AxM)'])
        self._subset_assert(basic_unions['M-3 U(AxA)'], basic_unions['M-4 U(AxM)-2'])
        self._subset_assert(basic_unions['M-4 U(AxM)'], basic_unions['M-4 U(AxM)-2'])
        # Special case for structure Union's conditional return in is_subset() for GenesisSetM
        self.assertTrue(Union([GenesisSetM()]).is_subset(GenesisSetM()))
        # String representation
        self.assertEqual('M', Union([GenesisSetM()]).__str__())
        self.assertEqual('(M U N)', Union([GenesisSetM(), GenesisSetN()]).__str__())
        self.assertEqual('Union([GenesisSetM()])', Union([GenesisSetM()]).__repr__())
        self.assertEqual('Union([GenesisSetM(), GenesisSetN()])', Union([GenesisSetM(), GenesisSetN()]).__repr__())

    def test_PowerSet(self):
        """Basic properties and subset relationships of the power set."""
        self._basic_assert(basic_pss, PowerSet)
        self._equality_helper(basic_pss)
        # Subset relationships.
        self._subset_assert(basic_pss['A'], basic_pss['M'])
        self._subset_deny(basic_pss['A'], basic_pss['AxA'])
        self._subset_assert(basic_pss['AxA'], basic_pss['MxM'])
        self._subset_deny(basic_pss['AxA'], basic_pss['P(AxA)'])
        self._subset_assert(basic_pss['P(AxA)'], basic_pss['P(MxM)'])

    def test_str(self):
        self.assertEqual(str(empties['{}']), '{}')
        self.assertEqual(str(setas['A']), 'A')
        self.assertEqual(str(setms['M']), 'M')
        self.assertEqual(str(basic_cps['AxA']), '(A x A)')
        self.assertEqual(str(setms['M']), 'M')

    def test_get_powerset_level(self):
        """Test the get_powerset_level function."""
        for zero_levels in [empties, setas, setms, setns]:
            for zero_level in zero_levels.values():
                for pset in basic_pss.values():
                    self.assertEqual(zero_level.get_powerset_level(pset), 0)
        for cp in basic_cps.values():
            for pset in basic_pss.values():
                self.assertEqual(cp.get_powerset_level(pset), 0)
        for un in basic_unions.values():
            for pset in basic_pss.values():
                self.assertEqual(un.get_powerset_level(pset), 0)
        self.assertEqual(basic_pss['A'].get_powerset_level(basic_pss['AxA']), 0)
        self.assertEqual(basic_pss['AxA'].get_powerset_level(basic_pss['A']), 0)
        self.assertEqual(basic_pss['AxA'].get_powerset_level(basic_pss['M']), 0)
        # One level:
        self.assertEqual(basic_pss['A'].get_powerset_level(GenesisSetA()), 1)
        self.assertEqual(basic_pss['A'].get_powerset_level(GenesisSetM()), 1)
        self.assertEqual(basic_pss['AxA'].get_powerset_level(basic_cps['AxA']), 1)
        self.assertEqual(basic_pss['AxA'].get_powerset_level(basic_cps['AxM']), 1)
        self.assertEqual(basic_pss['AxA'].get_powerset_level(basic_cps['MxM']), 1)
        self.assertEqual(basic_pss['MxM'].get_powerset_level(basic_cps['AxA']), 0)
        self.assertEqual(basic_pss['MxM'].get_powerset_level(basic_cps['AxM']), 0)
        self.assertEqual(basic_pss['MxM'].get_powerset_level(basic_cps['MxM']), 1)
        self.assertEqual(basic_pss['P(AxA)'].get_powerset_level(basic_pss['AxA']), 1)
        self.assertEqual(basic_pss['P(AxA)'].get_powerset_level(basic_pss['MxM']), 1)
        self.assertEqual(basic_pss['P(MxM)'].get_powerset_level(basic_pss['AxA']), 0)
        self.assertEqual(basic_pss['P(MxM)'].get_powerset_level(basic_pss['MxM']), 1)
        self.assertEqual(basic_pss['PP(AxA)'].get_powerset_level(basic_pss['P(AxA)']), 1)
        self.assertEqual(basic_pss['PP(AxA)'].get_powerset_level(basic_pss['P(MxM)']), 1)
        self.assertEqual(basic_pss['PP(MxM)'].get_powerset_level(basic_pss['P(AxA)']), 0)
        self.assertEqual(basic_pss['PP(MxM)'].get_powerset_level(basic_pss['P(MxM)']), 1)
        self.assertEqual(basic_pss['PPP(AxA)'].get_powerset_level(basic_pss['PP(AxA)']), 1)
        self.assertEqual(basic_pss['PPP(AxA)'].get_powerset_level(basic_pss['PP(MxM)']), 1)
        self.assertEqual(basic_pss['PPP(MxM)'].get_powerset_level(basic_pss['PP(AxA)']), 0)
        self.assertEqual(basic_pss['PPP(MxM)'].get_powerset_level(basic_pss['PP(MxM)']), 1)
        # Two levels:
        self.assertEqual(basic_pss['P(AxA)'].get_powerset_level(basic_cps['AxA']), 2)
        self.assertEqual(basic_pss['P(AxA)'].get_powerset_level(basic_cps['AxM']), 2)
        self.assertEqual(basic_pss['P(AxA)'].get_powerset_level(basic_cps['MxM']), 2)
        self.assertEqual(basic_pss['P(MxM)'].get_powerset_level(basic_cps['AxA']), 0)
        self.assertEqual(basic_pss['P(MxM)'].get_powerset_level(basic_cps['AxM']), 0)
        self.assertEqual(basic_pss['P(MxM)'].get_powerset_level(basic_cps['MxM']), 2)
        self.assertEqual(basic_pss['PP(AxA)'].get_powerset_level(basic_pss['AxA']), 2)
        self.assertEqual(basic_pss['PP(AxA)'].get_powerset_level(basic_pss['MxM']), 2)
        self.assertEqual(basic_pss['PP(MxM)'].get_powerset_level(basic_pss['AxA']), 0)
        self.assertEqual(basic_pss['PP(MxM)'].get_powerset_level(basic_pss['MxM']), 2)
        self.assertEqual(basic_pss['PPP(AxA)'].get_powerset_level(basic_pss['P(AxA)']), 2)
        self.assertEqual(basic_pss['PPP(AxA)'].get_powerset_level(basic_pss['P(MxM)']), 2)
        self.assertEqual(basic_pss['PPP(MxM)'].get_powerset_level(basic_pss['P(AxA)']), 0)
        self.assertEqual(basic_pss['PPP(MxM)'].get_powerset_level(basic_pss['P(MxM)']), 2)
        # Three levels:
        self.assertEqual(basic_pss['PP(AxA)'].get_powerset_level(basic_cps['AxA']), 3)
        self.assertEqual(basic_pss['PP(AxA)'].get_powerset_level(basic_cps['AxM']), 3)
        self.assertEqual(basic_pss['PP(AxA)'].get_powerset_level(basic_cps['MxM']), 3)
        self.assertEqual(basic_pss['PP(MxM)'].get_powerset_level(basic_cps['AxA']), 0)
        self.assertEqual(basic_pss['PP(MxM)'].get_powerset_level(basic_cps['AxM']), 0)
        self.assertEqual(basic_pss['PP(MxM)'].get_powerset_level(basic_cps['MxM']), 3)
        self.assertEqual(basic_pss['PPP(AxA)'].get_powerset_level(basic_pss['AxA']), 3)
        self.assertEqual(basic_pss['PPP(AxA)'].get_powerset_level(basic_pss['MxM']), 3)
        self.assertEqual(basic_pss['PPP(MxM)'].get_powerset_level(basic_pss['AxA']), 0)
        self.assertEqual(basic_pss['PPP(MxM)'].get_powerset_level(basic_pss['MxM']), 3)
        # Four levels:
        self.assertEqual(basic_pss['PPP(AxA)'].get_powerset_level(basic_cps['AxA']), 4)
        self.assertEqual(basic_pss['PPP(AxA)'].get_powerset_level(basic_cps['AxM']), 4)
        self.assertEqual(basic_pss['PPP(AxA)'].get_powerset_level(basic_cps['MxM']), 4)
        self.assertEqual(basic_pss['PPP(MxM)'].get_powerset_level(basic_cps['AxA']), 0)
        self.assertEqual(basic_pss['PPP(MxM)'].get_powerset_level(basic_cps['AxM']), 0)
        self.assertEqual(basic_pss['PPP(MxM)'].get_powerset_level(basic_cps['MxM']), 4)

    def test_complex_structures(self):
        """Test more complex structures and their subset relationships."""
        # DA-36
        # P((A x P(A x P((A x P(A x A)) U (A x P(A x P(A))) U (A x A)))) U (A x A))
        s1 = PowerSet(
            Union([
                CartesianProduct(
                    GenesisSetA(),
                    PowerSet(
                        CartesianProduct(
                            GenesisSetA(),
                            PowerSet(
                                Union([
                                    CartesianProduct(
                                        GenesisSetA(),
                                        PowerSet(
                                            CartesianProduct(GenesisSetA(), GenesisSetA())
                                        )
                                    ),
                                    CartesianProduct(
                                        GenesisSetA(),
                                        PowerSet(
                                            CartesianProduct(
                                                GenesisSetA(),
                                                PowerSet(GenesisSetA())
                                            )
                                        )
                                    ),
                                    CartesianProduct(GenesisSetA(), GenesisSetA())
                                ])
                            )
                        )
                    )
                ),
                CartesianProduct(GenesisSetA(), GenesisSetA())
            ])
        )
        s2 = PowerSet(CartesianProduct(GenesisSetM(), GenesisSetM()))
        self.assertTrue(s1.is_subset(s2))

    # --------------------------------------------------------------------------------------------------

    def _basic_assert(self, testobjects, my_class):
        """Test basic properties.

        The tests are: type structure, representation, equality and subset relationship (with
        itself) and printing out both standard representations.

        :param testobjects: A dictionary of instances of `Structure` to be tested.
        :param my_class: The class type of the members of `testobjects`.
        """
        if self.print_examples:
            print('(printing examples)')  # Make 'nosetests -s' more readable.
            for obj in testobjects.values():
                print('{msg1} {msg2} (str): {str}'.format(
                    msg1=my_class.__name__, msg2=obj._test_msg, str=str(obj)))
                print('{msg1} {msg2} (repr): {repr}'.format(
                    msg1=my_class.__name__, msg2=obj._test_msg, repr=repr(obj)))

        def _individual_test(test_struct):
            # Test type structure.
            self.assertTrue(isinstance(test_struct, Structure))
            self.assertTrue(isinstance(test_struct, my_class))
            for cls in [GenesisSetA, GenesisSetM, CartesianProduct, Union, PowerSet]:
                if cls != my_class:
                    self.assertFalse(isinstance(test_struct, cls))
            # Test representation.
            repr_exec = 'self.assertEqual(test_struct, {0})'.format(repr(test_struct))
            exec(repr_exec)
            # Test equality and subset relationship to self.
            self._equality_assert(test_struct, test_struct)
            self.assertTrue(test_struct.is_subset(test_struct))
            self.assertLessEqual(test_struct, test_struct)
            self.assertTrue(test_struct <= test_struct)
        # Run tests.
        for struct in testobjects.values():
            _individual_test(struct)

    def _equality_helper(self, testobjects):
        for cp1 in testobjects.values():
            for cp2 in testobjects.values():
                if cp1._test_msg.split('-', 1)[0] == cp2._test_msg.split('-', 1)[0]:
                    self._equality_assert(cp1, cp2)
                else:
                    self._inequality_assert(cp1, cp2)

    def _equality_assert(self, var1, var2):
        self.assertTrue(var1.is_same(var2))
        self.assertEqual(var1, var2)
        self.assertTrue(var1 == var2)
        self.assertFalse(var1 != var2)
        self.assertEqual(hash(var1), hash(var2))
        self.assertTrue(var1.is_subset(var2))
        self.assertTrue(var2.is_subset(var1))

    def _inequality_assert(self, var1, var2):
        self.assertFalse(var1.is_same(var2))
        self.assertNotEqual(var1, var2)
        self.assertFalse(var1 == var2)
        self.assertTrue(var1 != var2)
        self.assertNotEqual(hash(var1), hash(var2))

    def _subset_assert(self, subset, superset):
        self.assertTrue(subset.is_subset(superset))
        self.assertLessEqual(subset, superset)
        self.assertTrue(subset <= superset)

    def _subset_deny(self, subset, notsuperset):
        self.assertFalse(subset.is_subset(notsuperset))
        self.assertFalse(subset <= notsuperset)


# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
