"""Test the util.latexPrinter module."""

# $Id: test_latexprinter.py 22614 2015-07-15 18:14:53Z gfiedler $

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
#
# Build unit test up here for now
#
import inspect
import os
import unittest
import algebraixlib.util.latexprinter as latexPrinter  # latexPrinter.colorize_output
from algebraixlib.util.latexprinter import math_object_to_latex
from algebraixlib.mathobjects import Atom, Couplet, Set


class LatexPrinterTest(unittest.TestCase):
    """Test the latex printer functions."""

    _print_examples = False

    # Test Input Data
    _a1 = Atom('scooby')
    _a2 = Atom('doo')
    _c1 = Couplet(left=_a1, right=_a2)
    _a3 = Atom('shaggy')
    _a4 = Atom('rogers')
    _c2 = Couplet(left=_a3, right=_a4)
    _a5 = Atom('mystery')
    _a6 = Atom('van')
    _c3 = Couplet(left=_a5, right=_a6)
    _s1 = Set([_c1, _c2, _c3])

    _a7 = Atom('velma')
    _a8 = Atom('dinkley')
    _c4 = Couplet(left=_a7, right=_a8)
    _a9 = Atom('fred')
    _a10 = Atom('jones')
    _c5 = Couplet(left=_a9, right=_a10)
    _a11 = Atom('daphne')
    _a12 = Atom('blake')
    _c6 = Couplet(left=_a11, right=_a12)
    _a13 = Atom('mystery')
    _a14 = Atom('team')
    _c7 = Couplet(left=_a13, right=_a14)
    _s2 = Set([_c4, _c5, _c6, _c7])

    _s3 = Set([_s1, _s2])

    def _enable_colorization(self, on_off):
        latexPrinter.Config.colorize_output = on_off

    def test_atom_printer(self):
        self._enable_colorization(False)

        # Actual LaTeX Output Data
        latex_atom = math_object_to_latex(self._a1)
        # Expected LaTeX Output Data
        latex_atom_ex = "\mbox{'scooby'}"
        self.assertEqual(latex_atom_ex, latex_atom)

        if self._print_examples:
            print("test_atom_printer Begin:")
            print('\tAtom={a!s}'.format(a=self._a1))
            print('\tLatex={l!s}'.format(l=latex_atom))
            print("Test End.")

    def test_couplet_printer(self):
        self._enable_colorization(False)
        # Actual LaTeX Output Data
        latex_couplet = math_object_to_latex(self._c1)
        # Expected LaTeX Output Data
        latex_couplet_ex = "\mbox{'scooby'}{\mapsto}{\mbox{'doo'}}"
        self.assertEqual(latex_couplet_ex, latex_couplet)

        if self._print_examples:
            print("test_couplet_printer Begin:")
            print('\tCouplet={c!s}'.format(c=self._c1))
            print('\tLatex={l!s}'.format(l=latex_couplet))
            print("Test End.")

    def test_set_printer(self):
        self._enable_colorization(False)
        # Actual LaTeX Output Data
        latex_set1 = math_object_to_latex(self._s1)
        latex_set2 = math_object_to_latex(self._s2)

        # Expected LaTeX Output Data
        latex_set_ex1 = ("\left\{\ \mbox{'van'}^{\mbox{'mystery'}},\ "
                         "\mbox{'doo'}^{\mbox{'scooby'}},\ "
                         "\mbox{'rogers'}^{\mbox{'shaggy'}}\ \\right\}")

        latex_set_ex2 = ("\left\{\ \mbox{'blake'}^{\mbox{'daphne'}},\ "
                         "\mbox{'jones'}^{\mbox{'fred'}},\ "
                         "\mbox{'team'}^{\mbox{'mystery'}},\ "
                         "\mbox{'dinkley'}^{\mbox{'velma'}}\ \\right\}")
        latex_mixed_set_with_couplet = math_object_to_latex(Set('a', Couplet('x', 'y')))
        if self._print_examples:
            print("test_set_printer Begin:")
            print('\tSet={s!s}'.format(s=self._s1))
            print('\tLatex={l!s}'.format(l=latex_set1))
            print('\tSet={s!s}'.format(s=self._s2))
            print('\tLatex={l!s}'.format(l=latex_set2))
            print("Test End.")

    def test_set_of_set_printer(self):
        self._enable_colorization(False)
        # large comparisons needs diff size increased
        self.maxDiff = None
        # Actual LaTeX Output Data
        latex_set = math_object_to_latex(self._s3)

        # Expected LaTeX Output Data
        latex_set_ex_p1 = ("\left\{\mbox{'mystery'}{\mapsto}{\mbox{'van'}},"
                           "\ \mbox{'scooby'}{\mapsto}{\mbox{'doo'}},\ "
                           "\mbox{'shaggy'}{\mapsto}{\mbox{'rogers'}}\\right\}")

        latex_set_ex_p2 = ("\left\{\mbox{'daphne'}{\mapsto}{\mbox{'blake'}},\ "
                           "\mbox{'fred'}{\mapsto}{\mbox{'jones'}},\ "
                           "\mbox{'mystery'}{\mapsto}{\mbox{'team'}},\ "
                           "\mbox{'velma'}{\mapsto}{\mbox{'dinkley'}}\\right\}")

        latex_set_ex = "\left\{\\begin{array}{l}" + \
                       latex_set_ex_p2 + ",\\\\\n" + latex_set_ex_p1 + \
                       "\end{array}\\right\}"
        self.assertEqual(latex_set_ex, latex_set)

        if self._print_examples:
            print("test_set_of_set_printer Begin:")
            print('Set={s!s}'.format(s=self._s3))
            print('Act={l!s}'.format(l=latex_set))
            print('Exp={l!s}'.format(l=latex_set_ex))
            print("Test End.")

# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()