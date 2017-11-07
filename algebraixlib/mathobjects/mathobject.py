"""This module contains the abstract base class for all classes that represent data.

The class :class:`~.MathObject` is the base class of all other data classes and can't be
instantiated.

This module also provides the utility functions :func:`~.raise_if_not_mathobject` and
:func:`~.raise_if_not_mathobjects` that raise a `TypeError` if the argument is not an instance
of :class:`~.MathObject` (resp. is not a collection of such instances).
"""

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
import abc as _abc

import algebraixlib.structure as _structure
import algebraixlib.undef as _undef

from ..cache_status import CacheStatus
from ._flags import Flags as _Flags


# --------------------------------------------------------------------------------------------------

def raise_if_not_mathobject(obj):
    """Raise a `TypeError` exception if ``obj`` is not an instance of `MathObject`."""
    if not isinstance(obj, MathObject):
        raise TypeError(
            "'obj' must be an instance of 'algebraixlib.mathobjects.MathObject'. "
            "It is a {type}.".format(type=type(obj)))


def raise_if_not_mathobjects(*objs):
    """Raise a `TypeError` exception if any member of ``objs`` is not a `MathObject`."""
    for obj in objs:
        raise_if_not_mathobject(obj)


def is_mathobject_or_undef(obj):
    """Return ``True`` if ``obj`` is  an instance of `MathObject` or `Undef()` else ``False``."""
    return isinstance(obj, MathObject) or obj is _undef.Undef()


# --------------------------------------------------------------------------------------------------

