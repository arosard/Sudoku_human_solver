import unittest
from sudoku import Sudoku
from sudoku_parser import SudokuParser
from sudoku_human_solver import SudokuSolver


class BasicRules(unittest.TestCase):
    sudoku = Sudoku()

    @classmethod
    def setUpClass(cls):
        cls.sudoku.set_value(0, 0, 1)

    def test_impossible_value(self):
        is_ok = self.sudoku.set_value(0, 1, 10)
        self.assertFalse(is_ok)

    def test_same_square_2_times(self):
        is_ok = self.sudoku.set_value(1, 1, 1)
        self.assertFalse(is_ok)

    def test_same_row_2_times(self):
        is_ok = self.sudoku.set_value(0, 3, 1)
        self.assertFalse(is_ok)

    def test_same_col_2_times(self):
        is_ok = self.sudoku.set_value(3, 0, 1)
        self.assertFalse(is_ok)

    def test_regular_insertion(self):
        is_ok = self.sudoku.set_value(1, 1, 2)
        self.assertTrue(is_ok)
        is_ok = self.sudoku.set_value(4, 5, 1)
        self.assertTrue(is_ok)

    def test_insertion_same_square_bug_1(self):
        new_sudoku = Sudoku()
        is_ok = new_sudoku.set_value(2, 0, 6)
        self.assertTrue(is_ok)
        is_ok = new_sudoku.set_value(1, 0, 6)
        self.assertFalse(is_ok)
        is_ok = new_sudoku.set_value(0, 1, 6)
        self.assertFalse(is_ok)

    def test_impossible_sudoku(self):
        new_sudoku = Sudoku()
        for i in range(8):
            new_sudoku.set_value(0, i, i + 1)
        new_sudoku.set_value(1, 8, 9)
        self.assertTrue(new_sudoku.is_impossible())


class SolverStrategies(unittest.TestCase):
    def test_only_one_candidate(self):
        sudoku = SudokuParser.parse_sudoku("example_sudoku/sudoku_easy_1.csv")
        solver = SudokuSolver(sudoku)
        is_ok = solver.only_one_candidate()
        self.assertTrue(is_ok)
        self.assertEqual(6, solver.sudoku.cells[2][0].value)

    def test_sudoku_solve_one_candidate(self):
        sudoku = SudokuParser.parse_sudoku("example_sudoku/sudoku_easy_1.csv")
        solver = SudokuSolver(sudoku)
        solver.solve()
        self.assertTrue(solver.sudoku.is_sudoku_solved())

    def test_only_position_in_row(self):
        new_sudoku = Sudoku()
        for i in range(8):
            new_sudoku.set_value(0, i, i + 1)

        solver = SudokuSolver(new_sudoku)
        is_ok = solver.only_position_in_row()
        self.assertTrue(is_ok)
        self.assertEqual(9, new_sudoku.cells[0][8].value)

    def test_only_position_in_col(self):
        new_sudoku = Sudoku()
        for i in range(8):
            new_sudoku.set_value(i, 0, i + 1)

        solver = SudokuSolver(new_sudoku)
        is_ok = solver.only_position_in_col()
        self.assertTrue(is_ok)
        self.assertEqual(9, new_sudoku.cells[8][0].value)

    def test_only_position_in_square(self):
        new_sudoku = Sudoku()
        for i in range(3):
            for j in range(3):
                number = 3 * i + j + 1
                if number != 9:
                    new_sudoku.set_value(i, j, number)

        solver = SudokuSolver(new_sudoku)
        is_ok = solver.only_position_in_square()
        self.assertTrue(is_ok)
        self.assertEqual(9, new_sudoku.cells[2][2].value)

class SolverRemoveCandidates(unittest.TestCase):
    def test_remove_hidden_pair(self):
        sudoku = Sudoku()
        for col in range(4,9):
            sudoku.set_value(0, col, col+1)
        sudoku.set_value(3,0,1)
        sudoku.set_value(4,0,2)
        sudoku.set_value(6,1,1)
        sudoku.set_value(7,1,2)

        solver = SudokuSolver(sudoku)
        solver.hidden_n_tuples()

        self.assertNotIn(3, sudoku.cells[0][3].candidates)
        self.assertNotIn(4, sudoku.cells[0][3].candidates)
        self.assertNotIn(3, sudoku.cells[0][4].candidates)
        self.assertNotIn(4, sudoku.cells[0][4].candidates)

    def test_remove_hidden_triplet(self):
        sudoku = Sudoku()
        sudoku.set_value(0,6,7)
        sudoku.set_value(0,7,8)
        sudoku.set_value(0,8,9)
        sudoku.set_value(3,0,1)
        sudoku.set_value(4,0,2)
        sudoku.set_value(5,0,3)
        sudoku.set_value(6,1,1)
        sudoku.set_value(7,1,2)
        sudoku.set_value(8,1,3)
        sudoku.set_value(6, 3, 3)
        sudoku.set_value(7, 3, 1)
        sudoku.set_value(8, 3, 2)

        solver = SudokuSolver(sudoku)
        solver.hidden_n_tuples()

        self.assertNotIn(4, sudoku.cells[0][2].candidates)
        self.assertNotIn(5, sudoku.cells[0][2].candidates)
        self.assertNotIn(6, sudoku.cells[0][2].candidates)

    def test_remove_naked_row_triple_from_square(self):
        sudoku = Sudoku()
        for col in range(6):
            sudoku.set_value(0, col, col+1)

        solver = SudokuSolver(sudoku)
        solver.naked_n_tuples()

        for candidate in [7, 8, 9]:
            for row in [1, 2]:
                for col in [6, 7, 8]:
                    self.assertNotIn(candidate, sudoku.cells[row][col].candidates)

if __name__ == "__main__":
    unittest.main()
