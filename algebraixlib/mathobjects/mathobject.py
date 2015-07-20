"""The abstract base class for all math objects."""

# $Id: mathobject.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import abc

import algebraixlib.structure as _structure
from algebraixlib.mathobjects.flags import Flags as _Flags
from algebraixlib.undef import make_or_raise_undef as _make_or_raise_undef


def raise_if_not_mathobject(obj):
    """Raise a `TypeError` exception if ``obj`` is not an instance of `MathObject`."""
    if not isinstance(obj, MathObject):
        raise TypeError(
            "'obj' must be instance of 'mathobjects.MathObject'. It is a {type}.".format(
                type=type(obj)))


def raise_if_not_mathobjects(*objs):
    """Raise a `TypeError` exception if any member of ``objs`` is not a `MathObject`."""
    for obj in objs:
        raise_if_not_mathobject(obj)


class MathObject(abc.ABC):
    """An abstract base class (see the base class `abc.ABC`) for all classes that represent data.

    .. note:: This class can't be instantiated. Only derived classes that implement all abstract
        methods can be instantiated. Since derived classes are expected to be hashable, they must
        be immutable.
    """
    def __init__(self):
        self._flags = _Flags()

    @abc.abstractmethod
    def get_ground_set(self) -> _structure.Structure:
        """Return the :term:`ground set` of the lowest-level :term:`algebra` of this
        `MathObject`."""

    def get_left_set(self) -> bool:
        """Return the :term:`left set` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def get_right_set(self) -> bool:
        """Return the :term:`right set` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def is_left_regular(self) -> bool:
        """Return ``True`` if :term:`left-regular` or `Undef()` if not applicable."""

    def is_left_functional(self) -> bool:
        """Return ``True`` if :term:`left-functional` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def is_right_functional(self) -> bool:
        """Return ``True`` if :term:`right-functional` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def is_bijection(self) -> bool:
        """Return ``True`` if left- and right-functional or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def is_reflexive(self) -> bool:
        """Return ``True`` if :term:`reflexive` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def is_symmetric(self) -> bool:
        """Return ``True`` if :term:`symmetric` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def is_transitive(self) -> bool:
        """Return ``True`` if :term:`transitive` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def is_equivalence_relation(self) -> bool:
        """Return ``True`` if :term:`equivalence relation` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    @abc.abstractmethod
    def get_repr(self) -> str:
        """Return the instance's code representation."""

    @abc.abstractmethod
    def get_str(self) -> str:
        """Return the instance's string representation."""

    # ----------------------------------------------------------------------------------------------

    @abc.abstractmethod
    def __eq__(self, other) -> bool:
        """Return ``True`` if ``self`` and ``other`` are equal, based on their values."""

    @abc.abstractmethod
    def __ne__(self, other) -> bool:
        """Return ``True`` if ``self`` and ``other`` are not equal, based on their values."""

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
        return _make_or_raise_undef()

    def __getitem__(self, left) -> 'P( M )':
        """With the syntax ``mo[left]``, return a set of rights associated with ``left``.

        :param left: The :term:`left` of the :term:`couplet`\(s) of which the
            :term:`right`\(s) are returned.
        :return: If ``self`` is a :term:`relation`, return a :term:`set` that contains the
            right(s) of the couplet(s) that have a left that matches ``left``. (This set may
            be empty if no couplet with the given left exists.) Return `Undef()` if ``self`` is not
            a relation.
        """
        return _make_or_raise_undef()

    @abc.abstractmethod
    def __hash__(self) -> int:
        """Return a hash based on the member values (must match the implementation of `__eq__`).

        .. note:: The fact that we calculate a hash of an instance requires that instances of
            classes derived from this class are immutable (see also `Immutable Sequence Types`_)
            and all its contained elements `hashable`_ (see also `object.__hash__`_).

        .. _object.__hash__:
            https://docs.python.org/3/reference/datamodel.html#object.__hash__
        .. _hashable:
            https://docs.python.org/3/glossary.html#term-hashable
        .. _Immutable Sequence Types:
            https://docs.python.org/3/library/stdtypes.html?immutable-sequence-types
        """

    @abc.abstractmethod
    def __repr__(self) -> str:
        """Return the instance's code representation."""

    @abc.abstractmethod
    def __str__(self) -> str:
        """Return the instance's string representation."""

    @property
    def cached_is_not_relation(self) -> bool:
        return self._flags.not_relation

    @property
    def cached_is_relation(self) -> bool:
        return self._flags.relation

    def cache_is_relation(self, value: bool):
        assert not value
        self._flags.relation = False
        return self

    @property
    def cached_is_not_clan(self) -> bool:
        return self._flags.not_clan

    @property
    def cached_is_clan(self) -> bool:
        return self._flags.clan

    def cache_is_clan(self, value: bool):
        assert not value
        self._flags.clan = False
        return self

    @property
    def cached_is_not_multiclan(self) -> bool:
        return self._flags.not_multiclan

    @property
    def cached_is_multiclan(self) -> bool:
        return self._flags.multiclan

    def cache_is_multiclan(self, value: bool):
        assert not value
        self._flags.multiclan = False
        return self

    @property
    def cached_is_not_left_functional(self) -> bool:
        return self._flags.not_left_functional

    @property
    def cached_is_left_functional(self) -> bool:
        return self._flags.left_functional

    def cache_is_left_functional(self, value: bool):
        assert not value
        self._flags.left_functional = False
        return self

    @property
    def cached_is_not_right_functional(self) -> bool:
        return self._flags.not_right_functional

    @property
    def cached_is_right_functional(self) -> bool:
        return self._flags.right_functional

    def cache_is_right_functional(self, value: bool):
        assert not value
        self._flags.right_functional = False
        return self

    @property
    def cached_is_not_left_regular(self) -> bool:
        return self._flags.not_left_regular

    @property
    def cached_is_left_regular(self) -> bool:
        return self._flags.left_regular

    def cache_is_left_regular(self, value: bool):
        assert not value
        self._flags.left_regular = False
        return self

    @property
    def cached_is_not_reflexive(self) -> bool:
        return self._flags.not_reflexive

    @property
    def cached_is_reflexive(self) -> bool:
        return self._flags.reflexive

    def cache_is_reflexive(self, value: bool):
        assert not value
        self._flags.reflexive = False
        return self

    @property
    def cached_is_not_symmetric(self) -> bool:
        return self._flags.not_symmetric

    @property
    def cached_is_symmetric(self) -> bool:
        return self._flags.symmetric

    def cache_is_symmetric(self, value: bool):
        assert not value
        self._flags.symmetric = False
        return self

    @property
    def cached_is_not_transitive(self) -> bool:
        return self._flags.not_transitive

    @property
    def cached_is_transitive(self) -> bool:
        return self._flags.transitive

    def cache_is_transitive(self, value: bool):
        assert not value
        self._flags.transitive = False
        return self
