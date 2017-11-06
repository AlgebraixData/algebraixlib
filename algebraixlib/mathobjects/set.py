r"""Provide the class :class:`~.Set`; it represents a :term:`set`."""

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
import algebraixlib.undef as _undef
import algebraixlib.util.miscellaneous as _misc
from algebraixlib.tmp_sqlda_op import tmp_sqlda_op

from .atom import auto_convert, Atom
from .mathobject import MathObject, raise_if_not_mathobject
from ..cache_status import CacheStatus
from ._flags import Flags as _Flags


# On-demand import 'statements' that avoid problems with circular imports.

def _couplets():
    """Load :mod:`~.algebras.couplets` on demand."""
    _couplets.algebra = getattr(_couplets, 'algebra', None)
    if _couplets.algebra is None:
        import algebraixlib.algebras.couplets as couplets
        _couplets.algebra = couplets
    return _couplets.algebra


def _sets():
    """Load :mod:`~.algebras.sets` on demand."""
    _sets.algebra = getattr(_sets, 'algebra', None)
    if _sets.algebra is None:
        import algebraixlib.algebras.sets as sets
        _sets.algebra = sets
    return _sets.algebra


def _relations():
    """Load :mod:`~.algebras.relations` on demand."""
    _relations.algebra = getattr(_relations, 'algebra', None)
    if _relations.algebra is None:
        import algebraixlib.algebras.relations as relations
        _relations.algebra = relations
    return _relations.algebra


def _clans():
    """Load :mod:`~.algebras.clans` on demand."""
    _clans.algebra = getattr(_clans, 'algebra', None)
    if _clans.algebra is None:
        import algebraixlib.algebras.clans as clans
        _clans.algebra = clans
    return _clans.algebra


# --------------------------------------------------------------------------------------------------

def _init_cache_not_empty() -> int:
    """Initialization function for `Set._INIT_CACHE` for non-empty sets."""
    # This instance may be a relation or clan.
    flags = _Flags()
    # Known to be true:
    flags.f.set = CacheStatus.IS
    # Known to be false:
    flags.f.atom = CacheStatus.IS_NOT
    flags.f.couplet = CacheStatus.IS_NOT
    flags.f.multiset = CacheStatus.IS_NOT
    flags.f.multiclan = CacheStatus.IS_NOT
    return flags.asint


def _init_cache_empty() -> int:
    """Initialization function for `Set._INIT_CACHE_EMPTY` for empty sets."""
    # These are being set at the end of the constructor. Any flags set before will be overwritten.
    flags = _Flags()
    # Known to be true:
    flags.f.set = CacheStatus.IS
    flags.f.clan = CacheStatus.IS
    flags.f.relation = CacheStatus.IS
    flags.f.functional = CacheStatus.IS
    flags.f.regular = CacheStatus.IS
    flags.f.right_functional = CacheStatus.IS
    flags.f.reflexive = CacheStatus.IS
    flags.f.symmetric = CacheStatus.IS
    flags.f.transitive = CacheStatus.IS
    # Known to be false:
    flags.f.atom = CacheStatus.IS_NOT
    flags.f.couplet = CacheStatus.IS_NOT
    flags.f.multiset = CacheStatus.IS_NOT
    flags.f.multiclan = CacheStatus.IS_NOT
    return flags.asint


@tmp_sqlda_op(True)
def make_set(*args):
    """Factory wrapper to create a :class:`~.Set`."""
    return Set(*(arg for arg in args if arg is not _undef.Undef()))


@tmp_sqlda_op(True)
def make_set_unchecked(*args):
    """Factory wrapper to create a :class:`~.Set` (unchecked version)."""
    return Set(*(arg for arg in args if arg is not _undef.Undef()), direct_load=True)


