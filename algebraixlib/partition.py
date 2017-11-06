r"""Operations for partitioning :term:`set`\s and :term:`multiset`\s."""

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

import algebraixlib.mathobjects as _mo


def _create_partition_dict_from_set(set_, class_invariant_func):
    r"""Return the data of a partition defined by ``class_invariant_func`` on ``set_``.

    :param set_: The :term:`set` to be partitioned.
    :param class_invariant_func: A function from ``set_`` to :term:`set M`.
    :return: A ``dict`` of ``set``\s, where the keys of the ``dict`` are the range of the
        equivalence relation implemented by ``class_invariant_func`` and the ``set``\s are the
        members of ``set_`` that are associated with each given key. Both the keys and the members
        of the value ``set``\s are `MathObject`\s.
    """
    # Collect the data of the partition in a dictionary of sets.
    partition_dict = {}

    for element in set_:
        # equivalence_class must be a MathObject.
        equivalence_class = _mo.auto_convert(class_invariant_func(element))

        # equivalence_class is a MathObject, so it is hashable and can be used as dict key.
        if equivalence_class not in partition_dict:
            partition_dict[equivalence_class] = set()
        partition_dict[equivalence_class].add(element)

    return partition_dict


def _create_partition_dict_from_multiset(mset, class_invariant_func):
    r"""Return the data of a partition defined by ``class_invariant_func`` on ``mset``.

    :param mset: The :term:`multiset` to be partitioned.
    :param class_invariant_func: A function from ``mset`` to :term:`set M`.
    :return: A ``dict`` of :class:`~collection.Counter`\s, where the keys of the ``dict`` are the
        range of the equivalence relation implemented by ``class_invariant_func`` and the
        ``Counter``\s are the members of ``mset`` that are associated with each given key. Both
        the keys and the value members of the ``Counter``\s are `MathObject`\s.
    """

    # Collect the data of the partition in a dictionary of Counters.
    partition_dict = {}

    for element, count in mset.data.items():
        # equivalence_class must be a MathObject.
        equivalence_class = _mo.auto_convert(class_invariant_func(element))

        # equivalence_class is a MathObject, so it is hashable and can be used as dict key.
        if equivalence_class not in partition_dict:
            partition_dict[equivalence_class] = _collections.Counter()
        partition_dict[equivalence_class][element] = count

    return partition_dict


def partition(set_or_mset, class_invariant_func):
    r"""Return ``set_or_mset`` partitioned according to ``class_invariant_func``.

    :param set_or_mset: The :term:`set` or :term:`multiset` that is to be partitioned.
    :param class_invariant_func: A function from elements of ``set_or_mset`` to
        `MathObject`\s. It defines an :term:`equivalence relation` on ``set_or_mset`` such that

        .. math:: x, y \in set\_or\_mset :
            x \equiv y \iff class\_invariant\_func(x) = class\_invariant\_func(y)

    :return: A set with structure :math:`P(set\_or\_mset.ground\_set)` that defines a partition on
        ``set_or_mset``, imposed by the equivalence relation defined by the function
        ``class_invariant_func``.
    """
    if set_or_mset.is_set:
        partition_dict = _create_partition_dict_from_set(set_or_mset, class_invariant_func)
        # Create the resulting Set of Sets from the partition components.
        return _mo.Set((_mo.Set(components, direct_load=True)
            .cache_clan(set_or_mset.cached_clan)
            for components in partition_dict.values()), direct_load=True)
    elif set_or_mset.is_multiset:
        partition_dict = _create_partition_dict_from_multiset(set_or_mset, class_invariant_func)
        # Create the resulting Set of Multisets from the partition components.
        return _mo.Set((_mo.Multiset(counter, direct_load=True)
            .cache_multiclan(set_or_mset.cached_multiclan)
            for counter in partition_dict.values()), direct_load=True)
    else:
        raise AssertionError('First argument must be Set or Multiset')


def make_labeled_partition(set_or_mset, class_invariant_func):
    r"""Return a 'labeled' partition of ``set_or_mset``, partitioned according to
    ``class_invariant_func``.

    :param set_or_mset: The :term:`set` or :term:`multiset` that is to be partitioned.
    :param class_invariant_func: A function from elements of ``set_or_mset`` to `MathObject`\s. It
        defines an :term:`equivalence relation` on ``set_or_mset`` such that

        .. math:: x, y \in set\_or\_mset :
            x \equiv y \iff class\_invariant\_func(x) = class\_invariant\_func(y)

    :return: A :term:`function` with structure :math:`P(range(class\_invariant\_func) \times
        P(set\_or\_mset.ground\_set))` that maps the range of ``class_invariant_func`` when
        applied to ``set_or_mset`` to sets of elements of ``set_or_mset`` that belong to the
        given equivalence class.
    """
    if set_or_mset.is_set:
        partition_dict = _create_partition_dict_from_set(set_or_mset, class_invariant_func)
        return _mo.Set((_mo.Couplet(label, _mo.Set(components, direct_load=True)
                .cache_clan(set_or_mset.cached_clan), direct_load=True)
            for label, components in partition_dict.items()), direct_load=True)
    elif set_or_mset.is_multiset:
        partition_dict = _create_partition_dict_from_multiset(set_or_mset, class_invariant_func)
        return _mo.Set((_mo.Couplet(label, _mo.Multiset(counter, direct_load=True)
                .cache_multiclan(set_or_mset.cached_multiclan), direct_load=True)
            for label, counter in partition_dict.items()), direct_load=True)
    else:
        raise AssertionError('First argument must be Set or Multiset')
