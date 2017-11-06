r"""This package contains the modules that define the classes that represent data.

The modules that contain classes that represent data are:

-   :mod:`~.mathobject`: Contains the abstract base class :class:`~.MathObject`. It is the base
    class of all other data classes and can't be instantiated.

    It also provides the utility functions :func:`~.raise_if_not_mathobject` and
    :func:`~.raise_if_not_mathobjects` that raise a `TypeError` if the argument is not an instance
    of :class:`~.MathObject` (resp. is not a collection of such instances).

-   :mod:`~.atom`: Contains the class :class:`~.Atom`. Instances of this class represent
    :term:`atom`\s; that is, values of non-math objects, like numbers, strings or any immutable
    Python value. All instances of :class:`~.Atom` are members of :term:`set A` (:math:`A`), or
    conversely, :term:`set A` is the set of all instances of :class:`~.Atom`.

    It also provides the utility function :func:`~.auto_convert` that makes sure that its argument
    is always an instance of :class:`~.MathObject`; if it isn't, it converts it into an
    :class:`~.Atom`.

-   :mod:`~.couplet`: Contains the class :class:`~.Couplet` that represents a :term:`couplet`.

-   :mod:`~.set`: Contains the class :class:`~.Set` that represents a :term:`set`.

-   :mod:`~.multiset`: Contains the class :class:`~.Multiset` that represents a :term:`multiset`.

-   :mod:`~.utils`: Provides various utilities for the other modules in this package.

In addition to the modules with classes that represent data, there is a private module
``_flags``. It contains the class ``_flags.Flags`` that provides a mechanism to cache
certain properties of :class:`~.MathObject`\s. It is used by property accessors like
:attr:`~.MathObject.cached_relation` and is not meant to be used by itself. (See also
[PropCache]_.)

All module-level symbols (functions and classes, except ``_flags.Flags``) are exposed at the
package level, so if you ``import mathobjects`` (the package), these module-level symbols are
imported. (Similarly, ``from mathobjects import ...`` can be used to import individual symbols
from the package.)
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

# These statements make the imported classes directly available after importing mathobjects.
from .atom import Atom, auto_convert
from .couplet import Couplet, make_couplet, make_couplet_unchecked
from .mathobject import MathObject, is_mathobject_or_undef, raise_if_not_mathobject, \
    raise_if_not_mathobjects
from .multiset import Multiset
from .set import Set, make_set, make_set_unchecked
