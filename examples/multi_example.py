"""This module contains the example code for the algebras created for representing data which has multiples."""

# $Id: multi_example.py 22614 2015-07-15 18:14:53Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $$
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
import algebraixlib.algebras.multiclans as _multiclans
import algebraixlib.algebras.multisets as _multisets
import algebraixlib.mathobjects as _mo
from algebraixlib.util.latexprinter import math_object_to_latex as _math_object_to_latex

# --------------------------------------------------------------------------------------------------

ms_1 = _mo.Multiset({'a': 3, 'b': 3})
ms_2 = _mo.Multiset({'b': 2, 'c': 1})

# Multiset Union operation Example
simple_union = _multisets.union(ms_1, ms_2)

print(str(ms_1) + ' UNION ' + str(ms_2))
print('=> EVALUATES TO ' + str(simple_union))

ms_3 = _mo.Multiset({'a': 3, 'b': 3, 'c': 1})
if ms_3 == simple_union:
    print("multiset's union takes the max of all the multiples merges the arguments into one result multiset.\n")

# Multiset Intersect Operation Example
simple_intersect = _multisets.intersect(ms_1, ms_2)

print(str(ms_1) + ' INTERSECT ' + str(ms_2))
print('=> EVALUATES TO ' + str(simple_intersect))

ms_4 = _mo.Multiset({'b': 2})
if ms_4 == simple_intersect:
    print("multiset's intersect takes the min of all the multiples merges the arguments into one result multiset.\n")

# Multiset Addition operation Example
simple_addition = _multisets.addition(ms_1, ms_2)

print(str(ms_1) + ' ADDITION ' + str(ms_2))
print('=> EVALUATES TO ' + str(simple_addition))

ms_5 = _mo.Multiset({'a': 3, 'b': 5, 'c': 1})
if ms_5 == simple_addition:
    print("multiset's addition sums all the multiples of like values in the arguments into one result multiset.\n")

# Multiset Intersect Operation Example
simple_minus = _multisets.minus(ms_1, ms_2)

print(str(ms_1) + ' MINUS ' + str(ms_2))
print('=> EVALUATES TO ' + str(simple_minus))

ms_6 = _mo.Multiset({'a': 3, 'b': 1})
if ms_6 == simple_minus:
    print("multiset's minus subtracts all the rhs multiples from the lhs.\n")

# Moving on to multiclan examples now

# Setting up multiclan relations
rel_1 = _mo.Set(_mo.Couplet('x', 'y'), _mo.Couplet('w', 'y'))
rel_2 = _mo.Set(_mo.Couplet('a', 'x'), _mo.Couplet('b', 'w'))
rel_3 = _mo.Set(_mo.Couplet('x', 'z'), _mo.Couplet('v', 'y'))
rel_4 = _mo.Set(_mo.Couplet('c', 'z'), _mo.Couplet('a', 'v'))
rel_5 = _mo.Set(_mo.Couplet('b', 'w'), _mo.Couplet('w', 'y'))
rel_6 = _mo.Set(_mo.Couplet('a', 'x'), _mo.Couplet('x', 'y'))

# Creating multiclans (multisets of relations)
mc_1 = _mo.Multiset({rel_1: 2, rel_3: 3})
mc_2 = _mo.Multiset({rel_2: 5, rel_4: 1})
mc_3 = _mo.Multiset({rel_1: 2, rel_6: 7})
mc_4 = _mo.Multiset({rel_2: 5, rel_5: 11})

# Multiset Transpose Operation Example
simple_transpose = _multiclans.transpose(mc_1)

print('TRANSPOSE ' + str(mc_1))
print('=> EVALUATES TO ' + str(simple_transpose))

mc_tmp = _mo.Multiset(
    {_mo.Set(_mo.Couplet('y', 'x'), _mo.Couplet('y', 'w')): 2,
     _mo.Set(_mo.Couplet('z', 'x'), _mo.Couplet('y', 'v')): 3})
if mc_tmp == simple_transpose:
    print("multiclan's transpose swaps the left and right values of the relations, "
          "leaving multiplicity to be the same.\n")

