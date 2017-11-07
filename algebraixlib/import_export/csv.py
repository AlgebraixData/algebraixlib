r"""Import :term:`regular` :term:`clan`\s from and export them to CSV data."""

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
import collections as _collections
import csv as _csv

import algebraixlib.algebras.clans as _clans
import algebraixlib.algebras.multiclans as _multiclans
import algebraixlib.algebras.relations as _relations
# noinspection PyProtectedMember
import algebraixlib.import_export._util as _util
import algebraixlib.mathobjects as _mo
import algebraixlib.undef as _ud
import algebraixlib.util.miscellaneous as _misc

from ..cache_status import CacheStatus


def export_csv(absolute_clan_or_multiclan, file_or_path, ordered_lefts=None, sort_key=None):
    r"""Export an absolute clan or absolute multiclan as CSV file with header row.

    The :term:`left component`\s of the :term:`clan` or term:`multiclan` are interpreted as
    column names and are exported as header row. Every :term:`relation` in the input becomes a
    data row in the CSV file.

    :param absolute_clan_or_multiclan: An :term:`absolute clan` or term:`absolute multiclan`. If
        it is not :term:`regular`, ``ordered_lefts`` must be given.
    :param file_or_path: Either a file path (in this case the CSV data is written to a file at this
        location) or a file object (in this case the CSV data is written to its ``.write()``
        function).
    :param ordered_lefts: (Optional) A ``Sequence`` of :term:`left`\s that are exported in the
        given order. Default is the sequence that is the lexically sorted :term:`left set` of the
        (multi)clan. This parameter is required if ``absolute_clan_or_multiclan`` is not
        term:`regular`.
    :param sort_key: (Optional) A function that compares two row-:term:`relation`\s and provides an
        order (for use with :func:`sorted`). The output is not sorted if ``sort_key`` is missing.
    :return: ``True`` if the CSV export succeeded, ``False`` if not.
    """
    if not _clans.is_absolute_member(absolute_clan_or_multiclan) \
            and not _multiclans.is_absolute_member(absolute_clan_or_multiclan):
        return False
    regular_clan = _clans.is_member(absolute_clan_or_multiclan) \
            and _clans.is_regular(absolute_clan_or_multiclan)
    regular_mclan = _multiclans.is_member(absolute_clan_or_multiclan) \
            and _multiclans.is_regular(absolute_clan_or_multiclan)
    if ordered_lefts is None and not (regular_clan or regular_mclan):
        return False

    if ordered_lefts is None:
        # Since this clan is regular, get first relation to acquire left set.
        rel = next(iter(absolute_clan_or_multiclan))
        # left_set is sorted to guarantee consistent iterations
        ordered_lefts = sorted([left.value for left in rel.get_left_set()])

    # Generate dictionaries that associates left components with their right components for each
    # relation.
    clan_as_list_of_dicts = _convert_clan_to_list_of_dicts(
        ordered_lefts, (absolute_clan_or_multiclan
            if sort_key is None else sorted(absolute_clan_or_multiclan, key=sort_key)))
    # Write the dictionaries.
    _csv_dict_writer(file_or_path, ordered_lefts, clan_as_list_of_dicts)
    return True


def _csv_dict_writer(file_or_path, ordered_columns: _collections.Sequence,
                     data: _collections.Sequence):
    """Write a CSV file using `csv.DictWriter`.

    :param file_or_path: Either a file path (in this case the CSV data is written to a file at this
        location) or a file object (in this case the CSV data is written to its ``.write()``
        function).
    :param ordered_columns: A `Sequence` of column names (atoms). The columns are
        written in the given order.
    :param data: A `Sequence` of rows, where each row is a dictionary, mapping a column name to its
        value in the given row. Both the column name and the value are atoms.
    """
    def write_data(out_file):
        writer = _csv.DictWriter(
            f=out_file, fieldnames=ordered_columns, dialect='excel')
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    _misc.write_to_file_or_path(file_or_path, write_data)


