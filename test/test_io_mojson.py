"""Test the io.mojson module."""

# $Id: test_io_mojson.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import json

from algebraixlib.mathobjects import Atom, Couplet, Set
from algebraixlib.io.mojson import ExportJson, ImportJson


class JsonTest(unittest.TestCase):
    """Test json encoding and decoding."""

    to_debug = False
    to_file = False

    def test_atom(self):
        if self.to_debug:
            print("test_atom")

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
            Atom(frozenset([None, bool(2), int(2), float(2), complex('1+2j'), str(2), bytes(2),
                range(-1, 5), frozenset([Couplet('x', 'y'), tuple((34, 35)), Set('1', '2', '3')]),
                Atom('abc'), Couplet(-1, -2), Set('x', 'y', 'z')])),
        ]

        if not self.to_file:
            self.verify_string_import_export(atoms, self.to_debug)
        else:
            self.verify_file_import_export(atoms, "atom", self.to_debug)

    def test_couplet(self):
        if self.to_debug:
            print("test_couplet")

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
                Couplet(-1, -2), Set('x', 'y', 'z')]),
            frozenset([Couplet(0, 1), Couplet(2, 3)]),
            frozenset([Set('a', 'b', 'c'), Set([1, 2, 3])]),
            tuple((34, 35)),
            Atom(33),
            Couplet(0, 'abc'),
            Set(frozenset([None, 'xyz'])),
        ]

        couplets = [Couplet(s, c) for s in elements for c in elements]

        if not self.to_file:
            self.verify_string_import_export(couplets, self.to_debug)
        else:
            self.verify_file_import_export(couplets, "couplet", self.to_debug)

    def test_set(self):
        if self.to_debug:
            print("test_set")

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
                           Couplet(-1, -2), Set('x', 'y', 'z')])),
            Set(tuple((34, 35))),
            Set(Atom('jkh')),
            Set(Couplet('a', '1')),
        ]

        if not self.to_file:
            self.verify_string_import_export(sets, self.to_debug)
        else:
            self.verify_file_import_export(sets, "set", self.to_debug)

    def test_negative_tests(self):
        if self.to_debug:
            print("test_negative_tests")

        # Verify encoding only works on math objects. Simple built in types (bool, int, float, str)
        # are handled by json encoder and not sent to the custom encoder.
        moe = ExportJson()
        self.assertRaises(TypeError, lambda: moe.encode(complex('1+2j')))
        self.assertRaises(TypeError, lambda: moe.encode(bytes(2)))
        self.assertRaises(TypeError, lambda: moe.encode(bytearray(2)))
        self.assertRaises(TypeError, lambda: moe.encode(range(2, 4, 2)))
        self.assertRaises(TypeError, lambda: moe.encode(list([bytes(2)])))
        self.assertRaises(TypeError, lambda: moe.encode(set(None)))
        self.assertRaises(TypeError, lambda: moe.encode(frozenset(None)))
        self.assertRaises(TypeError, lambda: moe.encode(tuple(None)))
        self.assertRaises(TypeError, lambda: moe.encode(moe))
        self.assertRaises(AssertionError, lambda: moe._encode_object(moe))

        mod = ImportJson()

        # Only one math object is decoded at a time. This supports the json library's management of
        # collections and deferring to the decoder only when the object is unfamiliar.
        errant = json.dumps({})
        self.assertRaises(TypeError, lambda: mod.decode(errant))

        errant = json.dumps({"one": 1, "two": 2})
        self.assertRaises(TypeError, lambda: mod.decode(errant))

        errant = json.dumps({'Atom': {"one": 1, "two": 2}})
        self.assertRaises(TypeError, lambda: mod.decode(errant))

        # Atom can only be initialized with another Atom or hashable objects, not math objects or
        # unknown types. Using Set, Couplet and foo below.
        errant = json.dumps({'Atom': {'Set': None}})
        self.assertRaises(TypeError, lambda: mod.decode(errant))

        errant = json.dumps({'Atom': {'Couplet': {'left': None, 'right': None}}})
        self.assertRaises(TypeError, lambda: mod.decode(errant))

        errant = json.dumps({'Atom': {'foo': 'bar'}})
        self.assertRaises(TypeError, lambda: mod.decode(errant))

        # Couplet can only be initialized with math or hashable objects; using list below.
        errant = json.dumps({'Couplet': {'left': ['1'], 'right': ['2']}})
        self.assertRaises(TypeError, lambda: mod.decode(errant))

        # Verify decoding only works on math objects. Simple built in types (bool, int, float, str)
        # are handled by json encoder and not sent to the custom encoder.
        errant = json.dumps({'complex': None})
        self.assertRaises(TypeError, lambda: mod.decode(errant))

        errant = json.dumps({'bytes': None})
        self.assertRaises(TypeError, lambda: mod.decode(errant))

        errant = json.dumps({'bytearray': None})
        self.assertRaises(TypeError, lambda: mod.decode(errant))

        errant = json.dumps({'range': ['a', 'b', 'c']})
        self.assertRaises(TypeError, lambda: mod.decode(errant))

        errant = json.dumps({'set': None})
        self.assertRaises(TypeError, lambda: mod.decode(errant))

        errant = json.dumps({'frozenset': None})
        self.assertRaises(TypeError, lambda: mod.decode(errant))

        errant = json.dumps({'tuple': None})
        self.assertRaises(TypeError, lambda: mod.decode(errant))

        errant = json.dumps({'foo': None})
        self.assertRaises(TypeError, lambda: mod.decode(errant))

        # list is not a math object
        errant = json.dumps([{'Set': 1}])
        self.assertRaises(TypeError, lambda: mod.decode(errant))

        # Cannot initialize with an empty dictionary
        errant = json.dumps({})
        self.assertRaises(TypeError, lambda: mod.decode(errant))

    @staticmethod
    def show_result(original, decoded):
        """Print whether or not the objects are equal. Print the objects."""
        if original == decoded:
            print('equal')
        else:
            print('not equal')
        print("original: " + str(original))
        print("decoded: " + str(decoded))

    def check_equality(self, original, decoded, show):
        """Compare two objects for equality. Uses special logic for collections because in practice
        they are sometimes not the same order but contain the correct results. Other times they are
        not the same container"""
        if show:
            self.show_result(original, decoded)

        self.assertEqual(original, decoded)

    def verify_string_import_export(self, objects, show=False):
        """Test encoding and decoding using json string facilities."""
        for o in objects:
            encoded = json.dumps(o, cls=ExportJson)
            decoded = json.loads(encoded, cls=ImportJson)
            self.check_equality(o, decoded, show)

    def verify_file_import_export(self, objects, typename, show=False):
        """Test encoding and decoding using json file facilities. Doesn't remove files generated
        during the test."""
        file_index = 1

        for o in objects:
            filename = str(typename) + "_to_json_test_" + str(file_index) + ".txt"
            with open(filename, 'w') as out_file:
                json.dump(o, out_file, cls=ExportJson)
            with open(filename, 'r') as in_file:
                decoded = json.load(in_file, cls=ImportJson)
            self.check_equality(o, decoded, show)

            file_index += 1


# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
