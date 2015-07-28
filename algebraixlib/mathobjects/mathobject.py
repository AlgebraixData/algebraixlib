"""This module contains the abstract base class for all classes that represent data.

The class :class:`~.MathObject` is the base class of all other data classes and can't be
instantiated.

This module also provides the utility functions :func:`~.raise_if_not_mathobject` and
:func:`~.raise_if_not_mathobjects` that raise a `TypeError` if the argument is not an instance
of :class:`~.MathObject` (resp. is not a collection of such instances).
"""

# $Id: mathobject.py 22702 2015-07-28 20:20:56Z jaustell $
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
import abc as _abc

import algebraixlib.structure as _structure
from algebraixlib.undef import make_or_raise_undef as _make_or_raise_undef

# noinspection PyProtectedMember
from algebraixlib.mathobjects._flags import Flags as _Flags


# --------------------------------------------------------------------------------------------------

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


# --------------------------------------------------------------------------------------------------

class MathObject(_abc.ABC):
    """An abstract base class (see the base class `abc.ABC`) for all classes that represent data.

    This class uses ``_flags.Flags`` to cache a number of properties of all data classes. See also
    [PropCache]_.

    .. note:: This class can't be instantiated. Only derived classes that implement all abstract
        methods can be instantiated. Since derived classes are expected to be hashable, they must
        be immutable.

    .. [PropCache]
        Several Boolean properties are automatically cached when first requested. For this we use
        a caching mechanism based on the class ``_flags.Flags`` that provides two flags for each
        Boolean property: one that indicates whether the property is "known to be true", and one
        that indicates whether it is "known to be false". Both flags are initially cleared. When the
        property is read and the value is not yet known, it is calculated and then cached. The flags
        may also be set by an explicit setter function.

        Each cached property is represented by three accessor functions that use the following
        naming convention (for a property with name ``<property>``):

        -   ``cached_is_<property>``: Return the "known to be true" flag. A ``True`` value
            means that the property is known to be ``True``. A ``False`` value means that either
            the value of the property is ``False`` or not known. In this case you need to examine
            the value of the ``cached_is_not_<property>`` accessor to find out.
        -   ``cached_is_not_<property>``: Return the "known to be false" flag. A ``True`` value
            means that the property is known to be ``False``. A ``False`` value means that either
            the value of the property is ``True`` or not known. In this case you need to examine
            the value of the ``cached_is_<property>`` accessor to find out.
        -   ``cache_is_<property>``: Set the value of one of the cache flags, depending on the
            Boolean argument ``value``. If ``value`` is ``False``, the "is known to be false"
            flag is set; if it is ``True``, the "is known to be true" flag is set. Use this
            function if you know the state of one of these properties when creating a
            :class:`~.MathObject`. (The flag setters in ``_flags.Flags`` assert that an already
            cached property isn't set to a different value.)

        :class:`~.MathObject` provides a default implementation for these methods. The
        implementations of ``cache_is_<property>`` only allow the "is known to be false" flag to be
        set. This works for derived classes for which a given property is always false. Derived
        classes for which a given property may be true must provide their own implementations of
        ``cache_is_<property>`` (see for example :meth:`.Set.cache_is_relation`).
    """
    def __init__(self):
        self._flags = _Flags()

    # ----------------------------------------------------------------------------------------------
    # Characteristics of the instance.

    @_abc.abstractmethod
    def get_ground_set(self) -> _structure.Structure:
        """Return the :term:`ground set` of the lowest-level :term:`algebra` of this
        `MathObject`."""

    def get_left_set(self) -> 'P( M )':
        """Return the :term:`left set` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def get_right_set(self) -> 'P( M )':
        """Return the :term:`right set` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def is_regular(self) -> bool:
        """Return whether ``self`` is :term:`regular` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def is_functional(self) -> bool:
        """Return whether ``self`` is :term:`functional` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def is_right_functional(self) -> bool:
        """Return whether ``self`` is :term:`right-functional` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def is_bijective(self) -> bool:
        """Return whether ``self`` is :term:`bijective` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def is_reflexive(self) -> bool:
        """Return whether ``self`` is :term:`reflexive` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def is_symmetric(self) -> bool:
        """Return whether ``self`` is :term:`symmetric` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def is_transitive(self) -> bool:
        """Return whether ``self`` is :term:`transitive` or `Undef()` if not applicable."""
        return _make_or_raise_undef()

    def is_equivalence_relation(self) -> bool:
        """Return whether ``self`` is an :term:`equivalence relation` or `Undef()` if not
        applicable.
        """
        return _make_or_raise_undef()

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
        return _make_or_raise_undef()

    def __getitem__(self, left) -> 'P( M )':
        r"""With the syntax ``mo[left]``, return a set of rights associated with ``left``.

        :param left: The :term:`left component` of the :term:`couplet`\(s) of which the
            :term:`right component`\(s) are returned.
        :return: If ``self`` is a :term:`relation`, return a :term:`set` that contains the
            right(s) of the couplet(s) that have a left that matches ``left``. (This set may
            be empty if no couplet with the given left exists.) Return `Undef()` if ``self`` is not
            a relation.
        """
        return _make_or_raise_undef()

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

    @property
    def cached_is_not_relation(self) -> bool:
        """Return ``True`` if ``self`` is known to not be a :term:`relation`. See [PropCache]_."""
        return self._flags.not_relation

    @property
    def cached_is_relation(self) -> bool:
        """Return ``True`` if ``self`` is known to be a :term:`relation`. See [PropCache]_."""
        return self._flags.relation

    def cache_is_relation(self, value: bool):
        """Cache whether ``self`` is or is not a :term:`relation`. See [PropCache]_."""
        self._flags.relation = value
        return self

    @property
    def cached_is_not_clan(self) -> bool:
        """Return ``True`` if ``self`` is known to not be a :term:`clan`. See [PropCache]_."""
        return self._flags.not_clan

    @property
    def cached_is_clan(self) -> bool:
        """Return ``True`` if ``self`` is known to be a :term:`clan`. See [PropCache]_."""
        return self._flags.clan

    def cache_is_clan(self, value: bool):
        """Cache whether ``self`` is or is not a :term:`clan`. See [PropCache]_."""
        self._flags.clan = value
        return self

    @property
    def cached_is_not_multiclan(self) -> bool:
        """Return ``True`` if ``self`` is known to not be a :term:`multiclan`. See [PropCache]_."""
        return self._flags.not_multiclan

    @property
    def cached_is_multiclan(self) -> bool:
        """Return ``True`` if ``self`` is known to be a :term:`multiclan`. See [PropCache]_."""
        return self._flags.multiclan

    def cache_is_multiclan(self, value: bool):
        """Cache whether ``self`` is or is not a :term:`multiclan`. See [PropCache]_."""
        self._flags.multiclan = value
        return self

    @property
    def cached_is_not_functional(self) -> bool:
        """Return ``True`` if ``self`` is known to not be :term:`functional`. See [PropCache]_."""
        return self._flags.not_functional

    @property
    def cached_is_functional(self) -> bool:
        """Return ``True`` if ``self`` is known to be :term:`functional`. See [PropCache]_."""
        return self._flags.functional

    def cache_is_functional(self, value: bool):
        """Cache whether ``self`` is or is not :term:`functional`. See [PropCache]_.

        This function shouldn't be called. Override in a derived class where it applies.
        """
        raise Exception("Property not supported for type %s" % type(self))

    @property
    def cached_is_not_right_functional(self) -> bool:
        """Return ``True`` if ``self`` is known to not be :term:`right-functional`. See
        [PropCache]_.
        """
        return self._flags.not_right_functional

    @property
    def cached_is_right_functional(self) -> bool:
        """Return ``True`` if ``self`` is known to be :term:`right-functional`. See [PropCache]_."""
        return self._flags.right_functional

    def cache_is_right_functional(self, value: bool):
        """Cache whether ``self`` is or is not a :term:`right-functional`. See [PropCache]_.

        This function shouldn't be called. Override in a derived class where it applies.
        """
        raise Exception("Property not supported for type %s" % type(self))

    @property
    def cached_is_not_regular(self) -> bool:
        """Return ``True`` if ``self`` is known to not be :term:`regular`. See [PropCache]_."""
        return self._flags.not_regular

    @property
    def cached_is_regular(self) -> bool:
        """Return ``True`` if ``self`` is known to be :term:`regular`. See [PropCache]_."""
        return self._flags.regular

    def cache_is_regular(self, value: bool):
        """Cache whether ``self`` is or is not :term:`regular`. See [PropCache]_.

        This function shouldn't be called. Override in a derived class where it applies.
        """
        raise Exception("Property not supported for type %s" % type(self))

    @property
    def cached_is_not_reflexive(self) -> bool:
        """Return ``True`` if ``self`` is known to not be :term:`reflexive`. See [PropCache]_."""
        return self._flags.not_reflexive

    @property
    def cached_is_reflexive(self) -> bool:
        """Return ``True`` if ``self`` is known to be :term:`reflexive`. See [PropCache]_."""
        return self._flags.reflexive

    def cache_is_reflexive(self, value: bool):
        """Cache whether ``self`` is or is not :term:`reflexive`. See [PropCache]_.

        This function shouldn't be called. Override in a derived class where it applies.
        """
        raise Exception("Property not supported for type %s" % type(self))

    @property
    def cached_is_not_symmetric(self) -> bool:
        """Return ``True`` if ``self`` is known to not be :term:`symmetric`. See [PropCache]_."""
        return self._flags.not_symmetric

    @property
    def cached_is_symmetric(self) -> bool:
        """Return ``True`` if ``self`` is known to be :term:`symmetric`. See [PropCache]_."""
        return self._flags.symmetric

    def cache_is_symmetric(self, value: bool):
        """Cache whether ``self`` is or is not :term:`symmetric`. See [PropCache]_.

        This function shouldn't be called. Override in a derived class where it applies.
        """
        raise Exception("Property not supported for type %s" % type(self))

    @property
    def cached_is_not_transitive(self) -> bool:
        """Return ``True`` if ``self`` is known to not be :term:`transitive`. See [PropCache]_."""
        return self._flags.not_transitive

    @property
    def cached_is_transitive(self) -> bool:
        """Return ``True`` if ``self`` is known to be :term:`transitive`. See [PropCache]_."""
        return self._flags.transitive

    def cache_is_transitive(self, value: bool):
        """Cache whether ``self`` is or is not :term:`transitive`. See [PropCache]_.

        This function shouldn't be called. Override in a derived class where it applies.
        """
        raise Exception("Property not supported for type %s" % type(self))

    def copy_flags(self, other):
        """Set the cached flags of ``self`` to the value of the cached flags of ``other``."""
        # noinspection PyProtectedMember
        self._flags = other._flags
        return self
