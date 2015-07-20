"""Math object example data for tests."""

# $Id: data_mathobjects.py 22614 2015-07-15 18:14:53Z gfiedler $
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
from algebraixlib.mathobjects import Atom, Couplet, Set, Multiset
from algebraixlib.algebras.relations import diag as _diag
from algebraixlib.util.test import create_test_object as _create_test_object

_print_examples = False


def _print_object_collection(name):
    if _print_examples:
        print('{name}:'.format(name=name))
        for key, val in sorted(globals()[name].items()):
            print('  "{key}": {val}'.format(key=key, val=val))


#: Basic Atom instances.
basic_atoms = {key: _create_test_object(Atom(val), key, val) for key, val in {
    '2': 2,
    '2.0': 2.0,
    "'2'": '2',
    '5': 5,
    "'6'": '6',
    'atom': Atom(33),
    'atom of atom': Atom(Atom(34)),
}.items()}
_print_object_collection('basic_atoms')

#: Basic Couplet instances.
basic_couplets = {key: _create_test_object(Couplet(**val), key, val) for key, val in {
    '3x2': {'left': 2, 'right': 3},
    "'5'x'4'": {'left': '4', 'right': '5'},
    "'7'x6": {'left': Atom(6), 'right': Atom('7')},
    'Coupl x Set': {'left': Couplet(8, 9), 'right': Set((10, Atom(11)))}
}.items()}
_print_object_collection('basic_couplets')

#: Basic Set instances.
basic_sets = {key: _create_test_object(Set(val), key, val) for key, val in {
    'empty': [],
    'num in dict': {Atom(1), Atom(2), Atom(3)},
    'str in array': [Atom(el) for el in 'abc'],
    'single num': 1,
    'single Coupl': Couplet(right='a', left='b'),
    'left func': [Couplet(s, c) for s, c in zip('abc', [1, 2, 3])],
    'left func/lefts': ['a', 'b', 'c'],
    'left func/rights': [1, 2, 3],
    'not left func': [Couplet(s, c) for s, c in zip('abca', [1, 2, 3, 4])],
    'not right func': [Couplet(s, c) for s, c in zip('abcd', [1, 2, 3, 1])],
    'diagonal': [Couplet(s, s) for s in 'abc']
}.items()}
_print_object_collection('basic_sets')

#: Basic Multiset instances.
#basic_multisets = {key: _create_test_object(Multiset(val), key, val) for key, val in {
    #'empty': [],
    #'dict': dict([('a', 3), ('b', 2), ('c', 5)]),
    #'num in dict': {Atom(1), Atom(2), Atom(3)},
    #'str in array': [Atom(el) for el in 'abc'],
    #'single alpha': 'A'
#}.items()}
#_print_object_collection('basic_multisets')

#: Relation instances for testing the relation algebra.
algebra_relations = {key: _create_test_object(val, key) for key, val in {
    'rel1': Set([Couplet('a', 1), Couplet('b', 2), Couplet('c', 3)]),
    'rel1/lefts': Set('a', 'b', 'c'),
    'rel1/rights': Set([1, 2, 3]),
    'rel2': Set([Couplet('x', 'a'), Couplet('zzz', 'zzz'), Couplet('y', 'c')]),
    'rel2/lefts': Set(['x', 'zzz', 'y']),
    'rel2/rights': Set(['a', 'zzz', 'c']),
    'rel1comp1': Set(),
    'rel1comp2': Set([Couplet('x', 1), Couplet('y', 3)]),
    'rel2comp2': Set(Couplet('zzz', 'zzz')),
    'rel1transp': Set([Couplet(1, 'a'), Couplet(2, 'b'), Couplet(3, 'c')]),
    'reldiag': _diag('a', 'b', 'c', 'x', 'zzz', 'y', 1, 2, 3),
}.items()}
_print_object_collection('algebra_relations')

#: Basic clan instances.
basic_clans = {key: _create_test_object(Set(val), key, val) for key, val in {
    'left func': basic_sets['left func'],
    'left func2': [
        basic_sets['left func'], Set([Couplet(s, c) for s, c in zip('def', [4, 5, 6])])
    ],
    'not left func': basic_sets['not left func'],
    'not right func': basic_sets['not right func'],
    'diagonal': basic_sets['diagonal']
}.items()}
_print_object_collection('basic_clans')

