"""A math object that represents a set."""

# $Id: set.py 22614 2015-07-15 18:14:53Z gfiedler $
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
from algebraixlib.mathobjects import auto_convert, Couplet, MathObject, raise_if_not_mathobject


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


class Set(MathObject):
    """A :term:`set` consisting of zero or more different `MathObject` instances."""

    def __init__(self, *args, direct_load=False):
        """Construct a :class:`Set` from a single `MathObject` or value or an iterable collection of
         such.

        :param args: Zero or more unnamed arguments that are placed into the created set.
        :param direct_load: Flag they allows bypassing the normal auto-converting of elements.
            The elements must all be instances of `MathObject`.

        If no argument is given or the given iterable is empty, an empty set is created.

        .. note:: A string is an iterable, so an explicit conversion to an :class:`~.Atom` (or
            wrapping it into brackets or braces) is required for multi-character strings.
        """
        super().__init__()
        elements = args[0] if len(args) == 1 else args

        # Normally load an argument. May come from 'elements' or from unnamed arguments.
        if isinstance(elements, Set):
            # A Set as argument: create a Set that contains a Set.
            self._data = frozenset({elements})
        elif isinstance(elements, str):
            # Strings are iterable, but that is undesired behaviour in this instance
            self._data = frozenset({auto_convert(elements)})
        elif isinstance(elements, _collections.Iterable) and not isinstance(elements, MathObject):
            # An Iterable (that is not a MathObject) as argument: create a Set with all elements.
            if direct_load:
                self._data = frozenset(elements)
            else:
                self._data = frozenset(auto_convert(element) for element in elements)
        else:
            # Anything else as argument: create a set with a single element.
            if direct_load:
                self._data = frozenset({elements})
            else:
                self._data = frozenset({auto_convert(elements)})
        self._hash = 0
        if self.is_empty:
            self.cache_is_clan(True).cache_is_relation(True).cache_is_left_functional(True).\
                cache_is_left_regular(True)
        self.cache_is_multiclan(False)

    @property
    def data(self) -> frozenset:
        """Read-only; return the elements of this instance as a `frozenset` of `MathObject`
        instances.
        """
        return self._data

    @property
    def cardinality(self) -> int:
        """Read-only; return the number of elements in the set."""
        return len(self)

    @property
    def is_empty(self) -> bool:
        """Return ``True`` if this set is empty."""
        return not self._data

    def has_element(self, elem: MathObject) -> bool:
        """Return ``True`` if ``elem`` is an element of this set. ``elem`` must be a `MathObject`.

        For a more relaxed version (that auto-converts non-`MathObject` arguments into instances of
        :class:`~.Atom`) see `__contains__` and the construct ``elem in Set``.
        """
        raise_if_not_mathobject(elem)
        return elem in self.data

    def get_ground_set(self) -> _structure.Structure:
        """Return the ground set of the lowest-level algebra of this :class:`Set`."""
        if len(self.data) == 0:
            return _structure.Structure()
        elements_ground_set = _structure.Union(elem.get_ground_set() for elem in self.data)
        if len(elements_ground_set.data) == 1:
            return _structure.PowerSet(_get_single_iter_elem(elements_ground_set.data))
        else:
            return _structure.PowerSet(elements_ground_set)

    def get_left_set(self) -> 'P( A )':
        """Get the left set for this :class:`Set`. Return `Undef` if not applicable."""
        if _relations().is_member(self):
            return _relations().get_lefts(self, _checked=False)
        if self.get_ground_set().get_powerset_level(_relations().get_ground_set()) > 0:
            _itr = iter(self)
            left_set = next(_itr).get_left_set()
            for e in _itr:
                left_set = _sets().union(e.get_left_set(), left_set, _checked=False)
            return left_set

        return _ud.make_or_raise_undef()

    def get_right_set(self) -> 'P( A )':
        """Get the right set for this :class:`Set`. Return `Undef` if not applicable."""
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
        """Execute ``method_name`` on all elements of this :class:`Set` if it is element of an n-th
        power set of ``ground_set``.

        :param ground_set: The ground set of which this :class:`Set` should be part of (at the n-th
            power set level).
        :param method_name: A member function that should be run on all elements in this
            :class:`Set`.
        :return: ``True`` if this instance is element of an n-th power set of ``ground_set`` and all
            set elements return ``True`` for ``method_name``.
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

    def is_left_regular(self) -> bool:
        """Return ``True`` if this :class:`Set` is left-regular. Return `Undef` if not
        applicable."""
        if self.cached_is_left_regular or self.cached_is_not_left_regular:
            return self.cached_is_left_regular
        if _clans().is_member(self):
            return _clans().is_left_regular(self, _checked=False)

        regular = False if self.cached_is_not_left_functional else self._is_powerset_property(
            _clans().get_ground_set(), 'is_left_regular')
        if regular is not _ud.Undef():
            self.cache_is_left_regular(regular)
            return regular
        return _ud.make_or_raise_undef(2)

    def is_left_functional(self) -> bool:
        """Return ``True`` if this :class:`Set` is left-functional. Return `Undef` if not
        applicable."""
        if self.cached_is_left_functional or self.cached_is_not_left_functional:
            return self.cached_is_left_functional
        if _relations().is_member(self):
            return _relations().is_left_functional(self, _checked=False)

        functional = self._is_powerset_property(_relations().get_ground_set(), 'is_left_functional')
        if functional is not _ud.Undef():
            self.cache_is_left_functional(functional)
            return functional

        return _ud.make_or_raise_undef(2)

    def is_right_functional(self) -> bool:
        """Return ``True`` if this :class:`Set` is right-functional. Return `Undef` if not
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

    def is_bijection(self) -> bool:
        """Return ``True`` if this :class:`Set` is both left and right-functional. Return
        `Undef` if not applicable."""
        if ((self.cached_is_left_functional or self.cached_is_not_left_functional) and
                (self.cached_is_right_functional or self.cached_is_not_right_functional)):
            return self.cached_is_left_functional and self.cached_is_right_functional
        sf = self.is_left_functional()
        if sf is not _ud.Undef():
            # If the left functional check did not return Undef, the right functional won't either.
            if not sf:
                return False
            cf = self.is_right_functional()
            if cf is not _ud.Undef():
                return cf and sf
        return _ud.make_or_raise_undef(2)

    def is_reflexive(self) -> bool:
        """Return ``True`` if this :class:`Set` is reflexive. Return `Undef` if not applicable."""
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
        """Return ``True`` if this :class:`Set` is symmetric. Return `Undef` if not applicable."""
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
        """Return ``True`` if this :class:`Set` is transitive. Return `Undef` if not applicable."""
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
        """Return ``True`` if this :class:`Set` is reflexive, symmetric, and transitive. Return
        `Undef` if not applicable."""
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

    def get_repr(self) -> str:
        """Return the instance's code representation."""
        return 'Set({0})'.format(', '.join(repr(elem) for elem in sorted(self.data)))

    def get_str(self) -> str:
        """Return the instance's string representation."""
        return '{{{0}}}'.format(', '.join(str(elem) for elem in sorted(self.data)))

    # ----------------------------------------------------------------------------------------------
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

        This allows Boolean expressions of the form ``element in set``.
        """
        return auto_convert(item) in self.data

    def __iter__(self):
        """Iterate over the elements of this instance in no particular order."""
        for each in self._data:
            yield each

    def __len__(self):
        """Return the cardinality of this set."""
        return len(self._data)

    def _call(self, left):
        if _relations().is_member(self) and _relations().is_left_functional(self, _checked=False):
            self._call_redirect = _types.MethodType(Set._call_function, self)
        else:
            self._call_redirect = _types.MethodType(Set._call_undef, self)
        return self._call_redirect(left)

    def _call_function(self, left):
        def get_right():
            left_mo = auto_convert(left)
            for elem in self:
                if elem.left == left_mo:
                    return elem.right
            return _ud.make_or_raise_undef(2)
        return get_right()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def _call_undef(self, left):
        return _ud.Undef()

    _call_redirect = _call

    def __call__(self, *args, **kwargs) -> '( M )':
        """With the syntax ``mo(left)``, return the right associated with ``left``.

        :param args: Exactly one argument is expected; it is the :term:`left` of the
            :term:`couplet` of which the :term:`right` is returned.
        :param kwargs: Named arguments are not supported.
        :return: If ``self`` is a :term:`left-functional` :term:`relation`, return the right
            of the couplet that has as left the single argument if one exists; return `Undef()` if
            no couplet with the given left exists. Also return `Undef()` if ``self`` is not a
            left-functional relation.
        """
        assert len(args) == 1
        assert len(kwargs) == 0
        return self._call_redirect(args[0])

    def _getitem(self, left):
        # The re-assignment of _getitem_redirect is at instance level; use types.MethodType.
        if _relations().is_member(self):
            self._getitem_redirect = _types.MethodType(Set._getitem_relation, self)
        elif _clans().is_member(self):
            self._getitem_redirect = _types.MethodType(Set._getitem_clan, self)
        else:
            self._getitem_redirect = _types.MethodType(Set._getitem_undef, self)
        return self._getitem_redirect(left)

    def _getitem_relation(self, left):
        left_mo = auto_convert(left)
        return Set((elem.right for elem in self if elem.left == left_mo), direct_load=True)

    def _getitem_clan(self, left):
        result = Set()
        for rel in self:
            rel_result = rel[left]
            if rel_result is not _ud.Undef():
                result = Set(result.data.union(rel_result.data), direct_load=True)
        return result

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def _getitem_undef(self, left):
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
            self._hash = _get_hash('algebraixlib.mathobjects.set.Set', self.data)
        return self._hash

    def __repr__(self):
        """Return the instance's code representation."""
        return self.get_repr()

    __str = None

    def __str__(self):
        """Return the instance's string representation."""
        return self.get_str()

    def cache_is_relation(self, value: bool):
        if value:
            assert not self.cached_is_clan or self.is_empty
            assert not self.cached_is_multiclan
            if value and not self.is_empty:
                self.cache_is_clan(False)
            self.cache_is_multiclan(False)
        self._flags.relation = value
        return self

    def cache_is_clan(self, value: bool):
        if value:
            assert not self.cached_is_relation or self.is_empty
            assert not self.cached_is_multiclan
            if value and not self.is_empty:
                self.cache_is_relation(False)
            self.cache_is_multiclan(False)
        self._flags.clan = value
        return self

    def cache_is_left_functional(self, value: bool):
        self._flags.left_functional = value
        return self

    def cache_is_right_functional(self, value: bool):
        self._flags.right_functional = value
        return self

    def cache_is_left_regular(self, value: bool):
        self._flags.left_regular = value
        return self

    def cache_is_reflexive(self, value: bool):
        self._flags.reflexive = value
        return self

    def cache_is_symmetric(self, value: bool):
        self._flags.symmetric = value
        return self

    def cache_is_transitive(self, value: bool):
        self._flags.transitive = value
        return self