@_functools.total_ordering
class Set(MathObject):
    """A :term:`set` containing zero or more different `MathObject` instances."""

    _INIT_CACHE_NOT_EMPTY = _init_cache_not_empty()
    _INIT_CACHE_EMPTY = _init_cache_empty()

    def __init__(self, *args, direct_load=False):
        """
        :param args: Zero or more unnamed arguments that are placed into the created :class:`~.Set`.
            If you want to pass in an iterable, you need to prefix it with an asterisk ``*``. If
            no argument is given or the given iterable is empty, an empty :term:`set` is created.
            (A Python string of type ``str`` is an iterable, but it is considered a single,
            non-iterable argument.)
        :param direct_load: (Optional) Set to ``True`` if you know that all arguments (or all
            elements of the iterable) are instances of `MathObject`.
        """
        super().__init__(self._INIT_CACHE_NOT_EMPTY)
        elements = args[0] if len(args) == 1 else args

        # Normally load an argument. May come from 'elements' or from unnamed arguments.
        if isinstance(elements, Set):
            # A Set as argument: create a Set that contains a Set.
            self._data = frozenset({elements})
        elif isinstance(elements, str):
            # Strings are iterable, but we treat them as a single value in this case.
            self._data = frozenset({Atom(elements)})
        elif isinstance(elements, _collections.Iterable) and not isinstance(elements, MathObject):
            # An Iterable (that is not a MathObject) as argument: create a Set with all elements.
            self._data = frozenset(elements) if direct_load \
                else frozenset(auto_convert(element) for element in elements)
        else:
            # Anything else as argument: create a set with a single element.
            self._data = frozenset({elements} if direct_load else {auto_convert(elements)})

        self._hash = 0
        if self.is_empty:
            self._flags.asint = self._INIT_CACHE_EMPTY

    # ----------------------------------------------------------------------------------------------
    # Characteristics of the instance.

    @property
    def data(self) -> frozenset:
        """Read-only; return the elements of this instance as a `frozenset` of `MathObject`
        instances.
        """
        return self._data

    @property
    def cardinality(self) -> int:
        """Read-only; return the number of elements in the :term:`set`."""
        return len(self)

    @property
    def is_empty(self) -> bool:
        """Return ``True`` if this :term:`set` is empty, ``False`` if not."""
        return not self._data

    def has_element(self, elem: MathObject) -> bool:
        """Return whether ``elem`` is an element of this set. ``elem`` must be a `MathObject`.

        For a more relaxed version (that auto-converts non-`MathObject` arguments into instances of
        :class:`~.Atom`) see `__contains__` and the construct ``elem in Set``.
        """
        raise_if_not_mathobject(elem)
        return elem in self.data

    def get_ground_set(self) -> _structure.Structure:
        """Return the :term:`ground set` of the lowest-level algebra of this :class:`Set`."""
        if len(self.data) == 0:
            return _structure.Structure()
        elements_ground_set = _structure.Union(elem.get_ground_set() for elem in self.data)
        if len(elements_ground_set.data) == 1:
            return _structure.PowerSet(_misc.get_single_iter_elem(elements_ground_set.data))
        else:
            return _structure.PowerSet(elements_ground_set)

    def get_left_set(self) -> 'P( M )':
        """Get the :term:`left set` for this :class:`Set`. Return `Undef()` if not applicable."""
        if _relations().is_member(self):
            return _relations().get_lefts(self, _checked=False)
        if self.get_ground_set().get_powerset_level(_relations().get_ground_set()) > 0:
            _itr = iter(self)
            left_set = next(_itr).get_left_set()
            for elem in _itr:
                left_set = _sets().union(elem.get_left_set(), left_set, _checked=False)
            return left_set

        return _undef.make_or_raise_undef()

    def get_right_set(self) -> 'P( M )':
        """Get the :term:`right set` for this :class:`Set`. Return `Undef()` if not applicable."""
        if _relations().is_member(self):
            return _relations().get_rights(self, _checked=False)
        if self.get_ground_set().get_powerset_level(_relations().get_ground_set()) > 0:
            _itr = iter(self)
            left_set = next(_itr).get_right_set()
            for elem in _itr:
                left_set = _sets().union(elem.get_right_set(), left_set, _checked=False)
            return left_set

        return _undef.make_or_raise_undef()

    # ----------------------------------------------------------------------------------------------
    # (Python-)Special functions.

    def __eq__(self, other):
        """Implement value-based equality. Return ``True`` if type and set elements match."""
        return isinstance(other, Set) and (self.data == other.data)

    def __ne__(self, other):
        """Implement value-based inequality. Return ``True`` if type or set elements don't match."""
        return not isinstance(other, Set) or (self.data != other.data)

    def __lt__(self, other):
        """A value-based comparison for less than. Return ``True`` if ``self < other``.

        This implementation must be aligned with `__eq__`; an object must not be equal to and less
        than another object at the same time.

        :return Normally a `bool` (`True` if ``self`` is less than ``other``), or `NotImplemented`
            if the types can't be compared.
        """
        if not isinstance(other, MathObject):
            return NotImplemented
        if other.is_set:
            return repr(self) < repr(other)
        else:
            return super()._less_than(other)

    def __contains__(self, item):
        """Return ``True`` if ``item`` is a member of this set. If ``item`` is not a `MathObject`,
        it is converted into an :class:`~.Atom`.

        This allows Boolean expressions of the form ``element in Set``.
        """
        return auto_convert(item) in self.data

    def __iter__(self):
        """Iterate over the elements of this instance in no particular order."""
        for each in self._data:
            yield each

    def __len__(self):
        """Return the number of elements in (cardinality of) this set."""
        return len(self._data)

    def __hash__(self):
        """Return a hash based on the value that is calculated on demand and cached."""
        if not self._hash:
            self._hash = _misc.get_hash('algebraixlib.mathobjects.set.Set', self.data)
        return self._hash

    def __repr__(self):
        """Return the instance's code representation."""
        return 'Set({0})'.format(', '.join(repr(elem) for elem in sorted(self.data)))

    def __str__(self):
        """Return the instance's string representation."""
        return '{{{0}}}'.format(', '.join(str(elem) for elem in sorted(self.data)))

    # __call__ mechanism for function call syntax `mo(left)`. --------------------------------------

    def _call(self, left):
        """The initial function assigned to ``_call_redirect``. Determine whether ``self`` is a
        function, set ``_call_redirect`` accordingly and return the appropriate result."""
        # The re-assignment of _getitem_redirect is at instance level; use types.MethodType.
        if _relations().is_member(self) and _relations().is_functional(self, _checked=False):
            self._call_redirect = _types.MethodType(Set._call_function, self)
        else:
            self._call_redirect = _types.MethodType(Set._call_undef, self)
        return self._call_redirect(left)

    def _call_function(self, left):
        """Find a couplet with a left of ``left`` and return its right or Undef() if none found."""
        def get_right():  # pylint: disable=missing-docstring
            left_mo = auto_convert(left)
            for elem in self:
                if elem.left == left_mo:
                    return elem.right
            return _undef.make_or_raise_undef(2)
        return get_right()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def _call_undef(self, left):  # pylint: disable=unused-argument, no-self-use
        """Return ``Undef()``. Used for ``self``s that are not functions."""
        return _undef.Undef()

    #: The private member that stores the currently active function. This is used to cache the
    #: information whether ``self`` is a function or not.
    _call_redirect = _call

    def __call__(self, *args, **kwargs) -> '( M )':
        """With the syntax ``mo(left)``, return the :term:`right` associated with ``left``.

        :param args: Exactly one argument is expected; it is the :term:`left` of the
            :term:`couplet` of which the :term:`right` is returned.
        :param kwargs: Named arguments are not supported.
        :return: If ``self`` is a :term:`function`, return the :term:`right component` of the
            couplet that has as left the single argument if one exists; return `Undef()` if
            no couplet with the given left exists. Also return `Undef()` if ``self`` is not a
            function.
        """
        assert len(args) == 1
        assert len(kwargs) == 0
        return self._call_redirect(args[0])

    # __getitem__ mechanism for indexing syntax `mo[left]`. ----------------------------------------

    def _getitem(self, left):
        """The initial function assigned to ``_getitem_redirect``. Determine whether ``self`` is a
        relation or clan, set ``_getitem_redirect`` accordingly and return the appropriate
        result."""
        # The re-assignment of _getitem_redirect is at instance level; use types.MethodType.
        if _relations().is_member(self):
            self._getitem_redirect = _types.MethodType(Set._getitem_relation, self)
        elif _clans().is_member(self):
            self._getitem_redirect = _types.MethodType(Set._getitem_clan, self)
        else:
            self._getitem_redirect = _types.MethodType(Set._getitem_undef, self)
        return self._getitem_redirect(left)

    def _getitem_relation(self, left):
        """Return a set with the rights of all the couplets that have a left of ``left``."""
        left_mo = auto_convert(left)
        return _relations().get_rights_for_left(self, left_mo, _checked=False)

    def _getitem_clan(self, left):
        """Return a set with the rights of all the couplets in all relations that have a left of
        ``left``."""
        result = Set()
        for rel in self:
            rel_result = rel[left]
            if rel_result is not _undef.Undef():
                result = Set(result.data.union(rel_result.data), direct_load=True)
        return result

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def _getitem_undef(self, left):  # pylint: disable=unused-argument, no-self-use
        """Return ``Undef()``. Used for ``self``s that are neither relations nor clans."""
        return _undef.Undef()

    #: The private member that stores the currently active function. This is used to cache the
    #: information whether ``self`` is a clan, a relation or neither.
    _getitem_redirect = _getitem

    def __getitem__(self, left) -> 'P( M )':
        r"""With the syntax ``mo[left]``, return a set of rights associated with ``left``.

        :param left: The :term:`left component` of the :term:`couplet`\(s) of which the
            :term:`right component`\(s) are returned.
        :return: If ``self`` is a :term:`relation`, return a :term:`set` that contains the
            right(s) of the :term:`couplet`\(s) that have a left component that matches ``left``.
            If ``self`` is a :term:`clan`, return a set that contains the right(s) of all
            couplets in all relations that have a left component that matches ``left``. (The
            returned set may be empty if no couplet with the given left exists.) Return `Undef()`
            if ``self`` is neither a relation nor a clan.
        """
        return self._getitem_redirect(left)
