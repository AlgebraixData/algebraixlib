"""Example code that implements a modified version of the TPC-H query 5.

For detailed explanations, see the IPython notebooks in the same directory. The code here is similar
but not necessarily exactly the same as the code in the notebooks. The code here is structured
similarly to how it is presented in the notebooks to make it easy to cross-reference.

For the code that we used to create the modified data, see the file format_conversions.py in the
same directory.
"""

# $Id: TPC-H_Query5.py 22614 2015-07-15 18:14:53Z gfiedler $
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
from datetime import datetime
import rdflib

import algebraixlib.algebras.clans as clans
import algebraixlib.algebras.relations as relations
import algebraixlib.algebras.sets as sets
import algebraixlib.io.csv as csv
import algebraixlib.io.rdf as rdf
import algebraixlib.io.xml as xml
from algebraixlib.mathobjects import Couplet, Set
import algebraixlib.partition as partition
from algebraixlib.util.miscellaneous import FunctionTimer

# --------------------------------------------------------------------------------------------------

# Query parameter: region name.
region_name = 'MIDDLE EAST'

# Query parameters: date range.
# (Python has no native date (year/month) calculation, so we provide an end date instead of
# calculating it from `start_date` and an interval.)
start_date = datetime(1994, 1, 1).date()
end_date = datetime(1997, 1, 1).date()


# --------------------------------------------------------------------------------------------------
# Code in the notebook 2-Tables.

def get_customers_nations_projected(nations):
    """Execute the equivalent of the following SQL query, querying the CSV file customer.csv:
        SELECT
            custkey, nationkey, nationname
        FROM
            customer
        JOIN
            nations
        ON
            customer.nationkey = nations.nationkey
    """
    timer = FunctionTimer()
    short_prints = True

    customer_types = {'custkey': int, 'nationkey': int, 'acctbal': float}
    customers = csv.import_csv('customer.csv', customer_types)
    timer.lap('customers', short=short_prints)

    customers_nations = clans.functional_cross_union(customers, nations)
    timer.lap('customers_nations', short=short_prints)

    customers_nations_projected = clans.project(customers_nations,
                                                'custkey', 'nationkey', 'nationname')
    timer.end('customers_nations_projected', short=short_prints)

    return customers_nations_projected


def get_orders_restricted_projected(startdate, enddate):
    """Execute the equivalent of the following SQL query, querying the CSV file orders.csv:
        SELECT
            orderkey, custkey
        FROM
            orders
        WHERE
            startdate <= orders.orderdate and orders.orderdate < enddate

    :param startdate: The lower boundary (inclusive) of the date range for the column 'orderdate'.
    :param enddate: The upper boundary (exclusive) of the date range for the column 'orderdate'.
    """
    timer = FunctionTimer()
    short_prints = True

    def read_date(date_str: str) -> datetime:
        return datetime.strptime(date_str, '%Y-%m-%d').date()

    orders_types = {
        'orderkey': int, 'custkey': int, 'orderdate': read_date,
        'totalprice': float, 'shippriority': int
    }
    orders = csv.import_csv('orders.csv', orders_types)
    timer.lap('orders', short=short_prints)

    def select_dates(rel) -> bool:
        orderdate = rel('orderdate').value
        return (startdate <= orderdate) and (orderdate < enddate)

    orders_restricted = sets.restrict(orders, select_dates)
    timer.lap('orders_restricted', short=short_prints)

    orders_restricted_projected = clans.project(orders_restricted, 'orderkey', 'custkey')
    timer.end('orders_restricted_projected', short=short_prints)

    return orders_restricted_projected


# --------------------------------------------------------------------------------------------------
# Code in the notebook 3-Graphs.

def get_supplier_solutions():
    """Execute the equivalent of the following SPARQL query, querying the Turtle file supplier.ttl:
        SELECT
            ?suppkey, ?nationkey
        FROM
            supplier
        WHERE {
            ?supplier <tpch:suppkey> ?suppkey .
            ?supplier <tpch:nationkey> ?nationkey .
        }
    """
    timer = FunctionTimer()
    short_prints = True

    suppliers = rdf.import_graph('supplier.ttl')
    timer.lap('suppliers', short=short_prints)

    # Find all triples that define a 'suppkey' (as predicate).
    bgp_suppkey_matches = clans.superstrict(
        suppliers, clans.from_dict({'p': rdflib.URIRef('tpch:suppkey')}))
    # Give the subject a name for later joining and object the name we need in the output.
    bgp_suppkey = clans.compose(
        bgp_suppkey_matches, clans.from_dict({'supplier': 's', 'suppkey': 'o'}))

    # Find all triples that define a 'nationkey' (as predicate) and give the subject a name for
    # later joining and object the name we need in the output.
    bgp_nationkey = clans.compose(
        clans.superstrict(suppliers, clans.from_dict({'p': rdflib.URIRef('tpch:nationkey')})),
        clans.from_dict({'supplier': 's', 'nationkey': 'o'}))

    # Join the previous results on 'supplier' and project the columns we need.
    supplier_solutions = clans.project(
        clans.functional_cross_union(bgp_suppkey, bgp_nationkey), 'nationkey', 'suppkey')
    timer.end('supplier_solutions', short=short_prints)

    return supplier_solutions


