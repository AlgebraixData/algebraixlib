"""Test the io.mojson module."""

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
import json
import os
import shutil
import unittest

from algebraixlib.mathobjects import Atom, Couplet, Set, Multiset
from algebraixlib.import_export.mojson import ExportJson, ImportJson


class JsonTest(unittest.TestCase):
    """Test JSON encoding and decoding."""

    to_debug = False  # Set to `True` to see test types and the generated JSON in the debug output.

    def print_string(self, text: str) -> None:
        """If `to_debug` is ``True``, print ``text``."""
        if self.to_debug:
            print(text)

    def print_comparison(self, original, roundtrip, string: str, filepath: str) -> None:
        """If `to_debug` is ``True``, print the objects and whether or not they are equal."""
        if self.to_debug:
            is_equal = original == roundtrip
            if string is not None:
                assert filepath is None
                json_str = string
            else:
                assert filepath is not None
                with open(filepath) as file:
                    json_str = file.read()
            print('equal:' if is_equal else 'ERROR: not equal:')
            print('  original:  ' + repr(original))
            print('  json text: ' + json_str)
            if not is_equal:
                print('  roundtrip: ' + repr(roundtrip))

    def test_atom(self):
        self.print_string('test_atom')
        atoms = [
            Atom(None),
            Atom(bool(0)),
            Atom(bool(1)),
            Atom(int(2)),
            Atom(float(2)),
            Atom(str(2)),
            Atom(bytes(2)),
            Atom(complex('1+2j')),
            Atom(frozenset([Atom(1), Atom(2)])),
            Atom(tuple((34, 35))),
            Atom(range(-1, 5)),
            Atom(frozenset([
                None, bool(2), int(2), float(2), complex('1+2j'), str(2), bytes(2), range(-1, 5),
                frozenset([Couplet('x', 'y'), tuple((34, 35)),
                Set('1', '2', '3')]), Atom('abc'), Couplet(-1, -2), Set('x', 'y', 'z')
            ])),
        ]
        self.verify_string_import_export(atoms)
        self.verify_file_import_export(atoms)

    def test_couplet(self):
        self.print_string('test_couplet')
        elements = [
            None,
            bool(2),
            int(2),
            float(2),
            complex('1+2j'),
            str(2),
            bytes(2),
            range(-1, 5),
            frozenset([None, bool(2), int(2), float(2), complex('1+2j'), str(2), bytes(2),
                range(-1, 5), frozenset([None, None]), tuple((34, 35)), Atom(int(2)),
                Couplet(-1, -2), Set('x', 'y', 'z')
            ]),
            frozenset([Couplet(0, 1), Couplet(2, 3)]),
            frozenset([Set('a', 'b', 'c'), Set([1, 2, 3])]),
            tuple((34, 35)),
            Atom(33),
            Couplet(0, 'abc'),
            Set(frozenset([None, 'xyz'])),
        ]
        couplets = [Couplet(s, c) for s in elements for c in elements]
        self.verify_string_import_export(couplets)
        self.verify_file_import_export(couplets)

    def test_set(self):
        self.print_string('test_set')
        sets = [
            Set(None),
            Set(False),
            Set(int(2)),
            Set(float(2)),
            Set(complex('1+2j')),
            Set(str(2)),
            Set(bytes(2)),
            Set(range(-1, 5)),
            Set(frozenset([None, bool(2), int(2), float(2), complex('1+2j'), str(2), bytes(2),
                range(-1, 5), frozenset([None, None]), tuple((34, 35)), Atom(int(2)),
                Couplet(-1, -2), Set('x', 'y', 'z')
            ])),
            Set(tuple((34, 35))),
            Set(Atom('jkh')),
            Set(Couplet('a', '1')),
        ]
        self.verify_string_import_export(sets)
        self.verify_file_import_export(sets)

    def test_multiset(self):
        self.print_string('test_multiset')
        msets = [
            Multiset(None, None),
            Multiset(False, False),
            Multiset(2, 2, 1),
            Multiset(2.0, 2.0, 3),
            Multiset(complex('1+2j')),
            Multiset('2', '3', '2'),
            Multiset(bytes(2)),
            Multiset(range(-1, 5), range(-1, 5), range(1, 5)),
            Multiset(frozenset([None, bool(2), int(2), float(2), complex('1+2j'), str(2), bytes(2),
                range(-1, 5), frozenset([None, None]), tuple((34, 35)), Atom(int(2)),
                Couplet(-1, -2), Set('x', 'y', 'z')
            ])),
            Multiset(tuple((34, 35))),
            Multiset(Atom('jkh'), Atom('jkh'), Atom('AA'), Atom('jkh')),
            Multiset(Couplet('a', 1), Couplet('B', 1), Couplet('a', 1)),
        ]
        self.verify_string_import_export(msets)
        self.verify_file_import_export(msets)

    def check_equality(self, original, roundtrip, *, string: str=None, filepath: str=None):
        """Compare two objects for equality and optionally print the comparison result, the JSON
        string and the objects."""
        self.print_comparison(original, roundtrip, string=string, filepath=filepath)
        self.assertEqual(original, roundtrip)

    def verify_string_import_export(self, objects):
        """Test encoding and decoding using JSON string facilities. Optionally print debug data."""
        for obj in objects:
            json_string = json.dumps(obj, cls=ExportJson)
            roundtrip = json.loads(json_string, cls=ImportJson)
            self.check_equality(obj, roundtrip, string=json_string)

    def verify_file_import_export(self, objects):
        """Test encoding and decoding using JSON file facilities. Optionally print debug data."""
        test_dir = '_io_mojson'
        try:
            os.makedirs(test_dir, exist_ok=True)
            for index, obj in enumerate(objects):
                filepath = os.path.join(
                    test_dir, obj.__class__.__name__ + '-' + str(index) + '.json')
                with open(filepath, 'w') as json_file:
                    json.dump(obj, json_file, cls=ExportJson)
                with open(filepath, 'r') as json_file:
                    roundtrip = json.load(json_file, cls=ImportJson)
                self.check_equality(obj, roundtrip, filepath=filepath)
        finally:
            shutil.rmtree(test_dir, ignore_errors=True)


# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
