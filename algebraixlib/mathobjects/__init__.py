"""This package contains the modules that define the classes that represent data.

The modules are:

-   :mod:`~.mathobject`: Contains the abstract base class :class:`~.MathObject`. It is the base
    class of all other data classes and can't be instantiated.
    It also provides the utility functions :func:`~.raise_if_not_mathobject` and
    :func:`~.raise_if_not_mathobjects` that raise a `TypeError` if the argument is not an instance
    of :class:`~.MathObject` (resp. is not a collection of such instances).
-   :mod:`~.atom`: Contains the class :class:`~.Atom`. Instances of this class represent
    :term:`atom`\s; that is, values (of non-math objects, like numbers, strings or any immutable
    Python value). All instances of :class:`~.Atom` are members of :term:`set A` (:math:`A`), or
    conversely, :term:`set A` is the set of all instances of :class:`~.Atom`.
    It also provides the utility function :func:`~.auto_convert` that makes sure that its argument
    is always an instance of :class:`~.MathObject`; if it isn't, it converts it into an
    :class:`~.Atom`.
-   :mod:`~.couplet`: Contains the class :class:`~.Couplet` that represents a :term:`couplet`.
-   :mod:`~.set`: Contains the class :class:`~.Set` that represents a :term:`set`.

If you ``import mathobjects`` (the package), all module-level symbols (functions, classes) are
imported.
"""

# $Id: __init__.py 22614 2015-07-15 18:14:53Z gfiedler $
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

# These statements make the imported classes directly available after importing mathobjects.
from .atom import Atom, auto_convert
from .couplet import Couplet
from .mathobject import MathObject, raise_if_not_mathobject, raise_if_not_mathobjects
from .set import Set
from .multiset import Multiset
