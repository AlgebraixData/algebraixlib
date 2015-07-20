"""An example data algebra script.  Naively solve a Sudoku game using techniques a person would
likely use.  This is a teaching exercise, not an attempt at writing the fastest solver possible."""

# $Id: sudoku.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import time
from functools import partial
import itertools

from algebraixlib.mathobjects import Couplet, Set
import algebraixlib.algebras.relations as relations
import algebraixlib.algebras.clans as clans
import algebraixlib.algebras.sets as sets
import algebraixlib.extension as extension
import algebraixlib.partition as partition
from algebraixlib.undef import Undef


verbose = False
# verbose = True

BLOCK_SIZE = 3
GRID_SIZE = BLOCK_SIZE*BLOCK_SIZE
BLOCK_VALUES_CLAN = Set(Set(Couplet('value', i)
                            ).cache_is_relation(True).cache_is_left_functional(True)
                        for i in range(1, GRID_SIZE+1)
                        ).cache_is_clan(True).cache_is_left_functional(True)
BANDS_STACKS = Set((relations.from_dict({'row': r, 'col': c,
                                         'band': int((r-1) / BLOCK_SIZE)+1,
                                         'stack': int((c-1) / BLOCK_SIZE)+1})
                    for r, c in itertools.product(list(range(1, GRID_SIZE+1)),
                                                  list(range(1, GRID_SIZE+1))))
                   ).cache_is_clan(True).cache_is_left_functional(True)


def _sorted(iterable, key=None):
    return sorted(iterable, key=key)


def _unsorted(iterable, key=None):
    _ = key
    return iterable  # sorting is for debugging...for performance don't sort

# _sort = _sorted  # To get consistent timing/debugging
_sort = _unsorted


def make_board(_puzzle):
    assert len(_puzzle) == GRID_SIZE*GRID_SIZE
    board = set()
    for i, v in enumerate(_puzzle):
        value = 0 if v == '.' else int(v)
        col = (i % GRID_SIZE) + 1
        row = int(i / GRID_SIZE) + 1
        band = int((row-1) / BLOCK_SIZE)+1
        stack = int((col-1) / BLOCK_SIZE)+1
        # cell = {'row': row, 'col': col}
        cell = {'row': row, 'col': col, 'band': band, 'stack': stack}
        if value != 0:
            cell['value'] = value
        board.add(relations.from_dict(cell))
    return Set(board, direct_load=True).cache_is_clan(True).cache_is_left_functional(True)


def print_string(board):
    if verbose:
        print(get_string(board))


def by_key(key, rel):
    return rel(key)


def by_keys(key1, key2, rel):
    val1 = rel(key1)
    val2 = rel(key2)
    return val1, val2


def by_clan_key(key, clan):
    return sets.single(clan[key])


def by_clan_keys(key1, key2, clan):
    val1 = sets.single(clan[key1])
    val2 = sets.single(clan[key2])
    return val1, val2


def get_string(board):
    digits = []
    for cell in sorted(board, key=partial(by_keys, 'row', 'col')):
        value = cell('value')
        digits.append(0 if value is Undef() else value.value)

    assert len(digits) == GRID_SIZE*GRID_SIZE
    return ''.join(str(x) for x in digits)


def get_filled_cells(board):
    return clans.defined_at(board, 'value')


def project(clan: 'PP(M x M)', *lefts) -> 'PP(M x M)':
    clan = clans.project(clan, *lefts)
    return clan


def get_missing_values(clan):
    """Get remaining values from passed in clan by subtracting it from from all possible values."""
    values_clan = project(clan, 'value')
    return sets.minus(BLOCK_VALUES_CLAN, values_clan)


def get_missing_rowcols(block_clan):
    band, stack = by_clan_keys('band', 'stack', block_clan)

    # Get block defined by band, stack
    full_block_clan = clans.superstrict(BANDS_STACKS,
                                        clans.from_dict({'band': band, 'stack': stack}))
    # Get missing rows/cols from the block
    target_rowcols = sets.minus(project(full_block_clan, 'row', 'col'),
                                project(block_clan, 'row', 'col'))
    return target_rowcols


def get_new_board(board, new_cells):
    if verbose:
        for cell in new_cells:
            row = cell('row').value
            col = cell('col').value
            value = cell('value').value
            print("*** value %d goes in Row %d, Col %d" % (value, row, col))

    cell_filter = project(new_cells, 'row', 'col')
    old_cells = clans.superstrict(board, cell_filter)
    new_board = sets.minus(board, old_cells)

    bands_stacks = clans.superstrict(BANDS_STACKS, cell_filter)
    new_cells = clans.functional_cross_union(new_cells, bands_stacks)

    new_board = sets.union(new_board, new_cells)
    # if verbose:
    #     print(get_string(new_board))
    assert len(new_board) == GRID_SIZE*GRID_SIZE
    return new_board


