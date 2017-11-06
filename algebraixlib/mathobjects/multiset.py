"""Provide the class :class:`~.Multiset`; it represents a :term:`multiset`."""

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
import functools as _functools
import types as _types

import algebraixlib.structure as _structure
import algebraixlib.undef as _ud
import algebraixlib.util.miscellaneous as _misc

from .atom import auto_convert
from .mathobject import MathObject, raise_if_not_mathobject
from ..cache_status import CacheStatus
from ._flags import Flags as _Flags


# On-demand import 'statements' that avoid problems with circular imports.

def _multiclans():
    """Load :mod:`~.algebras.multiclans` on demand."""
    _multiclans.algebra = getattr(_multiclans, 'algebra', None)
    if _multiclans.algebra is None:
        import algebraixlib.algebras.multiclans as multiclans
        _multiclans.algebra = multiclans
    return _multiclans.algebra


# --------------------------------------------------------------------------------------------------

def _init_cache_not_empty() -> int:
    """Initialization function for `Multiset._INIT_CACHE_NOT_EMPTY` for non-empty multisets."""
    # This instance may be a multiclan.
    flags = _Flags()
    # Known to be true:
    flags.f.multiset = CacheStatus.IS
    # Known to be false:
    flags.f.atom = CacheStatus.IS_NOT
    flags.f.couplet = CacheStatus.IS_NOT
    flags.f.set = CacheStatus.IS_NOT
    flags.f.relation = CacheStatus.IS_NOT
    flags.f.clan = CacheStatus.IS_NOT
    return flags.asint


def _init_cache_empty() -> int:
    """Initialization function for `Multiset._INIT_CACHE_EMPTY` for empty multisets."""
    # These are being set at the end of the constructor. Any flags set before will be overwritten.
    flags = _Flags()
    # Known to be true:
    flags.f.multiset = CacheStatus.IS
    flags.f.multiclan = CacheStatus.IS
    flags.f.functional = CacheStatus.IS
    flags.f.right_functional = CacheStatus.IS
    flags.f.regular = CacheStatus.IS
    # These three are defined for multiclans (multisets of relations), where they inherit the
    # definition from (non-multi) relations.
    flags.f.reflexive = CacheStatus.IS
    flags.f.symmetric = CacheStatus.IS
    flags.f.transitive = CacheStatus.IS
    # Known to be false:
    flags.f.atom = CacheStatus.IS_NOT
    flags.f.couplet = CacheStatus.IS_NOT
    flags.f.set = CacheStatus.IS_NOT
    flags.f.relation = CacheStatus.IS_NOT
    flags.f.clan = CacheStatus.IS_NOT
    return flags.asint


