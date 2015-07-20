"""Testing the operations module."""

# $Id: test_operations.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import unittest

import algebraixlib.extension as extension
import algebraixlib.partition as partition
import algebraixlib.algebras.clans as clans
import algebraixlib.algebras.sets as sets
import algebraixlib.algebras.relations as relations
from algebraixlib.mathobjects import Atom, Couplet, Set, Multiset
from algebraixlib.undef import make_or_raise_undef as _make_or_raise_undef, Undef
from numbers import Number


class OperationsTests(unittest.TestCase):

    _print_examples = False

    def test_diagonal(self):
        base_set = Set(Atom(1))
        diag_rels = [
            relations.diag(*base_set), relations.diag(1)]
        for diag_rel in diag_rels:
            self.assertEqual(diag_rel.cardinality, 1)
            self.assertTrue(relations.is_member(diag_rel))
            self.assertTrue(diag_rel.has_element(Couplet(1, 1)))

        base_set = Set(Atom(1), Atom('a'))
        diag_clan = clans.diag(1, 'a')
        self.assertEqual(diag_clan.cardinality, 1)
        diag_rels = [
            relations.diag(*base_set), relations.diag(1, 'a'), sets.single(diag_clan)]
        for diag_rel in diag_rels:
            self.assertEqual(diag_rel.cardinality, 2)
            self.assertTrue(relations.is_member(diag_rel))
            self.assertTrue(diag_rel.has_element(Couplet(1, 1)))
            self.assertTrue(diag_rel.has_element(Couplet('a', 'a')))

        arg1 = Set(1, 2, 3)
        arg2 = [v for v in Set(1, 2, 3)]
        result_diag = Set(Couplet(1, 1), Couplet(2, 2), Couplet(3, 3))
        self.assertEqual(relations.diag(*arg1), result_diag)
        self.assertEqual(relations.diag(*arg2), result_diag)

    test_set1 = {
        "input": Set([Couplet(1, '1'), Couplet(2, '2'), Couplet(3, '3'), Couplet(4, '4'),
                      Couplet(5, '5')]),
        "even_part": Set([Set([Couplet(2, '2'), Couplet(4, '4')]),
                          Set([Couplet(1, '1'), Couplet(3, '3'), Couplet(5, '5')])]),
        "even_part_equiv": Set([Couplet(Atom(True), Set([Couplet(2, '2'), Couplet(4, '4')])),
                                Couplet(Atom(False), Set([Couplet(1, '1'), Couplet(3, '3'),
                                                          Couplet(5, '5')]))]),
        "input2": Set([Couplet(1, '1'), Couplet(2, '2'), Couplet(3, '3'), Couplet(4, '4'),
                       Couplet(5, '5'),
                       Couplet(6, '6'), Couplet(7, '7'), Couplet(8, '8'), Couplet(9, '9'),
                       Couplet(10, '10'),
                       Couplet(11, '11'), Couplet(12, '12'), Couplet(13, '13'), Couplet(14, '14'),
                       Couplet(15, '15')]),
        "thirds_part": Set([Set([Couplet(1, '1'), Couplet(4, '4'), Couplet(7, '7'),
                                 Couplet(10, '10'), Couplet(13, '13')]),
                            Set([Couplet(2, '2'), Couplet(5, '5'), Couplet(8, '8'),
                                 Couplet(11, '11'), Couplet(14, '14')]),
                            Set([Couplet(3, '3'), Couplet(6, '6'), Couplet(9, '9'),
                                 Couplet(12, '12'), Couplet(15, '15')])])
        }

    def test_partition(self):
        test_set = OperationsTests.test_set1
        even_part = partition.partition(test_set["input"], lambda elem: elem.left.value % 2 == 0)
        self.assertEqual(even_part, test_set["even_part"])
        if OperationsTests._print_examples:
            print("Even partition Actual:  ", even_part)
            print("Even partition Expected:", test_set["even_part"])

        thirds_part = partition.partition(test_set["input2"], lambda elem: elem.left.value % 3)
        self.assertEqual(thirds_part, test_set["thirds_part"])
        if OperationsTests._print_examples:
            print("Thirds partition Actual:  ", thirds_part)
            print("Thirds partition Expected:", test_set["thirds_part"])

        even_part_equiv = \
            partition.left_equiv_relation(test_set["input"], lambda elem: elem.left.value % 2 == 0)
        self.assertEqual(even_part_equiv, test_set["even_part_equiv"])
        if OperationsTests._print_examples:
            print(even_part_equiv)

        # Negative test, returning something that can not be put inside an atom
        my_equiv_rel_fun = lambda elem: "even" if elem.left.value % 2 == 0 else Undef()
        self.assertRaises(TypeError, lambda: partition.partition(test_set["input2"], my_equiv_rel_fun))
        my_left_eq_rel_fn = lambda: partition.left_equiv_relation(test_set["input2"], my_equiv_rel_fun)
        self.assertRaises(TypeError, my_left_eq_rel_fn)

    def test_unary_extend(self):
        """Verify that unary extend uses the input set and operation to invoke the equivalent
        operation in next higher power set."""
        self.assertEqual(Set(Set(Couplet(1, 1))), extension.unary_extend(Set(*Set(1)), relations.diag))

    def test_unary_extend_errors(self):
        self.assertIs(extension.unary_extend(1, sets.big_union), Undef())

    def test_binary_extend_errors(self):
        self.assertIs(extension.binary_extend(1, 2, sets.union), Undef())
        self.assertIs(extension.binary_extend(Set(1), 2, sets.union), Undef())
        self.assertIs(extension.binary_extend(1, Set(2), sets.union), Undef())

    def test_binary_multi_extend_errors(self):
        self.assertIs(extension.binary_multi_extend(1, 2, sets.union), Undef())
        self.assertIs(extension.binary_multi_extend(Multiset(1), 2, sets.union), Undef())
        self.assertIs(extension.binary_multi_extend(1, Multiset(2), sets.union), Undef())


# --------------------------------------------------------------------------------------------------
def add_atom(e1, e2):
    if type(e1) != Atom:
        return _make_or_raise_undef()
    if type(e2) != Atom:
        return _make_or_raise_undef()
    if not isinstance(e1.value, Number):
        return _make_or_raise_undef()
    if not isinstance(e2.value, Number):
        return _make_or_raise_undef()
    try:
        # noinspection PyUnresolvedReferences
        result = e1.value + e2.value
    except TypeError:
        result = Undef()
    return Atom(result) if result is not Undef() else result
