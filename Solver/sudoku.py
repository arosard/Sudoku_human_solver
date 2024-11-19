import logging


class SudokuCell:
    def __init__(self):
        self.value = None
        self.candidates = set(range(1, 10))

    def set_value(self, value):
        """

        :param value: value to put (1-9)
        :return: True is value was placed in the cell, False otherwise
        """
        if value in self.candidates:
            self.candidates = []
            self.value = value
            return True
        else:
            return False

    def remove_candidate(self, value):
        """
        Removes a value from the candidates of the cell if it exists
        Does nothing if the value is not in the candidates

        :param value: value to remove (1-9)
        :return: True is value was removed, False otherwise
        """
        if value in self.candidates:
            self.candidates.remove(value)
            return True
        else:
            logging.debug(str(value) + " not in the candidates of this cell")
            return False

    def nb_remaining_candidates(self):
        return len(self.candidates)


class Sudoku:
    def __init__(self):
        self.cells = [[SudokuCell() for _ in range(9)] for _ in range(9)]

    def set_value(self, row, col, value):
        """
        Try to set the value in the specified cell
        and removes this value from the candidates of the cells in the same row, column and square
        Does if the value is not in the candidates of the cell

        :param row: index of the row of the cell (0-8)
        :param col: index of the column of the cell (0-8)
        :param value: sudoku cell value (1-9)
        :return: True is value was placed in the cell, False otherwise
        """
        logging.debug(
            "Setting value "
            + str(value)
            + " in square ("
            + str(row)
            + ", "
            + str(col)
            + ")"
        )
        is_ok = self.cells[row][col].set_value(value)
        if not is_ok:
            logging.debug(
                str(value) + " cannot be in square (" + str(row) + ", " + str(col) + ")"
            )
            return False


        self.remove_candidate_from_cells(value, [(row, i) for i in range(9)])
        self.remove_candidate_from_cells(value, [(i, col) for i in range(9)])
        self.remove_candidate_from_cells(value, [(row // 3 * 3 + i, col // 3 * 3 + j) for i in range(3) for j in range(3)])
        return True

    def remove_candidate_from_cells(self, candidate, cell_positions):
        nb_removed = 0
        for i,j in cell_positions:
            if self.cells[i][j].remove_candidate(candidate):
                nb_removed += 1
        return nb_removed

    def get_square_cells(self, number):
        """
        Get the cells of the square identified by its number.
        Number goes from 0, to 8 from left to right and top to bottom

        :param number: index of the square (0-8)
        :return: list of the cells in the square
        """
        return [
            self.cells[number // 3 * 3 + i][number % 3 * 3 + j]
            for i in range(3)
            for j in range(3)
        ]

    def get_row_cells(self, number):
        """
        Get the cells of the row identified by its number.
        Number goes from 0 to 8 from top to bottom

        :param number: index of the row (0-8)
        :return: list of the cells in the row
        """
        return self.cells[number]

    def get_col_cells(self, number):
        """
        Get the cells of the column identified by its number.
        Number goes from 0 to 8 from left to right

        :param number: index of the column (0-8)
        :return: list of the cells in the column
        """
        return [self.cells[i][number] for i in range(9)]

    def get_position_from_cell(self, cell):
        """
        Get the position of a cell in the sudoku

        :param cell: cell to find
        :return: position of the cell in the sudoku
        """
        for i, row in enumerate(self.cells):
            for j, c in enumerate(row):
                if c == cell:
                    return i, j

    def is_sudoku_solved(self):
        logging.debug("Checking if sudoku is solved")
        return all(cell.value for row in self.cells for cell in row)

    def is_impossible(self):
        logging.debug("Checking if sudoku is impossible")
        return any(
            not cell.value and cell.nb_remaining_candidates() == 0
            for row in self.cells
            for cell in row
        )

    def print_sudoku(self):
        for i, row in enumerate(self.cells):
            if i % 3 == 0 and i != 0:
                print("—" * 21)
            for j, cell in enumerate(row):
                if j % 3 == 0 and j != 0:
                    print("│", end=" ")
                print(cell.value if cell.value else " ", end=" ")
            print()