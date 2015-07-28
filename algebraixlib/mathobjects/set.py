"""Provide the class :class:`~.Set`; it represents a :term:`set`."""

# $Id: set.py 22702 2015-07-28 20:20:56Z jaustell $
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
import collections as _collections
import types as _types

import algebraixlib.structure as _structure
import algebraixlib.undef as _ud
import algebraixlib.util.miscellaneous as _misc

from algebraixlib.mathobjects.atom import auto_convert, Atom
from algebraixlib.mathobjects.mathobject import MathObject, raise_if_not_mathobject


# On-demand import 'statements' that avoid problems with circular imports.

def _couplets():
    _couplets.algebra = getattr(_couplets, 'algebra', None)
    if _couplets.algebra is None:
        import algebraixlib.algebras.couplets as couplets
        _couplets.algebra = couplets
    return _couplets.algebra


def _sets():
    _sets.algebra = getattr(_sets, 'algebra', None)
    if _sets.algebra is None:
        import algebraixlib.algebras.sets as sets
        _sets.algebra = sets
    return _sets.algebra


def _relations():
    _relations.algebra = getattr(_relations, 'algebra', None)
    if _relations.algebra is None:
        import algebraixlib.algebras.relations as relations
        _relations.algebra = relations
    return _relations.algebra


def _clans():
    _clans.algebra = getattr(_clans, 'algebra', None)
    if _clans.algebra is None:
        import algebraixlib.algebras.clans as clans
        _clans.algebra = clans
    return _clans.algebra


# --------------------------------------------------------------------------------------------------

