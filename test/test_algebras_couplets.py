"""Test the algebras.couplets module."""

<<<<<<< HEAD
# $Id: test_algebras_couplets.py 22744 2015-08-05 22:16:56Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-08-05 17:16:56 -0500 (Wed, 05 Aug 2015) $
=======
# $Id: test_algebras_couplets.py 22698 2015-07-28 17:09:23Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-28 12:09:23 -0500 (Tue, 28 Jul 2015) $
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
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
from algebraixlib.structure import CartesianProduct, GenesisSetA, GenesisSetM
from algebraixlib.undef import RaiseOnUndef, Undef, UndefException

from algebraixlib.algebras.couplets import \
    get_ground_set, get_absolute_ground_set, get_name, is_member, is_absolute_member, \
    compose, transpose


_couplet_b_to_a = Couplet(left='b', right='a')
_couplet_a_to_b = Couplet(left='a', right='b')
_couplet_c_to_b = Couplet(left='c', right='b')
_couplet_d_to_c = Couplet(left='d', right='c')
_couplet_c_to_a = Couplet(left='c', right='a')
_couplet_d_to_b = Couplet(left='d', right='b')


class CoupletsTest(unittest.TestCase):
    """Test the algebras.couplets module."""

    print_examples = False

    def test_metadata(self):
        self.assertEqual(get_ground_set(), CartesianProduct(GenesisSetM(), GenesisSetM()))
        self.assertEqual(get_absolute_ground_set(), CartesianProduct(GenesisSetA(), GenesisSetA()))
        self.assertEqual(get_name(), 'Couplets(M): (M x M)')

    # noinspection PyTypeChecker
    def test_membership(self):
        self.assertTrue(is_member(Couplet(1, 2)))
        self.assertFalse(is_member(Atom(3)))
        self.assertTrue(is_absolute_member(Couplet(1, 2)))
        self.assertFalse(is_absolute_member(Couplet(Set(1), 2)))
<<<<<<< HEAD
        self.assertRaises(AttributeError, lambda: is_member(3))
=======
        self.assertRaises(TypeError, lambda: is_member(3))
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272

    def test_compose(self):
        """Basic tests of couplets.compose()."""
        # Wrong argument types.
<<<<<<< HEAD
        try:
            self.assertRaises(AttributeError, lambda: compose(3, Couplet(1, 2)))
            self.assertRaises(AttributeError, lambda: compose(Couplet(1, 2), 3))
            self.assertIs(compose(Atom(3), Couplet(1, 2)), Undef())
            self.assertIs(compose(Couplet(1, 2), Atom(3)), Undef())
            RaiseOnUndef.set_level(1)
            self.assertRaises(UndefException, lambda: compose(Set('a', 'b'), Set('c', 'd')))
            RaiseOnUndef.reset()
        except:  # Make sure RaiseOnUndef level gets reset.
            RaiseOnUndef.reset()
            raise
=======
        self.assertRaises(TypeError, lambda: compose(3, Couplet(1, 2)))
        self.assertRaises(TypeError, lambda: compose(Couplet(1, 2), 3))
        self.assertIs(compose(Atom(3), Couplet(1, 2)), Undef())
        self.assertIs(compose(Couplet(1, 2), Atom(3)), Undef())
        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: compose(Set('a', 'b'), Set('c', 'd')))
        RaiseOnUndef.reset()
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272

        result = compose(_couplet_b_to_a, _couplet_c_to_b)
        self.assertEqual(result, _couplet_c_to_a)

        result = compose(_couplet_c_to_b, _couplet_d_to_c)
        self.assertEqual(result, _couplet_d_to_b)

<<<<<<< HEAD
        try:
            result = compose(_couplet_b_to_a, _couplet_d_to_c)
            self.assertIs(result, Undef())
            RaiseOnUndef.set_level(2)
            self.assertRaises(UndefException, lambda: compose(_couplet_b_to_a, _couplet_d_to_c))
            RaiseOnUndef.reset()
        except:  # Make sure RaiseOnUndef level gets reset.
            RaiseOnUndef.reset()
            raise
=======
        result = compose(_couplet_b_to_a, _couplet_d_to_c)
        self.assertIs(result, Undef())
        RaiseOnUndef.set_level(2)
        self.assertRaises(UndefException, lambda: compose(_couplet_b_to_a, _couplet_d_to_c))
        RaiseOnUndef.reset()
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272

        result = compose(_couplet_c_to_b, _couplet_b_to_a)
        self.assertIs(result, Undef())

    def test_transpose(self):
        """Basic tests of couplets.transpose()."""
        # Wrong argument types.
<<<<<<< HEAD
        try:
            self.assertRaises(AttributeError, lambda: transpose(3))
            self.assertIs(transpose(Atom(3)), Undef())
            RaiseOnUndef.set_level(1)
            self.assertRaises(UndefException, lambda: transpose(Set('a', 'b')))
            RaiseOnUndef.reset()
        except:  # Make sure RaiseOnUndef level gets reset.
            RaiseOnUndef.reset()
            raise
=======
        self.assertRaises(TypeError, lambda: transpose(3))
        self.assertIs(transpose(Atom(3)), Undef())
        RaiseOnUndef.set_level(1)
        self.assertRaises(UndefException, lambda: transpose(Set('a', 'b')))
        RaiseOnUndef.reset()
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272

        result = transpose(_couplet_b_to_a)
        self.assertEqual(result, _couplet_a_to_b)


# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
