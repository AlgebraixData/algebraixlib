"""Addition to unittest to be able to create non-failing 'expect'-like tests."""

# $Id: test.py 22614 2015-07-15 18:14:53Z gfiedler $
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

import algebraixlib.mathobjects as _mo


def create_test_object(obj: object, msg: str, val: object=None) -> object:
    """Add the content of msg and optionally val as properties to obj.

    :param obj: The object to be 'decorated'.
    :param msg: Added as property '_test_msg' to obj.
    :param val: If present, added as property '_test_val' to obj.
    :return: The 'decorated' obj.
    """
    obj._test_msg = msg
    if val is not None:
        obj._test_val = val
    return obj


def assert_mathobjects(mo: _mo.MathObject) -> bool:
    """Return True if and only if all elements in mo are instances of MathObject."""
    if isinstance(mo, _mo.Set):
        result = True
        for elem in mo:
            result = result and assert_mathobjects(elem)
            if not result:
                return False
        return True
    elif isinstance(mo, _mo.Couplet):
        return assert_mathobjects(mo.left) and assert_mathobjects(mo.right)
    elif isinstance(mo, _mo.Atom):
        return True
    return False


def get_test_file_name(test_module: str, file_id: str) -> str:
    """Return the file name of a test file.

    Test file names are composed of the test test_module file's base name with an appended dash
    ('-') and an identifying ``file_id``. ``file_id`` should end with the desired file extension.

    :param test_module: The name of the test to which the test file belongs. Typically
        this will be `__file__`.
    :param file_id: The identification of the file (final part of the name, including extension).
    """
    name = os.path.basename(test_module)
    assert name.endswith('.py')
    name = name[:-3]
    return name + '-' + file_id


def get_test_file_path(test_module: str, file_id: str) -> str:
    """Return the (absolute) file path of a test file. Test file names are composed

    :param test_module: The name of the test test_module to which the test file belongs. Typically
        this will be `__file__`.
    :param file_id: The identification of the file (final part of the name, including extension).
    """
    return os.path.abspath(os.path.join(
        os.path.dirname(test_module),
        get_test_file_name(test_module, file_id)
    ))
