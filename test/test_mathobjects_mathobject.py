"""Testing mathobjects.mathobject module."""

# $Id: test_mathobjects_mathobject.py 22614 2015-07-15 18:14:53Z gfiedler $
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

from algebraixlib.mathobjects import MathObject, raise_if_not_mathobjects


class MathObjectTest(unittest.TestCase):
    """Test the MathObject class."""

    def test_MathObject(self):
        """Create a MathObject."""
        # MathObject itself can't be instantiated (it is an abstract base class).
        self.assertRaises(TypeError, lambda: MathObject())
        self.assertRaises(TypeError, lambda: raise_if_not_mathobjects(1))
        self.assertRaises(TypeError, lambda: raise_if_not_mathobjects(*[1]))

# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
