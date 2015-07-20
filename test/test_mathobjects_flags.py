"""Testing the mathobjects.flags module."""

# $Id: test_mathobjects_flags.py 22614 2015-07-15 18:14:53Z gfiedler $
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
from ctypes import c_uint32

from algebraixlib.mathobjects.flags import Flags


class MathObjectFlagsTest(unittest.TestCase):
    def test_initial(self):
        flags = Flags()
        self.assertLessEqual(len(flags._fields_), 32)
        for field_name, field_type, field_size in flags._fields_:
            self.assertEqual(field_type, c_uint32)
            self.assertEqual(field_size, 1)
            self.assertEqual(getattr(flags, field_name), 0)

    def test_relation(self):
        flags = Flags(_relation=True)
        flags.relation = True  # No change = no problem
        self.assertTrue(flags.relation)
        self.assertRaises(AssertionError, lambda: setattr(flags, 'relation', False))

    def test_clan(self):
        flags = Flags(_clan=1)
        flags.clan = True  # No change = no problem
        self.assertTrue(flags.clan)
        self.assertRaises(AssertionError, lambda: setattr(flags, 'clan', False))

# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
