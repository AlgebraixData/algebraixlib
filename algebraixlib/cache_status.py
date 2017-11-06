"""Defines CacheStatus class, a quaternary-valued type used to represent several algebraic
properties (such as left-functional) that may apply to MathObjects or classes supporting the
MathObjects interface (such as Undef).
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


class CacheStatus:
    r"""Provide the 4 states that we use for caching the property values for `MathObject`\s.

    In ``_flags.Flags`` we provide 2-bit bitfields that store the cached value of properties that
    are associated with the `MathObject` instances. This class provides symbols for the values
    that we store in these bitfields and functions that work on them.

    See also [PropCache].
    """

    #: Value of the 2-bit bitfield if the associated property is unknown. When accessed, it will be
    #: evaluated and set to one of the other states. This is the only state that can change.
    #: This value is special in that it sets both bits of the 2-bit bitfield to 0. There is logic
    #: elsewhere that depends on all bits being 0 meaning 'all properties are unknown'. This is in
    #: alignment with the default state of a structure without any explicit initialization; it seems
    #: to be 'all bits 0'. (We didn't find documentation that confirms this, but it seems to be the
    #: case.)
    UNKNOWN = 0
    #: Value of the 2-bit bitfield if the associated property is known to be true. Once a bitfield
    #: is set to this state, its value cannot change anymore.
    IS = 1  # pylint: disable=invalid-name
    #: Value of the 2-bit bitfield if the associated property is known to be false. Once a bitfield
    #: is set to this state, its value cannot change anymore.
    IS_NOT = 2
    #: Value of the 2-bit bitfield if the associated property is known to be undefined (that is, it
    #: doesn't apply). For example, :term:`functional` is not defined for :term:`set`\s of
    #: :term:`atom`\s. Once a bitfield is set to this state, its value cannot change anymore. (The
    #: name ``N_A`` has been chosen instead of ``UNDEFINED`` to avoid confusion with `UNKNOWN`
    #: and to simplify working with IDEs.)
    N_A = 3

    @staticmethod
    def from_bool(bool_value: bool) -> int:
        """Return the ``CacheStatus`` value that corresponds to the Boolean ``bool_value``."""
        return CacheStatus.IS if bool_value else CacheStatus.IS_NOT

    @staticmethod
    def is_bool(cache_status: int) -> bool:
        """Return ``True`` if ``cache_status`` represents a Boolean (``IS`` or ``IS_NOT``)."""
        return cache_status == CacheStatus.IS or cache_status == CacheStatus.IS_NOT
