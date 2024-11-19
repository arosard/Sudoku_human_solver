import logging
from sudoku import Sudoku

class SudokuParser:
    @staticmethod
    def parse_sudoku(sudoku_file):
        logging.debug("Parsing sudoku from file " + sudoku_file)
        sudoku = Sudoku()
        with open(sudoku_file) as f:
            for line in f:
                row, col, value = line.split(",")
                sudoku.set_value(int(row) - 1, int(col) - 1, int(value.strip()))
        return sudoku