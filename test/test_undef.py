"""Test the undef module."""

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

from algebraixlib.undef import make_or_raise_undef, RaiseOnUndef, Undef, UndefException


class UndefTest(unittest.TestCase):
    """Test the undef module."""

    print_examples = False

    def test_basic_properties(self):
        u1 = Undef()
        self.assertEqual(str(u1), 'undef')

    def test_singleton(self):
        """Test singleton characteristics."""
        u1 = Undef()
        u2 = Undef()
        self.assertIs(u1, u2)
        self.assertIs(u1, Undef())
        self.assertIs(u2, Undef())
        self.assertTrue(u1 is Undef())
        self.assertFalse(u1 is Undef, 'Undef refers to the class Undef, not the instance Undef()')

    def test_eq(self):
        """Test equality."""
        u1 = Undef()
        u2 = Undef()
        self.assertRaises(TypeError, lambda: u1 == u2)
        self.assertRaises(TypeError, lambda: u2 == u1)
        self.assertRaises(TypeError, lambda: u1 == u1)
        self.assertRaises(TypeError, lambda: u2 == u2)
        self.assertRaises(TypeError, lambda: u1 == 'a')

    def test_ne(self):
        """Test inequality."""
        u1 = Undef()
        u2 = Undef()
        self.assertRaises(TypeError, lambda: u1 != u2)
        self.assertRaises(TypeError, lambda: u2 != u1)
        self.assertRaises(TypeError, lambda: u1 != u1)
        self.assertRaises(TypeError, lambda: u2 != u2)
        self.assertRaises(TypeError, lambda: u1 != 3)

    def test_conversions(self):
        """test conversions"""
        u1 = Undef()
        u2 = Undef()
        self.assertRaises(TypeError, lambda: not u1)
        self.assertRaises(TypeError, lambda: u1 and u2)
        self.assertRaises(TypeError, lambda: u1 or u2)
        self.assertRaises(TypeError, lambda: bool(u1))
        self.assertRaises(TypeError, lambda: int(u1))
        self.assertRaises(TypeError, lambda: float(u1))
        self.assertRaises(TypeError, lambda: {Undef()})  # Can't put Undef() in set()...not hashable

    def test_raise_on_undef(self):
        """Test the static class RaiseOnUndef."""
        self.assertRaises(AssertionError, lambda: RaiseOnUndef())
        self.assertEqual(RaiseOnUndef.get_level(), 0)
        RaiseOnUndef.set_level(2)
        self.assertEqual(RaiseOnUndef.get_level(), 2)
        RaiseOnUndef.set_level(4)
        self.assertEqual(RaiseOnUndef.get_level(), 4)
        RaiseOnUndef.reset()
        self.assertEqual(RaiseOnUndef.get_level(), 0)

    def test_make_or_raise_undef(self):
        """Test make_or_raise_undef() together with RaiseOnUndef."""
        try:
            self.assertEqual(RaiseOnUndef.get_level(), 0)
            self.assertIs(make_or_raise_undef(), Undef())
            RaiseOnUndef.set_level(1)
            self.assertRaises(UndefException, lambda: make_or_raise_undef())
            self.assertIs(make_or_raise_undef(2), Undef())
            RaiseOnUndef.set_level(2)
            self.assertRaises(UndefException, lambda: make_or_raise_undef(2))
            RaiseOnUndef.reset()
            self.assertIs(make_or_raise_undef(2), Undef())
        except:  # Make sure RaiseOnUndef level gets reset.
            RaiseOnUndef.reset()
            raise

# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