def check_values(_board):
    """Look for values where only one is missing.  If there is only one missing, then there is
    only one cell where adding the value would not cause a duplicate in a row or column.  Fill
    in those cells if they exist."""
    if verbose:
        print("* check_values")
    board = get_filled_cells(_board)

    new_cells = Set()
    value_clans = partition.partition(board, partial(by_key, 'value'))
    for value_clan in _sort(value_clans, key=partial(by_clan_key, 'value')):
        # If there is only 1 missing value..fill in the cell
        if value_clan.cardinality == GRID_SIZE-1:
            # Get the set of rows and cols containing value
            occupied_rows = project(value_clan, 'row')
            occupied_cols = project(value_clan, 'col')
            # Get the entire set of rows and cols based on the occupied rows and cols
            occupied = clans.superstrict(_board, sets.union(occupied_rows, occupied_cols))
            # Remove all occupied rows to get the only candidate row_col left
            row_col = sets.minus(_board, occupied)
            value = project(value_clan, 'value')
            new_cells = sets.union(new_cells, clans.cross_union(row_col, value))
    if new_cells:
        return get_new_board(_board, new_cells)
    return _board


def check_rows(_board):
    """Look for rows where there is only one missing value.  If any are found fill in the missing
    value.  Look for rows where there are two missing values.  If either missing value is blocked
    by the same value in the candidate row, col, or block then the other value can be placed in
    the blocked cell.  The other value can be placed in the other cell.  Look for rows with more
    than two missing values.  Check each empty cell to see only one of the missing values can be
    placed in it.  Check each value to see if there is only one cell where it can be placed."""
    if verbose:
        print("* check_rows")
    board = get_filled_cells(_board)

    all_rows_clans = partition.partition(board, partial(by_key, 'row'))
    for row_clan in _sort(all_rows_clans, key=partial(by_clan_key, 'row')):
        row = project(row_clan, 'row')
        board_row = clans.superstrict(_board, row)
        values_clan = get_missing_values(row_clan)

        if row_clan.cardinality == GRID_SIZE-1:
            # Row is missing only 1 value, remove row_clan from the board leaving target row_col
            row_col = sets.minus(board_row, row_clan)
            new_cells = clans.cross_union(row_col, values_clan)
            _board = get_new_board(_board, new_cells)
            continue

        # Get the set of candidate col/value pairs
        row_possible = clans.cross_union(values_clan,
                                         project(sets.minus(board_row, row_clan), 'col'))

        if row_clan.cardinality == GRID_SIZE-2:

            # The occupied_clan is the col/value pair that is a conflict for each col/value
            occupied_clan = project(clans.superstrict(board, row_possible), 'col', 'value')

            # If there are no conflicts neither value can be placed without checking entire board
            if not occupied_clan.is_empty:
                # ..remove occupied_clan col/value pairs from all possible
                new_possible = sets.minus(row_possible, occupied_clan)

                if new_possible.cardinality == 2:
                    # Of the 4 possibilities (2 values * 2 cols), 2 were removed, place remaining
                    new_cells = clans.cross_union(row, new_possible)
                    _board = get_new_board(_board, new_cells)
                    continue

                # 3 of the possibilities remain...
                occupied_col = project(occupied_clan, 'col')

                # Remove the occupied_col choices to get the first col/value pair
                col_value1 = clans.superstrict(new_possible, occupied_col)

                occupied_val = project(col_value1, 'value')

                # Remove the occupied_val choices to get the second col/value pair
                col_value2 = sets.minus(new_possible, clans.superstrict(new_possible, occupied_val))

                new_cells = clans.cross_union(row, col_value1)
                new_cells = sets.union(new_cells, clans.cross_union(row, col_value2))
                _board = get_new_board(_board, new_cells)
                continue

        # The occupied_clan is the row/col/value set that could be a conflict for values
        occupied_clan = clans.superstrict(board, values_clan)

        # If there are no conflicts then no cells can be placed
        if occupied_clan.is_empty:
            continue

        # Add row to row_possible for remaining checks
        all_possible = clans.cross_union(row_possible, row)

        # Get the set of conflicts...conflicting row/value + col/value
        conflict = sets.union(
            clans.superstrict(all_possible,
                              project(occupied_clan, 'value', 'col')),
            clans.superstrict(all_possible,
                              project(occupied_clan, 'value', 'row')))

        # Remove the conflicts from all_possible
        new_possible = sets.minus(all_possible, conflict)

        if new_possible.is_empty:
            continue  # All possible may have been excluded due to row/col conflicts

        # Otherwise...need to check for block (band+stack) conflicts too!!
        # ...if value exists in same block as element of all_possible

        # Add band/stack
        new_targets = clans.superstrict(BANDS_STACKS, project(new_possible, 'row', 'col'))
        new_possible3 = clans.functional_cross_union(new_targets, new_possible)
        occupied_clan2 = occupied_clan

        # Remove block (band+stack) conflicts
        new_possible4a = sets.minus(project(new_possible3, 'value', 'band', 'stack'),
                                    project(occupied_clan2, 'value', 'band', 'stack'))
        new_possible4 = clans.superstrict(new_possible3, new_possible4a)

        # Partition by row/col
        placed = 0
        candidates = partition.partition(new_possible4, partial(by_keys, 'row', 'col'))
        for candidate in _sort(candidates, key=partial(by_clan_key, 'col')):
            # If any row/col has only 1 candidate, place it
            if candidate.cardinality == 1:
                # Remove band/stack
                cell = project(candidate, 'row', 'col', 'value')
                _board = get_new_board(_board, cell)
                placed += 1

        if placed:
            continue

        # Partition by value
        candidates = partition.partition(new_possible4, partial(by_key, 'value'))
        for candidate in _sort(candidates, key=partial(by_clan_key, 'value')):
            # If any value fits in only 1 cell, place it
            if candidate.cardinality == 1:
                # Remove band/stack
                cell = project(candidate, 'row', 'col', 'value')
                _board = get_new_board(_board, cell)
    return _board


