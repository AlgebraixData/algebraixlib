"""Import data from JSON."""

# $Id: json.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import algebraixlib.mathobjects as _mo


def import_json(json_file_or_filepath) -> 'P( A x M )':
    """Import the file ``json_file_or_filepath`` as JSON file and return nested relations.

    :param json_file_or_filepath: A file path or a file object of the file to be imported.
    :return: A nested relation that represents the JSON document.
    """
    def _process_nodes(nodes):
        for key, value in nodes.items():
            if isinstance(value, list):
                for list_data in value:
                    child = _process_nodes(list_data)
                    yield _mo.Couplet(_mo.Atom(key), _mo.Set(child), direct_load=True)
            elif isinstance(value, dict):
                children = _process_nodes(value)
                yield _mo.Couplet(_mo.Atom(key), _mo.Set(children), direct_load=True)
            elif isinstance(value, str):
                yield _mo.Couplet(_mo.Atom(key), _mo.Atom(value), direct_load=True)
            else:
                assert False  # Node type not supported.

    def _import_json(json_file):
        import json
        tree = json.load(json_file)
        return _mo.Set(_process_nodes(tree), direct_load=True)

    if hasattr(json_file_or_filepath, "readlines"):  # support StringIO
        return _import_json(json_file_or_filepath)
    else:
        with open(json_file_or_filepath) as file:
            return _import_json(file)