#: Clan instances for testing the clan algebra.
algebra_clans = {key: _create_test_object(val, key) for key, val in {
    'clan1': Set({
        Set([Couplet(s, c) for c, s in zip([1, 2, 3], 'abc')]),
        Set([Couplet(s, c) for c, s in zip([4, 5, 6], 'abc')]),
    }),
    'clan1/lefts': Set('a', 'b', 'c'),
    'clan1/rights': Set([1, 2, 3, 4, 5, 6]),
    # left-functional, right-functional, regular
    'clan2': Set({
        Set([Couplet(s, c) for c, s in zip(['a', 'zzz', 'c'], ['x', 'zzz', 'y'])]),
    }),
    'clan2/lefts': Set(['x', 'zzz', 'y']),
    'clan2/rights': Set(['a', 'zzz', 'c']),
    # left-functional, not right-functional, regular
    'clan3': Set({
        Set([Couplet(s, c) for c, s in zip([1, 2, 3], 'abc')]),
        Set([Couplet(s, c) for c, s in zip([4, 5, 5], 'abc')]),
    }),
    'clan3/lefts': Set('a', 'b', 'c'),
    'clan3/rights': Set([1, 2, 3, 4, 5]),
    # not left-functional, right-functional, regular
    'clan4': Set({
        Set([Couplet(s, c) for c, s in zip('abc', [1, 2, 3])]),
        Set([Couplet(s, c) for c, s in zip('abc', [4, 5, 5])]),
    }),
    'clan4/lefts': Set([1, 2, 3, 4, 5]),
    'clan4/rights': Set('a', 'b', 'c'),
    # left-functional, right-functional, not regular
    'clan5': Set({
        Set([Couplet(s, c) for c, s in zip([1, 2, 3], 'abc')]),
        Set([Couplet(s, c) for c, s in zip([4, 5], 'ab')]),
    }),
    'clan5/lefts': Set('a', 'b', 'c'),
    'clan5/rights': Set([1, 2, 3, 4, 5]),
    # clan1 with different ordering (should compare equal)
    'clan1reordered': Set({
        Set([Couplet(s, c) for c, s in zip([4, 6, 5], 'acb')]),
        Set([Couplet(s, c) for c, s in zip([3, 2, 1], 'cba')]),
    }),
    # compose(clan1, clan2)
    'clan1comp2': Set({
        Set([Couplet(s, c) for c, s in zip([1, 3], 'xy')]),
        Set([Couplet(s, c) for c, s in zip([4, 6], 'xy')]),
    }),
    # compose(clan2, clan1)
    'clan2comp1': Set({
        Set(),
        Set(),
    }),
    # transpose(clan1)
    'clan1transp': Set({
        Set([Couplet(s, c) for c, s in zip('abc', [1, 2, 3])]),
        Set([Couplet(s, c) for c, s in zip('abc', [4, 5, 6])]),
    }),
    # union(clan1, clan2), functional_cross_union(clan1, clan2),
    # right_functional_cross_union(clan1, clan2)
    'clan1union2': Set({
        Set([Couplet(s, c) for c, s in zip(
            [1, 2, 3, 'a', 'zzz', 'c'], ['a', 'b', 'c', 'x', 'zzz', 'y'])]),
        Set([Couplet(s, c) for c, s in zip(
            [4, 5, 6, 'a', 'zzz', 'c'], ['a', 'b', 'c', 'x', 'zzz', 'y'])]),
    }),
    # functional_cross_union(clan1, clan3)
    'clan1sfcu3': Set({
        Set([Couplet(s, c) for c, s in zip([1, 2, 3], 'abc')]),
    }),
    # functional_cross_union(clan1, clan4)
    'clan1sfcu4': Set({
        Set([Couplet(s, c) for c, s in zip(['a', 'b', 'c', 1, 2, 3], [1, 2, 3, 'a', 'b', 'c'])]),
        Set([Couplet(s, c) for c, s in zip(['a', 'b', 'c', 4, 5, 6], [1, 2, 3, 'a', 'b', 'c'])]),
    }),
    # right_functional_cross_union(clan1, clan3)
    'clan1cfcu3': Set({
        Set([Couplet(s, c) for c, s in zip([1, 2, 3], 'abc')]),
        Set([Couplet(s, c) for c, s in zip([1, 2, 3, 4, 5, 6], 'abcabc')]),
    }),
    # right_functional_cross_union(clan1, clan4)
    'clan1cfcu4': Set({
        Set([Couplet(s, c) for c, s in zip([1, 2, 3, 'a', 'b', 'c'], ['a', 'b', 'c', 1, 2, 3])]),
        Set([Couplet(s, c) for c, s in zip([1, 2, 3, 'a', 'b', 'c'], ['a', 'b', 'c', 4, 5, 5])]),
        Set([Couplet(s, c) for c, s in zip([4, 5, 6, 'a', 'b', 'c'], ['a', 'b', 'c', 1, 2, 3])]),
        Set([Couplet(s, c) for c, s in zip([4, 5, 6, 'a', 'b', 'c'], ['a', 'b', 'c', 4, 5, 5])]),
    }),
    # intersect(clan1, clan3)
    'clan1inters3': Set({
        Set([Couplet(s, c) for c, s in zip([1, 2, 3], 'abc')]),
        Set([Couplet(s, c) for c, s in zip([4, 5], 'ab')]),
        Set()
    }),
    # substrict(clan1, clan3), superstrict(clan1, clan3)
    'clan1subsupstr3': Set({
        Set([Couplet(s, c) for c, s in zip([1, 2, 3], 'abc')]),
    }),
}.items()}
_print_object_collection('algebra_clans')

