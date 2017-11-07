r"""Extend :mod:`json` so that it can convert constructs that contain `MathObject`\s and a few
other normally not supported types to and from JSON. A lossless round-trip is supported.

Supported types:

-   The `MathObject` types :class:`~.Atom`, :class:`~.Couplet`, :class:`~.Set` and
    :class:`~.Multiset`.
-   The Python types `bytes`, `complex`, `frozenset`, `range`.
-   The Python types `list` and `tuple` are already supported by the base implementation, but it
    can't distinguish between them. Our implementation can.
"""

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
import json as _json

import algebraixlib.mathobjects as _mo


def encode(obj):
    """Encode ``obj`` as construct of objects known to the JSON encoder or return it as-is. If
    ``obj`` is not known to the JSON encoder, it will fail on it.
    """
    if isinstance(obj, bytes):
        return {'__cls__': 'builtin.bytes', '__val__': [elem for elem in obj]}
    if isinstance(obj, complex):
        return {'__cls__': 'builtin.complex', '__val__': str(obj)}
    if isinstance(obj, frozenset):
        return {'__cls__': 'builtin.frozenset', '__val__': [encode(elem) for elem in obj]}
    if isinstance(obj, list):
        return {'__cls__': 'builtin.list', '__val__': obj}
    if isinstance(obj, range):
        return {'__cls__': 'builtin.range', '__val__': [obj.start, obj.stop, obj.step]}
    if isinstance(obj, tuple):
        return {'__cls__': 'builtin.tuple', '__val__': obj}
    if isinstance(obj, _mo.Atom):
        return {'__cls__': 'Atom', '__val__': encode(obj.value)}
    if isinstance(obj, _mo.Couplet):
        return {'__cls__': 'Couplet', '__val__': [encode(obj.left), encode(obj.right)]}
    if isinstance(obj, _mo.Set):
        return {'__cls__': 'Set', '__val__': [encode(elem) for elem in obj]}
    if isinstance(obj, _mo.Multiset):
        return {'__cls__': 'Multiset',
            '__val__': [(encode(val), mult) for val, mult in obj.data.items()]}
    return obj


def decode(obj):
    """``obj`` is a representation of a straightforward translation of JSON into Python. For a known
    special construct, convert it into its correct object representation and return it. Otherwise
    return ``obj`` as-is.
    """
    if isinstance(obj, dict):
        return object_hook_f(obj)
    return obj


def object_hook_f(obj):
    """``obj`` is a representation of a straightforward translation of JSON into Python. For a known
    special construct (must be a ``dict``), convert it into its correct object representation and
    return it. Otherwise return ``obj`` as-is. (May be used as ``object_hook`` function for the
    various JSON decoder APIs.)
    """
    if len(obj) == 2 and '__cls__' in obj and '__val__' in obj:
        if obj['__cls__'] == 'builtin.bytes':
            return bytes(elem for elem in obj['__val__'])
        if obj['__cls__'] == 'builtin.complex':
            return complex(obj['__val__'])
        if obj['__cls__'] == 'builtin.frozenset':
            return frozenset(decode(elem) for elem in obj['__val__'])
        if obj['__cls__'] == 'builtin.list':
            return list(decode(elem) for elem in obj['__val__'])
        if obj['__cls__'] == 'builtin.range':
            return range(decode(obj['__val__'][0]), decode(obj['__val__'][1]),
                decode(obj['__val__'][2]))
        if obj['__cls__'] == 'builtin.tuple':
            return tuple(decode(elem) for elem in obj['__val__'])
        if obj['__cls__'] == 'Atom':
            return _mo.Atom(decode(obj['__val__']), direct_load=True)
        if obj['__cls__'] == 'Couplet':
            return _mo.Couplet(
                left=decode(obj['__val__'][0]), right=decode(obj['__val__'][1]), direct_load=True)
        if obj['__cls__'] == 'Set':
            return _mo.Set((decode(elem) for elem in obj['__val__']), direct_load=True)
        if obj['__cls__'] == 'Multiset':
            return _mo.Multiset(
                {decode(val): mult for val, mult in obj['__val__']}, direct_load=True)
    return obj


class ExportJson(_json.JSONEncoder):
    r"""Export a construct that may contain `MathObject`\s and other normally not supported
    types as a custom JSON format that allows a round-trip."""

    def default(self, obj):
        """Convert ``obj`` into a representation that can be converted into JSON (and back)."""
        return encode(obj)


class ImportJson(_json.JSONDecoder):
    """Import the JSON format created by `ExportJson` and create an object from it."""

    def __init__(self, object_hook=None, parse_float=None, parse_int=None, parse_constant=None,
            strict=True, object_pairs_hook=None):
        """The arguments are the same as for `_json.JSONDecoder`, except for the ones listed here:

        :param object_hook: If this argument is not set, the function `object_hook_f` is used.
        """
        if object_hook is None:
            object_hook = object_hook_f
        super().__init__(object_hook=object_hook, parse_float=parse_float, parse_int=parse_int,
            parse_constant=parse_constant, strict=strict, object_pairs_hook=object_pairs_hook)