# Multiset Compose Operation Example
simple_compose_1 = _multiclans.compose(mc_1, mc_2)

print(str(mc_1) + ' COMPOSE ' + str(mc_2))
print('=> EVALUATES TO ' + str(simple_compose_1))

print("multiclan's compose applies a cross compose of the relations in each sides multiclan, "
      "the multiplicity is the product of each sides multiplicity.\n")

simple_compose_2 = _multiclans.compose(mc_2, mc_1)

print(str(mc_2) + ' COMPOSE ' + str(mc_1))
print('=> EVALUATES TO ' + str(simple_compose_2))

print("multiclan's compose can result in relation compositions such that two different operations"
      "yield the same result.  For multiclans operations these same results are summed together.\n")

# Multiset Cross Union Operation Example
simple_cross_union_1 = _multiclans.cross_union(mc_1, mc_2)

print(str(mc_1) + ' CROSS UNION ' + str(mc_2))
print('=> EVALUATES TO ' + str(simple_cross_union_1))

print("multiclan's cross union applies the relation's union for all relations in the multiclan of each argument.  "
      "Again the resulting multiple is the product of the two relations multiples.\n")

simple_cross_union_2 = _multiclans.cross_union(mc_3, mc_4)

print(str(mc_3) + ' CROSS UNION ' + str(mc_4))
print('=> EVALUATES TO ' + str(simple_cross_union_2))

print("multiclan's cross union like other operations can yield the same result for different inner relation unions"
      "These same results are summed together.\n")

# Multiset Cross Intersect Operation Example
simple_cross_intersect_1 = _multiclans.cross_intersect(mc_1, mc_2)

print(str(mc_1) + ' CROSS INTERSECT ' + str(mc_2))
print('=> EVALUATES TO ' + str(simple_cross_intersect_1))

print("multiclan's cross intersect applies relation's intersect for all relations in the multiclan of each argument."
      "Again the resulting multiple is the product of the two relations multiples.\n")

simple_cross_intersect_2 = _multiclans.cross_intersect(mc_3, mc_4)

print(str(mc_3) + ' CROSS INTERSECT ' + str(mc_4))
print('=> EVALUATES TO ' + str(simple_cross_intersect_2))

print("multiclan's cross intersect can yield the same result for different inner relation intersect"
      "These same results are summed together.\n")

# CSV TIME
sales_csv = """product,cashier
apple,jane
banana,doug
apple,jane
peach,doug
rice,frank
rice,frank
banana,doug
apple,doug
rice,jane
apple,jane
"""

# Tables can be modeled as multisets of binary relations, which we call clans.
from io import StringIO
from algebraixlib.io.csv import import_csv
from algebraixlib.io.csv import export_csv

file = StringIO(sales_csv)
sales_multiclan = import_csv(file, has_dup_rows=True)  # note the use of flag to return a multiclan
print(sales_multiclan)

# lets see how our cashiers are doing
cashier_diagonal = _mo.Multiset({_mo.Set(_mo.Couplet('cashier', 'cashier')): 1})
cashier_sales = _multiclans.compose(sales_multiclan, cashier_diagonal)
print("To find out how many sales each cashier has had, we can do the following:")
print(str("sales_multiclan") + ' COMPOSE ' + str(cashier_diagonal))
print('=> EVALUATES TO ' + str(cashier_sales) + "\n")

# lets see what products we sold for the day
product_diagonal = _mo.Multiset({_mo.Set(_mo.Couplet('product', 'product')): 1})
product_sales = _multiclans.compose(sales_multiclan, product_diagonal)
print("To find out how many products we sold, we can do the following:")
print(str("sales_multiclan") + ' COMPOSE ' + str(product_diagonal))
print('=> EVALUATES TO ' + str(product_sales) + "\n")

# Print some of these new math objects in LaTeX.
print(_math_object_to_latex(simple_union))
print(_math_object_to_latex(sales_multiclan))
print(_math_object_to_latex(product_sales))

# Export a multiclan
print("\nConverting the multiclan back to a csv file is easy.")
sales_csv_out = StringIO()
export_csv(sales_multiclan, sales_csv_out)
csv_str = sales_csv_out.getvalue()
print(csv_str)
