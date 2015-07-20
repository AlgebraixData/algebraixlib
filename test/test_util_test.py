"""Test the util.test module."""

# $Id: test_util_test.py 22614 2015-07-15 18:14:53Z gfiedler $
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

from algebraixlib.mathobjects import Atom
from algebraixlib.util.test import create_test_object, assert_mathobjects,\
    get_test_file_name, get_test_file_path


class TestTest(unittest.TestCase):
    """Test the test module."""

    def test_create_test_object(self):
        obj = create_test_object(Atom('abc'), 'testing abc', 123)
        self.assertEqual(obj._test_msg, 'testing abc')
        self.assertEqual(obj._test_val, 123)

    def test_assert_mathobjects(self):
        self.assertTrue(assert_mathobjects(Atom(3)))
        # noinspection PyTypeChecker
        self.assertFalse(assert_mathobjects('abc'))

    def test_get_test_file_name(self):
        self.assertEqual(get_test_file_name(__file__, 'abc.ttl'), 'test_util_test-abc.ttl')
        self.assertEqual(get_test_file_name(__file__, '123'), 'test_util_test-123')

    def test_get_test_file_path(self):
        abspath = __file__[:-3]
        self.assertEqual(get_test_file_path(__file__, 'abc.ttl'), abspath + '-abc.ttl')
        self.assertEqual(get_test_file_path(__file__, '123'), abspath + '-123')


# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
