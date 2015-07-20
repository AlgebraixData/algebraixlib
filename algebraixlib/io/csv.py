"""Import clans from and export them to CSV data."""

# $Id: csv.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import csv as _csv

import algebraixlib.algebras.clans as _clans
import algebraixlib.algebras.multiclans as _multiclans
import algebraixlib.algebras.relations as _relations
# noinspection PyProtectedMember
import algebraixlib.io._util as _util
import algebraixlib.mathobjects as _mo
import algebraixlib.undef as _ud
import algebraixlib.util.miscellaneous as _misc


def export_csv(absolute_clan: 'PP(A x A)', file_or_path, column_order=None, sort_key=None):
    """This function takes an absolute, left regular clan and produces a CSV file, where the
    left components are in the header line and the rows are the individual relations.

    :param absolute_clan: A :class:`algebraixlib.mathobjects.set.Set`. It must be an absolute and
        left-regular clan.
    :param file_or_path: Either a file path (in this case the CSV data is written to a file at this
        location) or a file object (in this case the CSV data is written to its ``.write()``
        function).
    :param column_order: The optional left set to be exported in the specified order.
    :param sort_key: The optional key to be provided to sorted (sorted not called if None).
    :return: ``True`` if the CSV export succeeded.
    """
    if not _clans.is_absolute_member(absolute_clan) \
            and not _multiclans.is_absolute_member(absolute_clan):
        return _ud.make_or_raise_undef()
    if column_order is None and not absolute_clan.is_left_regular():
        return _ud.make_or_raise_undef()

    if column_order is None:
        # Since this clan is left regular, get first relation to acquire left set.
        rel = next(iter(absolute_clan))
        # left_set is sorted to guarantee consistent iterations
        column_order = sorted([left.value for left in rel.get_left_set()])

    # Build list of dictionaries that associates left components with their right components for each relation.
    clan_as_list_of_dicts = _convert_clan_to_list_of_dicts(column_order,
                                                           (absolute_clan if sort_key is None else
                                                            sorted(absolute_clan, key=sort_key)))
    # Write that dictionary.
    _csv_dict_writer(file_or_path, column_order, clan_as_list_of_dicts)

    return True


def _csv_dict_writer(file_or_path, ordered_lefts: list, data: list):
    """
    Writes a CSV file using csv.DictWriter.  Relies on the header names and dictionary of rows
    of dictionaries that map values to a header

    :param file_or_path: Either a file path (in this case the CSV data is written to a file at this
        location) or a file object (in this case the CSV data is written to its .write() function).
    :param ordered_lefts: Header values.
    :param data: List of rows, where each element is a dictionary mapping to the fieldname header
        values.
    """
    def write_data(out_file):
        writer = _csv.DictWriter(
            f=out_file, fieldnames=ordered_lefts, dialect='excel')
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    _misc.write_to_file_or_path(file_or_path, write_data)


def _convert_clan_to_list_of_dicts(sorted_lefts: 'P( A )', absolute_clan: 'PP(A x A)') -> list:
    """Takes an absolute and left-regular clan and its left set and produces a right
    projection list of dictionaries.
    :param sorted_lefts: The left set of absolute_clan.
    :param absolute_clan: An absolute and left-regular clan.
    :return: A dictionary that represents the data in absolute_clan.
    """
    for rel in absolute_clan:
        left_to_right_dict = {}
        for left in sorted_lefts:
            # Get the right component associated with left and add it to our row.
            right = _relations.get_right(rel, left)
            if right is not _ud.Undef():
                left_to_right_dict[left] = right.value
        # Add right component dictionary to result
        yield left_to_right_dict


def import_csv(csv_file_or_filepath, types=None, skip_rows=0, index_column=None,
               has_dup_rows=False) -> 'PP( A x M )':
    """Import the file ``csv_file_or_filepath`` as CSV data and return a clan.

    :param csv_file_or_filepath: The file path or file object (for example ``StringIO`` buffer) to
        import.
    :param types: An optional dictionary of type conversions. The keys are the column names; the
        values are functors (or types) that receive the string from the CSV cell and return the
        value to be imported. Example: ``{'foo': int, 'bar': float}``.
    :param skip_rows: An optional number of lines to skip (default 0). Some CSV files have a
        preamble that can be skipped with this option.
    :param index_column: An optional name for an index column. (No index column is created if this
        argument is not specified.) The index starts with 0.
    :param has_dup_rows: An optional flag to return a multiclan instead of a clan.  This option will
        count the duplicate rows of relations and store the quantities in a multiset.  It can not
        be used in conjunction with the index_column option.
    """
    if types is None:
        types = {}

    def _filter_row(row):
        """Remove missing and blank elements from the CSV row."""
        for key, val in row.items():
            if val is None or val == '':
                continue
            yield key, val

    _util.get_left_cached.left_cache = {}

    assert(((index_column is not None) & (has_dup_rows is False)) or (index_column is None))

    def _import_csv(csv_file):
        import csv
        for _ in range(0, skip_rows):
            next(csv_file)
        reader = csv.DictReader(csv_file)

        _index = 0
        for row in reader:
            filtered_row = {key: val for key, val in _filter_row(row)}
            for key, val in types.items():
                if key in filtered_row:
                    filtered_row[key] = val(filtered_row[key])
            if index_column is not None:
                filtered_row[index_column] = _index
                _index += 1
            yield _mo.Set(
                (_mo.Couplet(left=_util.get_left_cached(left), right=_mo.Atom(right),
                    direct_load=True)
                    for left, right in filtered_row.items()),
                direct_load=True).cache_is_relation(True).cache_is_left_functional(True)

    if hasattr(csv_file_or_filepath, "readlines"):  # Support StringIO.
        if has_dup_rows:
            return _mo.Multiset(_import_csv(csv_file_or_filepath), direct_load=True)
        else:
            return _mo.Set(_import_csv(csv_file_or_filepath), direct_load=True).cache_is_clan(
                True).cache_is_left_functional(True)
    else:
        with open(csv_file_or_filepath, encoding='utf-8', errors='ignore') as file:
            if has_dup_rows:
                return _mo.Multiset(_import_csv(file), direct_load=True)
            else:
                return _mo.Set(_import_csv(file), direct_load=True).cache_is_clan(
                    True).cache_is_left_functional(True)
