"""An example data algebra script to demonstrate that data algebra can be used to query XML. Here you will find a few
simple examples of how to use algebraixlib to create data algebra queries that are equivalent to XPath and XQuery
queries."""

# $Id: xml_example.py 22787 2015-08-12 16:20:01Z sjohnston $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-08-12 11:20:01 -0500 (Wed, 12 Aug 2015) $
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

# Show the xml data, truncated, prettied
from algebraixlib.io.xml import xml_to_str
pretty_xml = xml_to_str('TPC-H_Query5/regions.xml')
print(pretty_xml)

from algebraixlib.util.mathobjectprinter import mo_to_str
from algebraixlib.io.xml import import_xml
regions_document = import_xml('TPC-H_Query5/regions.xml', convert_numerics=True)
print('regions_document:\n' + mo_to_str(regions_document))

# Get all regions
# /regions/region
regions = regions_document('regions')
print('regions_relation:\n' + mo_to_str(regions))

regions = regions_document('regions')['region']
print('regions:\n' + mo_to_str(regions))

# Get all region keys
# /regions/region/regionkey
region_keys = regions['regionkey']
print('region_keys:\n' + mo_to_str(region_keys))

# Get all nation names
# /regions/region/nation/name
nations = regions['nation']
print('regions[\'nation\']:\n' + mo_to_str(nations))

nation_names = nations['name']
print('nation_names:\n' + mo_to_str(nation_names))

# Get all nation names of a given region
# for $x in doc("regions.xml")/regions/region where $x/name='AMERICA' return $x/nation/name
from algebraixlib.algebras.clans import superstrict, from_dict
america_region_name = from_dict({'name': 'AMERICA'})
print('america_region_name:\n' + mo_to_str(america_region_name))

america_region = superstrict(regions, america_region_name)
print('america_region:\n' + mo_to_str(america_region))

america_nations_names = america_region['nation']['name']
print('america_nations_names:\n' + mo_to_str(america_nations_names))

# Get all region key and nation name pairs
# for $x in doc("regions.xml")/regions/region/nation/name return <pair>{$x/../../regionkey}{$x}</pair>
from algebraixlib.mathobjects import Set
from algebraixlib.algebras.clans import project, cross_union
from algebraixlib.algebras.sets import union
region_key_nation_name_pairs_accumulator = Set()
for region in regions:
    region_key = project(Set(region), 'regionkey')
    print('region_key:\n' + mo_to_str(region_key))

    region_nations = region['nation']
    print('region_nations:\n' + mo_to_str(region_nations))

    region_nation_names = project(region_nations, 'name')
    print('region_nation_names:\n' + mo_to_str(region_nation_names))

    region_key_nation_name_pairs = cross_union(region_key, region_nation_names)
    print('region_key_nation_name_pairs:\n' + mo_to_str(region_key_nation_name_pairs))

    region_key_nation_name_pairs_accumulator = union(region_key_nation_name_pairs_accumulator, region_key_nation_name_pairs)
    print('region_key_nation_name_pairs_accumulator:\n' + mo_to_str(region_key_nation_name_pairs_accumulator))

print('region_key_nation_name_pairs_accumulator:\n' + mo_to_str(region_key_nation_name_pairs_accumulator))

# Get all regions with a nation named "UNITED STATES"
# for $x in doc("regions.xml")/regions/region/nation[name="UNITED STATES"] return <name>$x/../name</name>
from algebraixlib.mathobjects.couplet import Couplet
us_nation_name = from_dict({'name': 'UNITED STATES'})
print('us_nation_name:\n' + mo_to_str(us_nation_name))

us_region_key_nation_name_pair = superstrict(region_key_nation_name_pairs_accumulator, us_nation_name)
print('us_region_key_nation_name_pair:\n' + mo_to_str(us_region_key_nation_name_pair))

us_region_key = project(us_region_key_nation_name_pair, 'regionkey')
print('us_region_key:\n' + mo_to_str(us_region_key))

us_region = superstrict(regions, us_region_key)
print('us_region:\n' + mo_to_str(us_region))

us_region_name = project(us_region, 'name')
print('us_region_name:\n' + mo_to_str(us_region_name))

print('done')


