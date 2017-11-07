"""Testing the mathobjects.flags module."""

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
import inspect
import os
import time
import unittest
from ctypes import c_uint8

from algebraixlib.cache_status import CacheStatus
# noinspection PyProtectedMember
from algebraixlib.mathobjects._flags import Flags


# SIZE_IN_BITS is hardcoded here. There doesn't seem to be a good way to get the maximum number of
# bits in a ctypes type. This number relates to the definition of `asint` as `c_uint64`.
SIZE_IN_BITS = 32


class MathObjectFlagsTest(unittest.TestCase):
    def test_initial(self):
        union = Flags()
        self.assertEqual(len(union._fields_), 2)
        flags = union.f
        asint = union.asint
        self.assertLessEqual(len(flags._fields_), SIZE_IN_BITS / 2)  # 2 bits per bitfield.
        self.assertTrue(isinstance(asint, int))
        self.assertLessEqual(asint.bit_length(), SIZE_IN_BITS)
        for field_name, field_type, field_size in flags._fields_:
            self.assertEqual(field_type, c_uint8)
            self.assertEqual(field_size, 2)
            self.assertEqual(getattr(flags, field_name), 0)

    def test_relation(self):
        flags = Flags()
        bitfields = flags.f
        bitfields.relation = CacheStatus.IS
        self.assertEqual(bitfields.relation, CacheStatus.IS)
        flags_init = Flags(asint=flags.asint)
        bitfields_init = flags_init.f
        self.assertEqual(bitfields_init.relation, CacheStatus.IS)
        bitfields.relation = CacheStatus.IS  # No change = no problem
        bitfields_init.relation = CacheStatus.IS  # No change = no problem
        for state in [CacheStatus.UNKNOWN, CacheStatus.IS_NOT, CacheStatus.N_A]:
            self.assertRaises(AssertionError, lambda: setattr(bitfields_init, 'relation', state))
        for state in [CacheStatus.UNKNOWN, CacheStatus.IS_NOT, CacheStatus.N_A]:
            self.assertRaises(AssertionError, lambda: setattr(bitfields, 'relation', state))

    def test_clan(self):
        flags = Flags()
        flags.f.clan = CacheStatus.IS_NOT
        bitfields = Flags(asint=flags.asint).f
        self.assertEqual(bitfields.clan, CacheStatus.IS_NOT)
        bitfields.clan = CacheStatus.IS_NOT  # No change = no problem
        for state in [CacheStatus.UNKNOWN, CacheStatus.IS, CacheStatus.N_A]:
            self.assertRaises(AssertionError, lambda: setattr(bitfields, 'clan', state))

    def test_speed(self):
        # The relation property is enum-based and uses a setter helper function.
        # The clan property is int-based and uses a setter helper function.
        # The multiclan property is int-based and has the code of the setter helper function
        # directly in the setter.
        #
        # The approximate run times are (for 1e6 instances):
        #           rel (enum w/)   clan (int w/)   multiclan (int w/o)
        #   set     6.4 s           0.8 s           0.7 s
        #   get     5.3 s           1.5 s           1.5 s
        #
        # The performance difference (for int-based implementations) between using a setter helper
        # (clan) and not using it (multiclan) is minimal, and setting is rare, so I decided to
        # use a setter helper function. The performance difference between enum- and int-based
        # implementations (rel and clan) seems to be more relevant, especially since there is
        # also a hit when reading (the more frequent operation). So I decided not to use enums in
        # this interface.

        # NOTE: The actual code is not anymore like described above. In order to re-run this test,
        # the code from here must be used in _flags.py:
        #
        # class State(_enum.Enum):
        #     UNKNOWN = 0
        #     IS = 1
        #     IS_NOT = 2
        #     N_A = 3
        #
        # @staticmethod
        # def _setter_helper_enum(flags, value: State) -> int:
        #     int_val = value.value
        #     assert flags == State.UNKNOWN.value or flags == int_val
        #     assert 0 <= int_val <= 3
        #     return int_val
        #
        # @property
        # def relation(self) -> State:
        #     return State(self._relation)
        #
        # @relation.setter
        # def relation(self, value: State):
        #     self._relation = self._setter_helper_enum(self._relation, value)
        #
        # @multiclan.setter
        # def multiclan(self, value: int):
        #     assert self._multiclan == CacheStatus.UNKNOWN or self._multiclan == value
        #     assert 0 <= value <= 3
        #     self._multiclan = value

        if False:
            # noinspection PyUnusedLocal
            flags = [Flags() for i in range(1000000)]

            # Commented out because of missing enum State.
            # def time_rels():
            #     # Using an enum-based interface with a setter helper function.
            #     t1 = time.process_time()
            #     for flag in flags:
            #         flag.f.relation = State.IS_NOT
            #     t2 = time.process_time()
            #     for flag in flags:
            #         self.assertEqual(flag.f.relation, State.IS_NOT)
            #     t3 = time.process_time()
            #     for flag in flags:
            #         self.assertEqual(flag.f.relation, State.IS_NOT)
            #     t4 = time.process_time()
            #     print('set', t2 - t1)
            #     print('read1', t3 - t2)
            #     print('read2', t4 - t3)
            #     print('rels (enum w/)', t4 - t1, '\n')

            def time_clans():
                # Using an int-based interface with a setter helper function.
                t1 = time.process_time()
                for flag in flags:
                    flag.f.clan = CacheStatus.IS_NOT
                t2 = time.process_time()
                for flag in flags:
                    self.assertEqual(flag.f.clan, CacheStatus.IS_NOT)
                t3 = time.process_time()
                for flag in flags:
                    self.assertEqual(flag.f.clan, CacheStatus.IS_NOT)
                t4 = time.process_time()
                print('set', t2 - t1)
                print('read1', t3 - t2)
                print('read2', t4 - t3)
                print('clans (int w/)', t4 - t1, '\n')

            def time_multiclans():
                # Using an int-based interface without a setter helper function.
                t1 = time.process_time()
                for flag in flags:
                    flag.f.multiclan = CacheStatus.IS_NOT
                t2 = time.process_time()
                for flag in flags:
                    self.assertEqual(flag.f.multiclan, CacheStatus.IS_NOT)
                t3 = time.process_time()
                for flag in flags:
                    self.assertEqual(flag.f.multiclan, CacheStatus.IS_NOT)
                t4 = time.process_time()
                print('set', t2 - t1)
                print('read1', t3 - t2)
                print('read2', t4 - t3)
                print('multiclans (int w/o)', t4 - t1, '\n')

            # time_rels()
            time_clans()
            time_multiclans()
            # time_rels()
            time_clans()
            time_multiclans()
            # time_rels()
            time_clans()
            time_multiclans()

# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