#: Clan instances for testing the clan algebra.
algebra_multiclans = {key: _create_test_object(val, key) for key, val in {
    # Note that the data is ordered 'right, left', differently from what Couplet() expects.
    # left-functional, right-functional, regular
    'clan1': Multiset({
        Set([Couplet(s, c) for c, s in zip([1, 2, 3], 'abc')]),
        Set([Couplet(s, c) for c, s in zip([4, 5, 6], 'abc')]),
    }),
    'clan1/lefts': Set('a', 'b', 'c'),
    'clan1/rights': Set([1, 2, 3, 4, 5, 6]),
    # left-functional, right-functional, regular
    'clan2': Multiset({
        Set([Couplet(s, c) for c, s in zip(['a', 'zzz', 'c'], ['x', 'zzz', 'y'])]),
    }),
    'clan2/lefts': Set(['x', 'zzz', 'y']),
    'clan2/rights': Set(['a', 'zzz', 'c']),
    # left-functional, not right-functional, regular
    'clan3': Multiset({
        Set([Couplet(s, c) for c, s in zip([1, 2, 3], 'abc')]),
        Set([Couplet(s, c) for c, s in zip([4, 5, 5], 'abc')]),
    }),
    'clan3/lefts': Set('a', 'b', 'c'),
    'clan3/rights': Set([1, 2, 3, 4, 5]),
    # not left-functional, right-functional, regular
    'clan4': Multiset({
        Set([Couplet(s, c) for c, s in zip('abc', [1, 2, 3])]),
        Set([Couplet(s, c) for c, s in zip('abc', [4, 5, 5])]),
    }),
    'clan4/lefts': Set([1, 2, 3, 4, 5]),
    'clan4/rights': Set('a', 'b', 'c'),
    # left-functional, right-functional, not regular
    'clan5': Multiset({
        Set([Couplet(s, c) for c, s in zip([1, 2, 3], 'abc')]),
        Set([Couplet(s, c) for c, s in zip([4, 5], 'ab')]),
    }),
    'clan5/lefts': Set('a', 'b', 'c'),
    'clan5/rights': Set([1, 2, 3, 4, 5]),
    # clan1 with different ordering (should compare equal)
    'clan1reordered': Multiset({
        Set([Couplet(s, c) for c, s in zip([4, 6, 5], 'acb')]),
        Set([Couplet(s, c) for c, s in zip([3, 2, 1], 'cba')]),
    }),
    # compose(clan1, clan2)
    'clan1comp2': Multiset({
        Set([Couplet(s, c) for c, s in zip([1, 3], 'xy')]),
        Set([Couplet(s, c) for c, s in zip([4, 6], 'xy')]),
    }),
    # compose(clan2, clan1)
    'clan2comp1': Multiset({Set(): 2}),
    # transpose(clan1)
    'clan1transp': Multiset({
        Set([Couplet(s, c) for c, s in zip('abc', [1, 2, 3])]),
        Set([Couplet(s, c) for c, s in zip('abc', [4, 5, 6])]),
    }),
    # union(clan1, clan2), functional_cross_union(clan1, clan2),
    # right_functional_cross_union(clan1, clan2)
    'clan1union2': Multiset({
        Set([Couplet(s, c) for c, s in zip(
            [1, 2, 3, 'a', 'zzz', 'c'], ['a', 'b', 'c', 'x', 'zzz', 'y'])]),
        Set([Couplet(s, c) for c, s in zip(
            [4, 5, 6, 'a', 'zzz', 'c'], ['a', 'b', 'c', 'x', 'zzz', 'y'])]),
    }),
    # functional_cross_union(clan1, clan3)
    'clan1sfcu3': Multiset({
        Set([Couplet(s, c) for c, s in zip([1, 2, 3], 'abc')]),
    }),
    # functional_cross_union(clan1, clan4)
    'clan1sfcu4': Multiset({
        Set([Couplet(s, c) for c, s in zip(['a', 'b', 'c', 1, 2, 3], [1, 2, 3, 'a', 'b', 'c'])]),
        Set([Couplet(s, c) for c, s in zip(['a', 'b', 'c', 4, 5, 6], [1, 2, 3, 'a', 'b', 'c'])]),
    }),
    # right_functional_cross_union(clan1, clan3)
    'clan1cfcu3': Multiset({
        Set([Couplet(s, c) for c, s in zip([1, 2, 3], 'abc')]),
        Set([Couplet(s, c) for c, s in zip([1, 2, 3, 4, 5, 6], 'abcabc')]),
    }),
    # right_functional_cross_union(clan1, clan4)
    'clan1cfcu4': Multiset({
        Set([Couplet(s, c) for c, s in zip([1, 2, 3, 'a', 'b', 'c'], ['a', 'b', 'c', 1, 2, 3])]),
        Set([Couplet(s, c) for c, s in zip([1, 2, 3, 'a', 'b', 'c'], ['a', 'b', 'c', 4, 5, 5])]),
        Set([Couplet(s, c) for c, s in zip([4, 5, 6, 'a', 'b', 'c'], ['a', 'b', 'c', 1, 2, 3])]),
        Set([Couplet(s, c) for c, s in zip([4, 5, 6, 'a', 'b', 'c'], ['a', 'b', 'c', 4, 5, 5])]),
    }),
    # intersect(clan1, clan3)
    'clan1inters3': Multiset({
        Set([Couplet(s, c) for c, s in zip([1, 2, 3], 'abc')]): 1,
        Set([Couplet(s, c) for c, s in zip([4, 5], 'ab')]): 1,
        Set(): 2
    }),
    # substrict(clan1, clan3), superstrict(clan1, clan3)
    'clan1subsupstr3': Multiset({
        Set([Couplet(s, c) for c, s in zip([1, 2, 3], 'abc')]),
    }),
}.items()}
_print_object_collection('algebra_multiclans')


basic_hordes = {key: _create_test_object(Set(*val), key, val) for key, val in {
    'left func': basic_clans['left func'],
    'left func2': [
        basic_clans['left func2'], Set(Set([Couplet(s, c) for s, c in zip('ghi', [7, 8, 9])]))
    ],
    'not left func': basic_clans['not left func'],
    'not right func': basic_clans['not right func'],
    'diagonal': basic_clans['diagonal']
}.items()}
"""Basic Horde instances."""
_print_object_collection('basic_hordes')
