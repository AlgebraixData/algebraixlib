"""Testing the io.csv module."""

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
import unittest

from algebraixlib.import_export.csv import import_csv, export_csv
from algebraixlib.mathobjects import Couplet, Set, Multiset
from algebraixlib.cache_status import CacheStatus


class IoCsvTests(unittest.TestCase):

    @staticmethod
    def path(file):
        return os.path.join(os.path.dirname(__file__), file)

    def test_csv(self):
        """Test loading clan from csv."""
        clan = Set({Set({Couplet('a', '1'), Couplet('b', '2')})})
        st1 = import_csv(IoCsvTests.path('set1.csv'))
        self.assertEqual(clan, st1)
        self.assertEqual(st1.cached_clan, CacheStatus.IS)
        self.assertEqual(st1.cached_functional, CacheStatus.IS)
        self.assertEqual(st1.cached_regular, CacheStatus.IS)

        clan = Set({Set({Couplet('a', '1'), Couplet('b', '2')})})
        st1a = import_csv(IoCsvTests.path('set1a.csv'))
        # NOTE: duplicate row is removed
        self.assertEqual(clan, st1a)
        self.assertEqual(st1a.cached_clan, CacheStatus.IS)
        self.assertEqual(st1a.cached_functional, CacheStatus.IS)
        self.assertEqual(st1a.cached_regular, CacheStatus.IS)

        clan = Set(Set({Couplet('a', '1'), Couplet('b', '2'), Couplet('row', 0)}),
                   Set({Couplet('a', '1'), Couplet('b', '2'), Couplet('row', 1)}))
        st1a = import_csv(IoCsvTests.path('set1a.csv'), index_column='row')
        # NOTE: duplicate row is NOT removed
        self.assertEqual(clan, st1a)
        self.assertEqual(st1a.cached_clan, CacheStatus.IS)
        self.assertEqual(st1a.cached_functional, CacheStatus.IS)
        self.assertEqual(st1a.cached_regular, CacheStatus.IS)

        expected = Multiset({Set(Couplet('a', '1'), Couplet('b', '2')): 2})
        actual = import_csv(IoCsvTests.path('set1a.csv'), has_dup_rows=True)
        # NOTE: duplicate row is not removed
        self.assertEqual(actual, expected)

        self.assertEqual(actual.cached_multiclan, CacheStatus.IS)
        self.assertEqual(actual.cached_functional, CacheStatus.IS)
        self.assertEqual(actual.cached_regular, CacheStatus.IS)

        clan = Set({Set({Couplet('a', '1'), Couplet('b', '2')}),
                    Set({Couplet('a', '3'), Couplet('b', '4')})})
        st2 = import_csv(IoCsvTests.path('set2.csv'))
        self.assertEqual(clan, st2)
        self.assertEqual(st2.cached_clan, CacheStatus.IS)
        self.assertEqual(st2.cached_functional, CacheStatus.IS)
        self.assertEqual(st2.cached_regular, CacheStatus.IS)

        clan = Set(Set([Couplet(s, c) for s, c in zip('abcd', [1, 2, 3, 4])]),
                   Set([Couplet(s, c) for s, c in zip('abc', [5, 6, 7])]),
                   Set([Couplet(s, c) for s, c in zip('bd', [8, 9])]))
        types = {'a': int, 'b': int, 'c': int, 'd': int}
        st3 = import_csv(IoCsvTests.path('set3.csv'), types)
        # print("expected", clan)
        # print("actual", st3)
        self.assertEqual(clan, st3)
        self.assertEqual(st3.cached_clan, CacheStatus.IS)
        self.assertEqual(st3.cached_functional, CacheStatus.IS)
        self.assertEqual(st3.cached_regular, CacheStatus.IS_NOT)

        expected = Multiset({Set(Couplet('a', '1'), Couplet('b', '2'), Couplet('c', '3'),
                                 Couplet('d', '4')): 1,
                             Set(Couplet('a', '5'), Couplet('b', '6'), Couplet('c', '7')): 1,
                             Set(Couplet('b', '8'), Couplet('d', '9')): 1})
        actual = import_csv(IoCsvTests.path('set3.csv'), has_dup_rows=True)
        self.assertEqual(actual, expected)

        self.assertEqual(actual.cached_multiclan, CacheStatus.IS)
        self.assertEqual(actual.cached_functional, CacheStatus.IS)
        self.assertEqual(actual.cached_regular, CacheStatus.IS_NOT)

        expected = Multiset({Set(Couplet('a', '5'), Couplet('b', '6'), Couplet('c', '7')): 1,
                             Set(Couplet('b', '8'), Couplet('d', '9')): 1,
                             Set(Couplet('a', '1'), Couplet('b', '2'), Couplet('c', '3'),
                                 Couplet('d', '4')): 1})
        export_path = IoCsvTests.path('export.csv')
        self.assertFalse(export_csv(expected, export_path))
        self.assertTrue(export_csv(expected, export_path, ordered_lefts='abcd'))
        actual = import_csv(export_path, has_dup_rows=True)
        self.assertEqual(actual, expected)


# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