# --------------------------------------------------------------------------------------------------
# Code in the notebook 4-Hierarchies.

def get_nations(regionname):
    """Execute the equivalent of the following XQuery statement and convert the XML into a clan:
        for $x in doc("regions.xml")/regions/region[name="MIDDLE EAST"]/nation
            return <nation>{$x/nationkey}<nationname>{data($x/name)}</nationname></nation>
    """
    timer = FunctionTimer()
    short_prints = True

    # Load the XML document. (Don't use multiplicity or sequence; our data doesn't require this.)
    regions = xml.import_xml('regions.xml', convert_numerics=True)
    timer.lap('regions', short=short_prints)

    # Get a clan where each region is a row.
    regions_clan = regions('regions')['region']
    timer.lap('regions_clan', short=short_prints)

    # Filter this clan down to the region of interest (name is `regionname`).
    target_region = clans.superstrict(regions_clan, clans.from_dict({'name': regionname}))
    timer.lap('target_region', short=short_prints)

    # Get all 'nation' lefts out of this clan and create a clan where every row is a nation's data.
    nations_clan = target_region['nation']
    timer.lap('nations_clan', short=short_prints)

    # Rename 'name' to 'nationname' and project 'nationkey' and 'nationname' (removing 'comment').
    nations = clans.compose(nations_clan,
                            clans.from_dict({'nationkey': 'nationkey', 'nationname': 'name'}))
    timer.end('nations', short=short_prints)

    return nations


# --------------------------------------------------------------------------------------------------
# Code in the notebook 5-Query.

def query5():
    # select
    #     nationname,
    #     sum(lineitem.extendedprice * (1 - lineitem.discount)) as revenue
    # from
    #     customer, orders, lineitem,   -- Loaded from CSV
    #     nation, region                -- Loaded from XML
    # where
    #     customer.custkey = orders.custkey
    #     and lineitem.orderkey = orders.orderkey
    #     and customer.nationkey = nation.nationkey
    #     and supplier.nationkey = nation.nationkey
    #     and nation.regionkey = region.regionkey
    #     and region.name = 'AMERICA'
    #     and orders.orderdate >= date '1996-01-01'
    #     and orders.orderdate < date '1996-01-01' + interval '1' year
    # group by
    #     n_name
    timer = FunctionTimer()
    short_prints = True

    # Join supplier_solutions and customers_nations_projected on 'nationkey'.
    result1 = clans.functional_cross_union(
        get_supplier_solutions(), get_customers_nations_projected(get_nations(region_name)))
    timer.lap('result1', short=short_prints)

    # Join result1 with orders_restricted_projected on 'custkey'.
    result2 = clans.functional_cross_union(
        result1, get_orders_restricted_projected(start_date, end_date))
    timer.lap('result2', short=short_prints)

    # Join result with lineitem on 'orderkey' and 'suppkey'.
    lineitem_types = {
        'orderkey': int, 'suppkey': int, 'extendedprice': float, 'discount': float,
        'partkey': int, 'linenumber': int, 'quantity': int, 'tax': float,
    }
    result3 = clans.functional_cross_union(result2, csv.import_csv('lineitem.csv', lineitem_types))
    timer.lap('result3', short=short_prints)

    # Add the 'revenue' column.
    def calc_revenue(rel):
        return Couplet('revenue', rel('extendedprice').value * (1 - rel('discount').value))
    result4 = Set(relations.functional_add(rel, calc_revenue(rel)) for rel in result3)
    timer.lap('result4', short=short_prints)
    # Remove unnecessary columns.
    revenue_by_nations = clans.project(result4, 'revenue', 'nationname')

    # Partition the result on 'nationname'.
    revenue_grouped_by_nations = partition.partition(
        revenue_by_nations, lambda rel: rel('nationname'))
    timer.lap('revenue_grouped_by_nations', short=short_prints)

    # Almost generic aggregation function. (Handles 'normal' cases, but not all edge cases.)
    def aggregate(horde, group_left, aggregation_left, aggregate_func):
        aggregation = {}
        for clan in horde:
            aggregation_value = aggregate_func.identity
            for relation in clan:
                aggregation_value = aggregate_func(aggregation_value,
                                                   relation(aggregation_left).value)
            first_relation = next(iter(clan))
            aggregation[first_relation(group_left)] = aggregation_value
        return Set([Set(Couplet(group_left, key),
                        Couplet(aggregation_left, aggregation[key])) for key in aggregation])

    # Our aggregation function (adding two numbers, identity is 0).
    def aggregate_sum(arg1, arg2):
        return arg1 + arg2
    aggregate_sum.identity = 0

    # Calculate the aggregation result.
    # noinspection PyTypeChecker
    query5_result = aggregate(
        revenue_grouped_by_nations, 'nationname', 'revenue', aggregate_sum)
    timer.end('query5_result')

    return query5_result


# --------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # Run the full query.
    query5()
