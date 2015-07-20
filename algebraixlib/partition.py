"""Definitions for partitioning and other set operations that P(M) is not closed under."""

# $Id: partition.py 22614 2015-07-15 18:14:53Z gfiedler $
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


def _create_partition_dict(set1, equivalence_relation):
    """Return the data of a partition defined by ``equivalence_relation`` on ``set1``.

    :param set1: The :term:`set` to be partitioned.
    :param equivalence_relation: A function from ``set1`` to :term:`set M`.
    :return: A ``dict`` of ``set``\s, where the keys of the ``dict`` are the range of the
        equivalence relation implemented by ``equivalence_relation`` and the ``set``\s are the
        members of ``set1`` that are associated with each given key.
    """

    # Collect the data of the partition in a dictionary of lists, which later is converted into a
    # Set of Sets.
    partition_dict = {}

    for element in set1:
        # equivalence_class must be a MathObject.
        equivalence_class = _mo.auto_convert(equivalence_relation(element))

        # equivalence_class is a MathObject, so it is hashable and can be used as dict key.
        if equivalence_class not in partition_dict:
            partition_dict[equivalence_class] = set()
        partition_dict[equivalence_class].add(element)

    return partition_dict


def partition(set1, equivalence_relation):
    """Returns a set with structure P(set1.ground_set) that defines a partition on set1, imposed by
    the equivalence relation defined by the equivalence_relation function: a function from elements
    of set1 to MathObjects."""

    partition_dict = _create_partition_dict(set1, equivalence_relation)
    # Create the resulting Set of Sets from the partition components
    return _mo.Set((_mo.Set(components, direct_load=True).cache_is_clan(set1.cache_is_clan)
                    for components in partition_dict.values()), direct_load=True)


def left_equiv_relation(set1, equivalence_relation):
    """Returns a set with structure P(set1.ground_set) that defines a partition on set1, imposed by
    the equivalence relation defined by the equivalence_relation function: a function from elements
    of set1 to a value that can be placed in a Atom."""

    # Collect the data of the partition in a dictionary of lists, which later is converted into a
    # Set of Sets.
    partition_dict = _create_partition_dict(set1, equivalence_relation)

    return _mo.Set((_mo.Couplet(label, _mo.Set(components))
                    for label, components in partition_dict.items()),
                   direct_load=True)