def _convert_clan_to_list_of_dicts(ordered_lefts: 'P( A )', absolute_clan: 'PP(A x A)') -> list:
    """Convert a regular, absolute clan into a list of dictionaries.

    :param ordered_lefts: The left components of ``absolute_clan`` that are converted.
    :param absolute_clan: A regular, absolute clan that is converted into a list of dictionaries.
    :return: A list of dictionaries. Every dictionary represents a single relation in
        ``absolute_clan``. The lefts of the relation become the keys, the rights become the values
        of the dictionary.
    """
    for rel in absolute_clan:
        left_to_right_dict = {}
        for left in ordered_lefts:
            # Get the right component associated with left and add it to our row.
            right = _relations.get_right(rel, left)
            if right is not _ud.Undef():
                left_to_right_dict[left] = right.value
        # Add right component dictionary to result
        yield left_to_right_dict


def import_csv(csv_file_or_filepath, types: {}=None, skip_rows: int=0, index_column: str=None,
               has_dup_rows: bool=False, columns: []=None) -> 'PP( A x M )':
    r"""Import the file ``csv_file_or_filepath`` as CSV data and return a clan or multiclan.

    :param csv_file_or_filepath: The file path or file object (for example ``StringIO`` buffer) to
        import.
    :param types: (Optional) A dictionary of type conversions. The keys are the column names; the
        values are functors (or types) that receive the string from the CSV cell and return the
        value to be imported. Example: ``{'foo': int, 'bar': float}``. By default all values are
        interpreted as `string`\s.
    :param skip_rows: (Optional) A number of lines to skip (default 0). Some CSV files have a
        preamble that can be skipped with this option.
    :param index_column: (Optional) A name for an index column. (No index column is created if this
        argument is not specified.) The index starts with 0. (This option is not compatible with the
        ``has_dup_rows`` option.)
    :param has_dup_rows: (Optional) If ``True``, allow duplicate rows and return a multiclan
        instead of a clan. By default, the value is ``False`` and a clan is returned. (This option
        is not compatible with the option ``index_column``.)
    :param columns: (Optional) A list of column names. If present, this list is used as the
        sequence of columns (and all lines in the data are loaded). If missing, the first line of
        the data must be a header that contains the column names (and this header line is not
        loaded as data).
    :return: A :term:`clan` (if ``has_dup_rows is ``False`` or not provided) or a :term:`multiclan`
        (if ``has_dup_rows`` is ``True``).
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
    import_csv.regular = True  # Set to false if any row is missing one or more values

    assert ((index_column is not None) & (has_dup_rows is False)) or (index_column is None)

    def _import_csv(csv_file):
        for _ in range(0, skip_rows):
            next(csv_file)
        reader = _csv.DictReader(csv_file, fieldnames=columns)

        _index = 0
        for row in reader:
            filtered_row = {key: val for key, val in _filter_row(row)}
            if import_csv.regular and len(row) != len(filtered_row):
                import_csv.regular = False
            for key, val in types.items():
                if key in filtered_row:
                    filtered_row[key] = val(filtered_row[key])
            if index_column is not None:
                filtered_row[index_column] = _index
                _index += 1
            yield _mo.Set(
                (_mo.Couplet(left=_util.get_left_cached(left), right=_mo.Atom(right),
                direct_load=True) for left, right in filtered_row.items()), direct_load=True)\
                .cache_relation(CacheStatus.IS).cache_functional(CacheStatus.IS)

    if hasattr(csv_file_or_filepath, "readlines"):  # Support StringIO.
        if has_dup_rows:
            return _mo.Multiset(_import_csv(csv_file_or_filepath),
                                direct_load=True).cache_multiclan(
                CacheStatus.IS).cache_functional(CacheStatus.IS).cache_regular(
                CacheStatus.from_bool(import_csv.regular))
        else:
            return _mo.Set(_import_csv(csv_file_or_filepath), direct_load=True)\
                .cache_clan(CacheStatus.IS).cache_functional(CacheStatus.IS)\
                .cache_regular(CacheStatus.from_bool(import_csv.regular))
    else:
        with open(csv_file_or_filepath, encoding='utf-8', errors='ignore') as file:
            if has_dup_rows:
                return _mo.Multiset(_import_csv(file), direct_load=True).cache_multiclan(
                    CacheStatus.IS).cache_functional(CacheStatus.IS).cache_regular(
                    CacheStatus.from_bool(import_csv.regular))
            else:
                return _mo.Set(_import_csv(file), direct_load=True)\
                    .cache_clan(CacheStatus.IS).cache_functional(CacheStatus.IS)\
                    .cache_regular(CacheStatus.from_bool(import_csv.regular))