class MathObject(_abc.ABC):
    r"""An abstract base class (see the base class `abc.ABC`) for all classes that represent data.

    This class uses ``_flags.Flags`` to cache a number of properties of all data classes. See also
    [PropCache]_.

    .. note:: This class can't be instantiated. Only derived classes that implement all abstract
        methods can be instantiated. Since derived classes are expected to be hashable, they must
        be immutable.

    .. [PropCache]
        Several Boolean properties are automatically cached when first requested. For this we use
        a caching mechanism based on the class ``_flags.Flags`` that provides a 2-bit field for each
        Boolean property, with the states `UNKNOWN`, `IS`, `IS_NOT` and `N_A` (see `CacheStatus`).
        Some of these properties are set during the constructors of the classes derived from
        `MathObject`, others are set when a given `MathObject` is created by an operation. They
        also may be set by user code when a property's state is known due to the characteristics
        of the `MathObject`.

        In the `MathObject`\s, most cached properties are represented by two accessors that use the
        following naming convention (for a property with name ``<property>``):

        -   ``cached_<property>``: Return the current cached state (may be `UNKNOWN`). This is a
            Python property accessor, so parentheses are not needed when querying the state.
        -   ``cache_<property>``: Set the value of the cached state. Note that the only state that
            may be changed is `UNKNOWN`; all others cannot be changed once set. (Setting it again
            to the same value is unnecessary but not an error.)

        Several properties have also convenience accessors of the following forms:

        -   ``cached_is_<property>``: Means "is known to be <property>".
        -   ``cached_is_not_<property>``: Means "is known not to be <property>".

        (Keep in mind that while these two accessors never return ``True`` for both, they may
        return ``False`` for both. This happens if the property's state is unknown or if it
        doesn't apply to the given object. Only use them for questions of the "is known (not) to
        be ..." variety.)

        Then there are four special cases: `is_atom`, `is_couplet`, `is_multiset` and `is_set`.
        All these properties are always either ``True`` or ``False`` and they are set during
        object construction and never can be set again. Therefore, for these four properties,
        all we have are these Boolean read accessors.

        .. note:: The serialized values of the structure where these bits are stored depends on
            the system's byte order (endianness). Without specific measures, serialized data can't
            be exchanged between systems with different byte order.
    """
    # pylint: disable=too-many-public-methods
    def __init__(self, cached_flags: int=0):
        self._flags = _Flags(asint=cached_flags)

    # noinspection PyUnusedLocal
    def __deepcopy__(self, _memo):
        """Override of deepcopy to return self - all MathObjects are immutable."""
        return self

    # ----------------------------------------------------------------------------------------------
    # Characteristics of the instance.

    @property
    def is_empty(self) -> bool:  # pylint: disable=no-self-use
        """Return ``True`` if this `MathObject` is empty, ``False`` if not.

        :return: Always ``False`` unless overridden by a derived class.
        """
        return False

    @_abc.abstractmethod
    def get_ground_set(self) -> _structure.Structure:
        """Return the :term:`ground set` of the lowest-level :term:`algebra` of this
        `MathObject`."""

    def get_left_set(self) -> 'P( M )':  # pylint: disable=no-self-use
        """Return the :term:`left set` or `Undef()` if not applicable."""
        return _undef.make_or_raise_undef()

    def get_right_set(self) -> 'P( M )':  # pylint: disable=no-self-use
        """Return the :term:`right set` or `Undef()` if not applicable."""
        return _undef.make_or_raise_undef()

    # ----------------------------------------------------------------------------------------------
    # Helper functions for use in derived classes.

    def _less_than(self, other) -> bool:
        r"""Compare two `MathObject`\s of different types. They are ordered lexically by their
        type names.
        """
        assert isinstance(other, MathObject)
        assert type(self) != type(other)
        return self.__class__.__name__ < other.__class__.__name__

    # ----------------------------------------------------------------------------------------------
    # (Python-)Special functions.

    @_abc.abstractmethod
    def __eq__(self, other) -> bool:
        """Return whether ``self`` and ``other`` are equal, based on their values."""

    @_abc.abstractmethod
    def __ne__(self, other) -> bool:
        """Return whether ``self`` and ``other`` are not equal, based on their values."""

    def __call__(self, *args, **kwargs) -> '( M )':
        """With the syntax ``mo(left)``, return the right associated with ``left``.

        :param args: Exactly one argument is expected; it is the :term:`left component` of the
            :term:`couplet` of which the :term:`right component` is returned.
        :param kwargs: Named arguments are not supported. It is part of the function signature.
        :return: If ``self`` is a :term:`function`, return the :term:`right component` of the
            couplet that has as left component the single argument if one exists; return `Undef()`
            if no couplet with the given left exists. Also return `Undef()` if ``self`` is not a
            function.
        """
        return _undef.make_or_raise_undef()

    def __getitem__(self, left) -> 'P( M )':
        r"""With the syntax ``mo[left]``, return a set of rights associated with ``left``.

        :param left: The :term:`left component` of the :term:`couplet`\(s) of which the
            :term:`right component`\(s) are returned.
        :return: If ``self`` is a :term:`relation`, return a :term:`set` that contains the
            right(s) of the couplet(s) that have a left that matches ``left``. (This set may
            be empty if no couplet with the given left exists.) Return `Undef()` if ``self`` is not
            a relation.
        """
        return _undef.make_or_raise_undef()

    @_abc.abstractmethod
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

    @_abc.abstractmethod
    def __repr__(self) -> str:
        """Return the instance's code representation."""

    @_abc.abstractmethod
    def __str__(self) -> str:
        """Return the instance's string representation."""

    # ----------------------------------------------------------------------------------------------
    # Property cache functions.

    # Indicate MathObject type (2-state binary logic).

    @property
    def is_atom(self) -> bool:
        """Return ``True`` if ``self`` is an :class:`~.Atom`, ``False`` otherwise."""
        return self._flags.f.atom == CacheStatus.IS

    @property
    def is_couplet(self) -> bool:
        """Return ``True`` if ``self`` is a :class:`~.Couplet`, ``False`` otherwise."""
        return self._flags.f.couplet == CacheStatus.IS

    @property
    def is_multiset(self) -> bool:
        """Return ``True`` if ``self`` is a :class:`~.Multiset`, ``False`` otherwise."""
        return self._flags.f.multiset == CacheStatus.IS

    @property
    def is_set(self) -> bool:
        """Return ``True`` if ``self`` is a :class:`~.Set`, ``False`` otherwise."""
        return self._flags.f.set == CacheStatus.IS

    # Indicate algebra membership.

    @property
    def cached_relation(self) -> int:
        """Return the cached state of being a :term:`relation`. See [PropCache]_."""
        return self._flags.f.relation

    @property
    def cached_is_relation(self) -> bool:
        """Return ``True`` if ``self`` is known to be a :term:`relation`. See [PropCache]_."""
        return self._flags.f.relation == CacheStatus.IS

    @property
    def cached_is_not_relation(self) -> bool:
        """Return ``True`` if ``self`` is known not to be a :term:`relation`. See [PropCache]_."""
        return self._flags.f.relation == CacheStatus.IS_NOT

    def cache_relation(self, value: int):
        """Set the cached state of being a :term:`relation`. See [PropCache]_."""
        if value == CacheStatus.N_A:
            raise Exception('Cached value of "relation" may never be `N_A`.')
        elif value == CacheStatus.IS and not self.is_empty:
            assert self.cached_clan != CacheStatus.IS
            assert self.cached_multiclan != CacheStatus.IS
            self.cache_clan(CacheStatus.IS_NOT)
            self.cache_multiclan(CacheStatus.IS_NOT)
            self.cache_regular(CacheStatus.N_A)
            self.cache_right_regular(CacheStatus.N_A)
        self._flags.f.relation = value
        return self

    @property
    def cached_clan(self) -> int:
        """Return the cached state of being a :term:`clan`. See [PropCache]_."""
        return self._flags.f.clan

    @property
    def cached_is_clan(self) -> bool:
        """Return ``True`` if ``self`` is known to be a :term:`clan`. See [PropCache]_."""
        return self._flags.f.clan == CacheStatus.IS

    @property
    def cached_is_not_clan(self) -> bool:
        """Return ``True`` if ``self`` is known not to be a :term:`clan`. See [PropCache]_."""
        return self._flags.f.clan == CacheStatus.IS_NOT

    def cache_clan(self, value: int):
        """Set the cached state of being a :term:`clan`. See [PropCache]_."""
        if value == CacheStatus.N_A:
            raise Exception('Cached value of "clan" may never be `N_A`.')
        elif value == CacheStatus.IS and not self.is_empty:
            assert self.cached_relation != CacheStatus.IS
            assert self.cached_multiclan != CacheStatus.IS
            self.cache_relation(CacheStatus.IS_NOT)
        self._flags.f.clan = value
        return self

    @property
    def cached_multiclan(self) -> int:
        """Return the cached state of being a :term:`multiclan`. See [PropCache]_."""
        return self._flags.f.multiclan

    @property
    def cached_is_multiclan(self) -> bool:
        """Return ``True`` if ``self`` is known to be a :term:`multiclan`. See [PropCache]_."""
        return self._flags.f.multiclan == CacheStatus.IS

    @property
    def cached_is_not_multiclan(self) -> bool:
        """Return ``True`` if ``self`` is known not to be a :term:`multiclan`. See [PropCache]_."""
        return self._flags.f.multiclan == CacheStatus.IS_NOT

    def cache_multiclan(self, value: int):
        """Set the cached state of being a :term:`multiclan`. See [PropCache]_."""
        if value == CacheStatus.N_A:
            raise Exception('Cached value of "multiclan" may never be `N_A`.')
        self._flags.f.multiclan = value
        return self

    @property
    def cached_absolute(self) -> int:
        """Return the cached state of being :term:`absolute`. See [PropCache]_.

        .. note:: Keep in mind that this does not tell you what kind of absolute algebra member
            this is. For example, an absolute :term:`relation` is a non-absolute :term:`set`.
        """
        return self._flags.f.absolute

    @property
    def cached_is_absolute(self) -> bool:
        """Return ``True`` if ``self`` is known to be :term:`absolute`. See [PropCache]_.

        .. note:: Keep in mind that this does not tell you what kind of absolute algebra member
            this is known to be. For example, an absolute :term:`relation` is a non-absolute
            :term:`set`.
        """
        return self._flags.f.absolute == CacheStatus.IS

    @property
    def cached_is_not_absolute(self) -> bool:
        """Return ``True`` if ``self`` is known not to be :term:`absolute`. See [PropCache]_.

        .. note:: Keep in mind that this does not tell you what kind of absolute algebra member
            this is known not to be. For example, an absolute :term:`relation` is a non-absolute
            :term:`set`.
        """
        return self._flags.f.absolute == CacheStatus.IS_NOT

    def cache_absolute(self, value: int):
        """Set the cached state of being :term:`absolute`. See [PropCache]_."""
        if value == CacheStatus.N_A:
            raise Exception('Cached value of "absolute" may never be `N_A`.')
        self._flags.f.absolute = value
        return self

    # Relation properties (defined on relations, clans, multiclans).

    @property
    def cached_functional(self) -> int:
        """Return the cached state of being :term:`functional`. See [PropCache]_."""
        return self._flags.f.functional

    @property
    def cached_is_functional(self) -> bool:
        """Return ``True`` if ``self`` is known to be :term:`functional`. See [PropCache]_."""
        return self._flags.f.functional == CacheStatus.IS

    @property
    def cached_is_not_functional(self) -> bool:
        """Return ``True`` if ``self`` is known not to be :term:`functional`. See [PropCache]_."""
        return self._flags.f.functional == CacheStatus.IS_NOT

    def cache_functional(self, value: int):
        """Set the cached state of being :term:`functional`. See [PropCache]_."""
        self._flags.f.functional = value
        return self

    @property
    def cached_right_functional(self) -> int:
        """Return the cached state of being :term:`right-functional`. See [PropCache]_."""
        return self._flags.f.right_functional

    @property
    def cached_is_right_functional(self) -> bool:
        """Return ``True`` if ``self`` is known to be :term:`right-functional`. See [PropCache]_."""
        return self._flags.f.right_functional == CacheStatus.IS

    @property
    def cached_is_not_right_functional(self) -> bool:
        """Return ``True`` if ``self`` is known not to be :term:`right-functional`. See
        [PropCache]_."""
        return self._flags.f.right_functional == CacheStatus.IS_NOT

    def cache_right_functional(self, value: int):
        """Set the cached state of being :term:`right-functional`. See [PropCache]_."""
        self._flags.f.right_functional = value
        return self

    @property
    def cached_reflexive(self) -> int:
        """Return the cached state of being :term:`reflexive`. See [PropCache]_."""
        return self._flags.f.reflexive

    @property
    def cached_is_reflexive(self) -> bool:
        """Return ``True`` if ``self`` is known to be :term:`reflexive`. See [PropCache]_."""
        return self._flags.f.reflexive == CacheStatus.IS

    @property
    def cached_is_not_reflexive(self) -> bool:
        """Return ``True`` if ``self`` is known not to be :term:`reflexive`. See [PropCache]_."""
        return self._flags.f.reflexive == CacheStatus.IS_NOT

    def cache_reflexive(self, value: int):
        """Set the cached state of being :term:`reflexive`. See [PropCache]_."""
        self._flags.f.reflexive = value
        return self

    @property
    def cached_symmetric(self) -> int:
        """Return the cached state of being :term:`symmetric`. See [PropCache]_."""
        return self._flags.f.symmetric

    @property
    def cached_is_symmetric(self) -> bool:
        """Return ``True`` if ``self`` is known to be :term:`symmetric`. See [PropCache]_."""
        return self._flags.f.symmetric == CacheStatus.IS

    @property
    def cached_is_not_symmetric(self) -> bool:
        """Return ``True`` if ``self`` is known not to be :term:`symmetric`. See [PropCache]_."""
        return self._flags.f.symmetric == CacheStatus.IS_NOT

    def cache_symmetric(self, value: int):
        """Set the cached state of being :term:`symmetric`. See [PropCache]_."""
        self._flags.f.symmetric = value
        return self

    @property
    def cached_transitive(self) -> int:
        """Return the cached state of being :term:`transitive`. See [PropCache]_."""
        return self._flags.f.transitive

    @property
    def cached_is_transitive(self) -> bool:
        """Return ``True`` if ``self`` is known to be :term:`transitive`. See [PropCache]_."""
        return self._flags.f.transitive == CacheStatus.IS

    @property
    def cached_is_not_transitive(self) -> bool:
        """Return ``True`` if ``self`` is known not to be :term:`transitive`. See [PropCache]_."""
        return self._flags.f.transitive == CacheStatus.IS_NOT

    def cache_transitive(self, value: int):
        """Set the cached state of being :term:`transitive`. See [PropCache]_."""
        self._flags.f.transitive = value
        return self

    # Clan properties (defined on clans, multiclans).

    @property
    def cached_regular(self) -> int:
        """Return the cached state of being :term:`regular`. See [PropCache]_."""
        return self._flags.f.regular

    @property
    def cached_is_regular(self) -> bool:
        """Return ``True`` if ``self`` is known to be :term:`regular`. See [PropCache]_."""
        return self._flags.f.regular == CacheStatus.IS

    @property
    def cached_is_not_regular(self) -> bool:
        """Return ``True`` if ``self`` is known not to be :term:`regular`. See [PropCache]_."""
        return self._flags.f.regular == CacheStatus.IS_NOT

    def cache_regular(self, value: int):
        """Set the cached state of being :term:`regular`. See [PropCache]_."""
        self._flags.f.regular = value
        if value == CacheStatus.IS:
            self.cache_functional(CacheStatus.IS)
        return self

    @property
    def cached_right_regular(self) -> int:
        """Return the cached state of being :term:`right-regular`. See [PropCache]_."""
        return self._flags.f.right_regular

    @property
    def cached_is_right_regular(self) -> bool:
        """Return ``True`` if ``self`` is known to be :term:`right-regular`. See [PropCache]_."""
        return self._flags.f.right_regular == CacheStatus.IS

    @property
    def cached_is_not_right_regular(self) -> bool:
        """Return ``True`` if ``self`` is known not to be :term:`right-regular`. See
        [PropCache]_."""
        return self._flags.f.right_regular == CacheStatus.IS_NOT

    def cache_right_regular(self, value: int):
        """Set the cached state of being :term:`right-regular`. See [PropCache]_."""
        self._flags.f.right_regular = value
        if value == CacheStatus.IS:
            self.cache_right_functional(CacheStatus.IS)
        return self