@_functools.total_ordering
class Multiset(MathObject):
    """A :term:`multiset` consisting of zero or more different `MathObject` instances."""

    _INIT_CACHE_NOT_EMPTY = _init_cache_not_empty()
    _INIT_CACHE_EMPTY = _init_cache_empty()

    def __init__(self, *args, direct_load=False):
        """
        :param args: Zero or more unnamed arguments that are placed into the created ``Multiset``.
            If you want to pass in an iterable, you need to prefix it with an asterisk ``*``. If
            no argument is given or the given iterable is empty, an empty :term:`multiset` is
            created. (A Python string of type ``str`` is an iterable, but it is considered a
            single, non-iterable argument.) Arguments of type :class:`~collections.Counter` are
            loaded directly, and arguments of type `dict` must map values or instances of
            `MathObject` to integers; the integers are interpreted as multiplicity values for the
            given keys. (In order to create a ``Multiset`` that contains a ``Counter`` or `dict`,
            put the ``Counter`` or `dict` in an :class:`~.Atom` or an array first.)
        :param direct_load: (Optional) Set to ``True`` if you know that all arguments (or all
            elements of the iterable) are instances of `MathObject`.
        """
        super().__init__(self._INIT_CACHE_NOT_EMPTY)
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
            # Strings are iterable, but we treat them as a single value in this case.
            self._data = _collections.Counter({auto_convert(elements): 1})
        elif isinstance(elements, _collections.Iterable) and not isinstance(elements, MathObject):
            # An Iterable (that is not a Multiset, Counter or dict) as argument: create a Multiset
            # with all elements.
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
        if self.is_empty:
            self._flags.asint = self._INIT_CACHE_EMPTY

    # ----------------------------------------------------------------------------------------------
    # Characteristics of the instance.

    @property
    def data(self) -> _collections.Counter:
        """Read-only; return the elements of this instance as a :class:`~collections.Counter` of
        `MathObject` instances.

        .. note:: Even though the returned data is a `dict` and can be modified, this should be
            avoided if at all possible, and if needed, it should be done with care. It may only be
            done as long as the instance has not been read by code other than the modifying code,
            and as long as the hash has not yet been calculated. Modifying the data must follow the
            'as-if' rule: the modification must be done in a way as if the instance were
            immutable (for all relevant purposes).
        """
        return self._data

    @property
    def cardinality(self) -> int:
        """Read-only; return the number of elements in the :term:`multiset`."""
        return sum(self._data.values())

    @property
    def is_empty(self) -> bool:
        """Return ``True`` if this :term:`multiset` is empty, ``False`` if not."""
        return not self._data

    def has_element(self, elem: MathObject) -> bool:
        """Return whether ``elem`` is an element of this multiset. ``elem`` must be a `MathObject`.

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
        """Return the :term:`ground set` of the lowest-level algebra of this :class:`Multiset`."""
        if len(self.data) == 0:
            return _structure.Structure()

        elements_ground_set = _structure.Union(elem.get_ground_set() for elem in self.data)
        if len(elements_ground_set.data) == 1:
            return _structure.PowerSet(_structure.CartesianProduct(
                _misc.get_single_iter_elem(elements_ground_set.data), _structure.GenesisSetN()))
        else:
            return _structure.PowerSet(_structure.CartesianProduct(
                elements_ground_set, _structure.GenesisSetN()))

    def get_left_set(self) -> 'P( M )':
        """Get the :term:`left set` for this :class:`Multiset`. Return `Undef()` if not
        applicable.

        .. todo:: Once multipowersets are fully implemented,
            see :meth:`~algebraixlib.mathobjects.set.Set.get_left_set`.
        """
        if _multiclans().is_member(self):
            return _multiclans().get_lefts(self, _checked=False)
        return _ud.make_or_raise_undef()

    def get_right_set(self) -> 'P( M )':
        """Get the :term:`right set` for this :class:`Multiset`. Return `Undef()` if not
        applicable.

        .. todo:: Once multipowersets are fully implemented,
            see :meth:`~algebraixlib.mathobjects.set.Set.get_right_set`.
        """
        if _multiclans().is_member(self):
            return _multiclans().get_rights(self, _checked=False)
        return _ud.make_or_raise_undef()

    # ----------------------------------------------------------------------------------------------
    # (Python-)Special functions.

    def __eq__(self, other):
        """Implement value-based equality. Return ``True`` if type and data match."""
        return isinstance(other, Multiset) and (self.data == other.data)

    def __ne__(self, other):
        """Implement value-based inequality. Return ``True`` if type or data don't match."""
        return not isinstance(other, Multiset) or (self.data != other.data)

    def __lt__(self, other):
        """A value-based comparison for less than. Return ``True`` if ``self < other``.

        This implementation must be aligned with `__eq__`; an object must not be equal to and less
        than another object at the same time.

        :return Normally a `bool` (`True` if ``self`` is less than ``other``), or `NotImplemented`
            if the types can't be compared.
        """
        if not isinstance(other, MathObject):
            return NotImplemented
        if other.is_multiset:
            return repr(self) < repr(other)
        else:
            return super()._less_than(other)

    def __contains__(self, item):
        """Return ``True`` if ``item`` is a member of this multiset. If ``item`` is not a
        `MathObject`, it is converted into an :class:`~.Atom`.

        This allows Boolean expressions of the form ``element in Multiset``.
        """
        return auto_convert(item) in self.data

    def __iter__(self):
        """Iterate over the elements of this instance in no particular order. Elements are iterated
        over according to their multiplicities."""
        for value in self._data.elements():
            yield value

    def __len__(self):
        """Return the cardinality of this multiset, considering multiplicities."""
        return sum(self._data.values())

    def __hash__(self):
        """Return a hash based on the value that is calculated on demand and cached."""
        if not self._hash:
            counter_parts = self.data.items()
            multiset_parts = ['algebraixlib.mathobjects.multiset.Multiset']
            # noinspection PyTypeChecker
            multiset_parts.extend(counter_parts)
            self._hash = _misc.get_hash(*multiset_parts)
        return self._hash

    def __repr__(self):
        """Return the instance's code representation."""
        return 'Multiset({{{0}}})'.format(', '.join(
            repr(key) + ': ' + repr(value) for key, value in sorted(self.data.items())))

    def __str__(self):
        """Return the instance's string representation."""
        return '[{elems}]'.format(elems=', '.join(
            str(key) + ':' + str(value) for key, value in sorted(self._data.items())))

    # __getitem__ mechanism for indexing syntax `mo[left]`. ----------------------------------------

    def _getitem(self, left):
        """The initial function assigned to ``_getitem_redirect``. Determine whether ``self`` is a
        multirelation, set ``_getitem_redirect`` accordingly and return the appropriate
        result."""
        def is_multirelation():  # pylint: disable=missing-docstring
            for elem in self.data.keys():
                if not elem.is_couplet:
                    return False
            return True

        # The re-assignment of _getitem_redirect is at instance level; use types.MethodType.
        if is_multirelation():
            self._getitem_redirect = _types.MethodType(Multiset._getitem_multirelation, self)
        elif _multiclans().is_member(self):
            self._getitem_redirect = _types.MethodType(Multiset._getitem_multiclan, self)
        else:
            self._getitem_redirect = _types.MethodType(Multiset._getitem_undef, self)
        return self._getitem_redirect(left)

    def _getitem_multiclan(self, left):
        """Return a multiset with the rights of all the couplets in all relations that have a
        left of ``left``."""
        result = Multiset()
        for rel in self:
            rel_result = rel[left]
            if rel_result is not _ud.Undef():
                result.data.update(rel_result)
        return result

    def _getitem_multirelation(self, left):
        """Return a multiset with the rights of all the couplets that have a left of ``left``."""
        left_mo = auto_convert(left)

        def _sum_same_left_relations(left_mo_):  # pylint: disable=missing-docstring
            return_count = _collections.Counter()
            for elem, multi in self.data.items():
                if elem.left == left_mo_:
                    return_count[elem.right] = multi
            return return_count

        return Multiset(_sum_same_left_relations(left_mo), direct_load=True)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def _getitem_undef(self, left):  # pylint: disable=unused-argument, no-self-use
        """Return ``Undef()``. Used for ``self``s that are neither relations nor clans."""
        return _ud.Undef()

    #: The private member that stores the currently active function. This is used to cache the
    #: information whether ``self`` is a multirelation or not.
    _getitem_redirect = _getitem

    def __getitem__(self, left):
        r"""With the syntax ``mo[left]``, return a set of rights associated with ``left``.

        :param left: The :term:`left component` of the :term:`couplet`\(s) of which the
            :term:`right component`\(s) are returned.
        :return: If ``self`` is a multi-relation, return a :term:`multiset` that contains the
            right(s) of the :term:`couplet`\(s) that have a left component that matches ``left``.
            (The returned multiset may be empty if no couplet with the given left exists.)
            Return `Undef()` if ``self`` is not a multi-relation.
        """
        return self._getitem_redirect(left)
