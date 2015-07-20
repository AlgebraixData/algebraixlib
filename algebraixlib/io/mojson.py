"""Import a `MathObject` from and export it to a custom JSON format that allows a round-trip."""

# $Id: mojson.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import json

import algebraixlib.mathobjects as _mo


class ExportJson(json.JSONEncoder):
    """Custom json encoder. Manages encoding math objects and supported built in data types."""

    @staticmethod
    def _get_type_name(o):
        """Return a string containing the name of the object passed in."""
        # split is used to remove any module and package prefixes from the object name.
        return type(o).__name__.split('.')[-1]

    @staticmethod
    def _encode_object(o):
        """Return a json string of a math object or supported built in data type."""

        assert(isinstance(o, (bool, int, float, str, complex, bytes, range, frozenset, tuple,
            _mo.Atom, _mo.Couplet, _mo.Set)) or o is None)

        if isinstance(o, (bool, int, float, str)) or o is None:
            return o
        elif isinstance(o, complex):
            return {'complex': str(o)}
        elif isinstance(o, bytes):
            return {'bytes': o.decode('utf-8')}
        elif isinstance(o, range):
            return {'range': [o.start, o.stop, o.step]}
        elif isinstance(o, (frozenset, tuple, _mo.Set)):
            type_name = ExportJson._get_type_name(o)
            return {type_name: [ExportJson._encode_object(value) for value in o]}
        elif isinstance(o, _mo.Atom):
            return {'Atom': ExportJson._encode_object(o.value)}
        elif isinstance(o, _mo.Couplet):
            return {'Couplet': {'right': ExportJson._encode_object(o.right),
                                'left': ExportJson._encode_object(o.left)}}

    def default(self, o):
        if isinstance(o, (_mo.Atom, _mo.Couplet, _mo.Set)):
            return ExportJson._encode_object(o)

        raise TypeError("Invalid math object, " + str(type(o)) +
                        ", provided to encoder. Expected Atom, Couplet or Set")


class ImportJson(json.JSONDecoder):
    """Custom json decoder. Manages decoding json into math objects and hashable data types."""

    @staticmethod
    def _is_math_object_text(s):
        return 'Atom' or 'Couplet' or 'Set' in s

    @staticmethod
    def _decode_object(o):
        """Return a math object or hashable data type decoded from a json string or raise TypeError
        for unknown type."""

        # Only json object, array and value types should make it here which are all handled so
        # there's no need for additional type checking.
        if isinstance(o, (bool, int, float, str)) or o is None:
            return o
        elif isinstance(o, list):
            return [ImportJson._decode_object(value) for value in o]
        elif isinstance(o, dict):
            # There should be only one element since dict is used by json for objects; dict is not
            # valid for math objects because it is not hashable.
            if len(o) != 1:
                raise TypeError("Invalid object provided to decoder. Expected a single object but "
                                "received " + str(len(o)))

            for key, value in o.items():
                if key == 'complex':
                    return complex(ImportJson._decode_object(value))
                elif key == 'bytes':
                    return bytes(ImportJson._decode_object(value), 'utf-8')
                elif key == 'range':
                    elements = ImportJson._decode_object(value)
                    return range(elements[0], elements[1], elements[2])
                elif key == 'frozenset':
                    return frozenset(ImportJson._decode_object(value))
                elif key == 'tuple':
                    return tuple(ImportJson._decode_object(value))
                elif key == 'Atom':
                    return _mo.Atom(ImportJson._decode_object(value))
                elif key == 'Couplet':
                    left = ImportJson._decode_object(value['left'])
                    right = ImportJson._decode_object(value['right'])
                    return _mo.Couplet(left, right)
                elif key == 'Set':
                    decoded = ImportJson._decode_object(value)
                    return _mo.Set(decoded)
                else:
                    raise TypeError("Invalid key, " + key + ", provided to decoder.")

    from json.decoder import WHITESPACE

    def decode(self, s, _w=WHITESPACE.match):
        # Use JSONDecoder to decode the json document into Python objects that we can then decode
        # into math objects.
        decoded = super().decode(s, _w)

        if isinstance(decoded, dict):
            # Only one math object is decoded at a time. This supports the json library's management
            # of collections and deferring to the decoder only when the object is unfamiliar.
            if len(decoded) != 1:
                raise TypeError("Invalid object provided to decoder. Expected a single Atom, "
                                "Couplet or Set but received " + str(len(decoded)))

            if ImportJson._is_math_object_text(decoded):
                return ImportJson._decode_object(decoded)

        raise TypeError("Invalid object, " + str(type(decoded)) +
                        ", provided to decoder. Expected Atom, Couplet or Set")