def check_cols(_board):
    """Check the columns the same way rows are checked"""
    if verbose:
        print("* check_cols")

    # Rotate the board by swapping row and col then call check_rows
    swaps = clans.from_dict({'row': 'col', 'band': 'stack'})
    rotated = extension.binary_extend(_board, swaps, partial(relations.swap, _checked=False)
                                     ).cache_is_clan(True).cache_is_left_functional(True)
    for rel in rotated:
        rel.cache_is_left_functional(True)

    new_board = check_rows(rotated)
    if rotated != new_board:
        _board = extension.binary_extend(new_board, swaps, partial(relations.swap, _checked=False)
                                         ).cache_is_clan(True).cache_is_left_functional(True)
        for rel in _board:
            rel.cache_is_left_functional(True)

    return _board


def check_blocks(_board):
    """Check each block.  If there is only one value missing..."""
    if verbose:
        print("* check_blocks")

    board = get_filled_cells(_board)
    blocks = partition.partition(board, partial(by_keys, 'band', 'stack'))
    for block_clan in _sort(blocks, key=partial(by_clan_keys, 'band', 'stack')):
        # Get the set of missing values...see if any can be placed due to row/col information
        values_clan = get_missing_values(block_clan)

        # Get the set of missing values...see if any can be placed due to row/col information
        target_rowcols = get_missing_rowcols(block_clan)

        if block_clan.cardinality == GRID_SIZE-1:
            new_cells = clans.cross_union(target_rowcols, values_clan)
            _board = get_new_board(_board, new_cells)
            continue

        # Need cross union values with rows
        rows_clan = project(target_rowcols, 'row')
        cols_clan = project(target_rowcols, 'col')
        possible_rows_values = clans.cross_union(values_clan, rows_clan)
        possible_cols_values = clans.cross_union(values_clan, cols_clan)

        possible_rows_cols_values = sets.union(possible_rows_values, possible_cols_values)

        # The occupied_clan is the row/col/value set that is a conflict for values
        occupied_clan = project(clans.superstrict(board, possible_rows_cols_values),
                                'value', 'row', 'col')

        # If there are no conflicts then no cells can be placed
        if occupied_clan.is_empty:
            continue

        all_possible = clans.cross_union(values_clan, target_rowcols).cache_is_left_functional(True)
        for rel in all_possible:
            rel.cache_is_left_functional(True)

        # Get the set of conflicts...conflicting row/value + col/value
        conflict = sets.union(
            clans.superstrict(all_possible, project(occupied_clan, 'value', 'col')),
            clans.superstrict(all_possible, project(occupied_clan, 'value', 'row')))

        # Remove the conflicts from all_possible
        new_possible = sets.minus(all_possible, conflict)

        if block_clan.cardinality == GRID_SIZE-2:
            # Knowing that the value in conflict can't be placed in the conflict cell
            # ..it must go in the other...
            first_choice = clans.superstrict(new_possible, project(conflict, 'value'))
            if first_choice.cardinality == 2:
                # place both values
                _board = get_new_board(_board, first_choice)
                continue

            # Remove the first choice for all_possible
            remaining_possible = sets.minus(new_possible, first_choice)

            # Knowing that first_choice goes in a row/col, remove other value from that cell
            first_rowcol = project(first_choice, 'row', 'col')

            # The remaining cell is the second choice
            second_choice = sets.minus(remaining_possible,
                                       clans.superstrict(remaining_possible, first_rowcol))

            new_cells = sets.union(first_choice, second_choice)
            _board = get_new_board(_board, new_cells)
            continue

        # Partition by value
        candidates = partition.partition(new_possible, partial(by_key, 'value'))
        for candidate in _sort(candidates, key=partial(by_clan_key, 'value')):
            # If any value fits in only 1 cell, place it
            if candidate.cardinality == 1:
                # Remove band/stack
                new_cell = project(candidate, 'row', 'col', 'value')
                _board = get_new_board(_board, new_cell)
    return _board