class Set(MathObject):
    """A :term:`set` containing zero or more different `MathObject` instances."""

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
        super().__init__()
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
            self._flags._clan = True
            self._flags._relation = True
            self._flags._functional = True
            self._flags._regular = True
            self._flags._right_functional = True
            self._flags._reflexive = True
            self._flags._symmetric = True
            self._flags._transitive = True
        self._flags._not_multiclan = True

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
        """Return ``True`` if this :term:`set` is empty."""
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
            for e in _itr:
                left_set = _sets().union(e.get_left_set(), left_set, _checked=False)
            return left_set

        return _ud.make_or_raise_undef()

    def get_right_set(self) -> 'P( M )':
        """Get the :term:`right set` for this :class:`Set`. Return `Undef()` if not applicable."""
        if _relations().is_member(self):
            return _relations().get_rights(self, _checked=False)
        if self.get_ground_set().get_powerset_level(_relations().get_ground_set()) > 0:
            _itr = iter(self)
            left_set = next(_itr).get_right_set()
            for e in _itr:
                left_set = _sets().union(e.get_right_set(), left_set, _checked=False)
            return left_set

        return _ud.make_or_raise_undef(2)

    def _is_powerset_property(self, ground_set, method_name) -> bool:
        """Execute ``method_name`` on all elements of this Set if it is element of an n-th power
        set of ``ground_set``.

        :param ground_set: The ground set of which this :class:`Set` should be part of (at the n-th
            power set level).
        :param method_name: A member function that should be run on all elements in this
            :class:`Set`.
        :return: Whether this instance is element of an n-th power set of ``ground_set`` and all
            set elements return ``True`` for ``method_name``, or `Undef()` if it isn't an element
            of an n-th power set.
        """
        if self.get_ground_set().get_powerset_level(ground_set) > 0:
            result = True
            for element in self:
                res = getattr(element, method_name)()
                if res is _ud.Undef():
                    return res
                if not res:
                    return False
            return result
        return _ud.Undef()

    def is_regular(self) -> bool:
        """Return whether ``self`` is :term:`regular`. Return `Undef()` if not applicable."""
        if self.cached_is_regular or self.cached_is_not_regular:
            return self.cached_is_regular
        if _clans().is_member(self):
            return _clans().is_regular(self, _checked=False)

        regular = False if self.cached_is_not_functional else self._is_powerset_property(
            _clans().get_ground_set(), 'is_regular')
        if regular is not _ud.Undef():
            self.cache_is_regular(regular)
            return regular
        return _ud.make_or_raise_undef(2)

    def is_functional(self) -> bool:
        """Return whether ``self`` is :term:`functional`. Return `Undef()` if not applicable."""
        if self.cached_is_functional or self.cached_is_not_functional:
            return self.cached_is_functional
        if _relations().is_member(self):
            return _relations().is_functional(self, _checked=False)

        functional = self._is_powerset_property(_relations().get_ground_set(), 'is_functional')
        if functional is not _ud.Undef():
            self.cache_is_functional(functional)
            return functional

        return _ud.make_or_raise_undef(2)

    def is_right_functional(self) -> bool:
        """Return whether ``self`` is :term:`right-functional`. Return `Undef()` if not
        applicable."""
        if self.cached_is_right_functional or self.cached_is_not_right_functional:
            return self.cached_is_right_functional
        if _relations().is_member(self):
            return _relations().is_right_functional(self, _checked=False)

        functional = self._is_powerset_property(
            _relations().get_ground_set(), 'is_right_functional')
        if functional is not _ud.Undef():
            self.cache_is_right_functional(functional)
            return functional

        return _ud.make_or_raise_undef(2)

    def is_bijective(self) -> bool:
        """Return whether ``self`` is :term:`bijective`. Return `Undef()` if not applicable."""
        if ((self.cached_is_functional or self.cached_is_not_functional) and
                (self.cached_is_right_functional or self.cached_is_not_right_functional)):
            return self.cached_is_functional and self.cached_is_right_functional
        sf = self.is_functional()
        if sf is not _ud.Undef():
            # If the left-functional check did not return Undef, the right-functional won't either.
            if not sf:
                return False
            cf = self.is_right_functional()
            if cf is not _ud.Undef():
                return cf and sf
        return _ud.make_or_raise_undef(2)

    def is_reflexive(self) -> bool:
        """Return whether ``self`` is :term:`reflexive`. Return `Undef()` if not applicable."""
        if self.cached_is_reflexive or self.cached_is_not_reflexive:
            return self.cached_is_reflexive
        if _relations().is_member(self):
            return _relations().is_reflexive(self, _checked=False)

        reflexive = self._is_powerset_property(_relations().get_ground_set(), 'is_reflexive')
        if reflexive is not _ud.Undef():
            self.cache_is_reflexive(reflexive)
            return reflexive

        return _ud.make_or_raise_undef(2)

    def is_symmetric(self) -> bool:
        """Return whether ``self`` is :term:`symmetric`. Return `Undef()` if not applicable."""
        if self.cached_is_symmetric or self.cached_is_not_symmetric:
            return self.cached_is_symmetric
        if _relations().is_member(self):
            return _relations().is_symmetric(self, _checked=False)

        symmetric = self._is_powerset_property(_relations().get_ground_set(), 'is_symmetric')
        if symmetric is not _ud.Undef():
            self.cache_is_symmetric(symmetric)
            return symmetric

        return _ud.make_or_raise_undef()

    def is_transitive(self) -> bool:
        """Return whether ``self`` is :term:`transitive`. Return `Undef()` if not applicable."""
        if self.cached_is_transitive or self.cached_is_not_transitive:
            return self.cached_is_transitive
        if _relations().is_member(self):
            return _relations().is_transitive(self, _checked=False)

        transitive = self._is_powerset_property(_relations().get_ground_set(), 'is_transitive')
        if transitive is not _ud.Undef():
            self.cache_is_transitive(transitive)
            return transitive

        return _ud.make_or_raise_undef()

    def is_equivalence_relation(self) -> bool:
        """Return whether ``self`` is an :term:`equivalence relation`. Return `Undef()` if not
        applicable."""
        if ((self.cached_is_reflexive or self.cached_is_not_reflexive) and
                (self.cached_is_symmetric or self.cached_is_not_symmetric) and
                (self.cached_is_transitive or self.cached_is_not_transitive)):
            return self.cached_is_reflexive and self.cached_is_symmetric \
                and self.cached_is_transitive
        r = self.is_reflexive()
        if r is not _ud.Undef():
            s = self.is_symmetric()
            if s is not _ud.Undef():
                t = self.is_transitive()
                if t is not _ud.Undef():
                    return r and s and t
        return _ud.make_or_raise_undef()

    # ----------------------------------------------------------------------------------------------
    # (Python-)Special functions.

    def __eq__(self, other):
        """Implement value-based equality. Return ``True`` if type and set elements match."""
        return isinstance(other, Set) and (self.data == other.data)

    def __ne__(self, other):
        """Implement value-based inequality. Return ``True`` if type or set elements don't match."""
        return not isinstance(other, Set) or (self.data != other.data)

    def __lt__(self, other):
        """A value-based comparison for less than. Return ``True`` if ``self < other``."""
        return not isinstance(other, Set) or (repr(self) < repr(other))

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
        def get_right():
            left_mo = auto_convert(left)
            for elem in self:
                if elem.left == left_mo:
                    return elem.right
            return _ud.make_or_raise_undef(2)
        return get_right()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def _call_undef(self, left):
        """Return ``Undef()``. Used for ``self``s that are not functions."""
        return _ud.Undef()

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
        return Set((elem.right for elem in self if elem.left == left_mo), direct_load=True)

    def _getitem_clan(self, left):
        """Return a set with the rights of all the couplets in all relations that have a left of
        ``left``."""
        result = Set()
        for rel in self:
            rel_result = rel[left]
            if rel_result is not _ud.Undef():
                result = Set(result.data.union(rel_result.data), direct_load=True)
        return result

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def _getitem_undef(self, left):
        """Return ``Undef()``. Used for ``self``s that are neither relations nor clans."""
        return _ud.Undef()

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

    # ----------------------------------------------------------------------------------------------
    # Overrides for property cache setters that are defined in base class MathObject.

    def cache_is_relation(self, value: bool):
        """Cache whether ``self`` is or is not a :term:`relation`. See [PropCache]_."""
        if value:
            assert not self.cached_is_clan or self.is_empty
            assert not self.cached_is_multiclan
            if value and not self.is_empty:
                self.cache_is_clan(False)
        self._flags.relation = value
        return self

    def cache_is_clan(self, value: bool):
        """Cache whether ``self`` is or is not a :term:`clan`. See [PropCache]_."""
        if value:
            assert not self.cached_is_relation or self.is_empty
            assert not self.cached_is_multiclan
            if not self.is_empty:
                self.cache_is_relation(False)
        self._flags.clan = value
        return self

    def cache_is_functional(self, value: bool):
        """Cache whether ``self`` is or is not :term:`functional`. See [PropCache]_."""
        self._flags.functional = value
        return self

    def cache_is_right_functional(self, value: bool):
        """Cache whether ``self`` is or is not a :term:`right-functional`. See [PropCache]_."""
        self._flags.right_functional = value
        return self

    def cache_is_regular(self, value: bool):
        """Cache whether ``self`` is or is not :term:`regular`. See [PropCache]_."""
        self._flags.regular = value
        return self

    def cache_is_reflexive(self, value: bool):
        """Cache whether ``self`` is or is not :term:`reflexive`. See [PropCache]_."""
        self._flags.reflexive = value
        return self

    def cache_is_symmetric(self, value: bool):
        """Cache whether ``self`` is or is not :term:`symmetric`. See [PropCache]_."""
        self._flags.symmetric = value
        return self

    def cache_is_transitive(self, value: bool):
        """Cache whether ``self`` is or is not :term:`transitive`. See [PropCache]_."""
        self._flags.transitive = value
        return self
