"""This file contains utility functions that create our formats from TPC-H original data.

The data that we use in our IPython notebooks and the query code has already been created. These
functions are only provided in case you want to run the tests (or similar code) on different data.
"""

# $Id: format_conversions.py 22614 2015-07-15 18:14:53Z gfiedler $
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
from os import path
import re


def convert_table_to_csv(table_path: str, columns: [str]):
    """Convert a TPC-H table file into a CSV file with header.

    :param table_path: The file name/path of the TPC-H table file. May have a prefixed path
        (relative or absolute). The table file name/path must have an extension of '.tbl'; the CSV
        output file name/path is derived by replacing the extension with '.csv'.
    :param columns: A list of strings with the column names.
    """

    assert table_path[-4:] == '.tbl'
    base_path = table_path[:-4]
    csv_path = base_path + '.csv'

    with open(table_path, 'r') as table, open(csv_path, 'w', newline='\r\n') as csv:
        # Get the number of columns by counting the termination character '|' in the first line.
        # The character terminates every column, and all rows have the same number of columns.
        separators = re.findall('\\|', table.readline())
        column_count = len(separators)
        assert column_count == len(columns)
        table.seek(0)

        # Write the CSV header line with the column names.
        csv_header = ','.join(['"{0}"'.format(column) for column in columns])
        csv.write(csv_header + '\n')

        # Create the regex match pattern (pre-compiled) and the substitution pattern (used as text).
        table_match_pattern_text = '([^|]*)\\|' * column_count
        table_match_pattern = re.compile(table_match_pattern_text)
        csv_subst_pattern_text = ','.join(
            ['"\\{0}"'.format(count) for count in range(1, column_count + 1)])

        # Apply the regex substitution to every data line and write the result to the CSV file.
        for line in table:
            csv_line = re.sub(table_match_pattern, csv_subst_pattern_text, line)
            csv.write(csv_line)

    print(csv_path, 'created.')


def create_regions_xml(dir_path: str=''):
    """Convert the tables 'region.tbl' and 'nation.tbl' into an XML document 'regions.xml'.

    The hierarchy relationship that is expressed by the column 'regionkey' in the table 'nation.tbl'
    is expressed by element hierarchy in the resulting XML document.

    :param dir_path: The directory path for the files. May be relative or absolute; defaults to the
        empty string (current directory). The file paths are derived by appending the file names to
        ``dir_path``.
    """

    region_tbl_path = path.join(dir_path, 'region.tbl')
    nation_tbl_path = path.join(dir_path, 'nation.tbl')
    regions_xml_path = path.join(dir_path, 'regions.xml')

    # Since both the 'region' and the 'nation' files are small, we can read them into memory, then
    # create the output data and write the output file from the data in memory.

    # Create a list `regions` that contains a dictionary for each row in 'region.tbl'.
    with open(region_tbl_path, 'r') as region_table:
        # Create a regex match pattern where the individual groups are named with the column names.
        # This makes the match result a dictionary with the column names as keys.
        region_columns = ['regionkey', 'name', 'comment']
        pattern_text = ''.join(['(?P<{0}>[^|]*)\\|'.format(column) for column in region_columns])
        pattern = re.compile(pattern_text)

        regions = []
        for line in region_table:
            match = re.match(pattern, line)
            result = match.groupdict()
            assert len(result) == len(region_columns)
            regions.append(result)

    # Create a list `nations` that contains a dictionary for each row in 'nation.tbl'.
    with open(nation_tbl_path, 'r') as nation_table:
        # Create a regex match pattern where the individual groups are named with the column names.
        # This makes the match result a dictionary with the column names as keys.
        nation_columns = ['nationkey', 'name', 'regionkey', 'comment']
        pattern_text = ''.join(['(?P<{0}>[^|]*)\\|'.format(column) for column in nation_columns])
        pattern = re.compile(pattern_text)

        nations = []
        for line in nation_table:
            match = re.match(pattern, line)
            result = match.groupdict()
            assert len(result) == len(nation_columns)
            nations.append(result)

    # Create a simple XML structure from the table data, placing nations that have a regionkey
    # that matches the current region's key underneath its associated region.
    with open(regions_xml_path, 'w') as regions_file:
        regions_file.write('<regions>\n')
        for region in regions:
            regions_file.write('  <region>\n')
            for key, val in region.items():
                regions_file.write('    <{key}>{val}</{key}>\n'.format(key=key, val=val))
            for nation in nations:
                if nation['regionkey'] == region['regionkey']:
                    regions_file.write('    <nation>\n')
                    for key, val in nation.items():
                        if key != 'regionkey':
                            regions_file.write('      <{key}>{val}</{key}>\n'.format(
                                key=key, val=val))
                    regions_file.write('    </nation>\n')
            regions_file.write('  </region>\n')
        regions_file.write('</regions>\n')

    print(regions_xml_path, 'created.')


