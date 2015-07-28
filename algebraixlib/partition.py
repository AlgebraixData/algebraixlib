r"""Operations for partitioning :term:`set`\s and :term:`multiset`\s."""

# $Id: partition.py 22702 2015-07-28 20:20:56Z jaustell $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-28 15:20:56 -0500 (Tue, 28 Jul 2015) $
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


def _create_partition_dict(set_, class_invariant_func):
    r"""Return the data of a partition defined by ``class_invariant_func`` on ``set_``.

    :param set_: The :term:`set` to be partitioned.
    :param class_invariant_func: A function from ``set_`` to :term:`set M`.
    :return: A ``dict`` of ``set``\s, where the keys of the ``dict`` are the range of the
        equivalence relation implemented by ``class_invariant_func`` and the ``set``\s are the
        members of ``set_`` that are associated with each given key. Both the keys and the members
        of the value ``set``\s are `MathObject`\s.
    """

    # Collect the data of the partition in a dictionary of lists, which later is converted into a
    # Set of Sets.
    partition_dict = {}

    for element in set_:
        # equivalence_class must be a MathObject.
        equivalence_class = _mo.auto_convert(class_invariant_func(element))

        # equivalence_class is a MathObject, so it is hashable and can be used as dict key.
        if equivalence_class not in partition_dict:
            partition_dict[equivalence_class] = set()
        partition_dict[equivalence_class].add(element)

    return partition_dict


def partition(set_, class_invariant_func):
    r"""Return ``set_`` partitioned according to ``class_invariant_func``.

    :param set_: The :term:`set` that is to be partitioned.
    :param class_invariant_func: A function from elements of ``set_`` to `MathObject`\s. It
        defines an :term:`equivalence relation` on ``set_`` such that

        .. math:: x, y \in set\_ :
            x \equiv y \iff class\_invariant\_func(x) = class\_invariant\_func(y)

    :return: A set with structure :math:`P(set\_.ground\_set)` that defines a partition on ``set_``,
        imposed by the equivalence relation defined by the function ``class_invariant_func``.
    """

    partition_dict = _create_partition_dict(set_, class_invariant_func)
    # Create the resulting Set of Sets from the partition components
    return _mo.Set((_mo.Set(components, direct_load=True).cache_is_clan(set_.cache_is_clan)
                    for components in partition_dict.values()), direct_load=True)


def make_labeled_partition(set_, class_invariant_func):
    r"""Return a 'labeled' partition of ``set_``, partitioned according to ``class_invariant_func``.

    :param set_: The :term:`set` that is to be partitioned.
    :param class_invariant_func: A function from elements of ``set_`` to `MathObject`\s. It
        defines an :term:`equivalence relation` on ``set_`` such that

        .. math:: x, y \in set\_ :
            x \equiv y \iff class\_invariant\_func(x) = class\_invariant\_func(y)

    :return: A :term:`function` with structure :math:`P(range(class\_invariant\_func) \times
        P(set\_.ground\_set))` that maps the range of ``class_invariant_func`` when applied to
        ``set_`` to sets of elements of ``set_`` that belong to the given equivalence class.
    """

    # Collect the data of the partition in a dictionary of lists, which later is converted into a
    # Set of Sets.
    partition_dict = _create_partition_dict(set_, class_invariant_func)

    return _mo.Set((_mo.Couplet(label, _mo.Set(components))
                    for label, components in partition_dict.items()),
                   direct_load=True)
