"""Testing the io.json module."""

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
import io
import os
import unittest

import algebraixlib.algebras.relations as relations
from algebraixlib.import_export.json import import_json
from algebraixlib.mathobjects import Set


class IoJsonTests(unittest.TestCase):

    def test_json(self):
        """Test loading clan from json."""
        data = [{"id": 1, "name": "foo"}, {"id": 2, "name": "bar"}, {"id": 3, "name": "baz"}]
        import json
        json_string = json.dumps(data)

        expected = Set(relations.from_dict(d) for d in data)
        actual = import_json(io.StringIO(json_string))
        self.assertEqual(expected, actual)


# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
