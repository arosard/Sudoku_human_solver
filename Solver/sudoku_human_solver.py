import logging
from collections import defaultdict
from itertools import combinations

STRATEGY_1 = "Only one candidate"
STRATEGY_2 = "Only position in row"
STRATEGY_3 = "Only position in column"
STRATEGY_4 = "Only position in square"
STRATEGY_5 = "Hidden n-tuples"
STRATEGY_6 = "Naked n-tuples"


class SudokuSolver:
    """
    Sudoku solver class

    Attributes:
    - sudoku: Sudoku object to solve
    - countStrategies: dictionary with stats of the strategies used
    """

    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.count_strategies = {
            STRATEGY_1: [0, 0],
            STRATEGY_2: [0, 0],
            STRATEGY_3: [0, 0],
            STRATEGY_4: [0, 0],
            STRATEGY_5: [0, 0],
            STRATEGY_6: [0, 0],
        }

    def stop(self):
        return self.sudoku.is_sudoku_solved() or self.sudoku.is_impossible()

    def solve(self):
        while not self.stop():
            if not (
                self.only_one_candidate()
                or self.only_position_in_row()
                or self.only_position_in_col()
                or self.only_position_in_square()
                or self.hidden_n_tuples()
                or self.naked_n_tuples()
            ):
                break

        if self.sudoku.is_sudoku_solved():
            logging.debug("Sudoku solved! :)")
        elif self.sudoku.is_impossible():
            logging.debug("Sudoku is impossible :(")
        else:
            logging.debug("Sudoku could not be solved :|")

    def only_one_candidate(self):
        logging.debug("Checking for cells with only one candidate")
        self.count_strategies[STRATEGY_1][0] += 1
        nb_found = 0
        for row in self.sudoku.cells:
            for cell in row:
                if (
                    cell.nb_remaining_candidates() == 1
                    and self.sudoku.set_value(
                        self.sudoku.cells.index(row),
                        row.index(cell),
                        int(next(iter(cell.candidates))),
                    )
                ) :
                    nb_found += 1
        self.count_strategies[STRATEGY_1][1] += nb_found
        return nb_found > 0

    def only_position_in_row(self):
        logging.debug("Checking for only position in row")
        self.count_strategies[STRATEGY_2][0] += 1
        nb_found = 0
        for number in range(1, 10):
            for row in self.sudoku.cells:
                candidates = [cell for cell in row if number in cell.candidates]
                if len(candidates) == 1:
                    candidate = candidates[0]
                    if self.sudoku.set_value(
                        self.sudoku.cells.index(row), row.index(candidate), number
                    ):
                        nb_found += 1
        self.count_strategies[STRATEGY_2][1] += nb_found
        return nb_found > 0

    def only_position_in_col(self):
        logging.debug("Checking for only position in column")
        self.count_strategies[STRATEGY_3][0] += 1
        nb_found = 0
        for number in range(1, 10):
            for col in range(9):
                candidates = [
                    (self.sudoku.cells.index(row), col)
                    for row in self.sudoku.cells
                    if number in row[col].candidates
                ]
                if len(candidates) == 1:
                    row, col = candidates[0]
                    if self.sudoku.set_value(row, col, number):
                        nb_found += 1
        self.count_strategies[STRATEGY_3][1] += nb_found
        return nb_found > 0

    def only_position_in_square(self):
        logging.debug("Checking for only position in square")
        self.count_strategies[STRATEGY_4][0] += 1
        nb_found = 0
        for square in range(9):  # number of the square (latin reading order)
            # top left corner of the square
            top_row, left_col = square // 3 * 3, square % 3 * 3
            for number in range(1, 10):
                candidates = [
                    (top_row + i, left_col + j)
                    for i in range(3)
                    for j in range(3)
                    if number
                    in self.sudoku.cells[top_row + i][left_col + j].candidates
                ]
                if len(candidates) == 1:
                    row, col = candidates[0]
                    if self.sudoku.set_value(row, col, number):
                        nb_found += 1
        self.count_strategies[STRATEGY_4][1] += nb_found
        return nb_found > 0

    def hidden_n_tuples(self):
        logging.debug("Checking for hidden n-tuples")
        self.count_strategies[STRATEGY_5][0] += 1
        nb_found = 0

        for row in self.sudoku.cells:
            nb_found += self.remove_other_candidates_from_n_tuple(row)

        for col in range(9):
            nb_found += self.remove_other_candidates_from_n_tuple(
                [row[col] for row in self.sudoku.cells]
            )

        for square in range(9):
            square_cells = self.sudoku.get_square_cells(square)
            nb_found += self.remove_other_candidates_from_n_tuple(square_cells)

        self.count_strategies[STRATEGY_5][1] += nb_found
        return nb_found > 0

    def naked_n_tuples(self):
        logging.debug("Checking for naked pairs")
        self.count_strategies[STRATEGY_6][0] += 1
        nb_found = 0

        for row in range(9):
            self.__naked_n_tuple_row_col_proc__([(row, col) for col in range(9)], 0)

        for col in range(9):
            self.__naked_n_tuple_row_col_proc__([(row, col) for row in range(9)], 1)

        for square in range(9):
            top_left = square // 3 * 3, square % 3 * 3
            square_cells_position = [top_left + (i, j) for i in range(3) for j in range(3)]
            candidates_positions = self.get_candidates_cells_position(square_cells_position)
            for candidate, positions in candidates_positions.items():
                if len(positions) == 2:
                    removable_positions = set(square_cells_position) - set(positions)
                    removable_positions = [(i,j) for i,j in removable_positions if candidate in self.sudoku.cells[i][j].candidates]
                    nb_found += self.sudoku.remove_candidate_from_cells(candidate, removable_positions)

        self.count_strategies[STRATEGY_6][1] += nb_found
        return nb_found > 0

    def __naked_n_tuple_row_col_proc__(self, cells_position, dimension):
        candidates_removed = 0
        candidates_positions = self.get_candidates_cells_position(cells_position)
        for candidate, positions in candidates_positions.items():
            if (
                self.are_positions_in_same_square(positions)
                and self.are_positions_in_same_dimension(positions, dimension)
            ):
                square_number = positions[0][0] // 3 * 3 + positions[0][1] // 3
                square_cells = self.sudoku.get_square_cells(square_number)
                for cell in set(square_cells) - set([self.sudoku.cells[i][j] for i, j in positions]):
                    if candidate in cell.candidates:
                        cell.remove_candidate(candidate)
                        candidates_removed += 1
        return candidates_removed

    @staticmethod
    def get_candidates_cells(cells):
        candidates_positions = defaultdict(list)
        for cell in cells:
            for candidate in cell.candidates:
                candidates_positions[candidate].append(cell)
        return candidates_positions

    def get_candidates_cells_position(self, cells_position):
        candidates_positions = defaultdict(list)
        for pos in cells_position:
            for candidate in self.sudoku.cells[pos[0]][pos[1]].candidates:
                candidates_positions[candidate].append(pos)
        return candidates_positions

    def remove_other_candidates_from_n_tuple(self, cells):
        nb_found = 0
        candidates_cells = self.get_candidates_cells(cells)
        for n in range(1, len(candidates_cells)-1):
            logging.debug(f"Checking for hidden {n}-tuples")
            n_tuples = {num: cells for num, cells in candidates_cells.items() if len(cells) == n}
            for combination in combinations(n_tuples.items(), n):
                all_cells = set([cell for _, cells in combination for cell in cells])
                if len(all_cells) != n:
                    continue
                for cell in all_cells:
                    for candidate in set(cell.candidates) - set(num for num, _ in combination):
                        cell.remove_candidate(candidate)
                        nb_found += 1
        return nb_found

    @staticmethod
    def are_positions_in_same_dimension(cells_position, dimension):
        if dimension not in [0,1]:
            raise ValueError("dimension must be 0 or 1")

        return (
            len(cells_position) != 0
            and all(pos[dimension] == cells_position[0][dimension] for pos in cells_position)
        )

    @staticmethod
    def are_positions_in_same_square(cells_position):
        return len(set((pos[0]//3, pos[1]//3) for pos in cells_position)) == 1

