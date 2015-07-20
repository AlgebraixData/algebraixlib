"""A math object that represents a Multiset."""

# $Id: multiset.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import collections as _collections
import types as _types

import algebraixlib.structure as _structure
import algebraixlib.undef as _ud
from algebraixlib.util.miscellaneous import get_hash as _get_hash
from algebraixlib.util.miscellaneous import get_single_iter_elem as _get_single_iter_elem

from algebraixlib.mathobjects.atom import auto_convert
from algebraixlib.mathobjects.couplet import Couplet
from algebraixlib.mathobjects.mathobject import MathObject, raise_if_not_mathobject


def _multisets():
    _multisets.algebra = getattr(_multisets, 'algebra', None)
    if _multisets.algebra is None:
        import algebraixlib.algebras.multisets as multisets
        _multisets.algebra = multisets
    return _multisets.algebra


class Multiset(MathObject):
    """A :term:`multiset` consisting of zero or more different `MathObject` instances."""

    def __init__(self, *args, direct_load=False):
        """Construct a :class:`Multiset` from a single `MathObject` or value or an iterable collection of
         such.

        :param args: Zero or more unnamed arguments that are placed into the created Multiset.
        :param direct_load: Flag they allows bypassing the normal auto-converting of elements.
            The elements must all be instances of `MathObject`.

        The prefered argument type will be a dictionary whose keys are mapped to positive
        integers.  The keys will be auto-converted based on the direct_load parameter.

        .. note:: A string is an iterable, so an explicit conversion to an :class:`~.Atom` (or
            wrapping it into brackets or braces) is required for multi-character strings.
        """
        super().__init__()
        elements = args[0] if len(args) == 1 else args

        # Normally load an argument. May come from 'elements' or from unnamed arguments.
        if isinstance(elements, Multiset):
            # A Multiset as argument: create a Multiset that contains a Multiset.
            self._data = _collections.Counter({elements: 1})
        elif isinstance(elements, _collections.Counter) or isinstance(elements, dict):
            self._data = _collections.Counter()
            for key in elements.keys():
                if direct_load:
                    self._data[key] = elements[key]
                else:
                    # only asserting in non direct mode, assumption is direct load has good data.
                    assert isinstance(elements[key], int) and elements[key] > 0
                    self._data[auto_convert(key)] = elements[key]
        elif isinstance(elements, str):
            # Strings are iterable, but that is undesired behaviour in this instance
            self._data = _collections.Counter({auto_convert(elements): 1})
        elif isinstance(elements, _collections.Iterable) and not isinstance(elements, MathObject):
            # An Iterable (that is not a Multiset) as argument: create a Multiset with all elements.
            if direct_load:
                self._data = _collections.Counter(elements)
            else:
                self._data = _collections.Counter([auto_convert(elem) for elem in elements])
        else:
            # Anything else as argument: create a Multiset with a single element.
            if direct_load:
                self._data = _collections.Counter({elements: 1})
            else:
                self._data = _collections.Counter({auto_convert(elements): 1})
        self._hash = 0

    @property
    def data(self) -> _collections.Counter:
        """Read-only; return the elements of this instance as a :class:`~collections.Counter` of
        `MathObject` instances.
        """
        return self._data

    def is_left_regular(self) -> bool:
        """Return ``True`` if this :class:`Multiset` is left-regular. Return `Undef` if not
        applicable."""
        tmp_clan = _multisets().demultify(self)

        return tmp_clan.is_left_regular()

    @property
    def cardinality(self) -> int:
        """Read-only; return the number of elements in the ``Multiset``."""
        return sum(self._data.values())

    @property
    def is_empty(self) -> bool:
        """Return ``True`` if this ``Multiset`` is empty."""
        return not self._data

    def has_element(self, elem: MathObject) -> bool:
        """Return ``True`` if ``elem`` is an element of this ``Multiset``. ``elem`` must be a `MathObject`.

        For a more relaxed version (that auto-converts non-`MathObject` arguments into instances of
        :class:`~.Atom`) see `__contains__` and the construct ``elem in Multiset``.
        """
        raise_if_not_mathobject(elem)
        return elem in self.data

    def get_multiplicity(self, elem: MathObject) -> int:
        """Return ``int`` if ``elem`` is an element of this ``Multiset`` where the value is the
        number of multiples for ``elem``. ``elem`` must be a `MathObject`.
        """
        raise_if_not_mathobject(elem)
        return self.data[elem]

    def get_ground_set(self) -> _structure.Structure:
        """Return the ground Multiset of the lowest-level algebra of this :class:`Multiset`."""
        if len(self.data) == 0:
            return _structure.Structure()

        elements_ground_set = _structure.Union(elem.get_ground_set() for elem in self.data)
        if len(elements_ground_set.data) == 1:
            return _structure.PowerSet(_structure.CartesianProduct(
                _get_single_iter_elem(elements_ground_set.data), _structure.GenesisSetN()))
        else:
            return _structure.PowerSet(_structure.CartesianProduct(
                elements_ground_set, _structure.GenesisSetN()))

    def get_repr(self) -> str:
        """Return the instance's code representation."""
        return 'Multiset({{{0}}})'.format(', '.join(
            repr(key) + ': ' + repr(value) for key, value in sorted(self.data.items())))

    def get_str(self) -> str:
        """Return the instance's string representation."""
        return '[{elems}]'.format(elems=', '.join(
            str(key) + ':' + str(value) for key, value in sorted(self._data.items())))

    # ----------------------------------------------------------------------------------------------

    def __eq__(self, other):
        """Implement value-based equality. Return ``True`` if type and data match."""
        return isinstance(other, Multiset) and (self.data == other.data)

    def __ne__(self, other):
        """Implement value-based inequality. Return ``True`` if type or data don't match."""
        return not isinstance(other, Multiset) or (self.data != other.data)

    def __lt__(self, other):
        """A value-based comparison for less than. Return ``True`` if ``self < other``."""
        return not isinstance(other, Multiset) or (repr(self) < repr(other))

    def __contains__(self, item):
        """Return ``True`` if ``item`` is a member of this Multiset. If ``item`` is not a `MathObject`,
        it is converted into an :class:`~.Atom`.

        This allows Boolean expressions of the form ``element in Multiset``.
        """
        return auto_convert(item) in self.data

    def __iter__(self):
        """Iterate over the elements of this instance in no particular order."""
        for value in sorted(self._data.elements()):
            yield value

    def __len__(self):
        """Return the cardinality of this Multiset.

        Note that the length includes the multiplicities of the elements.  This is to keep the
        length consistent with how iteration works.
        """
        return sum(self._data.values())

    def _getitem(self, left):
        def is_multirelation():
            for elem in self.data.keys():
                if not isinstance(elem, Couplet):
                    return False
            return True

        # The re-assignment of _getitem_redirect is at instance level; use types.MethodType.
        if is_multirelation():
            self._getitem_redirect = _types.MethodType(Multiset._getitem_multirelation, self)
        else:
            self._getitem_redirect = _types.MethodType(Multiset._getitem_not_multirelation, self)
        return self._getitem_redirect(left)

    def _getitem_multirelation(self, left):
        left_mo = auto_convert(left)

        def _sum_same_left_relations(left_mo):
            return_count = _collections.Counter()
            for elem, multi in self.data.items():
                if elem.left == left_mo:
                    return_count[elem.right] = multi

            return return_count

        return Multiset(_sum_same_left_relations(left_mo), direct_load=True)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def _getitem_not_multirelation(self, left):
        return _ud.Undef()

    _getitem_redirect = _getitem

    def __getitem__(self, left):
        """With the syntax ``mo[left]``, return a set of rights associated with ``left``.

        :param left: The :term:`left` of the :term:`couplet`\(s) of which the
            :term:`right`\(s) are returned.
        :return: If ``self`` is a :term:`relation`, return a :term:`set` that contains the
            right(s) of the couplet(s) that have a left that matches ``left``. (This set may
            be empty if no couplet with the given left exists.) Return `Undef()` if ``self`` is not
            a relation.
        """
        return self._getitem_redirect(left)

    def __hash__(self):
        """Return a hash based on the value that is calculated on demand and cached."""
        if not self._hash:
            counter_parts = self.data.items()
            multiset_parts = ['algebraixlib.mathobjects.multiset.Multiset']
            # noinspection PyTypeChecker
            multiset_parts.extend(counter_parts)
            self._hash = _get_hash(*multiset_parts)
        return self._hash

    def __repr__(self):
        """Return the instance's code representation."""
        return self.get_repr()

    __str = None

    def __str__(self):
        """Return the instance's string representation."""
        return self.get_str()

    def cache_is_multiclan(self, value: bool):
        self._flags.multiclan = value
        return self