def check_done(_board):
    board = get_filled_cells(_board)
    if board.cardinality == GRID_SIZE*GRID_SIZE:
        if verbose:
            print("done")
        return True
    if verbose:
        print("> %d cells remaining" % (GRID_SIZE*GRID_SIZE - board.cardinality))
    return False


def solve_board(board):
    while not check_done(board):
        board_start = board
        board = check_values(board)
        board = check_rows(board)
        board = check_cols(board)
        board = check_blocks(board)
        if board_start == board:
            if verbose:
                print("*** can't solve")
            break
    return board


def solve_puzzle(_puzzle, _answer):
    print(_puzzle)
    start = time.time()
    board = solve_board(make_board(_puzzle))
    result = get_string(board)
    if _answer != result:
        if verbose:
            print("*** Wrong answer\nExpected: %s\nActual  : %s" % (_answer, result))
        return False

    end = time.time()
    if verbose:
        print("solve_puzzle took: %d seconds" % (end - start))
    return True

import unittest


class SudokuTest(unittest.TestCase):
    # quick_tests = True
    quick_tests = False

    def _test_func(self, _puzzle, _answer, method):
        board = make_board(_puzzle.replace('\n', ''))
        global _sort
        sorting = _sort
        # NOTE: Tests with partial data (12...5.6) requires sorting to be enabled or tests will fail
        _sort = _sorted
        actual = get_string(method(board))
        _sort = sorting
        expected = _answer.replace('.', '0')
        if actual != expected:
            print("*** Wrong answer\nExpected: %s\nActual  : %s" % (expected, actual))
            self.assertEqual(actual, expected)

    def test_values(self):
        self._test_func(
            # Missing only one 1 in row 1 col 1
            '..........1.........1.........1.........1.........1.........1.........1.........1',
            '1.........1.........1.........1.........1.........1.........1.........1.........1',
            check_values)

    def test_row(self):
        self._test_func(
            # Single missing value in row 1
            '.23456789........................................................................',
            '123456789........................................................................',
            check_rows)

        if self.quick_tests:
            return

        self._test_func(
            # Two missing values..neither with conflicts..neither can be filled
            '.2345678.........................................................................',
            '.2345678.........................................................................',
            check_rows)

        self._test_func(
            # Two missing values..only 1 without conflicts..both can be filled
            '.2345678.1.......................................................................',
            '9234567811.......................................................................',
            check_rows)

        self._test_func(
            # Two missing values..both with conflicts..both can be filled
            '.2345678.1.......9...............................................................',
            '9234567811.......9...............................................................',
            check_rows)

        self._test_func(
            # Three missing values..only 1 without conflicts..1 can be placed in col 9
            '..345678.129............29.......................................................',
            '..3456781129............29.......................................................',
            check_rows)

        self._test_func(
            # 3 missing values on row 1, no conflicts with 2 in col 7
            '170904065059000740000507019002000957795426183381795426926178534834059071517040090',
            '170904265059000740000507019002000957795426183381795426926178534834059071517040090',
            check_rows)

        self._test_func(
            # 6 missing values...3 only fits in col 1
            '010500200900321000002008030500030007008017500600085004040100700000700006003804050',
            '310500200900321000002008030500030007008017500600085004040100700000700006003804050',
            check_rows)

        self._test_func(
            # 3 missing values, only 1 value without conflict
            '..4.5678912........3........1.......2........3....................2........3.....',
            '..415678912........3........1.......2........3....................2........3.....',
            check_rows)

        self._test_func(
            # Region conflict...3 missing values, 1 without conflict
            '...456789.23................1.............................................1......',
            '1..456789.23................1.............................................1......',
            check_rows)

        self._test_func(
            # Region conflict...3 missing values, only 1 value without conflict
            '..4.56789123.........2........3.....3....................................3.......',
            '..4156789123.........2........3.....3....................................3.......',
            check_rows)

        self._test_func(
            # Region conflicts...3 missing values, only 1 value without conflict
            # place 1 in row 1 col 4
            '..4.56789123.........23..........................................................',
            '..4156789123.........23..........................................................',
            check_rows)

    def test_column(self):
        self._test_func(
            # 1 value missing in column 1, place the 9
            '1........2........3........4........5........6........7........8.................',
            '1........2........3........4........5........6........7........8........9........',
            check_cols)

        if self.quick_tests:
            return

        self._test_func(
            # 2 values left in col 1, 1 with conflict, place both
            '.9.......2........3........4........5........6........7........8.................',
            '19.......2........3........4........5........6........7........8........9........',
            check_cols)

        # NOTE: This block is useful for setting up a column test..from a row string
        # board = make_board(
        # '052900180800230009900801002000709000300020907097000420005104290000090000009502700')
        # swaps = Set(Set(Couplet('row', 'col')))
        # rotated = partition.binary_extend(board, swaps, relations.swap)
        # print('052900180800230009900801002000709000300020907097000420005104290000090000009502700')
        # print(get_string(rotated))
        # rotated = partition.binary_extend(rotated, swaps, relations.swap)
        # print(get_string(rotated))

        self._test_func(
            # 3 goes in column 1 row 9
            '089030000500009000200007509928700105030020090001900402100094207800002900092070000',
            '089030000500009000200007509928700105030020090001900402100094207800002900392070000',
            check_cols)

    def test_block(self):
        self._test_func(
            # Only 1 value missing in block
            '.23......456......789............................................................',
            '123......456......789............................................................',
            check_blocks)

        if self.quick_tests:
            return
        self._test_func(
            # Only 1 place for 1 in first block..1 goes in row 3, col3
            '..3.....14.5......7.........1....................................................',
            '..3.....14.5......7.1.......1....................................................',
            check_blocks)

        self._test_func(
            # Only 1 place for 8 in first block and 7 in center block
            '9..321...31.5..2....2..8.3.5...3...7..8.1.5..6...85..4.4.1..7.....7....6..38.4.5.',
            '98.321...31.5..2....2..8.3.5...3...7..8.175..6...85..4.4.1..7.....7....6..38.4.5.',
            check_blocks)

        self._test_func(
            # Only 2 values left in block...1 with conflict
            '.93.....14.5......678............................................................',
            '293.....1415......678............................................................',
            check_blocks)

        self._test_func(
            # Only 2 values left in block...1 with conflict
            '.93.....24.5......678............................................................',
            '193.....2425......678............................................................',
            check_blocks)

        self._test_func(
            # Only 2 values left in block...both with conflict
            '.93.....14.5......678.......2....................................................',
            '293.....1415......678.......2....................................................',
            check_blocks)

        self._test_func(
            # Only 2 values left in block...no conflicts..can't place either
            '.93......4.5......678............................................................',
            '.93......4.5......678............................................................',
            check_blocks)

    def test_easy_from_file(self):
        # return
        if self.quick_tests:
            return

        from itertools import islice
        with open('sudoku.dat') as f:
            while True:
                ps = list(islice(f, 2))
                if not ps:
                    break
                expected = ps[1].rstrip()
                self.assertTrue(solve_puzzle(ps[0].rstrip(), expected))
        print()

    def test_one(self):
        """Use this to test solving an entire puzzle..first test of e50.txt"""
        self._test_func(
            '003020600900305001001806400008102900700000008006708200002609500800203009005010300',
            '483921657967345821251876493548132976729564138136798245372689514814253769695417382',
            solve_board)


import nose
if __name__ == '__main__':
    arguments = [
        '-s', '--nocapture', '-v',  # Don't capture stdout (show it in the console).
        '--with-coverage',  # Include unit test coverage
        '--tests=sudoku.py',
    ]
    nose.main(argv=arguments)