def create_supplier_graph(dir_path: str=''):
    """Convert the table 'supplier.tbl' into an RDF graph 'supplier.ttl'.

    In order to avoid having to deal with blank nodes, the subject node is an IRI derived from the
    suppkey instead of the customary blank node (skolemization). The column names are converted into
    ad-hoc IRIs of the form <tpch:columnname>.

    :param dir_path: The directory path for the files. May be relative or absolute; defaults to the
        empty string (current directory). The file paths are derived by appending the file names to
        ``dir_path``.
    """
    supplier_tbl_path = path.join(dir_path, 'supplier.tbl')
    supplier_rdf_path = path.join(dir_path, 'supplier.ttl')

    def quote_val(value):
        # If value can be converted into a number (float), return it as is. Otherwise, return it
        # double-quoted (and with double quotes doubled up).
        try:
            # If this succeeds, `value` represents a number. In this case, we write it as-is
            # (without quotes), so that it is read as number.
            float(value)
            return value
        except ValueError:
            # If the `float(value)` statement failed with a ValueError, treat `value` as string:
            # enclose it in double quotes and double up any double quotes in the string.
            return '"{0}"'.format(value.replace('"', '""'))

    with open(supplier_tbl_path, 'r') as supp_tbl, \
            open(supplier_rdf_path, 'w', newline='\r\n') as supp_ttl:
        # Create a regex match pattern where the individual groups are named with the column names.
        # This makes the match result a dictionary with the column names as keys.
        supp_cols = ['suppkey', 'name', 'address', 'nationkey', 'phone', 'acctbal', 'comment']
        pattern_text = ''.join(['(?P<{0}>[^|]*)\\|'.format(column) for column in supp_cols])
        pattern = re.compile(pattern_text)

        for line in supp_tbl:
            match = re.match(pattern, line)
            result = match.groupdict()
            assert len(result) == len(supp_cols)
            supp_iri = 'tpch:supplier-{0}'.format(result['suppkey'])
            for column_name, column_val in sorted(result.items()):
                triple = '<{subject_iri}> <tpch:{column_name}> {quoted_val} .\n'.format(
                    subject_iri=supp_iri, column_name=column_name, quoted_val=quote_val(column_val))
                supp_ttl.write(triple)

    print(supplier_rdf_path, 'created.')


# --------------------------------------------------------------------------------------------------
# Call the functions. Customize this section according to what you want to create.

if __name__ == '__main__':
    # For the XML and RDF graph conversions we assume the current directory; no argument is needed.
    create_regions_xml()
    create_supplier_graph()

    # The CSV conversions need table file name and column names. We assume the current directory.
    convert_table_to_csv('customer.tbl', ['custkey', 'name', 'address', 'nationkey', 'phone',
                                          'acctbal', 'mktsegment', 'comment'])
    convert_table_to_csv(
        'orders.tbl', ['orderkey', 'custkey', 'orderstatus', 'totalprice', 'orderdate',
                       'orderpriority', 'clerk', 'shippriority', 'comment'])
    convert_table_to_csv(
        'lineitem.tbl', ['orderkey', 'partkey', 'suppkey', 'linenumber','quantity', 'extendedprice',
                         'discount', 'tax', 'returnflag', 'linestatus', 'shipdate', 'commitdate',
                         'receiptdate', 'shipinstruct', 'shipmode', 'comment'])
