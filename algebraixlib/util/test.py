"""Test utilities."""

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
import os.path as _path

import algebraixlib.mathobjects as _mo


# --------------------------------------------------------------------------------------------------

def create_test_object(obj: object, msg: str, val: object=None) -> object:
    """Add the content of ``msg`` and optionally ``val`` as properties to ``obj``.

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
    """Return ``True`` if and only if all elements in ``mo`` are instances of `MathObject`."""
    if isinstance(mo, _mo.Set):
        return all(assert_mathobjects(elem) for elem in mo)
    elif isinstance(mo, _mo.Multiset):
        return all(assert_mathobjects(elem) for elem in mo.data)
    elif isinstance(mo, _mo.Couplet):
        return assert_mathobjects(mo.left) and assert_mathobjects(mo.right)
    elif isinstance(mo, _mo.Atom):
        return True
    return False


def get_test_file_name(test_module: str, file_id: str) -> str:
    """Return the file name of a test file.

    Test file names are composed of the test ``test_module`` file's base name with an appended dash
    ('-') and an identifying ``file_id``. ``file_id`` should end with the desired file extension.

    :param test_module: The name of the test to which the test file belongs. Typically
        this will be passed as `__file__`.
    :param file_id: The identification of the file (final part of the name, including extension).
        This function guarantees that there are no conflicts with outher test modules.
    """
    name = _path.basename(test_module)
    assert name.endswith('.py')
    name = name[:-3]
    return name + '-' + file_id


def get_test_file_path(test_module: str, file_id: str) -> str:
    """Return the (absolute) file path of a test file.

    The file name is generated with `get_test_file_name`.

    :param test_module: The name of the test to which the test file belongs. Typically
        this will be passed as `__file__`.
    :param file_id: The identification of the file (final part of the name, including extension).
    """
    return _path.abspath(_path.join(
        _path.dirname(test_module),
        get_test_file_name(test_module, file_id)
    ))
